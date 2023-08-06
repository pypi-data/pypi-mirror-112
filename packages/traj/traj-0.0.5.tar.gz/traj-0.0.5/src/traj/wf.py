"""Routines related to wavefunctions"""

from numpy import asarray, pi, exp

def gaussian_1d(x,t,sigma):
    
    _x, _t = asarray(x), asarray(t)
    _sig = float(sigma)
    assert _sig > 0
    
    _a = 1. + 1.j / (2.*_sig**2) * _t
    _wf = (1./(2.*pi*_sig))**0.25 * 1./(_a)**0.5 \
        * exp(-_x**2 / ((4.*_sig**2) * _a))
    
    return _wf

