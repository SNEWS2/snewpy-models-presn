import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def _interpolate(x,y,z,new_x=None, new_y=None, logx=True):
    if(new_x is not None): #interpolate in T
        if(logx):
            z = interp1d(np.log(x),np.log(z)
                         ,axis=1, bounds_error=False, fill_value=0)(np.log(new_x))
            z = np.exp(z)
        else:
            z = interp1d(x,z,axis=1, bounds_error=False, fill_value=0)(new_x)
        x = new_x
    if(new_y is not None): #interpolate in E
        z = interp1d(y,z,axis=0, bounds_error=False, fill_value=0)(new_y)
        y = new_y
    return x,y,np.nan_to_num(z)

def _read_Odrzywolek(fname, Es=None, Ts=None):
    if Es is None:
        Es = np.linspace(0,20,201)

    df = pd.read_csv(fname,delim_whitespace=True, skiprows=1, 
                 names=['step','time','Q','R','Eavg','Sigma','a','alpha','b'])
    a     = np.expand_dims(df.a,0)
    alpha = np.expand_dims(df.alpha,0)
    b     = np.expand_dims(df.b,0)
    Enu = np.expand_dims(Es,1)
    
    L = a*Enu**alpha*np.exp(-b*Enu)
    Ts0 = df.time.values
    
    ts1,es1,L1 = _interpolate(Ts0,Es,L,new_x=Ts)
    ex_ratio=0.19 #ratio from SK paper
    fluxes = {'ebar':(ts1,es1,L1)}
    fluxes['xbar']=(ts1,es1,L1*ex_ratio)
    fluxes['e']=fluxes['ebar']
    fluxes['x']=fluxes['xbar'] 
    return fluxes

def _read_Patton(fname,Es=None, Ts=None):
    df = pd.read_csv(fname, comment='#', delim_whitespace=True,
                     names=['time','Enu','Lnue','Lnuebar','Lnux','Lnuxbar'], 
                     usecols=range(6))

    df1 = df.set_index(['time','Enu']).unstack()
    fluxes = {}
    for flv in ['e','ebar','x','xbar']:
        table = df1[f'Lnu{flv}']
        Ts0=table.index.values*3600
        Es0=table.columns.values
        L =table.values.T
        #if flv in ['x','xbar']: L*=2
        fluxes[flv] = _interpolate(Ts0,Es0,L,new_x=Ts,new_y=Es)
    return fluxes

def _read_Kato(path,Es=None, Ts=None):
    fluxes = {}
    for flv in ['nue','nueb','nux','nuxb']:
        if flv.startswith('nue'):
            pth = f'{path}/total_{flv}'
            ts,step = np.loadtxt(f'{pth}/lightcurve_{flv}_all.dat', usecols=[0,3]).T
            fname1 = f'{pth}/spe_all'
        if flv.startswith('nux'):
            pth = f'{path}/total_nux'
            ts,step = np.loadtxt(f'{pth}/lightcurve.dat', usecols=[1,0]).T
            if flv=='nux':
                fname1 = f'{pth}/spe_sum_mu_nu'
            else:
                fname1 = f'{pth}/spe_sum_mu'
        d2NdEdT = []
        for s in step:
            es,dNdE = np.loadtxt(f'{fname1}{s:05.0f}.dat').T
            d2NdEdT+=[dNdE]

        d2NdEdT = np.stack(d2NdEdT).T
        fluxes[flv] = _interpolate(ts,es,d2NdEdT,new_x=Ts, new_y=Es)
    fluxes['e'] = fluxes.pop('nue')
    fluxes['x'] = fluxes.pop('nux')
    fluxes['ebar'] = fluxes.pop('nueb')
    fluxes['xbar'] = fluxes.pop('nuxb')
    
    return fluxes

from .snmodel import SNFlux, SNModel
def read_model(fname, fmt='Pat', Ts=None, Es=None,mass=None, **kwargs):
    
    reader = { 'Pat':_read_Patton, 
               'Odr':_read_Odrzywolek,
              'Kato':_read_Kato,
              }
    
    fluxes = reader[fmt](fname, Ts=Ts, Es=Es)
    fluxes = {f:SNFlux(*fluxes[f]) for f in fluxes}
    m = SNModel(fluxes, **kwargs)
    m.name = fmt
    m.mass = mass
    return m
    
    
    