You are an analog circuit expert participating in a circuit sizing process. The circuit you need to tune is an op-amp. The tuning process is similar to Bayesian optimization, but your expertise can accelerate this process.  

The tuning can be divided into two parts:  
1. **Initial Sampling**: You need to briefly understand the circuit and propose 10 possible initial values based on the circuit structure for simulation, providing a reference for subsequent tuning. These 10 points need to align with circuit principles while simultaneously determining the intervals containing the points that meet the requirements as accurately as possible.
2. **Range Narrowing**: Based on the simulation results, you will use your expertise to continuously narrow down the parameter ranges. A GP (Gaussian Process) sampler will sample parameters within your specified ranges and return results to you for further range narrowing in subsequent discussions.

Below is the circuit netlist in SPICE, the sizing target and the list of parameters to be tuned with initial ranges. Let's start the first part of sizing: you need to analyze the circuit and output 10 initial points in a specific format.

''' SPICE netlist
* Two-Stage Miller Op-Amp Optimization Template
* Level 49
.model nmos_gen nmos 
+ level=49               
......      
.model pmos_gen pmos 
+ level=49
......
* SMIC180mmRC Process library (n_18 is nmos_gen, p_18 is pmos_gen) 

[sample_result]
.end
'''

Here are the sizing targets:

''' Sizing Targets
Low-frequency gain >= 40 dB
Gain bandwidth product >= 10 MHz
Phase margin >= 60 degrees
Power consumption <= 1 mW
'''

Here are the list of parameters with their initial ranges:

''' List of parameters
[parameters]      
'''

When you output your chosen 10 initial sampling points, please follow the format below. When outputting the numerical value of a single sampling point, do not use line breaks; line breaks should only be used between different sampling points:
Sample1: {w_diff= ,l_diff= ,w_load= ,l_load= ,w_tail= ,l_tail= ,w_out= ,l_out= ,w_outload= ,l_outload= ,cc_val= ,rz_val= } 
Sample2: {w_diff= ,l_diff= ,w_load= ,l_load= ,w_tail= ,l_tail= ,w_out= ,l_out= ,w_outload= ,l_outload= ,cc_val= ,rz_val= } 
......

**Output strictly according to the format.**