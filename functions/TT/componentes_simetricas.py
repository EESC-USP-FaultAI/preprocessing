import numpy as np

def comp_sim_ABCto012(Xa, Xb, Xc):
    '''
    :param Xa: Phasor of phase A
    :param Xb: Phasor of phase B
    :param Xc: Phasor of phase C
    :return: 1−D array with symmetrical components phasors
    '''
    vetABC = [ Xa, Xb, Xc ]
    i = complex(0, 1)
    alfa = np.e**( i * (2*np.pi)/3 )
    A = [ [1, 1, 1], [1, alfa, alfa**2], [1, alfa**2, alfa] ]
    vet012 = []
    
    for row in A:
        aux=0
        for i in range(len(row)):
            aux += (1/3) * row[i] * vetABC[i]
        vet012.append( aux )
    
    return vet012
   
def comp_sim_012toABC(X0, X1, X2):
    '''
    :param X0: Zero sequence
    :param X1: Positive sequence
    :param X2: Negative sequence
    :return: 1−D array with ABC phasors
    '''
    vet012 = [ X0, X1, X2 ]
    i = complex(0, 1)
    alfa = np.e**( i * (2*np.pi)/3 )
    A = [ [1, 1, 1], [1, alfa**2, alfa], [1, alfa, alfa**2] ]
    vetABC = []
    
    for row in A:
        aux=0
        for i in range(len(row)):
            aux += row[i] * vet012[i]
        vetABC.append( abs(aux) )
    
    return vetABC