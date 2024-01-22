import componentes_simetricas as cs
import clarke
import park
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

def f(t, amp, ang):
    return amp * np.cos(60*2*np.pi*t + ang)


def DFT(sinal, N):
    length = len(sinal)
    harmonico=0
    for n in range(0, length):
            harmonico += sinal[n]*np.e**(complex(0, -1)*n*(2*np.pi)/N)
    
    return 2*harmonico/length

amostras = 128
TotalTime = 3*1/60
timeStep=1/(60*amostras)
t = np.arange(0, TotalTime, timeStep)

Va = f(t, 20, 0)
Vb = f(t, 20, 2*(2*np.pi)/3)
Vc = f(t, 20, (2*np.pi)/3)

Vpos = []
Vneg = []
Vzero = []

Valfa = []
Vbeta = []
Vzer0 = []

vD=[]
vQ=[]
v0=[]
for i in range(0, len(Va)-amostras):
    #Componentes simétricas
    vetAB0 = cs.comp_sim_ABCto012(DFT(Va[i:i + amostras], amostras),
                                  DFT(Vb[i:i + amostras], amostras),
                                  DFT(Vc[i:i + amostras], amostras))
    Vpos.append(vetAB0[1])
    Vneg.append(vetAB0[2])
    Vzero.append(vetAB0[0])

    #Clarke
    vetAB0 = clarke.clarke_ABCtoAB0(DFT(Va[i:i + amostras], amostras),
                                  DFT(Vb[i:i + amostras], amostras),
                                  DFT(Vc[i:i + amostras], amostras),True)
    Valfa.append(vetAB0[1])
    Vbeta.append(vetAB0[2])
    Vzer0.append(vetAB0[0])

    # Parke
    comp = 0#i*2*np.pi/amostras
    vetAB0 = park.park_ABCtoDQ(DFT(Va[i:i+amostras], amostras),
                               DFT(Vb[i:i+amostras], amostras),
                               DFT(Vc[i:i+amostras], amostras),
                               comp, True)
    v0.append(vetAB0[0])
    vD.append(vetAB0[1])
    vQ.append(vetAB0[2])

t=[k/(60*amostras) for k in range(0, len(Va)-amostras)]

fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(8,8))
axs = axs.flatten()

# Sinal de Referência
axs[0].plot(t, [Va[i] for i in range(len(t))], label=r'$V_{A}$')
axs[0].plot(t, [Vb[i] for i in range(len(t))], label=r'$V_{B}$')
axs[0].plot(t, [Vc[i] for i in range(len(t))], label=r'$V_{C}$')
axs[0].set_title('Sinal de Referência', fontsize=16)
axs[0].set_xlabel('Tempo [s]', fontsize=16)
axs[0].set_ylabel('Amplitude', fontsize=16)
axs[0].grid()
axs[0].legend(fontsize=12)

# Componentes simétricas
axs[1].plot(t, Vpos, label=r'$V_{+}$')
axs[1].plot(t, Vneg, label=r'$V_{-}$')
axs[1].plot(t, Vzero, label=r'$V_0$')
axs[1].set_title('Componentes Simétricas', fontsize=16)
axs[1].set_xlabel('Tempo [s]', fontsize=16)
axs[1].set_ylabel('Amplitude', fontsize=16)
axs[1].grid()
axs[1].legend(fontsize=12)

# Clarke
axs[2].plot(t, Valfa, label=r'$V_{\alpha}$')
axs[2].plot(t, Vbeta, label=r'$V_{\beta}$')
axs[2].plot(t, Vzer0, label=r'$V_0$')
axs[2].set_title('Transformada de Clarke', fontsize=16)
axs[2].set_xlabel('Tempo [s]', fontsize=16)
axs[2].set_ylabel('Amplitude', fontsize=16)
axs[2].grid()
axs[2].legend(fontsize=12)

# Parke
axs[3].plot(t, vD, label=r'$V_d$')
axs[3].plot(t, vQ, label=r'$V_q$')
axs[3].plot(t, v0, label=r'$V_0$')
axs[3].set_title('Transformada de Park', fontsize=16)
axs[3].set_xlabel('Tempo [s]', fontsize=16)
axs[3].set_ylabel('Amplitude', fontsize=16)
axs[3].grid()
axs[3].legend(fontsize=12)

fig.tight_layout()
plt.show()
