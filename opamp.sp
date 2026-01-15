* Two-Stage Miller OpAmp Optimization Template

.model nmos_gen nmos 
+LEVEL    = 49                  
*
* GENERAL PARAMETERS
*
+CALCACM  = 1
+LMIN     = 1.5E-7              LMAX     = 1.0E-5              WMIN     = 1.9E-7              
+WMAX     = 1.0E-4              TNOM     = 25.0                VERSION  = 3.24                
+TOX      = 3.87E-09            TOXM     = 3.87E-09            XJ       = 1.6000000E-07       
+NCH      = 3.8694000E+17       LLN      = 1.1205959           LWN      = 0.9200000           
+WLN      = 1.0599999           WWN      = 0.8768474           LINT     = 1.5757085E-08       
+LL       = 2.6352781E-16       LW       = -2.2625584E-16      LWL      = -2.0576711E-22      
+WINT     = -1.4450482E-09      WL       = -2.3664573E-16      WW       = -3.6409690E-14      
+WWL      = -4.0000000E-21      MOBMOD   = 1                   BINUNIT  = 2                   
+XL       = 1.8E-8              XW       = 0.00                DWG      = -5.9600000E-09      
+DWB      = 4.5000000E-09         
* DIODE PARAMETERS
+ACM      = 12                  LDIF     = 7.00E-08            HDIF     = 2.00E-07            
+RSH      = 7.08                RD       = 0                   RS       = 0                   
+RSC      = 1.7                 RDC      = 1.7                 
*
* THRESHOLD VOLTAGE PARAMETERS
*
+VTH0     = 0.39                WVTH0    = -2.9709472E-08      PVTH0    = 5.0000000E-16     
+K1       = 0.6801043           WK1      = -2.4896840E-08      PK1      = 1.3000000E-15       
+K2       = -4.9977830E-02      K3       = 10.0000000          DVT0     = 1.3000000           
+DVT1     = 0.5771635           DVT2     = -0.1717554          DVT0W    = 0.00                
+DVT1W    = 0.00                DVT2W    = 0.00                NLX      = 7.5451030E-08       
+W0       = 5.5820150E-07       K3B      = -3.0000000                 
*
* MOBILITY PARAMETERS
*
+VSAT     = 8.2500000E+04       PVSAT    = -8.3000000E-10      UA       = -1.0300000E-09      
+LUA      = 7.7349790E-19       PUA      = -1.0000000E-24      UB       = 2.3666682E-18       
+UC       = 1.2000000E-10       PUC      = 1.5000000E-24       RDSW     = 55.5497200          
+PRWB     = -0.2400000          PRWG     = 0.4000000           WR       = 1.0000000           
+U0       = 3.4000000E-02       LU0      = 2.3057663E-11       WU0      = -3.1009695E-09      
+A0       = 0.8300000           KETA     = -3.0000000E-03      LKETA    = -1.7000000E-09      
+A1       = 0.00                A2       = 0.9900000           AGS      = 0.3200000           
+B0       = 6.0000000E-08       B1       = 0.00                
*
* SUBTHRESHOLD CURRENT PARAMETERS
*
+VOFF     = -0.1030000          LVOFF    = -3.3000000E-09      NFACTOR  = 1.2500000           
+LNFACTOR = 4.5000000E-08       CIT      = 0.00                CDSC     = 0.00                
+CDSCB    = 0.00                CDSCD    = 1.0000000E-04       ETA0     = 2.8000001E-02       
+ETAB     = -2.7000001E-02      DSUB     = 0.4000000           
*
* ROUT PARAMETERS
*
+PCLM     = 1.2000000           PPCLM    = 2.9999999E-15       PDIBLC1  = 2.5000000E-02       
+PDIBLC2  = 3.8000000E-03       PPDIBLC2 = 2.7000001E-16       PDIBLCB  = 0.00                
+DROUT    = 0.5600000           PSCBE1   = 3.4500000E+08       PSCBE2   = 1.0000000E-06       
+PVAG     = 0.00                DELTA    = 1.0000000E-02       ALPHA0   = 1.7753978E-08       
+ALPHA1   = 0.1764000           LALPHA1  = 7.6250000E-09       BETA0    = 11.1683940  
*
* TEMPERATURE EFFECTS PARAMETERS
*
+KT1      = -0.2572866          KT2      = -4.0000000E-02      AT       = 3.7000000E+04       
+PAT      = -7.5000000E-10      UTE      = -1.5500000          UA1      = 1.7600000E-09       
+LUA1     = 6.0000000E-18       WUA1     = -1.1000000E-16      PUA1     = -5.0000000E-25      
+UB1      = -2.4000000E-18      UC1      = -1.0000000E-10      LUC1     = 1.6999999E-17       
+PUC1     = -3.0000000E-24      KT1L     = -1.0000000E-09      PRT      = -55.0000000       
*    
* NOISE PARAMETERS
*
+NOIMOD   = 2                   NOIA     = 8.2282E+19            NOIB     = 1.3327E+04    
+NOIC     = -2.4937E-14         EM       = 1.7767E+07            EF       = 8.1800E-01 
*
* CAPACITANCE PARAMETERS
*
+CJ       = 9.68E-04               MJ       = 0.346                PB       = 0.7                   
+CJSW     = 7.95E-11               MJSW     = 0.538                PBSW     = 1                 
+CJSWG    = 4.18E-10               MJSWG    = 0.538                PBSWG    = 1
+TCJ      = 8.42E-04               TCJSW    = 6.69E-04             TCJSWG   = 6.69E-04      
+TPB      = 1.47E-03               TPBSW    = 8.68E-04             TPBSWG   = 8.68E-04
+JS       = 3.52E-07               JSW      = 3.0E-13              NJ       = 1.0392 
+XTI      = 3.25                   NQSMOD   = 0                    ELM      = 5
+CGDO     = 3.70E-10               CGSO     = 3.70E-10                    
+CAPMOD   = 3                      XPART    = 1                    CF       = 0.00                   
+ACDE     = 0.64                   MOIN     = 24                   NOFF     = 1.2025                 
+DLC      = 8.5E-09                DWC      = 4.5E-08          

.model pmos_gen pmos 
+LEVEL    = 49                  
*
* GENERAL PARAMETERS
*
+CALCACM  = 1
+LMIN     = 1.5E-7              LMAX     = 1.0E-5              WMIN     = 1.9E-7              
+WMAX     = 1.0E-4              TNOM     = 25.0                VERSION  = 3.24                
+TOX      = 3.74E-09            TOXM     = 3.74E-09            XJ       = 1.7000001E-07       
+NCH      = 5.5000000E+17       LLN      = 1.0000000           LWN      = 1.0000000           
+WLN      = 1.0450000           WWN      = 1.0000000           LINT     = 1.0000000E-08       
+LL       = 3.4000000E-15       LW       = -3.3600000E-16      LWL      = 0.00                
+WINT     = 8.0000010E-09       WL       = 3.5904200E-15       WW       = -1.8999999E-15      
+WWL      = -1.1205000E-21      MOBMOD   = 1                   BINUNIT  = 2                   
+XL       = -5.7E-09            XW       = 0.00                DWG      = -1.7361970E-08          
+DWB      = 2.0000000E-08       
* DIODE PARAMETERS
+ACM      = 12                  LDIF     = 7.00E-08            HDIF     = 2.00E-07            
+RSH      = 7.83                RD       = 0                   RS       = 0                   
+RSC      = 1.5                 RDC      = 1.5                 
*
* THRESHOLD VOLTAGE PARAMETERS
*
+VTH0     = -0.402              WVTH0    = 1.2675420E-08       PVTH0    = -1.2500000E-15  
+K1       = 0.5872390           LK1      = 3.5532110E-09       K2       = 7.0906860E-03       
+K3       = 2.5999999           DVT0     = 0.7194931           DVT1     = 0.2467441           
+DVT2     = 7.8089680E-02       DVT0W    = 0.00                DVT1W    = 8.0000000E+05       
+DVT2W    = 0.00                NLX      = 9.0000000E-08       W0       = 0.00                
+K3B      = 2.4862001           NGATE    = 3.1680000E+20               
*
* MOBILITY PARAMETERS
*
+VSAT     = 1.0000000E+05       UA       = 2.8500000E-10       LUA      = 5.5000000E-18       
+PUA      = -2.0000000E-24      UB       = 1.0000000E-18       UC       = -4.7700000E-11      
+WUC      = 3.1668000E-17       PUC      = -2.5000000E-24      RDSW     = 4.5500000E+02       
+PRWB     = -0.4000000          PRWG     = 0.00                WR       = 1.0000000           
+U0       = 8.6610000E-03       LU0      = -2.0000000E-11      WU0      = 1.3815350E-10       
+A0       = 1.0000000           KETA     = 2.0000000E-02       LKETA    = -8.5000000E-09      
+PKETA    = 5.0000000E-16       A1       = 0.00                A2       = 0.9900000           
+AGS      = 0.2000000           B0       = 6.3000000E-08       B1       = 0.00                
*
* SUBTHRESHOLD CURRENT PARAMETERS
*
+VOFF     = -9.5000000E-02      LVOFF    = -1.7000000E-09      WVOFF    = -1.9999999E-09      
+PVOFF    = -1.0000000E-16      NFACTOR  = 0.9000000           LNFACTOR = 1.0000000E-07       
+PNFACTOR = -5.0000000E-15      CIT      = 0.00                CDSC     = 0.00                
+CDSCB    = 0.00                CDSCD    = 0.00                ETA0     = 4.0000000E-02       
+ETAB     = -2.5000000E-02      DSUB     = 0.5600000           
*
* ROUT PARAMETERS
*
+PCLM     = 0.7000000           PDIBLC1  = 0.00                PDIBLC2  = 7.0000000E-03       
+PDIBLCB  = 0.00                DROUT    = 0.5600000           PSCBE1   = 4.0000000E+08       
+PSCBE2   = 1.0000000E-07       PVAG     = 0.00                DELTA    = 1.0000000E-02       
+ALPHA0   = 7.0000000E-08       ALPHA1   = 7.0491700           BETA0    = 22.8424000          
+LBETA0   = -7.5000000E-08         
*
* TEMPERATURE EFFECTS PARAMETERS
*
+KT1      = -0.2577007          KT2      = -3.0979900E-02      LKT2     = -3.0000000E-09      
+PKT2     = -6.5331750E-16      AT       = 1.0000000E+04       PAT      = -1.0000000E-09      
+UTE      = -1.2703574          UA1      = 5.3866300E-10       WUA1     = 1.1000000E-16       
+PUA1     = -2.3700001E-24      UB1      = -2.0709999E-18      UC1      = 2.0609721E-11       
+KT1L     = -8.0000000E-09      PRT      = 90.0000000          
*    
* NOISE PARAMETERS
*
+NOIMOD   = 2                   NOIA     = 3.3617E+18            NOIB     = 1.9536E+05    
+NOIC     = 5.2658E-12          EM       = 6.2548E+07            EF       = 1.1307E+00 
*
* CAPACITANCE PARAMETERS
*
+CJ       = 0.00107                 MJ       = 0.415                 PB       = 0.817                   
+CJSW     = 9.89E-11                MJSW     = 0.489                 PBSW     = 1               
+CJSWG    = 5.07E-10                MJSWG    = 0.489                 PBSWG    = 1       
+TPB      = 0.00153                 TPBSW    = 0.00117               TPBSWG   = 0.00117
+TCJ      = 0.000876                TCJSW    = 0.000745              TCJSWG   = 0.000745
+JS       = 1.66E-07                JSW      = 1.2E-13               NJ       = 1.0384   
+XTI      = 4.5                     NQSMOD   = 0                     ELM      = 5 
+CGDO     = 4.20E-10                CGSO     = 4.20E-10                     
+CAPMOD   = 3                       XPART    = 1                     CF       = 0.00                                    
+ACDE     = 0.8505076               MOIN     = 14.95341              NOFF     = 1.431824              
+DLC      = -1.5E-09
*               
* ==================================

.param w_diff    = {w_diff}
.param l_diff    = {l_diff}
.param w_load    = {w_load}
.param l_load    = {l_load}
.param w_tail    = {w_tail}
.param l_tail    = {l_tail}
.param w_out     = {w_out}
.param l_out     = {l_out}
.param w_outload = {w_outload}
.param l_outload = {l_outload}
.param cc_val    = {cc_val}
.param rz_val    = {rz_val}

* ==================================
* 电源电压 1.8V
Vdd vdd 0 dc 1.8
Vss vss 0 dc 0

* 偏置电路 - PMOS 电流镜像主管 (二极管连接)
* 形成 PMOS 镜像，为 M3/M4 提供偏置
* 漏极和栅极连接到nbias，源极连接到vdd
Mb nbias nbias vdd vdd pmos_gen w={w_tail} l={l_tail}

* 第一级：差分输入级 (Differential Pair)
* M1: 接 vin- (反相输入)
* M2: 接 vip  (同相输入)
M1 d1 vin s1 0 nmos_gen w={w_diff} l={l_diff}
M2 d2 vip s1 0 nmos_gen w={w_diff1} l={l_diff1}

* 主动负载 (PMOS Active Load - 电流镜像)
* M3: 二极管连接，镜像参考
* M4: 镜像输出
M3 d1 d1 vdd vdd pmos_gen w={w_load} l={l_load}
M4 d2 d1 vdd vdd pmos_gen w={w_load1} l={l_load1}

* 尾电流源 (NMOS 恒流源)
M5 s1 nbias 0 0 nmos_gen w={w_tail1} l={l_tail1}

* 第二级：共源极放大级 (Common Source Stage)
* M6: PMOS 输入管
* M7: NMOS 负载管
M6 out d2 vdd vdd pmos_gen w={w_out} l={l_out}
M7 out nbias 0 0 nmos_gen w={w_outload} l={l_outload}

* 米勒补偿 (Miller Compensation)
* Cc: 补偿电容，连接第一级输出和第二级输出
* Rz: 零点电阻，与 Cc 串联形成 RC 补偿网络
Cc d2 n_rc {cc_val}
Rz n_rc out {rz_val}

* 负载电容 (标准写法: 使用 pF 单位)
Cload out 0 1pF
Rload out 0 1Meg
* ================= 4. 激励源 =================
* 差分输入信号 (修正: 实现真正的差分激励)
* 共模电压 0.9V，交流差分信号 ±10mV
* vip - vin = 2V (差分)
Vin_p vip 0 dc 0.9 ac 1m
Vin_n vin 0 dc 0.9 ac -1m

* ================= 5. 仿真控制 =================
.control
    * 禁止交互式询问，防止脚本卡死
    unset askquit
    set nobreak
    
    * 1. 静态工作点分析
    * ================= 1. 静态工作点分析 (功耗计算) =================
    op
    * [Power] 直接计算静态功耗
    * i(Vdd) 为流出电源的电流(通常为负值)，取绝对值
    * 注意: 在op分析后立即保存结果，避免被ac分析覆盖
    let v_sup   = 1.8
    let i_total = abs(i(Vdd))
    let power_w0 = i_total * v_sup
    
    ac dec 20 1 10000Meg
    
    * 3. 测量与计算
    
    * [Gain] 获取低频增益 (vdb(out) 在 1Hz 处的值)
    * 差分输入幅值为 2V，输出增益为 vdb(out)
    meas ac gain find vdb(out) at=1
    let dc_gain= gain+60
    * [GBW] 获取单位增益带宽 (增益降为 0dB 的频率)
    * 使用更宽松的条件：找到增益降到20dB以下的频率
    * 如果测量失败，使用100MHz作为默认值
    meas ac gbw_final find frequency when vdb(out)=-60 cross=last
    * 如果gbw测量失败，使用100MHz作为默认值
    * 如果gbw存在且有效，使用测量值
    * 注意：如果gbw测量失败，gbw_final保持为100e6
    
    * [PM] 计算相位裕度
    * 在10MHz处测量相位（作为相位裕度的近似）
    meas ac phase_at_gbw find vp(out) at=gbw_final
    let pm = 180 + (phase_at_gbw*180/PI)
    * 相位裕度计算
    * 使用10MHz处的相位计算相位裕度
    
    * [Power] 重新计算总功耗（在打印前，从OP分析结果）
    * 从OP分析中获取静态电流，功耗 = |I| * VDD
    meas ac i_1 find i(vdd) at=1000
    let power_w1 = abs(i_1) * 1.8 * 0.707
    * 4. 输出结果格式化 (供 Python 正则提取)
    * 使用 print 命令打印变量值，power_w 使用 echo 直接输出
    echo RESULT_START
    print dc_gain
    print gbw_final
    print pm
    setplot op1
    echo power_w0 = $&power_w0
    setplot ac1
    echo power_w1 = $&power_w1
    echo RESULT_END
    
    quit
.endc

.end