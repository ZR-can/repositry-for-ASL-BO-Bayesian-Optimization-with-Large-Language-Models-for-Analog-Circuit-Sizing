***0.18um Mixed Signal 1P6M with MIM Salicide 1.8V/3.3V Process***
*** For HSPICE only ***

Update History:
     V0.1 : Initiate
     V0.2 : Add interconnect model (section 7.8)
     V1.0 : Main document change description:
            1. Re-extraction RF MOS model due to process change.    
               The new model includes RF MOS of finger width =10um   
               and 5um. Page5~21 of section7.2. are updated.
            2. Re-extraction MOS and junction varactor models due to process change. 
               Page29~30 of section7.4. are updated.
            3. Re-extraction SAB resistor model due to process change. Add jc1a, jc1b, 
               jc2a and jc2b in resistor model for more accuracy. Revised the sub-circuit 
               of resistor model for more accuracy at high frequency region. 
               Page36~39 of section7.6. are updated.
            4. The fitting curves of MOS (page45~53), varactor (page57~64) 
               and resistor (page71~76) are updated.
            Attachment change description:
            1. Add the attachment, res.def, for resistor simulation by Spectre.
            2. Revised í—ms018_v1p0.libí˜, í—ms018_v1p0_spe.libí˜and separated into four 
               model files (í—ms018_v1p0.cktí˜ and í—ms018_v1p0_res.cktí˜for HSPICE,í—ms018_v1p0_spe.cktí˜ 
               and í—ms018_v1p0_res_spe.cktí˜for Spectre, respectively) to provide the individual  
               corner model of MOSFETs, MIM and resistors.
            3. Revised readme file for model card usage.
            4. Revised the following GDS files: RNDIFSAB_W2L10.gds, RPDIFSAB_W2L10.gds  
               RNPOSAB_W2L10.gds, RPPOSAB_W2L10.gds
     V1.1 : Main document change description:
            1. Add the emphasis: the resistors with LDD implant are used for the SAB resistor model. 
            2. Revise the typo of DW and DL of N+Poly(SAB), P+Poly(SAB) and HRP in page38. 
               The DW and DL in model cards are still right.
            Attachment change description:
            The contents of all the model cards are not changed expect the following two items:
            1. Revise the gds files of resistors and varactors.
            2. Revise the file name of res.def to res_rf.def.
     V1.2 : All models (MOS, inductor, varactor, MIM) parameters are re-extracted 
            due to extending the range of device's dimension, except resistor and interconnect model. 
            Detail information as follows:
            In main document:
            1.Update wafer information in section 7.1.
	    2.Add ELDO format information in section 7.2.1.
	    3.Add DPVTHO into cormer model table in section 7.2.5.
	    4.Update dimension and frequency of devices measured and modeled in section 7.2.1, 7.3.1, 7.4.1, 7.5.1 and 7.6.1.
	    5.Update test structure layout information in section 7.3.2, 7.4.2, 7.5.2 and 7.6.2.
	    6.Update equivalent circuit description in section 7.2.3, 7.3.3, 7.4.3 and 7.5.3.
	    7.Update MOS scaling formulas in section 7.2.4.
	    8.Update MOS corner model to match its pcm spec in section 7.2.5.
	    9.Update inductor scaling formulas and inductor scalable model parameter list table in section 7.3.4.
	    10.Update varactor model and separate it into section 7.4 and 7.5.
	    11.Update varactor scaling formulas and scalable model parameter table in section 7.4.4 and 7.5.4.
	    12.Center the sheet resistance in section 7.7.4.
            In attachment:
            1. model card files:
               ms018_rf_v1p2_readme.txt 
               ms018_rf_v1p2.lib 
               ms018_rf_v1p2_mos.ckt 
               ms018_rf_v1p2_ind.ckt 
               ms018_rf_v1p2_var.ckt 
               ms018_rf_v1p2_res.ckt
               ms018_rf_v1p2_mim.ckt 
            2. gds files:  
               N18_W10LD18N8.gds  
               P18_W10LD18N8.gds  
               N33_W10LD35N8.gds  
               P33_W10LD30N8.gds  
               IND_W8S1D5R60N3D5.gds  
               VAR_MOS_W10L1N20.gds  
               VAR_JUN_W5L20N20.gds  
               MIM_A900.gds
            3. plot files:
               0.18um_RF_v1.2_Core.ppt
               0.18um_RF_v1.2_IO.ppt
               0.18um_RF_v1.2_IND.ppt
               0.18um_RF_v1.2_MIM.ppt
               0.18um_RF_v1.2_MOS_Var.ppt
               0.18um_RF_v1.2_Jun_Var.ppt
               0.18um_RF_v1.2_Res.ppt
     V1.3 : Main document is not changed expect update version form 1.2 to 1.3.
            Attachment change description: 
            1. Revise Rdc/Rsc parameters in all MOS model cards.
            2. Function pow is instead of pwr in SPECTRE model card.
     V1.4 : Main document update
	    1. Re-extract differential inductor parameters.
	    2. Change name in section 7.3 into spiral inductor.
            3. Add differential inductor parameters in section 7.4.
	    4. Re-arange section number in the following section.
	    In attachment:
	    1. model card files:
	       ms018_rf_v1p4_diff_ind.ckt
	       ms018_rf_v1p4_spri_ind.ckt
	    2. gds file:
	       DIFF_IND_W8S1D5R60T5.gds
	       SPRI_IND_W8S1D5R60N3D5.gds
	    3. plot file:
	       0.18um_RF_v1.4_Diff_IND.ppt
	       0.18um_RF_v1.4_Sprial_IND.ppt.
            Update version from 1.3 to 1.4
     V1.5 : Main document updated in order to add section 7.10 substrate coupling noise characterization report.
               In attachment:
               1. gds file:
                   PAA_Substrate_Noise_S30.gds
                   PAA_GR_Substrate_Noise_S30.gds
                   PAA_DNwell_Substrate_Noise_S30.gds
            Update version from 1.4 to 1.5


Files:

      ms018_rf_v1p4_readme.txt             .... This file!
      ms018_rf_v1p4.lib                    .... Corner values for MOSFETs, resistors and MIM
      ms018_rf_v1p4_mos.ckt                .... Subcircuit model of MOSFETs
      ms018_rf_v1p4_ind.ckt                .... Subcircuit model of inductor 
      ms018_rf_v1p4_var.ckt                .... Subcircuit model of varactors
      ms018_rf_v1p4_res.ckt                .... Subcircuit model of resistors
      ms018_rf_v1p4_mim.ckt                .... Subcircuit model of MIM 
      ms018_rf_layer.map                   .... GDSII layers definition file
      ms018_rf_interconnect_struct_1.txt   .... Interconnect tables for structure-1 (Parallel lines above a bottom plate)
      ms018_rf_interconnect_struct_2.txt   .... Interconnect tables for structure-2 (Parallel lines between two plates)
      N18_W10LD18N8.gds                    .... GDSII file for 1.8V NMOS W/L/N=10/0.18/8
      P18_W10LD18N8.gds                    .... GDSII file for 1.8V PMOS W/L/N=10/0.18/8
      N33_W10LD35N8.gds                    .... GDSII file for 3.3V NMOS W/L/N=10/0.35/8
      P33_W10LD30N8.gds                    .... GDSII file for 3.3V PMOS W/L/N=10/0.30/8
      SPRI_IND_W8S1D5R60N3D5.gds           .... GDSII file for Sprial Inductor W/S/R/N=8/1.5/60/3.5
      DIFF_IND_W8S1D5R60T5.gds      	   .... GDSII file for Differential Inductor W/S/R/T=8/1.5/60/5
      VAR_MOS_W10L1N20.gds                 .... GDSII file for Varactor MOS W/L/N=10/1/20
      VAR_JUN_W5L20N20.gds                 .... GDSII file for Varactor Junction Diode W/L/N=5/20/20
      MIM_A900.gds                         .... GDSII file for MIM Area=30*30
      RNDIFSAB_W2L10.gds                   .... GDSII file for Non-silicide N+ Diffusion Resistor W/L=2/10
      RPDIFSAB_W2L10.gds                   .... GDSII file for Non-silicide P+ Diffusion Resistor W/L=2/10
      RNPOSAB_W2L10.gds                    .... GDSII file for Non-silicide N+ Poly Resistor W/L=2/10
      RPPOSAB_W2L10.gds                    .... GDSII file for Non-silicide P+ Poly Resistor W/L=2/10
      RHRPO_W2L10.gds                      .... GDSII file for Non-silicide HR Poly Resistor W/L=2/10
      PAA_Substrate_Noise_S30.gds        .......... GDSII file for P+AA to P+AA spacing=30um Substrate coupling noise structure  
      PAA_GR_Substrate_Noise_S30.gds     ...... GDSII file for P+AA to P+AA spacing=30um with P+AA Guard Ring isolation Substrate coupling noise structure  
      PAA_DNwell_Substrate_Noise_S30.gds   .... GDSII file for P+AA to P+AA spacing=30um with Deep Nwell isolation Substrate coupling noise structure  

      
How to use SMIC SPICE models in HSPICE:

   1. Run MOS, inductor and varactor simulation:
      Add the following statements to HSPICE netlist.    
      Specify model corner by the '.lib' statement;
          .lib '/xxx/xxx/ms018_rf_v1p5.lib' TT
                                            ^^ RF MOS model corner
          /xxx/xxx is the directory where lib and ckt files are located.
          
   2. Run resistor simulation:        
      Add the following statements to HSPICE netlist.    
      Specify model corner by the '.lib' statement;
          .lib '/xxx/xxx/ms018_rf_v1p5.lib' RES_TT
                                            ^^ Resistor corner
          /xxx/xxx is the directory where lib and ckt files are located.

   3. Run MIM simulation:        
      Add the following statements to HSPICE netlist.    
      Specify model corner by the '.lib' statement;
          .lib '/xxx/xxx/ms018_rf_v1p5.lib' MIM_TT
                                            ^^ MIM corner
          /xxx/xxx is the directory where lib and ckt files are located.

          In the .lib file, all the subcircuits are included.         
          Then add the following statement in the netlist to define
          the subcircuit you want to simuilate.
          e.g. 
          
          a. 1.8V NMOS width(wr)=10um length(lr)=0.18um finger(nf)=8

             X1 1 2 3 4 n18_ckt_rf wr=10u lr=0.18u nf=8
 

          b. Inductor width=8um spacing=1.5um inner_redius(r)=60um turns(n)=3.5
             (Note:Spacing is fixed at 1.5um and width is fixed at 8um)
             X1 1 2 ind_rf r=60u n=3.5
          

          c. MIM Area(ar)=900um^2(30um*30um)
             X1 1 2 mim1_rf lr=30u wr=30u


          d. MOS varactor width(wr)=10um length(lr)=1um finger(nf)=20
             X1 1 2 pvar18w10l1_ckt_rf wr=10u lr=1u nf=20


          e. Junction varactor width(wr)=5um length(lr)=20um finger(nf)=20
             X1 1 2 pvardio18_ckt_rf wr=5u lr=20u nf=20


          f. Non-silicide N+ diffision resistor width(wr)=2um length(lr)=10um
             X1 1 2 rndifsab_ckt_rf l=10u w=2u


      Model corners are provided for MOSFETs, MIM and resistors. They are
      ----------------------------------------------------
      MOS                name : corner
      ----------------------------------------------------
                       TT : Typical case
                       SS : Slow case
                       FF : Fast case
                       SNFP : Slow N Fast P case    
                       FNSP : Fast N Slow P case    
      ----------------------------------------------------
      Resistor           name : corner
      ----------------------------------------------------
                       RES_TT : Typical case
                       RES_SS : Slow case
                       RES_FF : Fast case 
      ----------------------------------------------------
      MIM                name : corner
      ----------------------------------------------------
                       MIM_TT : Typical case
                       MIM_SS : Slow case
                       MIM_FF : Fast case 
      ----------------------------------------------------

  Whereas, Five model corners are provided for RF MOS and
  Three model corners are provided for MIM and resistors. 
  They are defined respectively in the .lib files.
      