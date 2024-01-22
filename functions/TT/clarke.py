import numpy as np

def clarke_ABCtoAB0(Xa, Xb, Xc, AmpIn=True):
    '''
    :param Xa: Fasor da fase A
    :param Xb: Fasor da fase B
    :param Xc: Fasor da fase C
    :param AmpIn: Booleno - Se True as constantes são para amplitude invariável, potência invariável caso contrário
    :return: vetor com os fasores no domínio de Clarke
    '''
    vetABC = [ Xa, Xb, Xc ]
    
    if AmpIn:
        A = [[1/3, 1/3, 1/3], [2/3, -1/3, -1/3], [0, (3**0.5)/3, -(3**0.5)/3]]
    else:
        A = [[1/(3**0.5), 1/(3**0.5), 1/(3**0.5)], [(2/3)**0.5, -(1/2)*((2/3)**0.5), -(1/2)*((2/3)**0.5)], [0, (2**0.5)/2, -(2**0.5)/2]]
    vet0AB=[]
    for linha in A:
        aux=0
        for i in range(len(linha)):
            aux+=linha[i]*vetABC[i]
        vet0AB.append(aux)
    
    return vet0AB


def clarke_AB0toABC(X0, Xa, Xb, AmpIn=True):
    '''
    :param X0: Componente 0 de Clarke
    :param Xa: Componente alfa de Clarke
    :param Xb: Componente beta de Clarke
    :param AmpIn: Booleno - Se True as constantes são para amplitude invariável, potência invariável caso contrário
    :return: vetor com os fasores no domínio ABC
    '''
    vet0AB = [ X0, Xa, Xb ]
    if AmpIn:
        A = [[1, 1, 0], [1, -0.5, 0.8660254], [1, -0.5, -0.8660254]]
    else:
        A = [[0.57735027, 0.81649658, 0], [0.5773527, -0.40824829, 0.70710678], [0.5773527, -0.40824829, -0.70710678]]
    
    vetABC=[]
    for linha in A:
        aux=0
        for i in range(len(linha)):
            aux+=linha[i]*vet0AB[i]
        vetABC.append(aux)
    
    return vetABC