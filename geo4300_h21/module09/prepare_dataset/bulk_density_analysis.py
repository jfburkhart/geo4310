'''
Script to anaylyze bulk density behavior at Finse aver the past few years
S. Filhol, April 2018

1- look at bulk density vs depth
    - plot type of cutter as third variable
2- look at bulk density over season

3- try a simple linear model including time of winter and depth

4- try fancier model (sturm et al, and the newer one)


Publication of interest:
    https://www.the-cryosphere.net/8/521/2014/tc-8-521-2014.pdf


'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

#===================================================================0
#    Import densities

dendf = pd.read_csv('./density/data/bullk_density_all.csv', sep=';')

# extract date and calculate day of winter (dow) with October 15 as a reference
dendf['timestamp'] = pd.to_datetime(dendf.date, format="%Y%m%d")
dendf['doy'] = dendf.timestamp.dt.dayofyear
dendf['winter'] = dendf.doy
dendf.winter.loc[dendf.timestamp.dt.month >= 9] = dendf.timestamp.loc[dendf.timestamp.dt.month >= 9].dt.year + 1
dendf.winter.loc[dendf.timestamp.dt.month < 9] = dendf.timestamp.loc[dendf.timestamp.dt.month < 9].dt.year
dendf['dow'] = dendf.doy
dendf.dow.loc[dendf.doy<150] = dendf.doy.loc[dendf.doy<150] + (31+30+15)   # day of winter
dendf.dow.loc[dendf.doy>150] = dendf.doy.loc[dendf.doy>150] - (365-(31+30+15))   # day of winter

#====================================================================


plt.figure()
plt.scatter(dendf.snow_depth_cm, dendf.snow_density, c=dendf.winter)
plt.colorbar()
plt.show()

plt.figure()
plt.scatter(dendf.snow_depth_cm, dendf.dow, c=dendf.snow_depth_cm)
plt.colorbar()
plt.show()

plt.figure()
plt.hist(dendf.snow_density, bins=20)

#=====================================================
# stat models

results = smf.ols('snow_density ~ dow + snow_depth_cm + C(winter)', data=dendf).fit()
print(results.summary())

results = smf.ols('snow_density ~ (dow + snow_depth_cm) * C(winter)', data=dendf).fit()
print(results.summary())



for winter in np.unique(dendf.winter):
    print('\n\n*******************************************************************')
    print('Winter: ' + str(winter) + ' \n')
    dendftmp = dendf.loc[dendf.winter == winter]
    if dendftmp.shape[0]>=5:
        results = smf.ols('snow_density ~ dow + snow_depth_cm', data=dendftmp).fit()
        print(results.summary())
    else:
        print('WARNING: not enough observation to fit a model. 5 observations required')