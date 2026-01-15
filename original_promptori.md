You are an analog circuit expert participating in a circuit sizing process. The circuit you need to tune is an op-amp. The tuning process is similar to Bayesian optimization, but your expertise can accelerate this process.  

The tuning can be divided into two parts:  
1. **Initial Sampling**: You need to briefly understand the circuit and propose 10 possible initial values based on the circuit structure for simulation, providing a reference for subsequent tuning. These 10 points need to align with circuit principles while simultaneously determining the intervals containing the points that meet the requirements as accurately as possible.
2. **Range Narrowing**: Based on the simulation results, you will use your expertise to continuously narrow down the parameter ranges. A GP (Gaussian Process) sampler will sample parameters within your specified ranges and return results to you for further range narrowing in subsequent discussions.

Below is the circuit netlist in SPICE, the sizing target and the list of parameters to be tuned with initial ranges. Let's start the first part of sizing: you need to analyze the circuit and output 10 initial points in a specific format.

''' SPICE netlist
* Two-Stage Miller Op-Amp Optimization Template
* Two-Stage Miller Op-Amp Optimization Template
* Level 49
.model nmos_gen nmos 
+ level=49               
......      
.model pmos_gen pmos 
+ level=49
......
* SMIC180mmRC Process library (n_18 is nmos_gen, p_18 is pmos_gen) 

Vdd vdd 0 dc 1.8
Vss vss 0 dc 0

Mb nbias nbias vdd vdd pmos_gen w={w_tail} l={l_tail}

M1 d1 vin s1 0 nmos_gen w={w_diff} l={l_diff}
M2 d2 vip s1 0 nmos_gen w={w_diff} l={l_diff}

M3 d1 d1 vdd vdd pmos_gen w={w_load} l={l_load}
M4 d2 d1 vdd vdd pmos_gen w={w_load} l={l_load}

M5 s1 nbias 0 0 nmos_gen w={w_tail} l={l_tail}

M6 out d2 vdd vdd pmos_gen w={w_out} l={l_out}
M7 out nbias 0 0 nmos_gen w={w_outload} l={l_outload}

Cc d2 n_rc {cc_val}
Rz n_rc out {rz_val}

Cload out 0 1pF
Rload out 0 1Meg
*==================================
Vin_p vip 0 dc 0.9 ac 1m
Vin_n vin 0 dc 0.9 ac -1m
.end
'''

Here are the sizing targets:

''' Sizing Targets
Low-frequency gain >= 60 dB
Gain bandwidth product >= 20 MHz
Phase margin >= 90 degrees
Power consumption <= 1 mW
'''

Here are the list of parameters with their initial ranges:

''' List of parameters
w_diff: [1e-6, 100e-6],      
l_diff: [0.18e-6, 1e-5],   
w_diff1: [1e-6, 100e-6],      
l_diff1: [0.18e-6, 1e-5],
w_load: [1e-6, 100e-6],     
l_load: [0.18e-6, 1e-5],
w_load1: [1e-6, 100e-6],     
l_load1: [0.18e-6, 1e-5],   
w_tail: [1e-6, 100e-6],     
l_tail: [0.18e-6, 1e-5],   
w_tail1: [1e-6, 100e-6],     
l_tail1: [0.18e-6, 1e-5],
w_out: [1e-6, 100e-6],     
l_out: [0.18e-6, 1e-5],    
w_outload: [1e-6, 100e-6],  
l_outload: [0.18e-6, 1e-5], 
cc_val: [0.1e-12, 1e-10],  
rz_val: [100, 10000],       
'''

When you output your chosen 10 initial sampling points, please follow the format below. When outputting the numerical value of a single sampling point, do not use line breaks; line breaks should only be used between different sampling points:
Sample1: {w_diff= ,l_diff= ,w_diff1= ,l_diff1= ,w_load= ,l_load= ,w_load1= ,l_load1= ,w_tail= ,l_tail= ,w_out= ,l_out= ,w_outload= ,l_outload= ,cc_val= ,rz_val= } 
Sample2: {w_diff= ,l_diff= ,w_diff1= ,l_diff1= ,w_load= ,l_load= ,w_load1= ,l_load1= ,w_tail= ,l_tail= ,w_out= ,l_out= ,w_outload= ,l_outload= ,cc_val= ,rz_val= } 
......

**Output strictly according to the format.**