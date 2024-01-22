import numpy as np

def comp_sim_ABCto012(Xa, Xb, Xc):
    '''
    :param Xa: Fasor da fase A
    :param Xb: Fasor da fase B
    :param Xc: Fasor da fase C
    :return: vetor com os fasores no domínio das componenetes simétricas
    '''
    vetABC = [ Xa, Xb, Xc ]
    i = complex(0, 1)
    alfa = np.e**( i * (2*np.pi)/3 )
    A = [ [1, 1, 1], [1, alfa, alfa**2], [1, alfa**2, alfa] ]
    vet012 = []
    
    for linha in A:
        aux=0
        for i in range(len(linha)):
            aux += (1/3) * linha[i] * vetABC[i]
        vet012.append( aux )
    
    return vet012
   
def comp_sim_012toABC(X0, X1, X2):
    '''
    :param X0: Fasor da componente de sequência 0
    :param X1: Fasor da componente de sequência positiva
    :param X2: Fasor da componente de sequência negativa
    :return: vetor com os fasores no domínio ABC
    '''
    vet012 = [ X0, X1, X2 ]
    i = complex(0, 1)
    alfa = np.e**( i * (2*np.pi)/3 )
    A = [ [1, 1, 1], [1, alfa**2, alfa], [1, alfa, alfa**2] ]
    vetABC = []
    
    for linha in A:
        aux=0
        for i in range(len(linha)):
            aux += linha[i] * vet012[i]
        vetABC.append( abs(aux) )
    
    return vetABC