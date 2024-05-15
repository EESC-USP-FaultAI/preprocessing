import numpy as np

def clarke_ABCtoAB0(Xa, Xb, Xc, AmpIn=True):
    '''
    :param Xa: Phasor of phase A
    :param Xb: Phasor of phase B
    :param Xc: Phasor of phase C
    :param AmpIn: Booleno - f True the constants are for invariable amplitude, invariable power otherwise
    :return: 1−D array with Clarke’s phasors
    '''
    vetABC = [ Xa, Xb, Xc ]
    
    if AmpIn:
        A = [[1/3, 1/3, 1/3], [2/3, -1/3, -1/3], [0, (3**0.5)/3, -(3**0.5)/3]]
    else:
        A = [[1/(3**0.5), 1/(3**0.5), 1/(3**0.5)], [(2/3)**0.5, -(1/2)*((2/3)**0.5), -(1/2)*((2/3)**0.5)], [0, (2**0.5)/2, -(2**0.5)/2]]
    vet0AB=[]
    for row in A:
        aux=0
        for i in range(len(row)):
            aux+=row[i]*vetABC[i]
        vet0AB.append(aux)
    
    return vet0AB


def clarke_AB0toABC(X0, Xa, Xb, AmpIn=True):
    '''
    :param X0: Clarke component 0
    :param Xa: Clarke component alfa
    :param Xb: Clarke component beta
    :param AmpIn: Booleno - f True the constants are for invariable amplitude, invariable power otherwise
    :return: 1−D array with ABC’s phasors
    '''
    vet0AB = [ X0, Xa, Xb ]
    if AmpIn:
        A = [[1, 1, 0], [1, -0.5, 0.8660254], [1, -0.5, -0.8660254]]
    else:
        A = [[0.57735027, 0.81649658, 0], [0.5773527, -0.40824829, 0.70710678], [0.5773527, -0.40824829, -0.70710678]]
    
    vetABC=[]
    for row in A:
        aux=0
        for i in range(len(row)):
            aux+=row[i]*vet0AB[i]
        vetABC.append(aux)
    
    return vetABC