import numpy as np

def park_ABCtoDQ(Xa, Xb, Xc, teta, AmpIn=True):
    '''
    Function to convert the phasors from ABC to Park

    Parameters
    ----------
    Xa : complex
        Phasor of phase A
    Xb : complex
        Phasor of phase B
    Xc : complex
        Phasor of phase C
    teta : float
        Angle between the machine rotor and phase A [radians]

    Returns
    -------
    vetDQ : list
        1-D array with Park’s phasors

    Examples
    --------
    >>> import functions.TT as tt
    >>> import numpy as np
    >>> abc = [1, 1*np.exp(1j*2*np.pi/3), 1*np.exp(-1j*2*np.pi/3)]
    >>> dq = tt.park_ABCtoDQ(abc[0], abc[1], abc[2], np.pi/3)
    >>> print(dq)
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
    Function to convert the phasors from Park to ABC

    Parameters
    ----------  
    X0 : complex
        Phasor of the zero sequence component in the Park domain
    Xd : complex
        Phasor of the direct axis component in the Park domain
    Xq : complex
        Phasor of the quadrature axis component in the Park domain
    teta : float
        Angle between the machine rotor and phase A [radians]
    AmpIn : bool
        If True the constants are for invariable amplitude, invariable power otherwise

    Returns
    -------
    vetABC : list
        1-D array with ABC’s phasors

    Examples
    --------
    >>> import functions.TT as tt
    >>> import numpy as np
    >>> dq = [1, 1*np.exp(1j*np.pi/3), 1*np.exp(-1j*np.pi/3)]
    >>> abc = tt.park_DQtoABC(dq[0], dq[1], dq[2], np.pi/3)
    >>> print(abc)
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