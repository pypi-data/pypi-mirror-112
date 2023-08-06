from qfunction import *
from qfunction.quantum import *
from qfunction.quantum.quantum_circuit import q_phi
from numpy import sin,cos

def q_vector_bloch(gamma,theta:float=False,q=1,israd=True):
	gamma,theta = radian(gamma) if(not israd) else gamma, radian(theta) if(not israd) else theta
	q = (q+1)/2
	if(not(type(theta)==bool)):
		n_xq = sin(q_phi(gamma,q))*cos(q_phi(theta,q))
		n_yq = sin(q_phi(gamma,q))*cos(q_phi(theta,q))
		n_zq = cos(q_phi(gamma,q))

		all = [n_xq,n_yq,n_zq]
		return {'all':all,'x':n_xq,'y':n_yq,'z':n_zq}
	else:
		n_zq = cos(q_phi(gamma,q))
		return {'z':n_zq}

def q_vector_x(gamma:float,theta:float,q:float=1,israd:bool=True)-> list:
    return q_vector_bloch(gamma=gamma,theta=theta,q=q,israd=israd)['x']


def q_vector_y(gamma:float,theta:float,q:float=1,israd:bool=True)-> list:
    return q_vector_bloch(gamma=gamma,theta=theta,q=q,israd=israd)['y']


def q_vector_z(gamma:float,theta=False,q:float=1,israd:bool=True)-> list:
    return q_vector_bloch(gamma=gamma,theta=theta,q=q,israd=israd)['z']


def density_matrix(theta:float,gamma:float,q:float=1):
    1/2*np.array([[1+q_vector_z(theta=theta,gamma=gamma,q=q), q_vector_x(theta=theta,gamma=gamma,q=q)+1j*q_vector_y(theta=theta,gamma=gamma,q=q)],
                  [q_vector_x(theta=theta,gamma=gamma,q=q)-1j-q_vector_y(theta=theta,gamma=gamma,q=q),], 1-q_vector_z(theta=theta,gamma=gamma,q=q)])