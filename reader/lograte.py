import numpy as np

def sort(x,y):
        idx=np.argsort(x)
        return x[idx],y[idx]
    
class LogRate:
    def __init__(self, x,y):
        x,y = sort(x,y)
        a = np.diff(np.log(y))/np.diff(np.log(x))
        yi = (x[1:]*y[1:]-y[:-1]*x[:-1])/(a+1)
        yi = np.nan_to_num(yi)
        yi=np.append([0],yi)
        yi = np.cumsum(yi)
        self.x,self.y = x,y
        self.a,self.yi = a, yi
    
    def _index(self,x):
        if np.isscalar(x):
            x = [x]
        idx = np.searchsorted(self.x,x)-1
        idx[idx<0]=0
        idx[idx>len(self.a)-1] = len(self.a)-1
        return idx
    def __call__(self, x):
        idx = self._index(x)
        return self._eval(idx)(x)
    
    def _eval(self, idx):
        a = self.a[idx]
        x0,y0 = self.x[idx],self.y[idx]
        return lambda x:y0*(x/x0)**a
    
    def _int(self, x):
        idx = self._index(x)
        a = self.a[idx]
        x0,y0 = self.x[idx],self.y[idx]
        y1 = self._eval(idx)(x)
        res = self.yi[idx]+(y1*x-y0*x0)/(a+1)
        return res
    
    def integral(self,x0,x1):
        return self._int(x1)-self._int(x0)