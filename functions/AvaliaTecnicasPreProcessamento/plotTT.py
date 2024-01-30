import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

def plotTT(*args):
    Vtt = args[0]
    Vcs = args[1]
    Vck = args[2]
    Vpk = args[3]
    title = args[4]
    ppc = args[5]

    timestep = 1 / (ppc * 60)
    t = [timestep * i for i in range(0, len(Vcs[1]))]

    fig = plt.figure(figsize=(10, 10), layout='constrained')
    axs = fig.subplot_mosaic([["trifasico"],
                              ["cs"],
                              ["clarke"],
                              ["park"]])

    newTitle = ''
    for x in title.split('_')[1:]:
        newTitle += x.upper() + ' '
    fig.suptitle(newTitle)

    # Sinal de Referência
    axs["trifasico"].plot(t, [Vtt['A'][i] for i in range(len(t))], label=r'$V_{A}$')
    axs["trifasico"].plot(t, [Vtt['B'][i] for i in range(len(t))], label=r'$V_{B}$', alpha=0.3)
    axs["trifasico"].plot(t, [Vtt['C'][i] for i in range(len(t))], label=r'$V_{C}$', alpha=0.3)
    axs["trifasico"].set_title('Sinal de Referência')
    axs["trifasico"].set_xlabel('Tempo [s]')
    axs["trifasico"].set_ylabel('Amplitude')
    axs["trifasico"].grid()
    axs["trifasico"].legend(fontsize=12)

    #Componentes simétricas
    axs["cs"].plot(t, Vcs[0], label=r'$V_{+}$')
    axs["cs"].plot(t, Vcs[1], label=r'$V_{-}$')
    axs["cs"].plot(t, Vcs[2], label=r'$V_0$')
    axs["cs"].set_title('Componentes Simétricas')
    axs["cs"].set_xlabel('Tempo [s]')
    axs["cs"].set_ylabel('Amplitude')
    axs["cs"].grid()
    axs["cs"].legend(fontsize=12)

    # Clarke
    axs["clarke"].plot(t, Vck[0], label=r'$V_{\alpha}$')
    axs["clarke"].plot(t, Vck[1], label=r'$V_{\beta}$')
    axs["clarke"].plot(t, Vck[2], label=r'$V_0$')
    axs["clarke"].set_title('Transformada de Clarke')
    axs["clarke"].set_xlabel('Tempo [s]')
    axs["clarke"].set_ylabel('Amplitude')
    axs["clarke"].grid()
    axs["clarke"].legend(fontsize=12)

    axs["park"].plot(t, Vpk[0], label=r'$V_d$')
    axs["park"].plot(t, Vpk[1], label=r'$V_q$')
    axs["park"].plot(t, Vpk[2], label=r'$V_0$')
    axs["park"].set_title('Transformada de Park')
    axs["park"].set_xlabel('Tempo [s]')
    axs["park"].set_ylabel('Amplitude')
    axs["park"].grid()
    axs["park"].legend(fontsize=12)

    # plt.show()
    plt.savefig(title + '.png')

