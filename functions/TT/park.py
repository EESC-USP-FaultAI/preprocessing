import numpy as np

def park_ABCtoDQ(Xa, Xb, Xc, teta, AmpIn=True):
    '''
    :param Xa: Fasor da fase A
    :param Xb: Fasor da fase B
    :param Xc: Fasor da fase C
    :param teta: Ângulo entre o rotor da máquina e a fase A
    :param AmpIn: Booleno - Se True as constantes são para amplitude invariável, potência invariável caso contrário
    :return: vetor com os fasores no domínio de Park
    '''
    vetABC = [Xa, Xb, Xc]

    if AmpIn:
        const = 2/3
    else:
        const = (2/3)**(0.5)

    A = [[const, const, const],
         [const * np.cos(teta), const * np.cos(teta - 2 * np.pi / 3), const * np.cos(teta - 4 * np.pi / 3)],
         [const * np.sin(teta), const * np.sin(teta - 2 * np.pi / 3), const * np.sin(teta - 4 * np.pi / 3)]]

    vetDQ = []
    for linha in A:
        aux=0
        for i in range(len(linha)):
            aux+=linha[i]*vetABC[i]
        vetDQ.append(aux)

    return vetDQ

def park_DQtoABC(X0, Xd, Xq, teta, AmpIn=True):
    '''
    :param Xd: Fasor da componente de eixo direto no domínio de Park
    :param Xq: Fasor da componente de eixo em quadratura no domínio de Park
    :param teta: Ângulo entre o rotor da máquina e a fase A
    :param AmpIn: Booleno - Se True as constantes são para amplitude invariável, potência invariável caso contrário
    :return: Vetor com os fasores no domínio ABC
    '''
    vetDQ = [X0, Xd, Xq]
    if AmpIn:
        const = 1#1/(2/3)
    else:
        const = 1#1 / ((2 / 3)**(0.5))

    A = [[const, const * np.cos(teta), const * np.sin(teta)],
         [const, const * np.cos(teta - 2 * np.pi / 3), const * np.sin(teta - 2 * np.pi / 3)],
         [const, const * np.cos(teta - 4 * np.pi / 3), const * np.sin(teta - 4 * np.pi / 3)]]

    vetABC = []
    for linha in A:
        aux = 0
        for i in range(len(linha)):
            aux += linha[i] * vetDQ[i]
        vetABC.append(aux)

    return vetABC