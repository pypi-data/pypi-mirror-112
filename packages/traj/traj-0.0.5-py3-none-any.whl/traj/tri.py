"""routines for tridiagonal matrices"""

from numba import njit
import numpy as np
from numpy import asarray

@njit
def tridiag_mul(tri,x):
    _tri, _x = asarray(tri), asarray(x)
    _b = np.empty_like(_x)
    _b[0] = _tri[1,0] * _x[0] + _tri[0,1] * _x[1]
    for _i in range(1,_x.shape[0]-1):
        _b[_i] = _tri[2,_i-1] * _x[_i-1] \
                + _tri[1,_i] * _x[_i] \
                + _tri[0,_i+1] * _x[_i+1]
    _b[-1] = _tri[2,-2] * _x[-2] + _tri[1,-1] * _x[-1]
    return _b

def d2trid(N,h):
    _tr = np.empty((3,N))
    _tr[0,1:] = 1
    _tr[1,:] = -2
    _tr[2,:-1] = 1
    _tr *= 1./h**2
    return _tr

def eye_trid(N):
    _tr = np.empty((3,N))
    _tr[0,1:] = 0.
    _tr[1,:] = 1.
    _tr[2,:-1] = 0.
    return _tr
