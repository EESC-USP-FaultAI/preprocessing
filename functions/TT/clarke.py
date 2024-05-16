import numpy as np

def clarke_ABCtoAB0(Xa, Xb, Xc, AmpIn=True):
    '''
    Function to convert the phasors from ABC to αβ0

    Parameters
    ----------
    Xa : float
        Phasor of phase A
    Xb : float
        Phasor of phase B
    Xc : float
        Phasor of phase C
    AmpIn : bool, optional
        If True the constants are for invariable amplitude, invariable power otherwise. The default is True.

    Returns
    -------
    vet0AB : list
        1-D array with Clarke's phasors

    Examples
    --------
    >>> import functions.TT as tt
    >>> import numpy as np
    >>> abc = [1, 1*np.exp(1j*2*np.pi/3), 1*np.exp(-1j*2*np.pi/3)]
    >>> ab0 = tt.clarke_ABCtoAB0(abc[0], abc[1], abc[2])
    >>> print(ab0)
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
    Function to convert the phasors from αβ0 to ABC

    Parameters
    ----------
    X0 : float
        Clarke component 0
    Xa : float
        Clarke component alfa
    Xb : float
        Clarke component beta

    Returns
    -------
    vetABC : list
        1-D array with ABC’s phasors

    Examples
    --------
    >>> import functions.TT as tt
    >>> import numpy as np
    >>> ab0 = [1, 1*np.exp(1j*2*np.pi/3), 1*np.exp(-1j*2*np.pi/3)]
    >>> abc = tt.clarke_AB0toABC(ab0[0], ab0[1], ab0[2])
    >>> print(abc)
    
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