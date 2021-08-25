import sys
sys.path.append('/Users/norbert/Desktop/LYR/my_python_tools/')
from get_data_tools import *



df=pd.read_csv("NO-Adv_dataset.csv",parse_dates=True,index_col=0)

#pdb.set_trace()

ddf=df[df.qc_LE==0]
ddf=ddf[abs(ddf.LE)<150.]
ddf=ddf[ddf.index>'2015-06-01']
ddf=ddf[ddf.index<'2015-07-01']

outdf=ddf[['LE', 'T_air', 'P_air', 'RH_air', 'wind_speed', 'wind_dir', 'Enet','ground_heat_flux']]

outdf.to_csv('ET_Adv.csv')