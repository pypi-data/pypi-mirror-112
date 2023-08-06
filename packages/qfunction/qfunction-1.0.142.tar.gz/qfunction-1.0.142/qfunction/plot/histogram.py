from matplotlib import pyplot as plt
import numpy as np
from qfunction.quantum import QuantumCircuit as Qc

def plot_probabilities(qc:Qc):
    list_probs = qc.qprobs
    i = 0
    l,r =0,0
    for s in range(len(list_probs)):
        if s%2 == 0:
            l+=1
        else:
            r+=1
    fig,ax = plt.subplots(nrows=l,ncols=r,figsize=(5,4.5))
    l,r=-1,-1
    for qbit in list_probs:
        if (i+2)%2 == 0:
            l+=1
            #r+=1
            title = f"[qbit_{qbit['alloc']}]"
            x = [1,2]
            prob0 = round(float(qbit['|0>']),3)
            prob1 = round(float(qbit['|1>']),3)
            #print(f'x: [{prob0},{prob1}]')
            rects = ax[l,r].bar(x,[prob0,prob1])
            for rect in rects:
                height = rect.get_height()
                ax[l,r].text(rect.get_x() + rect.get_width()/2., 1.05*height,
                        f'{height:.3f}',
                        ha='center', va='bottom')

            ax[l,r].set_xticklabels(['','|0>','','|1>',''])
            ax[l,r].set_xlabel('state')
            ax[l,r].set_ylabel('prob')
            ax[l,r].set_ylim(0.,1.4)
            #ax[l,r].set_xlim(-0.4,1.4)
            ax[l,r].set_title(title)
            #ax[l,r].grid()
            #r-=1
        else:
            r+=1
            title = f"[qbit_{qbit['alloc']}]"
            x = [0,1]
            prob0 = round(float(qbit['|0>'].real),3)
            prob1 = round(float(qbit['|1>'].real),3)
            
            rects = ax[l,r].bar(x,[prob0,prob1])
            for rect in rects:
                height = rect.get_height()
                ax[l,r].text(rect.get_x() + rect.get_width()/2., 1.05*height,
                        f'{height:.3f}',
                        ha='center', va='bottom')
            ax[l,r].set_xticklabels(['','|0>','','|1>',''])
            ax[l,r].set_xlabel('state')
            ax[l,r].set_ylabel('prob')
            ax[l,r].set_ylim(0,1.4)
            ax[l,r].set_title(title)
            #ax[l,r].grid()
            #+=1
        i+=1
    plt.tight_layout()
    plt.show()
    return plt
