You are an analog circuit expert, involved in the sizing of an op-amp. You now need to read a SPICE circuit netlist, carefully analyze the circuit structure and parameters, and use your understanding of the circuit configuration to find equivalent relationships among these parameters, such as identical parameters for two transistors in a differential pair or current mirror.

Here is the SPICE circuit netlist:

''' SPICE netlist
* Two-Stage Miller Op-Amp Optimization Template
Vdd vdd 0 dc 1.8
Vss vss 0 dc 0

Mb nbias nbias vdd vdd pmos_gen w={w_tail} l={l_tail}

M1 d1 vin s1 0 nmos_gen w={w_diff} l={l_diff}
M2 d2 vip s1 0 nmos_gen w={w_diff1} l={l_diff1}

M3 d1 d1 vdd vdd pmos_gen w={w_load} l={l_load}
M4 d2 d1 vdd vdd pmos_gen w={w_load1} l={l_load1}

M5 s1 nbias 0 0 nmos_gen w={w_tail} l={l_tail}

M6 out d2 vdd vdd pmos_gen w={w_out} l={l_out}
M7 out nbias 0 0 nmos_gen w={w_outload} l={l_outload}

Cc d2 n_rc {cc_val}
Rz n_rc out {rz_val}

Cload out 0 1pF
Rload out 0 1Meg
* ==================================
Vin_p vip 0 dc 0.9 ac 10m
Vin_n vin 0 dc 0.9 ac -10m
'''

Below is the parameter list of the circuit:

''' List of parameters
w_diff
l_diff
w_diff1 
l_diff1
w_load    
l_load 
w_load1  
l_load1 
w_tail 
l_tail
w_tail1 
l_tail1
w_out 
l_out
w_outload
l_outload
cc_val
rz_val
'''

You need to analyze the circuit, utilize the relationships between its structure and parameters to find equivalent relationships among the above circuit parameters, thereby reducing variables during the tuning process. You must strictly follow the format below to output the equivalent relationships you derive from the analysis. When outputting an equivalent relationship, do not use line breaks; line breaks should only be used between different equivalent relationships:

Equality1: {w_diff=w_diff1}
Equality2: {w_diff=w_diff1}
......

**Please strictly adhere to the above format when outputting the equivalent relationships. Do not output any unnecessary content in your equality output. Do not use any other equal relationships except for structural symmetry.**