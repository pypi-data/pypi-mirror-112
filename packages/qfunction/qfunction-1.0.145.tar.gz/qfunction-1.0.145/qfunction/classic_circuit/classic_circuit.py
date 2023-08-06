from qfunction import q_cos,q_exp,q_sin
from qfunction import radian
import numpy as np


class ClassicComputer:
    def __init__(self, n_bits:int) -> None:
        self.n_bits = n_bits
        circuit_painel = []
        for i in range(n_bits):
            circuit_painel.append(f'[c{i}]--')
        self.circuit_painel = circuit_painel
        self.size_space = 0
        
    def measure(self,q_circuit,*n_bits):
        str_cir = '-[med]-'
        str_nan = '-------'
        q_circuit_painel = q_circuit.circuit_painel
        i = 0
        q_new_circuit = []
        for line in q_circuit_painel:
            if i in n_bits:
                size_spaces_q = len(line)
                line = line+str_cir
                q_new_circuit.append(line)
            else:
                line=line+str_nan
                q_new_circuit.append(line)
            i += 1
        if self.n_bits <= i:
                for s in range(i-self.n_bits):
                    self.circuit_painel.append(f'[c{self.n_bits+s}]--')
        new_circuit = []
        q_circuit.circuit_painel = q_new_circuit
        print(q_circuit.q_qubits)
        q_qubits = []
        for b in q_circuit.q_qubits:
            q_qubits.append(b)
        print(q_qubits)
        q_probs = []
        i = 0
        new_qubits = []
        for qbit in q_qubits:
            if i in n_bits:
                qbit_prob = {}
                total_state = qbit[0]+qbit[1]
                #print(f'[q{i}] {qbit}')
                percent_zero_state = qbit[0].real/total_state
                percent_one_state = qbit[1].real/total_state
                qbit_prob['alloc'] = i
                #print(f'[q{i}] {qbit}')
                qbit_prob['name_qbit'] = f'q{i}'
                qbit_prob['|0>'] = percent_zero_state
                qbit_prob['|1>'] = percent_one_state
                qbit_prob['state'] = '|0>' if qbit_prob['|0>']>=qbit_prob['|1>'] else '|1>'
                q_probs.append(qbit_prob)
                qbit[0] = 1 if qbit_prob['state']=='|1>' else 0
                qbit[1] = 0 if not qbit_prob['state']=='|1>' else 0
                #print(f'[q{i}] {qbit}')
            else:
                pass
            new_qubits.append(qbit)
            i+=1
        print(q_circuit.q_qubits)
        q_circuit.q_qubits = new_qubits
        print(q_circuit.q_qubits)
        n = 0
        c = 0
        print(q_probs)
        for line in self.circuit_painel:
            size_spaces = size_spaces_q - len(line)
            self.size_spaces = size_spaces_q
            if n in n_bits:
                line = line + '-'*(size_spaces-4)+q_probs[c]['state']+'---'
                new_circuit.append(line)
                c+=1
            else:
                line = line +'-'*(size_spaces)+'-'
                new_circuit.append(line)
            space = ' '*(size_spaces+3)+'|\n'
            self.space = space
            n+=1
        self.circuit_painel = new_circuit
        q_circuit.divisor_circuits = self.space
        q_circuit.classic_circuit_painel = self.circuit_painel
        
    def __str__(self):
        return '\n'.join(self.circuit_painel)
                