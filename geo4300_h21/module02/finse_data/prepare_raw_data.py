import pandas as pd
import glob
import pdb
import numpy as np

licor_files=glob.glob("*_LATICE-Flux_Finse.data")

for licor_file in licor_files:
    print licor_file
    
    df = pd.read_csv(licor_file, skiprows=7,index_col=0,parse_dates=[[5,6]],sep='\t')
    
    df['U_m/s']=np.sqrt( df['Aux 1 - U (m/s)']**2 + df['Aux 2 - V (m/s)']**2 )
    
    df['u_m/s']=df['Aux 1 - U (m/s)']
    df['v_m/s']=df['Aux 2 - V (m/s)']
    df['w_m/s']=df['Aux 3 - W (m/s)']
    
    df['T_degC']=(df['Aux 4 - SOS (m/s)'])**2 /1.4 /287.04 -273.15 #cf. CSAT3 manual eq.9
    
    df['CO2_ppm']=df['CO2 dry(umol/mol)']
    df['H2O_ppt']=df['H2O dry(mmol/mol)']
    
    outdf=df[['u_m/s','v_m/s','w_m/s','T_degC','CO2_ppm','H2O_ppt']]
    
    timestr=[outdf.index[ii].split(':')[0]+':'+ outdf.index[ii].split(':')[1]+':'+outdf.index[ii].split(':')[2]+'.' +outdf.index[ii].split(':')[3] for ii in range(len(outdf))]
    outdf=outdf.set_index(pd.to_datetime(timestr))
    
    outname='../'+licor_file.split('_')[0]+'.csv'
    
    outdf.to_csv(outname)
    
    

