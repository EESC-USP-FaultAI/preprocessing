import ST
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

# Gerando sinal sintético

amostras = 128
f=60
TotalTime = 2
timeInicio=1

t = 0
sinal=[]
for k in range(0, TotalTime*amostras*f):
    if k<(timeInicio*f*amostras):
        sinal.append(10*np.sin(2*np.pi*f*t))
    else:
        sinal.append(10*np.sin(2*np.pi*f*t) + 5*np.sin(3*2*np.pi*f*t) + 3*np.sin(10*2*np.pi*f*t))
    t+=1/(f*amostras)
sinal=np.array(sinal)


# Calcula a Transformada de Stockwell

ts = ST.Stockwell().calcula_TS_do_sinal(sinal, amostras)



# Plotando resultados - Amplitude

fig, axs = plt.subplots(nrows=2, ncols=2)
axs = axs.flatten()
t=[k/(f*amostras) for k in range(0, len(sinal))]

# Sinal no tempo
axs[0].plot(t, sinal)
axs[0].set_title('Sinal')
axs[0].set_xlabel('Tempo [s]')
axs[0].set_ylabel('Amplitude')
axs[0].grid()

# Fundamental
axs[1].plot(t, ts[0][1])
axs[1].set_title('Amplitude da fundamental')
axs[1].set_ylim(9,11)
axs[1].set_xlabel('Tempo [s]')
axs[1].set_ylabel('Amplitude')
axs[1].grid()

# Terceira harmônica
axs[2].plot(t, ts[0][3])
axs[2].set_title('Amplitude da terceira harmônica')
axs[2].set_xlabel('Tempo [s]')
axs[2].set_ylabel('Amplitude')
axs[2].grid()

# Décima harmônica
axs[3].plot(t, ts[0][10])
axs[3].set_title('Amplitude da décima harmônica')
axs[3].set_xlabel('Tempo [s]')
axs[3].set_ylabel('Amplitude')
axs[3].grid()

fig.tight_layout()


# Plotando resultados - Ângulo
fig, axs = plt.subplots(nrows=2, ncols=2)
axs = axs.flatten()
t=[k/(f*amostras) for k in range(0, len(sinal))]

# Sinal no tempo
axs[0].plot(t, sinal)
axs[0].set_title('Sinal')
axs[0].set_xlabel('Tempo [s]')
axs[0].set_ylabel('Ângulo [rad]')
axs[1].set_ylim(0,3)
axs[0].grid()

# Fundamental
axs[1].plot(t, ts[1][1])
axs[1].set_title('Ângulo da fundamental')
axs[1].set_xlabel('Tempo [s]')
axs[1].set_ylabel('Ângulo [rad]')
axs[1].grid()

# Terceira harmônica
axs[2].plot(t, ts[1][3])
axs[2].set_title('Ângulo da terceira harmônica')
axs[2].set_xlabel('Tempo [s]')
axs[2].set_ylabel('Ângulo [rad]')
axs[2].grid()

# Décima harmônica
axs[3].plot(t, ts[1][10])
axs[3].set_title('Ângulo da décima harmônica')
axs[3].set_xlabel('Tempo [s]')
axs[3].set_ylabel('Ângulo [rad]')
axs[3].grid()

fig.tight_layout()
plt.show()
