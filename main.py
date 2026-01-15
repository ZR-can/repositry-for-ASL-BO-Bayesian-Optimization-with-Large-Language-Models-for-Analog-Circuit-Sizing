import os
import re
import subprocess
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from pathlib import Path
from datetime import datetime

# 导入 BoTorch 核心组件
from botorch.models import SingleTaskGP
from botorch.fit import fit_gpytorch_mll
from gpytorch.mlls import ExactMarginalLogLikelihood
from botorch.acquisition import qLogExpectedImprovement
from botorch.optim import optimize_acqf
from botorch.utils.transforms import normalize, unnormalize
# ==================== 配置参数 ====================
class Config:
    # 路径配置
    SPICE_TEMPLATE = r"opamp.sp"
    NGSPICE_PATH = r"ngspice_con.exe"
    WORK_DIR = r"results2"
    
    # 优化参数范围 (参数名: [最小值, 最大值])
    PARAM_BOUNDS = {
        'w_diff': [1e-6, 100e-6],      
        'l_diff': [0.18e-6, 1e-5],    
        'w_diff1': [1e-6, 100e-6],      
        'l_diff1': [0.18e-6, 1e-5],   
        'w_load': [1e-6, 100e-6],    
        'l_load': [0.18e-6, 1e-5],   
        'w_load1': [1e-6, 100e-6],     
        'l_load1': [0.18e-6, 1e-5],
        'w_tail': [1e-6, 100e-6],     
        'l_tail': [0.18e-6, 1e-5],
        'w_tail1': [1e-6, 100e-6],     
        'l_tail1': [0.18e-6, 1e-5],     
        'w_out': [1e-6, 100e-6],      
        'l_out': [0.18e-6, 1e-5],     
        'w_outload': [1e-6, 100e-6],   
        'l_outload': [0.18e-6, 1e-5], 
        'cc_val': [0.1e-12, 1e-10],  
        'rz_val': [100, 10000],       
    }
    
    # 优化设置
    N_INIT = 10           # 初始随机采样点数
    N_ITERATIONS = 10     # 贝叶斯优化迭代次数
    N_CANDIDATES = 32   # 每次优化生成的候选点数
    
    # 目标权重 (用于FOM计算)
    WEIGHT_GAIN = 1.0     # 增益权重
    WEIGHT_GBW = 1.0      # 带宽权重
    WEIGHT_PM = 1.0       # 相位裕度权重
    WEIGHT_PWR = 1.0     # 功耗权重(负值表示越小越好)

# ==================== SPICE仿真器 ====================
class NgspiceSimulator:
    def __init__(self, template_path, ngspice_path, work_dir):
        self.template_path = Path(template_path)
        self.ngspice_path = Path(ngspice_path)
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
        # 读取模板
        with open(self.template_path, 'r', encoding='utf-8') as f:
            self.template = f.read()
        
        print(f"✓ 模板加载: {self.template_path}")
        print(f"✓ Ngspice: {self.ngspice_path}")
    
    def run_simulation(self, params, sim_id):
        """运行单次仿真"""
        # 生成SPICE文件
        spice_content = self.template
        for param_name, param_value in params.items():
            spice_content = spice_content.replace(f"{{{param_name}}}", f"{param_value:.6e}")
        
        # 保存临时文件
        temp_file = self.work_dir / f"sim_{sim_id}.sp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(spice_content)
        
        # 运行Ngspice
        try:
            result = subprocess.run(
                [str(self.ngspice_path), "-b", str(temp_file)],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='ignore'
            )
            
            output = result.stdout + result.stderr
            return output, None
            
        except subprocess.TimeoutExpired:
            return None, "Simulation timeout"
        except Exception as e:
            return None, str(e)
    
    def extract_metrics(self, output):
        """从Ngspice输出提取性能指标"""
        if output is None:
            return None
        
        # 检查是否有仿真错误
        if 'singular matrix' in output.lower() or 'simulation(s) aborted' in output.lower():
            return None
        
        try:
            # 查找RESULT_START和RESULT_END之间的内容
            result_match = re.search(r'RESULT_START(.*?)RESULT_END', output, re.DOTALL)
            if not result_match:
                return None
            
            result_text = result_match.group(1)
            
            # 提取各项指标
            metrics = {}
            
            # dc_gain (单位: dB)
            gain_match = re.search(r'dc_gain\s*[=:]?\s*([-+]?[\d.]+(?:[eE][-+]?\d+)?)', result_text, re.IGNORECASE)
            if gain_match:
                metrics['gain'] = float(gain_match.group(1))
            print(f"Gain={metrics['gain']:.2f}dB")
            # gbw (单位: Hz) - 支持 gbw_final 变量名
            gbw_match = re.search(r'gbw(?:_final)?\s*[=:]?\s*([-+]?[\d.]+(?:[eE][-+]?\d+)?)', result_text, re.IGNORECASE)
            if gbw_match:
                metrics['gbw'] = float(gbw_match.group(1))
            print(f"GBW={metrics['gbw']/1e6:.2f}MHz")
            # pm (单位: degrees)
            pm_match = re.search(r'pm\s*[=:]?\s*([-+]?[\d.]+(?:[eE][-+]?\d+)?)', result_text, re.IGNORECASE)
            if pm_match:
                metrics['pm'] = float(pm_match.group(1))
            if metrics['pm'] > 180:
                metrics['pm']= metrics['pm'] -360
            print(f"PM={metrics['pm']:.2f}°")
            # pwr (单位: W) - 支持多种变量名
            # power_w 可能输出向量，提取第一个值
            # 匹配格式：power_w = 0.451909 或 pwr = value
            pwr_match = re.search(r'(?:pwr|power_consumption|power_w0)\s*=\s*([-+]?[\d.]+(?:[eE][-+]?\d+)?)', result_text, re.IGNORECASE)
            if pwr_match:
                # 提取第一个数值（如果是向量，取第一个值）
                pwr_value = pwr_match.group(1)
                metrics['pwr0'] = float(pwr_value) * 1000  # 转换为mW
            print(f"Pwr0={metrics['pwr0']:.2f}mW")
            pwr1_match = re.search(r'(?:pwr|power_consumption|power_w1)\s*=\s*([-+]?[\d.]+(?:[eE][-+]?\d+)?)', result_text, re.IGNORECASE)
            if pwr1_match:
                # 提取第一个数值（如果是向量，取第一个值）
                pwr1_value = pwr1_match.group(1)
                metrics['pwr1'] = float(pwr1_value) * 1000  # 转换为mW
            print(f"Pwr1={metrics['pwr1']:.2f}mW")
            # 检查是否所有指标都成功提取
            required = ['gain', 'gbw', 'pm', 'pwr0','pwr1']
            if all(k in metrics for k in required):
                # 验证指标值的合理性
                if metrics['gbw'] <= 0 or metrics['pm'] > 180:
                    # GBW或PM值不合理，可能是测量失败
                    print(f"  ⚠ 指标值异常: GBW={metrics['gbw']:.2e}Hz, PM={metrics['pm']:.1f}°")
                    return None
                return metrics
            else:
                missing = [k for k in required if k not in metrics]
                print(f"  ⚠ 缺失指标: {missing}")
                return None
                
        except Exception as e:
            print(f"  ⚠ 提取错误: {e}")
            return None

# ==================== 优化器 ====================
def generate_sample_string(arr_list,PARAM_BOUNDS):
    # 提取参数名列表（顺序与字典一致）
    param_names = list(PARAM_BOUNDS.keys())
    
    # 存储每个采样点的字符串
    sample_strings = []
    
    # 遍历每个采样点数组
    for idx, arr in enumerate(arr_list):
        # 确保数组长度与参数数量一致
        if len(arr) != len(param_names):
            raise ValueError(f"采样点 {idx+1} 的数组长度 {len(arr)} 与参数数量 {len(param_names)} 不匹配")
        
        # 拼接单个采样点的参数字符串
        param_parts = []
        for param_name, value in zip(param_names, arr):
            # 保留合适的小数位数，避免科学计数法显示过长
            if 'cc_val' in param_name:
                # cc_val 是极小值，保留10位小数
                param_parts.append(f"{param_name}={value:.10e}")
            elif 'rz_val' in param_name:
                # rz_val 是较大的整数，保留2位小数
                param_parts.append(f"{param_name}={value:.2f}")
            else:
                # 其他参数保留8位小数
                param_parts.append(f"{param_name}={value:.8e}")
        
        # 拼接单个采样点的完整字符串
        sample_str = f"Sample{idx+1}: {{{', '.join(param_parts)}}}"
        sample_strings.append(sample_str)
    
    # 所有采样点字符串换行连接
    return '\n'.join(sample_strings)
def append_result_to_sample(sample_str, result_array):
    # 将采样字符串按行分割
    sample_lines = sample_str.split('\n')
    # 检查采样行数和结果数组长度是否匹配
    if len(sample_lines) != len(result_array):
        raise ValueError(f"采样行数 {len(sample_lines)} 与结果数组长度 {len(result_array)} 不匹配")
    # 存储拼接后的行
    final_lines = []
    # 遍历每行采样数据和对应结果
    for idx, (sample_line, result_data) in enumerate(zip(sample_lines, result_array)):
        result_idx = idx + 1  # Result 的序号（从1开始）    
        if result_data is None:
            # 结果为 None 时的格式
            result_part = f" Result{result_idx}:{{None}}"
        else:
            # 提取字典中的性能指标并计算总功耗
            gain = result_data.get('gain', 0.0)
            gbw = result_data.get('gbw', 0.0)
            pm = result_data.get('pm', 0.0)
            pwr0 = result_data.get('pwr0', 0.0)
            pwr1 = result_data.get('pwr1', 0.0)
            total_pwr = pwr0 + pwr1
            # 格式化性能指标字符串（保留合适小数位）
            result_part = (
                f" Result{result_idx}:{{gain={gain:.4f} db, gbw={gbw:.2f} Hz, "
                f"pm={pm:.4f} degree, pwr={total_pwr:.8f} W}}"
            )
        # 拼接采样行和结果行
        final_line = sample_line + result_part
        final_lines.append(final_line)    
    # 合并所有行并返回
    return '\n'.join(final_lines)
def extract_param_names_with_ranges_simple(param_dict):
    param_lines = [f"{name}: {range_val}" for name, range_val in param_dict.items()]
    return '\n'.join(param_lines)
class BayesianOptimizer:
    def __init__(self, config, simulator):
        self.config = config
        self.simulator = simulator
        
        # 参数边界
        self.param_names = list(config.PARAM_BOUNDS.keys())
        self.bounds = torch.tensor([
            [config.PARAM_BOUNDS[p][0] for p in self.param_names],
            [config.PARAM_BOUNDS[p][1] for p in self.param_names]
        ], dtype=torch.double)
        
        # 存储结果
        self.X = []  # 参数
        self.Y = []  # FOM值
        self.metrics_history = []  # 详细指标
        
        self.best_fom = -np.inf
        self.best_params = None
        self.best_metrics = None
    
    def calculate_fom(self, metrics):
        """计算优化目标函数 (Figure of Merit)"""
        if metrics is None:
            return -10.0
        
        # 归一化处理
        if metrics['gain'] < 50.0:
            gain_norm = metrics['gain'] / 50.0
        else:
            gain_norm = 1.0      # 目标60dB
        if metrics['gbw'] < 2e7:
            gbw_norm = (metrics['gbw'] / 2e7)    # 目标10MHz
        else:
            gbw_norm = 1.0
        if metrics['pm'] < 90.0:
            pm_norm = (metrics['pm'] / 90.0 if metrics['pm'] < 90.0 else 1.0 )      # 目标60度
        else:
            pm_norm = 1.0
        if (metrics['pwr0'] + metrics['pwr1']) > 1.0:
            pwr_norm = ((metrics['pwr0'] + metrics['pwr1']))
        else:
            pwr_norm = 0

        # 加权求和
        fom = (self.config.WEIGHT_GAIN * gain_norm +
               self.config.WEIGHT_GBW * gbw_norm +
               self.config.WEIGHT_PM * pm_norm -
               self.config.WEIGHT_PWR * pwr_norm)
        #fom =  metrics['gbw'] * 1e-6 / (metrics['pwr0'] + metrics['pwr1'])
        
        return fom
    
    def sample_params(self, n_samples):
        """在参数空间中随机采样"""
        samples = torch.rand(n_samples, len(self.param_names), dtype=torch.double)
        return unnormalize(samples, self.bounds)
    
    def params_to_dict(self, params_tensor):
        """将张量转换为参数字典"""
        return {name: float(params_tensor[i]) for i, name in enumerate(self.param_names)}
    
    def run_initial_sampling(self):
        """初始随机采样阶段"""
        print(f"\n{'='*70}")
        print(f"📍 阶段 1: 随机初始化 ({self.config.N_INIT} 点)")
        print(f"{'='*70}")
        
        for i in range(self.config.N_INIT):
            params_tensor = self.sample_params(10)[i]
            params_dict = self.params_to_dict(params_tensor)
            
            print(f"\n[{i+1}/{self.config.N_INIT}] 仿真中...", end=" ")
            
            output, error = self.simulator.run_simulation(params_dict, f"init_{i}")
            
            if error:
                print(f"✗ 错误: {error}")
            
            metrics = self.simulator.extract_metrics(output)
            fom = self.calculate_fom(metrics)
            

            self.X.append(params_tensor.numpy())
            self.Y.append(fom)
            self.metrics_history.append(metrics)
                
            if fom > self.best_fom:
                self.best_fom = fom
                self.best_params = params_dict
                self.best_metrics = metrics
                
            print(f"✓ FOM={fom:.2f} ")
        print(f"\n初始化完成: {len(self.Y)}/{self.config.N_INIT} 个有效点")
        if len(self.Y) == 0:
            raise ValueError("❌ 所有初始化点都失败,请检查SPICE文件!")
    
    def run_bo_iteration(self, iteration):
        """单次贝叶斯优化迭代（批量采样版本）：每轮采样前5个候选点并依次仿真"""
    # ========== 修复1：优化数据格式，解决numpy列表转张量警告 ==========
    # 将numpy数组列表转换为单个二维numpy数组，再转张量
        if iteration ==1:
            initial_sample=generate_sample_string(self.X, self.config.PARAM_BOUNDS)
            initial_result=append_result_to_sample(initial_sample, self.metrics_history)
            print(f"初始采样点:\n{initial_result}")
        else:
            initial_sample=generate_sample_string(self.X[-5:], self.config.PARAM_BOUNDS)
            initial_result=append_result_to_sample(initial_sample, self.metrics_history[-5:])
            print(f"初始采样点:\n{initial_result}")
        para=extract_param_names_with_ranges_simple(self.config.PARAM_BOUNDS)
        print(f"{para}")
        X_np = np.array(self.X, dtype=np.double)  # 合并为统一数组
        train_X = normalize(torch.tensor(X_np, dtype=torch.double), self.bounds)
    # Y同理优化（可选，提升效率）
        print(self.Y)
        Y_np = np.array(self.Y, dtype=np.double).reshape(-1, 1)
        train_Y = torch.tensor(Y_np, dtype=torch.double)
    
    # 训练高斯过程模型（与原逻辑一致）
        gp = SingleTaskGP(train_X, train_Y)
        mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
        fit_gpytorch_mll(mll)
    
    # ========== 修复2：改用支持批量采样的qEI采集函数 ==========
    # 替换LogExpectedImprovement为qExpectedImprovement（支持q>1）
        acq = qLogExpectedImprovement(
        model=gp,
        best_f=train_Y.max(),  # 历史最优值
        )
    
    # 优化采集函数：批量采样5个候选点
        candidates, acq_values = optimize_acqf(
        acq,
        bounds=torch.stack([
            torch.zeros(len(self.param_names), dtype=torch.double),
            torch.ones(len(self.param_names), dtype=torch.double)
        ]),
        q=5,  # 批量采样5个点
        num_restarts=10,
        raw_samples=self.config.N_CANDIDATES,
        )
    
    # 依次处理每个候选点
        for idx, candidate in enumerate(candidates):
        # 反归一化：还原到原始参数范围（修复维度问题）
            next_params = unnormalize(candidate.unsqueeze(0), self.bounds).squeeze(0)
            params_dict = self.params_to_dict(next_params)
        
        # 运行仿真（添加子索引标识批量中的第几个点）
            sample_id = f"bo_{iteration}_sample_{idx+1}"
            print(f"\n[{iteration}/{self.config.N_ITERATIONS}] 批量采样点 {idx+1}/5 仿真...", end=" ")
            output, error = self.simulator.run_simulation(params_dict, sample_id)
        
            if error:
               print(f"✗ 错误: {error}")
            # 若仿真出错，跳过该点
        
        # 计算指标和FOM
            metrics = self.simulator.extract_metrics(output)
            fom = self.calculate_fom(metrics)
        
        # 更新历史数据（转换为numpy数组，避免列表嵌套）
            self.X.append(next_params.cpu().numpy())
            self.Y.append(fom)
            self.metrics_history.append(metrics)
        
        # 更新最优结果
            if fom > self.best_fom:
                self.best_fom = fom
                self.best_params = params_dict
                self.best_metrics = metrics
                print(f"🎯 NEW BEST! FOM={fom:.2f}")
            else:
                print(f"✓ FOM={fom:.2f}")
        return True
    
    def optimize(self):
        """执行完整优化流程"""
        start_time = time.time()
        
        # 阶段1: 初始化
        self.run_initial_sampling()
        
        # 阶段2: 贝叶斯优化
        print(f"\n{'='*70}")
        print(f"🎯 阶段 2: 贝叶斯优化 ({self.config.N_ITERATIONS} 次迭代)")
        print(f"{'='*70}")
        
        for i in range(1, self.config.N_ITERATIONS + 1):
            self.run_bo_iteration(i)
        
        elapsed = time.time() - start_time
        
        # 输出最终结果
        print(f"\n{'='*70}")
        print(f"🏆 优化完成! 总耗时: {elapsed/60:.1f} 分钟")
        print(f"{'='*70}")
        print(f"\n最佳FOM: {self.best_fom:.4f}")
        print(f"\n最佳性能指标:")
        print(f"  • 增益 (Gain):     {self.best_metrics['gain']:.2f} dB")
        print(f"  • 带宽 (GBW):      {self.best_metrics['gbw']/1e6:.2f} MHz")
        print(f"  • 相位裕度 (PM):   {self.best_metrics['pm']:.2f} °")
        print(f"  • 功耗 (Power):    {self.best_metrics['pwr0']:.2f} mW | {self.best_metrics['pwr1']:.2f} mW")
        print(f"\n最佳参数:")
        for name, value in self.best_params.items():
            if 'w_' in name or 'l_' in name:
                print(f"  • {name:12s} = {value*1e6:.3f} µm")
            elif 'cc_' in name:
                print(f"  • {name:12s} = {value*1e12:.3f} pF")
            else:
                print(f"  • {name:12s} = {value:.2f} Ω")

# ==================== 可视化 ====================
class Visualizer:
    @staticmethod
    def plot_optimization_history(optimizer, save_path):
        """绘制优化历史"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Bayesian Optimization Results', fontsize=16, fontweight='bold')
        
        # 确保迭代次数基于有效数据长度
        iterations = np.arange(1, len(optimizer.Y) + 1)
        
        # 1. FOM曲线
        ax = axes[0, 0]
        ax.plot(iterations, optimizer.Y, 'b-', alpha=0.3, label='FOM')
        best_fom_cummax = np.maximum.accumulate(optimizer.Y)
        ax.plot(iterations, best_fom_cummax, 'r-', linewidth=2, label='Best FOM')
        ax.set_xlabel('Iteration')
        ax.set_ylabel('FOM')
        ax.set_title('FOM Evolution')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 2-5. 各项性能指标
        metrics_to_plot = [
            ('gain', 'Gain (dB)', axes[0, 1]),
            ('gbw', 'GBW (MHz)', axes[0, 2]),
            ('pm', 'Phase Margin (°)', axes[1, 0]),
            ('pwr0', 'Power (mW)', axes[1, 1]),
            ('pwr1', 'Power (mW)', axes[1, 1])
        ]
        metric_names = [item[0] for item in metrics_to_plot]  # ['gain', 'gbw', 'pm', 'pwr0', 'pwr1']
    
        # 处理 metrics_history 中的数据（修复缩进 + 保证数据长度匹配）
        processed_history = []
        # 确保处理后的历史数据长度和Y一致
        history_len = len(optimizer.metrics_history) if hasattr(optimizer, 'metrics_history') else 0
        target_len = len(optimizer.Y)
        
        # 扩展/截断metrics_history到和Y相同长度
        if history_len < target_len:
            # 补充缺失的轮次为None
            optimizer.metrics_history += [None] * (target_len - history_len)
        elif history_len > target_len:
            # 截断过长的部分
            optimizer.metrics_history = optimizer.metrics_history[:target_len]
        
        for m in optimizer.metrics_history:
            # 初始化当前轮次的结果字典
            current_metrics = {}
            
            # 情况1：当前轮次的项是 None，所有指标赋值为 -1
            if m is None:
                for metric in metric_names:
                    current_metrics[metric] = -1
            # 情况2：当前轮次的项是整数（兼容之前的报错场景）
            elif isinstance(m, (int, float)):
                # 如果是数值，默认给第一个指标赋值，其余为 -1（可根据需求调整）
                current_metrics[metric_names[0]] = m
                for metric in metric_names[1:]:
                    current_metrics[metric] = -1
            # 情况3：当前轮次的项是字典（正常情况）
            elif isinstance(m, dict):
                for metric in metric_names:
                    # 字典中有该指标则取原值，无则赋值 -1
                    current_metrics[metric] = m.get(metric, -1)
            # 情况4：其他无效类型，所有指标赋值为 -1
            else:
                for metric in metric_names:
                    current_metrics[metric] = -1
            
            processed_history.append(current_metrics)
        
        optimizer.metrics_history = processed_history
        
        for metric, ylabel, ax in metrics_to_plot:
            values = [m[metric] for m in optimizer.metrics_history]
            # 确保values长度和iterations一致
            values = values[:len(iterations)]
            
            if metric == 'gbw':
                values = [v/1e6 for v in values]
            
            ax.plot(iterations, values, 'o-', alpha=0.6)
            ax.set_xlabel('Iteration')
            ax.set_ylabel(ylabel)
            ax.set_title(ylabel)
            ax.grid(True, alpha=0.3)
        
        # 6. 参数分布（选取前3个重要参数）
        ax = axes[1, 2]
        important_params = ['w_diff', 'cc_val', 'rz_val']
        X_array = np.array(optimizer.X) if hasattr(optimizer, 'X') and optimizer.X else np.array([])
        
        # 确保X_array长度和iterations一致
        if len(X_array) > len(iterations):
            X_array = X_array[:len(iterations)]
        
        for i, pname in enumerate(important_params):
            if hasattr(optimizer, 'param_names') and pname in optimizer.param_names:
                idx = optimizer.param_names.index(pname)
                # 处理X_array为空的情况
                if len(X_array) > 0 and idx < X_array.shape[1]:
                    values = X_array[:, idx]
                    if 'w_' in pname or 'l_' in pname:
                        values = values * 1e6  # 转换为µm
                    elif 'cc_' in pname:
                        values = values * 1e12  # 转换为pF
                    ax.plot(iterations[:len(values)], values, 'o-', alpha=0.6, label=pname)
        
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Parameter Value')
        ax.set_title('Key Parameters Evolution')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ 图表已保存: {save_path}")
        plt.close()
    
    @staticmethod
    def save_results_table(optimizer, save_path):
        """保存结果表格"""
        # 创建DataFrame
        data = []
        metrics_to_plot = [
            ('gain', 'Gain (dB)'),
            ('gbw', 'GBW (MHz)'),
            ('pm', 'Phase Margin (°)'),
            ('pwr0', 'Power (mW)'),
            ('pwr1', 'Power (mW)' )
        ]
        metric_names = [item[0] for item in metrics_to_plot]  # ['gain', 'gbw', 'pm', 'pwr0', 'pwr1']
    
        # 处理 metrics_history 中的数据（修复缩进 + 长度匹配）
        processed_history = []
        history_len = len(optimizer.metrics_history) if hasattr(optimizer, 'metrics_history') else 0
        target_len = len(optimizer.Y) if hasattr(optimizer, 'Y') else 0
        
        # 对齐数据长度
        if history_len < target_len:
            optimizer.metrics_history += [None] * (target_len - history_len)
        elif history_len > target_len:
            optimizer.metrics_history = optimizer.metrics_history[:target_len]
        
        for m in optimizer.metrics_history:
            # 初始化当前轮次的结果字典
            current_metrics = {}
            
            # 情况1：当前轮次的项是 None，所有指标赋值为 -1
            if m is None:
                for metric in metric_names:
                    current_metrics[metric] = -1
            # 情况2：当前轮次的项是整数（兼容之前的报错场景）
            elif isinstance(m, (int, float)):
                # 如果是数值，默认给第一个指标赋值，其余为 -1（可根据需求调整）
                current_metrics[metric_names[0]] = m
                for metric in metric_names[1:]:
                    current_metrics[metric] = -1
            # 情况3：当前轮次的项是字典（正常情况）
            elif isinstance(m, dict):
                for metric in metric_names:
                    # 字典中有该指标则取原值，无则赋值 -1
                    current_metrics[metric] = m.get(metric, -1)
            # 情况4：其他无效类型，所有指标赋值为 -1
            else:
                for metric in metric_names:
                    current_metrics[metric] = -1
            
            processed_history.append(current_metrics)
        
        # 确保三个列表长度一致
        X_len = len(optimizer.X) if hasattr(optimizer, 'X') else 0
        Y_len = len(optimizer.Y) if hasattr(optimizer, 'Y') else 0
        hist_len = len(processed_history)
        
        # 取最小长度作为遍历上限
        min_len = min(X_len, Y_len, hist_len)
        
        for i in range(min_len):
            params = optimizer.X[i] if i < X_len else []
            fom = optimizer.Y[i] if i < Y_len else -1
            metrics = processed_history[i] if i < hist_len else {}
            
            row = {'iteration': i+1, 'FOM': fom}
            
            # 添加参数（修复：判断数组是否非空，解决ValueError）
            if hasattr(optimizer, 'param_names'):
                # 正确判断params是否为非空数组/列表
                params_is_valid = False
                if isinstance(params, (list, np.ndarray)):
                    params_is_valid = len(params) > 0
                elif params is not None:
                    params_is_valid = True
                
                if params_is_valid:
                    for j, pname in enumerate(optimizer.param_names):
                        if j < len(params):
                            row[pname] = params[j]
                        else:
                            row[pname] = np.nan
            
            # 添加性能指标
            row.update(metrics)
            data.append(row)
        
        df = pd.DataFrame(data)
        
        # 保存CSV
        csv_path = save_path.with_suffix('.csv')
        df.to_csv(csv_path, index=False, float_format='%.6e')
        print(f"✓ 数据表已保存: {csv_path}")
        
        # 保存最佳结果的详细报告（增加容错处理）
        report_path = save_path.with_suffix('.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("OpAmp Bayesian Optimization - Final Report\n")
            f.write("="*70 + "\n\n")
            
            # 容错处理：检查属性是否存在
            total_iter = len(optimizer.Y) if hasattr(optimizer, 'Y') else 0
            best_fom = getattr(optimizer, 'best_fom', -1)
            
            f.write(f"Total Iterations: {total_iter}\n")
            f.write(f"Best FOM: {best_fom:.6f}\n\n")
            
            f.write("Best Performance Metrics:\n")
            f.write("-" * 40 + "\n")
            
            # 处理best_metrics可能不存在的情况
            best_metrics = getattr(optimizer, 'best_metrics', {})
            gain = best_metrics.get('gain', -1)
            gbw = best_metrics.get('gbw', -1)
            pm = best_metrics.get('pm', -1)
            pwr0 = best_metrics.get('pwr0', 0)
            pwr1 = best_metrics.get('pwr1', 0)
            
            f.write(f"  Gain (dc_gain):      {gain:.3f} dB\n")
            f.write(f"  GBW:                 {gbw/1e6:.3f} MHz\n")
            f.write(f"  Phase Margin (PM):   {pm:.3f} °\n")
            f.write(f"  Power Consumption:   {pwr0 + pwr1:.3f} mW\n\n")
            
            f.write("Best Parameters:\n")
            f.write("-" * 40 + "\n")
            
            # 处理best_params可能不存在的情况
            best_params = getattr(optimizer, 'best_params', {})
            for name, value in best_params.items():
                if 'w_' in name or 'l_' in name:
                    f.write(f"  {name:15s} = {value*1e6:10.4f} µm\n")
                elif 'cc_' in name:
                    f.write(f"  {name:15s} = {value*1e12:10.4f} pF\n")
                else:
                    f.write(f"  {name:15s} = {value:10.2f} Ω\n")
        
        print(f"✓ 报告已保存: {report_path}")

# ==================== 主程序 ====================
def main():
    print("\n" + "="*70)
    print("🚀 OpAmp 贝叶斯优化系统")
    print("="*70)
    
    # 初始化配置
    config = Config()
    
    # 检查文件
    if not Path(config.SPICE_TEMPLATE).exists():
        raise FileNotFoundError(f"模板文件不存在: {config.SPICE_TEMPLATE}")
    if not Path(config.NGSPICE_PATH).exists():
        raise FileNotFoundError(f"Ngspice不存在: {config.NGSPICE_PATH}")
    
    # 创建仿真器和优化器
    simulator = NgspiceSimulator(config.SPICE_TEMPLATE, config.NGSPICE_PATH, config.WORK_DIR)
    optimizer = BayesianOptimizer(config, simulator)
    
    # 运行优化
    optimizer.optimize()
    
    # 生成可视化
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_dir = Path(config.WORK_DIR)
    
    Visualizer.plot_optimization_history(
        optimizer, 
        result_dir / f"optimization_history_{timestamp}.png"
    )
    
    Visualizer.save_results_table(
        optimizer,
        result_dir / f"optimization_results_{timestamp}"
    )
    
    print(f"\n✅ 所有结果已保存至: {result_dir}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()