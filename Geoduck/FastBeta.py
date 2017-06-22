
from scipy.stats import nbinom, beta
from numpy import exp,log,array,ndarray


import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from mquantiles import mquantiles
from InterpProd import WCHinterp

def Probit(x):
    if isinstance(x,list):return(list(Probit(array(x))))
    return(log(x/(1.-x)))

def antiProbit(x):
    if isinstance(x,list):return(list(antiProbit(array(x))))
    return(exp(x)/(1+exp(x)))

def InvCDF(a,b,QVals):
    '''InvCDF(a,b)
       A fast way to generate many inverse-CDFs for the beta-distribution.
       * a,b correspond to the alpha and beta values in the beta distribution
       * QVals 0 to 1.  are the cumulative probabilities for which we want to find the corresponding x-values
       '''

        #Establish benchmark cumulative probbilities
    Bmark=[.001,.01,.1,.5,.9,.99,.999]
    Bmx=beta.isf(1.-array(Bmark),a,b) #inverses of the benchmark

    #Convert values to a probit-scale
    pBmark,pBmx,pQVals=Probit(Bmark),Probit(Bmx),Probit(QVals)
    pnewx=WCHinterp(pBmark,pBmx,pQVals)#Do interpolation on probit-scale
    newx=antiProbit(pnewx)#Convert result to non-probit scale

    #make sure result is the same data-type as QVals
    if isinstance(QVals,float) and not(isinstance(newx,float)):newx=newx[0]
    if isinstance(QVals,list) and not(isinstance(newx,list)):newx=list(newx)
    if isinstance(QVals,ndarray) and not(isinstance(newx,ndarray)):newx=array(newx)
    return(newx)

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    shows1=1
    ducks1=2
    npoint=200
    QVals=GenQvals(n=npoint)

    EquProbVal=InvCDF(shows1+1,ducks1-shows1+1,QVals=QVals)
    xexact=beta.isf(1.-array(QVals),shows1+1,ducks1-shows1+1)
    
    #plt.plot(QVals,EquProbVal,'k-')
    #plt.plot(QVals,xexact,'r-',linewidth=5,alpha=0.2)
    plt.plot(xexact,EquProbVal,'r-',linewidth=5,alpha=0.2)
    plt.plot([0,1.],[0,1],'k-')
    
    plt.show()


