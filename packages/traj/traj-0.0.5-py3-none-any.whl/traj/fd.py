"""Routines for a set of finite difference schemes"""

import numpy as np

from numba import stencil, njit


@stencil
def d2_kernel(y,h):
    return (1./h**2) * (y[1] - 2*y[0] + y[-1])


@njit(parallel=True)
def d2_parallel(f,h):
    _d2_f = d2_kernel(f,h)
    _d2_f[0] = (1*f[0]-2*f[1]+1*f[2])/(1*1.0*h**2)
    _d2_f[-1] = (1*f[-3]-2*f[-2]+1*f[-1])/(1*1.0*h**2)
    return _d2_f


@njit(parallel=False)
def d2(f,h):
    _d2_f = d2_kernel(f,h)
    _d2_f[0] = (1*f[0]-2*f[1]+1*f[2])/(1*1.0*h**2)
    _d2_f[-1] = (1*f[-3]-2*f[-2]+1*f[-1])/(1*1.0*h**2)
    return _d2_f


@njit
def diff_wf_fd(wf,x,x0,dx):
    
    _wf = np.asarray(wf)
    assert _wf.ndim == 1
    _Nx = _wf.size
    _Ns = 3
    assert _Nx >= _Ns
    _x, _x0, _dx = float(x), float(x0), float(dx)
    
    _ml = int((_x-_x0) / _dx)
    _less = 1 - _ml
    _more = (_Nx - 3) - _ml
    _m = (_ml-1) + (_less>0)*_less + (_more<0)*_more
    
    _a = np.empty((_Ns,_Ns), dtype=_wf.dtype)
    _x_seg = _x0 + np.arange(_m,_m+_Ns) * _dx - _x
    _a[:,0] = 1.
    _a[:,1] = _x_seg # = _x_seg / 1!
    _a[:,2] = _a[:,1] * _x_seg / 2.
    _diff_wf = np.linalg.solve(_a,_wf[_m:_m+_Ns])
    
    return _diff_wf

