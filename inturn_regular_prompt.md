You continue proceeding to the second step and **narrow or change** the parameter range of the op-amp within the original range step by step. I will first provide you with the simulation results from the sampling points mentioned above. Based on these results and the previous circuit structure, you need to propose the sampling range for the next step. You can continuously narrow the range over 10 iterations to improve the performance of the selected parameters. **This is the [number] iteration.** After you propose the range, a GP proposer will select five possible parameters from your chosen range for simulation, and you will then need to narrow down the range further based on these results.

Here are the simulation results for the sampling points. (The simulation result for a point being "None" indicates that the op-amp is not functioning properly, with a low-frequency gain lower than 0dB.):

''' Simulation Results
[sample_result]
'''

Here are the sizing targets:

''' Sizing Targets
Low-frequency gain >= 50 dB
Gain bandwidth product >= 20 MHz
Phase margin >= 90 degrees
Power consumption <= 1 mW
'''

Here are the parameter list and the current parameter ranges:

''' List of parameters
[parameters]
'''

Now you need to output the range for each parameter in this iteration. You must strictly follow the format below to output your result. When outputting an equivalent relationship, do not use line breaks; line breaks should only be used between different equivalent relationships:
Bound: {w_diff: [1e-06, 0.0001]}
Bound: {l_diff: [1e-06, 0.0001]}
......

**The upper and lower bounds of a parameter range cannot be the same.**
**Please strictly adhere to the above format when outputting the parameters' ranges.**