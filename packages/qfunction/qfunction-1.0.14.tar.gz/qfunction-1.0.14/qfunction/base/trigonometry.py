from qfunction.base.base import *
from numpy import sin, cos
import numpy as np
from math import atan

def q_sin(u,q,cpx=False,israd=True):
    u = radian(u) if( not israd) else u
    b = 1j
    u*=1j
    if cpx:
        return ((q_exp(u,q)-q_exp(-u,q)))/(2*b)
    else:
        return (((q_exp(u,q)-q_exp(-u,q)))/(2*b)).real



def q_cos(u,q=1,cpx=False,israd=True):
    u = radian(u) if not israd else u
    u=u*1j;
    A =lambda w: 1/(1-w)
    if (q> 1.9 and u>= limit(A,q)):
        return np.nan
    else:
    	if cpx:
         return ((q_exp(u,q)+q_exp(-u,q)))/2
    	else:
         return (((q_exp(u,q)+q_exp(-u,q)))/2).real

