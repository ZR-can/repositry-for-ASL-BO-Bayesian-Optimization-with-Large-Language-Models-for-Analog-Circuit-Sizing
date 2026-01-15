* Two-Stage Miller Op-Amp Optimization Template
Vdd vdd 0 dc 1.8
Vss vss 0 dc 0

Mb nbias nbias vdd vdd pmos_gen w={w_tail} l={l_tail}

M1 d1 vin s1 0 nmos_gen w={w_diff} l={l_diff}
M2 d2 vip s1 0 nmos_gen w={w_diff1} l={l_diff1}

M3 d1 d1 vdd vdd pmos_gen w={w_load} l={l_load}
M4 d2 d1 vdd vdd pmos_gen w={w_load1} l={l_load1}

M5 s1 nbias 0 0 nmos_gen w={w_tail1} l={l_tail1}

M6 out d2 vdd vdd pmos_gen w={w_out} l={l_out}
M7 out nbias 0 0 nmos_gen w={w_outload} l={l_outload}

Cc d2 n_rc {cc_val}
Rz n_rc out {rz_val}

Cload out 0 1pF
Rload out 0 1Meg

Vin_p vip 0 dc 0.9 ac 1m
Vin_n vin 0 dc 0.9 ac -1m