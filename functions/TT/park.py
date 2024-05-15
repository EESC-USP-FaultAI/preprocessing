import numpy as np

def park_ABCtoDQ(Xa, Xb, Xc, teta, AmpIn=True):
    '''
    :param Xa: Phasor of phase A
    :param Xb: Phasor of phase B
    :param Xc: Phasor of phase C
    :param teta: Angle between the machine rotor and phase A [radians]
    :param AmpIn: Booleno - f True the constants are for invariable amplitude, invariable power otherwise
    :return: 1−D array with Park’s phasors
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
    for row in A:
        aux=0
        for i in range(len(row)):
            aux+=row[i]*vetABC[i]
        vetDQ.append(aux)

    return vetDQ

def park_DQtoABC(X0, Xd, Xq, teta, AmpIn=True):
    '''
    :param Xd: Phasor of the direct axis component in the Park domain
    :param Xq: Phasor of the quadrature axis component in the Park domain
    :param teta: ngle between the machine rotor and phase A [radians]
    :param AmpIn: Booleno -  True the constants are for invariable amplitude, invariable power otherwise
    :return: 1−D array with ABC’s phasors
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
    for row in A:
        aux = 0
        for i in range(len(row)):
            aux += row[i] * vetDQ[i]
        vetABC.append(aux)

    return vetABC