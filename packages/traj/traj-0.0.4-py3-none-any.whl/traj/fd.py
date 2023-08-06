"""Routines for a set of finite difference schemes"""

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

