import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


def plotST(*args):
    title = args[0]
    amp = args[1]
    ppc = args[2]
    start = args[3]
    end = args[4]
    signal = args[5]

    timestep = 1/(ppc * 60)

    t = [timestep * i for i in range(0, len(amp[1]))]

    fig = plt.figure(figsize=(7, 7), layout='constrained')
    axs = fig.subplot_mosaic([["fundamental", "fundamental"],
                              ["inicio", "fim"],
                              ["harmonicos", "harmonicos"]])

    newTitle = ''
    for x in title.split('_')[1:]:
        newTitle+= x.upper() + ' '
    fig.suptitle(newTitle)
    # Plota a fundamental
    axs["fundamental"].set_title("Fundamental")
    axs["fundamental"].plot(t, amp[1])
    axs["fundamental"].plot(t, signal[0:len(t)], alpha=0.3)
    axs["fundamental"].set_xlabel("Time (s)")
    axs["fundamental"].set_ylabel("Amplitude")
    axs["fundamental"].grid()

    #Plota o início do evento
    axs["inicio"].set_title("Início do evento")
    axs["inicio"].plot([timestep*i for i in range(int(start*ppc*60)-100, int(start*ppc*60)+100)],
                       amp[1][int(start*ppc*60)-100: int(start*ppc*60)+100])
    axs["inicio"].set_xlabel("Time (s)")
    axs["inicio"].set_ylabel("Amplitude")
    axs["inicio"].grid()

    #Plota o fim do evento
    axs["fim"].set_title("Fim do evento")
    axs["fim"].plot([timestep * i for i in range(int(end * ppc * 60) - 100, int(end * ppc * 60) + 100)],
                    amp[1][int(end * ppc * 60) - 100: int(end * ppc * 60) + 100])
    axs["fim"].set_xlabel("Time (s)")
    axs["fim"].set_ylabel("Amplitude")
    axs["fim"].grid()


    #Plota o histograma do espectro
    Z = amp[2:]
    # for line in amp[2:]:
    #     aux=[]
    #     for i in line:
    #         aux.append(np.log(i))
    #     Z.append(aux)
    x = [timestep*i for i in range(0, len(amp[1]))]
    y = np.arange(2, len(amp))

    im = axs["harmonicos"].pcolormesh(x, y, Z)
    fig.colorbar(im, ax=axs["harmonicos"])
    axs["harmonicos"].set_title("Harmônicas")
    axs["harmonicos"].set_xlabel("Time (s)")
    axs["harmonicos"].set_ylabel("Amplitude")

    # plt.show()
    plt.savefig(title+'.png')