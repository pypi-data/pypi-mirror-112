from qfunction.quantum import QuantumCircuit as Qc
import matplotlib.pyplot as plt


class ArenaGame:
    def __init__(self,qc:Qc):
        self.qc = qc
        print(qc.q_qubits[0][0])
        self.way = [[0,0]]
    
    def up(self):
        up_matriz = [0,1*float(self.qc.q_qubits[0][0])]
        self.way.append(up_matriz)
    
    def down(self):
        up_down =  [0,-1*float(self.qc.q_qubits[0][0])]
        self.way.append(up_down)
        
    def left(self):
        left_matriz = [1*float(self.qc.q_qubits[0][0]),0]
        self.way.append(left_matriz)
    
    def right(self):
        right_matriz = [-1*float(self.qc.q_qubits[0][0]),0]
        self.way.append(right_matriz)
        
    def show(self):
        for point in self.way:
            plt.plot(point,color='blue')
        plt.plot(8,9,'o',color='orange')
        plt.xlim(-10,10)
        plt.ylim(-10,10)
        plt.xticks([])
        plt.yticks([])
        plt.grid()
        plt.show()