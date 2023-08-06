from qfunction.quantum.quantum_circuit import q_psi, q_phi,q_cos,q_sin
from math import atan
from numpy import sin,cos
import numpy as np
def q_omega(theta_time,q=1):
    q = (1+q)/2
    return q_phi(theta_time,q)

def Sx(t,q=1):
    return (cos(q_omega(t,q))-sin(q_omega(t,q)))

def Sy(t,q=1):
    return (sin(q_omega(t,q))+cos(q_omega(t,q)))

def probabilities_q(theta,gamma,q):
    state = q_psi(theta=gamma,gamma=theta,q=q)
    total = abs(state[0])+abs(state[1])
    probs = [np.power(state[0],2),np.power(state[1],2)]
    return (probs[0][0],probs[1][0])

