
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (10, 6),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)
plt.style.use('ggplot')

# from IPython.display import display
# import ipywidgets as widgets
import pandas as pd
# from PIL import Image
from datetime import datetime


import numpy as np
from scipy.integrate import odeint

## Total population, N.
#N = 10000
## Initial number of infected and recovered individuals, I0 and R0.
#I0, Ri = 1, 0
## Everyone else, S0, is susceptible to infection initially.
#S0 = N - I0 - Ri
## Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
#beta, gamma = 0.3, 1./10 
#
#Tchange1=40
#beta2=beta/2
#gamma2= gamma
#
## A grid of time points (in days)
#t = np.linspace(0, 160, 160)
#t1=t[t<Tchange]
#t2=t[t>=Tchange]

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# Initial conditions vector
#y0 = S0, I0, Ri
## Integrate the SIR equations over the time grid, t.
#ret = odeint(deriv, y0, t1, args=(N, beta, gamma))
#S1, I1, R1 = ret.T
#y0=S1[-1], I1[-1], R1[-1]
#ret2 = odeint(deriv, y0, t2, args=(N, beta2, gamma2))
#S2, I2, R2 = ret2.T
#
#S= np.concatenate((S1,S2),axis=0)
#I= np.concatenate((I1,I2),axis=0)
#R= np.concatenate((R1,R2),axis=0)

#R0=beta/gamma
#print(R0)

def GetSIR(yx,tx,N,beta,gamma):
    
    ret = odeint(deriv, yx, tx, args=(N, beta, gamma))
    Sx, Ix, Rx = ret.T
    
    return Sx, Ix, Rx


def GetPlot(t,S,I,R,time,plot,P2=False,TChng=0,P3=False,TChng1=0):
    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
    ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
    ax.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
    ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
    ax.set_xlabel('Time /days')
    ax.set_ylabel('Number (1000s)')
    
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    if P2:
        plt.axvline(TChng,linestyle='--',color='red')
    if P3:
        plt.axvline(TChng1,linestyle='--',color='green')
    fig = plt.gcf()
    # plt.title('R0: {}'.format(round(R0,2)))
    plt.savefig('static/img/'+plot+time+'.jpg',bbox_inches='tight')
    return 

def Plot1(beta,gamma,time):
    # beta=0.3
    # gamma=0.1
    # Total population, N.
    N = 10000
    # Initial number of infected and recovered individuals, I0 and R0.
    I0, Ri = 1, 0
    # Everyone else, S0, is susceptible to infection initially.
    S0 = N - I0 - Ri
    
    # Initial conditions vector
    yx = S0, I0, Ri

    # A grid of time points (in days)
    tx = np.linspace(0, 160, 160)
    
    Sx, Ix, Rx = GetSIR(yx,tx,N,beta,gamma)
    # Ix.index(max(Ix))
    MaxInfInd = np.argmax(Ix)
    PerMaxInfVal = Ix[MaxInfInd]/100
    CumInf = Rx[-1]/100
    
    R0=beta/gamma
    print('R0: {}'.format(round(R0,2)))
    #fig = GetPlot(tx,Sx,Ix,Rx)
    GetPlot(tx,Sx,Ix,Rx,time=time,plot="one")
    return MaxInfInd,round(PerMaxInfVal,2),round(CumInf,2)

#yx,tx,N,beta,gamma = Plot1(beta,gamma)

def Plot2(beta2,gamma2,Tchange1,time,DecFactor):
    
    # Total population, N.
    N = 10000
    # Initial number of infected and recovered individuals, I0 and R0.
    I0, Ri = 1, 0
    # Everyone else, S0, is susceptible to infection initially.
    S0 = N - I0 - Ri
    
    # Initial conditions vector
    yx = S0, I0, Ri
    
    t = np.linspace(0, 160, 160)
    t1=t[t<Tchange1]
    t2=t[t>=Tchange1]
    
    beta= beta2*DecFactor
    gamma = gamma2
    S1, I1, R1 = GetSIR(yx,t1,N,beta,gamma)
    
    y1=S1[-1], I1[-1], R1[-1]
    
    beta = beta2
    gamma = gamma2
    R0=beta/gamma
    print('R0: {}'.format(round(R0,2)))
    
    S2, I2, R2 = GetSIR(y1,t2,N,beta,gamma)
    
    S= np.concatenate((S1,S2[1:]),axis=0)
    I= np.concatenate((I1,I2[1:]),axis=0)
    R= np.concatenate((R1,R2[1:]),axis=0)
    
    MaxInfInd = np.argmax(I)
    PerMaxInfVal = I[MaxInfInd]/100
    Cuminf = R[-1]/100
    
    GetPlot(t[:-1],S,I,R,P2=True,TChng=Tchange1,time=time,plot="two")
    return MaxInfInd,round(PerMaxInfVal,2),round(Cuminf,2)
    
# def fig2img(fig):
#     """Convert a Matplotlib figure to a PIL Image and return it"""
#     import io
#     buf = io.BytesIO()
#     fig.savefig(buf)
#     buf.seek(0)
#     img = Image.open(buf)
#     return img

#Plot2(0.3,0.1,40)

#gamma = 0.1
#betas = np.arange(0.8,gamma,-0.01)[:-1]
#images = []
#for beta in betas:
#    fig = Plot1(beta,gamma)
#    fig.suptitle('Gamma: {}, Beta: {}, R0: {}'.format(gamma,round(beta,4),round(beta/gamma,4)))
#    img = fig2img(fig)
#    images.append(img)
#images[0].save('SIR_Gif.gif',
#               save_all=True,
#               append_images=images[1:],
#               duration=100,
#               loop=0)

# def Display_gif():
#     animatedGif = "SIR_Gif.gif" #path relative to your notebook
#     file = open(animatedGif , "rb")
#     image = file.read()
#     progress= Image(
#         value=image,
#         format='gif',
#         width=900,
#         height=100)
#     display(progress)
#     return 

def Plot3(beta2,gamma2,Tchange1,Tchange2,time,DecFactor):
    # Total population, N.
    N = 10000
    # Initial number of infected and recovered individuals, I0 and R0.
    I0, Ri = 1, 0
    # Everyone else, S0, is susceptible to infection initially.
    S0 = N - I0 - Ri
    
    # Initial conditions vector
    yx = S0, I0, Ri
    
    t = np.linspace(0, 160, 160)
    t1=t[t<=Tchange1]
    t2=t[(t>=Tchange1)&(t<=Tchange2)]
    t3=t[t>=Tchange2]
    t2_I = t[(t>=Tchange1)]
    
    beta= beta2*DecFactor
    gamma = gamma2
    S1_I, I1_I, R1_I = GetSIR(yx,t,N,beta,gamma)
    S1, I1, R1 = GetSIR(yx,t1,N,beta,gamma)
    
    y1=S1[-1], I1[-1], R1[-1]
    
    beta = beta2
    gamma = gamma2
#    R0=beta/gamma
#    print('R0: {}'.format(round(R0,2)))
    S2_I, I2_I, R2_I = GetSIR(y1,t2_I,N,beta,gamma)
    S2, I2, R2 = GetSIR(y1,t2,N,beta,gamma)
    
    y2=S2[-1], I2[-1], R2[-1]
    
    beta = beta2*DecFactor
    gamma = gamma2
    R0=beta/gamma
    # print('R0: {}'.format(round(R0,2)))
    
    S3, I3, R3 = GetSIR(y2,t3,N,beta,gamma)
    
    #I1_I
    I2_I= np.concatenate((I1,I2_I),axis=0)
    I3= np.concatenate((I1,I2,I3),axis=0)
    
    Irate = pd.DataFrame({'Initial Rate':I1_I,
                          'Continued Social Distancing':I2_I,
                          'Easing the norms':I3,})
    Irate.plot()
    plt.axvline(t1[-1],linestyle='--',color='red')
    plt.axvline(t2[-1],linestyle='--',color='green')
    # plt.title('Infection rate comparison in various scenarios with R0: {}'.format(round(R0,2)))
    plt.savefig('static/img/three'+time+'.jpg',bbox_inches='tight')
#    S= np.concatenate((S1,S2[1:],S3[1:]),axis=0)
#    I= np.concatenate((I1,I2[1:],I3[1:]),axis=0)
#    R= np.concatenate((R1,R2[1:],R3[1:]),axis=0)
#    t = np.concatenate((t1,t2[1:],t3[1:]),axis=0)
#    
#    GetPlot(t,S,I,R,P2=True,TChng=Tchange1,P3=True,TChng1=Tchange2)
    return (round(max(I3)/100,2),round(R3[-1]/100,2))

# beta2 = 0.3/2
# gamma2 = 0.1
# Tchange1 = 40
# Tchange2 = 70
# time = datetime.now().strftime("%H%M%S")
# Plot3(beta2,gamma2,Tchange1,Tchange2,time=time)

# Beta=widgets.FloatSlider(
#     value=0.3,
#     min=0,
#     max=0.6,
#     description='Beta:',
#     step=0.1,
#     disabled=False
# )
# Gamma=widgets.FloatSlider(
#     value=0.1,
#     min=0.01,
#     max=0.6,
#     description='Gamma:',
#     step=0.1,
#     disabled=False
# )
# Tchange1=widgets.IntSlider(
#     value=40,
#     min=0,
#     max=160,
#     description='Tchange1:',
#     step=10,
#     disabled=False
# )





