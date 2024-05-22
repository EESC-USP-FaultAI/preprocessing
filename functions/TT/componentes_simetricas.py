import numpy as np

def comp_sim_ABCto012(Xa, Xb, Xc):
    '''
    Function to convert the phasors from ABC to symmetrical components

    Parameters
    ----------
    Xa : complex
        Phasor of phase A
    Xb : complex
        Phasor of phase B
    Xc : complex
        Phasor of phase C

    Returns
    -------
    vet012 : list
        1-D array with symmetrical components phasors

    Examples
    --------
    >>> import functions.TT as tt
    >>> import numpy as np
    >>> abc = [1, 1*np.exp(1j*2*np.pi/3), 1*np.exp(-1j*2*np.pi/3)]
    >>> v012 = tt.comp_sim_ABCto012(abc[0], abc[1], abc[2])
    >>> print(v012)
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
    Function to convert the phasors from symmetrical components to ABC

    Parameters
    ----------
    X0 : complex
        Zero sequence
    X1 : complex
        Positive sequence
    X2 : complex
        Negative sequence

    Returns
    -------
    vetABC : list
        1-D array with ABC phasors

    Examples
    --------
    >>> import functions.TT as tt
    >>> import numpy as np
    >>> v012 = [0, 1, 0]
    >>> abc = tt.comp_sim_012toABC(v012[0], v012[1], v012[2])
    >>> print(abc)
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