import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import trapz

def read_xsec(fname, scale=1e-41):
    Enu,Xsec = np.loadtxt(fname,usecols=[0,1]).T
    xsec = interp1d(Enu, Xsec*scale, bounds_error=False)
    return xsec

def N_targets(mass, mfrac=1.0):
    Na = 6.022e23 #atoms/mol
    mu = 1
    return Na*mass*mfrac*1e3/mu

def signal(f,xsec,Ntgt,eff=1.):
    res = xsec(f.E)*eff(f.E)*f.N.T*Ntgt
    return f.T,trapz(res,f.E, axis=1)

def read_eff(fname, Eshift=1.293):
    e,eff = np.loadtxt(fname, comments='#', delimiter=',').T
    e+=Eshift
    return interp1d(e,eff,kind='linear', bounds_error=False, fill_value=(0,eff[-1]))

class Detector:
    def __init__(self, name, eff, mass, mfrac):
        self.name = name
        if callable(eff):
            self.eff = eff
        elif isinstance(eff, str):
            self.eff = read_eff(eff)
        else:
            eff_val=eff
            self.eff = lambda e:eff_val*np.ones_like(e)

        self.mass = mass
        self.Ntgt = N_targets(mass,mfrac)
    def signal(self, flux, xsec):
        f = flux['ebar'][0]
        return signal(f,xsec,self.Ntgt, self.eff)
