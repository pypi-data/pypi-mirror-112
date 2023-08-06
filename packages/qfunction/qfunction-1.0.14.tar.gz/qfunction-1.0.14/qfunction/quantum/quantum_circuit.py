########################
## Author: Reinan Br. ##
## Date_init:01/07/21 ##
########################
from qfunction import q_sin,q_exp,q_cos,radian,limit
import numpy as np
from numpy import sqrt,array
from math import atan
############ quantum equations #############
def q_rho(u,q=1,cpx=False,israd=True):
	u = radian(u) if(not israd) else u
	u = u*1j
	if cpx:
		return sqrt(q_exp(u,q)*q_exp(-u,q))
	else:
		return (sqrt(q_exp(u,q)*q_exp(-u,q))).real



def q_psi(theta,gamma,q=1,israd=True):
    import numpy as np
    gamma = radian(gamma) if(not israd) else gamma
    theta = radian(theta) if(not israd) else theta
    theta = 1j*theta/2
    gamma = gamma/2
    gamma = gamma if abs(gamma) <= 2*np.pi else np.nan
    theta = theta if abs(theta) <= np.pi else np.nan
    coluna0 = [q_exp(-theta,q).real*q_cos(gamma,q).real]
    coluna1 = [q_exp(theta,q).real*q_sin(gamma,q).real]
    return array([coluna0,coluna1])


def q_phi(u,q=1,israd=True):
	u = radian(u) if(not israd) else u
	param_q = lambda q_: 1/(1-q_)
	param_q = limit(param_q,q)
	return param_q*atan((1-q)*u)


def q_qubit(state):
    pass


from IPython.display import Math,display
class QuantumCircuit:
    def __init__(self,n_bits,q: float=1,israd=True)-> None:
        import numpy as np
        self.q = q
        self.theta = .5*np.pi
        self.israd = israd
        self.n_bits = n_bits
        circuit_painel = []
        for i in range(n_bits):
            circuit_painel.append(f'[q{i}]--')
        self.circuit_painel = circuit_painel
        q_qubits = []
        for i in range(n_bits):
            q_qubits.append(q_psi(gamma=0*np.pi,theta=0,q=self.q))
        self.q_qubits = np.array(q_qubits)
        #print(self.q_qubits)
        self.divisor_circuits = False
        #creating a list for probabilistic
        self.probs_history = []
        
    
    def get_prob_from_qbits(self,qbits):
        #print(qbits)
        q_probs = []
        i = 0
        for qbit in qbits:
            qbit_prob = {}
            total_state = abs(qbit[0]) + abs(qbit[1])
            percent_zero_state = abs(qbit[0])/total_state
            percent_one_state = abs(qbit[1])/total_state
            
            #print(f'prob[{i}]: [{percent_zero_state},{percent_one_state}]')
            qbit_prob['alloc'] = i
            #print(f'[q{i}] {qbit}')
            qbit_prob['name_qbit'] = f'q{i}'
            qbit_prob['|0>'] = percent_zero_state
            qbit_prob['|1>'] = percent_one_state
            qbit_prob['state'] = '|0>' if qbit_prob['|0>']>=qbit_prob['|1>'] else '|1>'
            q_probs.append(qbit_prob)
            #print(q_probs[i])
            i+=1
        #print(f'qprobs: {q_probs}')
        return q_probs

            
        
        
    def R_x(self):
        theta = self.theta
        q = self.q
        israd = self.israd
        theta = theta if israd else radian(theta)
        theta = theta/2
        return np.array([[q_cos(u=theta,q=q,israd=israd),
                            q_sin(u=theta,q=q)*-1j],
                            [q_sin(theta,q=q,israd=israd)*-1j,
                            q_cos(u=theta,q=q,israd=israd)]
                            ])


    def R_y(self):
        theta = self.theta
        q = self.q
        israd = self.israd
        theta = theta if israd else radian(theta)
        theta = theta/2
        return np.array([[q_cos(u=theta,q=q,israd=israd),
                            q_sin(u=theta,q=q,israd=israd)*-1],
                            [q_sin(theta,q=q,israd=israd),
                            q_cos(u=theta,q=q,israd=israd)]
                            ]).real


    def R_z(self):
        theta = self.theta
        q = self.q
        israd = self.israd
        theta = theta if israd else radian(theta)
        theta = 1j*theta/2
        return np.array([[q_exp(u=-theta,q=q),0],
                            [0,q_exp(u=theta,q=q)]]).real


    def H(self,*n_bits):
        str_cir = '--[H]--'
        str_nan = '-------'
        circuit_painel = self.circuit_painel
        i = 0
        new_circuit = []
        for line in circuit_painel:
            if i in n_bits:
                line = line+str_cir
                new_circuit.append(line)
            else:
                line=line+str_nan
                new_circuit.append(line)
            i += 1
        self.circuit_painel = new_circuit
        self.qprobs = self.get_prob_from_qbits(self.q_qubits)

            
        theta = self.theta
        q = self.q
        israd = self.israd
        R_x = self.R_x
        R_y = self.R_y
        
        H_matriz = (R_x()+R_y()).real/np.sqrt(2)
        
        new_q_qubits = []
        q_qubits = self.q_qubits
        i = 0
        for qbit in q_qubits:
            if i in n_bits:
                qbit = np.dot(H_matriz,qbit)
                new_q_qubits.append(qbit)
            else:
                qbit = qbit
                new_q_qubits.append(qbit)
            i+=1
        self.q_qubits = new_q_qubits
        self.qprobs = self.get_prob_from_qbits(self.q_qubits)

    
    
    def X(self,*n_bits):
        str_cir = '--[X]--'
        str_nan = '-------'
        circuit_painel = self.circuit_painel
        i = 0
        new_circuit = []
        for line in circuit_painel:
            if i in n_bits:
                line = line+str_cir
                new_circuit.append(line)
            else:
                line=line+str_nan
                new_circuit.append(line)
            i += 1
        self.circuit_painel = new_circuit
            
        theta = self.theta
        q = self.q
        israd = self.israd
        R_x = self.R_x
        new_q_qubits = []
        q_qubits = self.q_qubits
        i = 0
        for qbit in q_qubits:
            if i in n_bits:
                qbit = np.dot(R_x(),qbit)
                new_q_qubits.append(qbit)
            else:
                qbit = qbit
                new_q_qubits.append(qbit)
            i+=1
        self.q_qubits = new_q_qubits
        self.qprobs = self.get_prob_from_qbits(self.q_qubits)


    def Y(self,*n_bits):
        str_cir = '--[Y]--'
        str_nan = '-------'
        circuit_painel = self.circuit_painel
        i = 0
        new_circuit = []
        for line in circuit_painel:
            if i in n_bits:
                line = line+str_cir
                new_circuit.append(line)
            else:
                line=line+str_nan
                new_circuit.append(line)
            i += 1
        self.circuit_painel = new_circuit
            
        theta = self.theta
        q = self.q
        israd = self.israd
        R_y = self.R_y
        new_q_qubits = []
        q_qubits = self.q_qubits
        i = 0
        for qbit in q_qubits:
            if i in n_bits:
                qbit = np.dot(R_y(),qbit)
                new_q_qubits.append(qbit)
            else:
                qbit = qbit
                new_q_qubits.append(qbit)
            i+=1
        self.q_qubits = new_q_qubits
        self.qprobs = self.get_prob_from_qbits(self.q_qubits)

    
    def Z(self,*n_bits):
        str_cir = '--[Z]--'
        str_nan = '-------'
        circuit_painel = self.circuit_painel
        i = 0
        new_circuit = []
        for line in circuit_painel:
            if i in n_bits:
                line = line+str_cir
                new_circuit.append(line)
            else:
                line=line+str_nan
                new_circuit.append(line)
            i += 1
        self.circuit_painel = new_circuit
            
        theta = self.theta
        q = self.q
        israd = self.israd
        R_z = self.R_z
        new_q_qubits = []
        q_qubits = self.q_qubits
        i = 0
        for qbit in q_qubits:
            if i in n_bits:
                qbit = np.dot(R_z(),qbit)
                new_q_qubits.append(qbit)
            else:
                qbit = qbit
                new_q_qubits.append(qbit)
            i+=1
        self.q_qubits = new_q_qubits
        self.qprobs = self.get_prob_from_qbits(self.q_qubits)

      
            
    def states(self) -> str:
        string = []
        i = 0
        for qbit in self.q_qubits:
            string.append(f'[q{i}]|ψ〉 = {round(qbit[0][0],3)}|0〉 + {round(qbit[1][0],3)}|1〉')
            i += 1
        string = '\n'.join(string)
        string = '\n'+string
        #print(display(Math(r'$\frac{df}{dx}$')))
        return string
    
    def med(self,*n_bits):
               #getting the probability of the two states of qbit
        q_probs = []
        i = 0
        new_qubits = []
        for qbit in self.q_qubits:
            if i in n_bits:
                qbit_prob = {}
                total_state = qbit[0]+qbit[1]
                percent_zero_state = qbit[0]/total_state
                percent_one_state = qbit[1]/total_state
                qbit_prob['alloc'] = i
                qbit_prob['name_qbit'] = f'q{i}'
                qbit_prob['|0>'] = percent_zero_state
                qbit_prob['|1>'] = percent_one_state
                qbit_prob['state'] = '|0>' if qbit_prob['|0>']>=qbit_prob['|1>'] else '|1>'
                q_probs.append(qbit_prob)
                if qbit_prob['state'] == '|1>':
                    qbit = [0,1]
                else:
                    qbit = [1,0]
                #print(f'[q{i}] {qbit}')
            else:
                pass
            new_qubits.append(qbit)
            i+=1
        #print(i)
        str_cir = '-[med]-'
        str_nan = '-----------'
        circuit_painel = self.circuit_painel
        i = 0
        c=0
        new_circuit = []
        for line in circuit_painel:
            if i in n_bits:
                #print(q_probs)
                n_simb = q_probs[c]['state']
                line = line+str_cir+f'{n_simb}-'
                new_circuit.append(line)
                c+=1
            else:
                line=line+str_nan
                new_circuit.append(line)
            i += 1
        self.circuit_painel = new_circuit
        self.q_probs = q_probs
        self.q_qubits = new_qubits
        self.qprobs = self.get_prob_from_qbits(self.q_qubits)

        return q_probs

    def med_all(self):
        n_bits = [nq for nq in range(len(self.q_qubits))]

        #getting the probability of the two states of qbit
        q_probs = []
        i = 0
        new_qubits = []
        qbits = [0,0]
        for qbit in self.q_qubits:
            #print('after',qbit)
            if i in n_bits:
                qbit_prob = {}
                total_state = qbit[0]+qbit[1]
                percent_zero_state = qbit[0]/total_state
                percent_one_state = qbit[1]/total_state
                #print('percent_one',percent_one_state)
                #print('percent_zero',percent_zero_state)
                qbit_prob['alloc'] = i
                qbit_prob['name_qbit'] = f'q{i}'
                qbit_prob['|0>'] = percent_zero_state
                qbit_prob['|1>'] = percent_one_state
                qbit_prob['state'] = '|0>' if qbit_prob['|0>']>=qbit_prob['|1>'] else '|1>'
                q_probs.append(qbit_prob)
                #print(qbit_prob['state'])
                #print(1 if qbit_prob['state']=='|1>' else 0)
                if qbit_prob['state'] == '|1>':
                    qbit = [0,1]
                else:
                    qbit = [1,0]
                #print(f'[q{i}] {qbit}')
            else:
                pass
            new_qubits.append(qbit)
            #print(new_qubits)
            i+=1
        #print(i)
        str_cir = '-[med]-'
        str_nan = '-----------'
        circuit_painel = self.circuit_painel
        i = 0
        c=0
        new_circuit = []
        for line in circuit_painel:
            if i in n_bits:
                #print(q_probs)
                n_simb = q_probs[c]['state']
                line = line+str_cir+f'{n_simb}-'
                new_circuit.append(line)
                c+=1
            else:
                line=line+str_nan
                new_circuit.append(line)
            i += 1
        self.circuit_painel = new_circuit
        self.q_probs = q_probs
        self.q_qubits = new_qubits
        #print(self.q_qubits)
        self.qprobs = self.get_prob_from_qbits(self.q_qubits)

        return q_probs
    
    def __str__(self):
        print_circuit = self.circuit_painel
        if self.divisor_circuits:
            print_circuit.append(self.divisor_circuits)
            print_circuit.append('\n'.join(self.classic_circuit_painel))
        #print(print_circuit)
        #self.circuit_painel = []
        return '\n'.join(print_circuit)
    
    
    
class q_qubitq:
    def __init__(self,*bit_values: int) -> None:
        self.values = list(bit_values)
# \na^2 + b^2 = {qbit[0][0]**2+qbit[1][0]**2}')

