# %load_ext watermark

# %watermark -v -m -p matplotlib,flask,pandas,datetime,numpy,scipy

from flask import Flask,render_template,url_for,request
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
from SIR_model2 import *
from datetime import datetime
# import pandas as pd

import numpy as np
from scipy.integrate import odeint

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/predict",methods=['POST'])
def predict():
    beta = float(request.form['beta'])
    gamma = float(request.form['gamma'])
    time = datetime.now().strftime("%H%M%S")
    
    OutputDict = {'p1':None,'p2':None,'time':time,'p3':None}
    try:
        DecFactor = int(request.form['DecFactor'])
        lkdown = int(request.form['lkdown'])
    except :
        time = datetime.now().strftime("%H%M%S")
        OutputDict["time"]=time
        plot1Info = Plot1(beta,gamma,time)
        OutputDict['p1'] = plot1Info
        time = datetime.now().strftime("%H%M%S")
        
        return render_template("predict.html",InfoDict = OutputDict)
    try:
        lkdownopen = int(request.form['lkdownopen'])
        lkdownopen = lkdown+lkdownopen
    except:
        time = datetime.now().strftime("%H%M%S")
        OutputDict["time"]=time
        plot1Info = Plot1(beta,gamma,time)
        OutputDict['p1'] = plot1Info
        beta2 = beta/DecFactor
        plot2Info = Plot2(beta2,gamma,lkdown,time=time,DecFactor=DecFactor)
        OutputDict['p2'] = plot2Info
        # OutputDict = {"p2":plot2Info,"time":time}
        return render_template("predict.html",InfoDict = OutputDict)
    time = datetime.now().strftime("%H%M%S")
    OutputDict["time"]=time
    beta2 = beta/DecFactor
    plot1Info = Plot1(beta,gamma,time)
    OutputDict['p1'] = plot1Info
    # beta2 = beta/DecFactor
    plot2Info = Plot2(beta2,gamma,lkdown,time=time,DecFactor=DecFactor)
    OutputDict['p2'] = plot2Info
    plot3Info = Plot3(beta2,gamma,lkdown,lkdownopen,time=time,DecFactor=DecFactor)
    OutputDict['p3'] = plot3Info
    return render_template("predict.html",InfoDict = OutputDict)

def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


# def SIR_Model(Beta,Gamma,DecFactor,lkdown,lkdownopen):
#     beta = Beta    
#     beta2 = beta/DecFactor
#     gamma = Gamma
#     Tchange1 = lkdown
#     Tchange2 = lkdownopen
#     time = datetime.now().strftime("%H%M%S")
#     i = Plot3(beta2,gamma,Tchange1,Tchange2,time=time,DecFactor=DecFactor)
#     plot2Info = Plot2(beta2,gamma,Tchange1,time=time,DecFactor=DecFactor)
#     plot1Info = Plot1(beta,gamma,time)
#     OutputDict = {"p1":plot1Info,"p2":plot2Info,"time":time}
#     return OutputDict   

    
if __name__ == "__main__":
    app.run(debug=True)

