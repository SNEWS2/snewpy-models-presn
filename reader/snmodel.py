import numpy as np
from copy import deepcopy as copy
from scipy.integrate import trapz

class _consts:
    kpc2cm = 3.086e+21
    Factor = 1/(4*np.pi*kpc2cm**2)
    FOE = 6.24150934326018e+11*1e51*1e-6 #Fifty-One-Erg to MeV
    sin12_2 = 0.308  #0.302
    sin13_2 = 0.0239 #0.02

    
class SNFlux:
    def __init__(self, T, E, d2NdEdT):
        assert(d2NdEdT.shape == (len(E),len(T)))
        self.E = E
        self.T = T
        self.N = d2NdEdT*_consts.Factor
    
    def projT(self):
        return self.T,trapz(self.N,x=self.E, axis=0)
    
    def projE(self):
        return self.E,trapz(self.N,x=self.T, axis=1)
    
    def __iadd__(self, other):
        if other is not None:
            assert(np.all(self.E==other.E))
            assert(np.all(self.T==other.T))
            self.N+=other.N
        return self
    
    def __imul__(self, factor):
        self.N*=factor
        return self
    
    def __mul__(self, factor):
        res = copy(self)
        res*=factor
        return res
    def __rmul__(self, factor):
        return self*factor
    
    def __add__(self, other):
        res = copy(self)
        res+=other
        return res
    
    def __radd__(self, other):
        return self+other
    
    def __repr__(self):
        return "SNFlux: \n * E={s.E},\n * T={s.T},\n * N={s.N}".format(s=self)

import re


def MSW(fluxes, order='N'):
    f0 = fluxes
    p0 = (1-_consts.sin12_2)*(1-_consts.sin13_2)
    p1 = _consts.sin13_2
    if order=='I':
        p0,p1 = p1,p0
    if order in {'N','I'}:
        fluxes = { 'e':p1*f0['e']+(1-p1)*f0['x'],
                  'x':p1*f0['x']+(1-p1)*f0['e'],
                  'ebar':p0*f0['ebar']+(1-p0)*f0['xbar'],
                  'xbar':p0*f0['xbar']+(1-p0)*f0['ebar'],
                 }
    else:
        fluxes = f0
    return fluxes

class SNModel:
    def __init__(self, fluxes, distance=1., order=None):
        self.fluxes = MSW(fluxes, order=order)
        self.set_distance(distance)
        self.order=order
        
    def set_distance(self, distance):
        self.distance = distance
        self.factor = 1/distance**2
        
    def at(self, distance):
        self.set_distance(distance)
        return self
    def MSW(self, order=None):
        if self.order is not None:
            raise RuntimeError(f"Can't apply MSW on oscillated ({self.order}) model")
        return SNModel(self.fluxes, self.distance, order=order)
    
    def __getitem__(self,flv_sel=".*"):
        match = lambda f:re.fullmatch(flv_sel,f)
        return [self.fluxes[f]*self.factor for f in self.fluxes if match(f)]
    