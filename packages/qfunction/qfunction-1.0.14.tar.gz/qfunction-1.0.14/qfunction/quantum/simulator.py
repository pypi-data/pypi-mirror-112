from qfunction.quantum import QuantumCircuit as Qc


def simulator(qc:Qc):
    list_bits = []
    qprobs = qc.med_all()
    #print(qprobs)
    for qbit in qprobs:
        #print((qbit['state']))
        state_bit = int(list(qbit['state'])[1])
        list_bits.append(state_bit)
    return list_bits