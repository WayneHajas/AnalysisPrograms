

from scipy.stats import nbinom, beta
from numpy import array


import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from mquantiles import mquantiles
import FastBeta 
import FastNBinom 

def GenQvals(n=100):
    result=list(map(lambda i: (i+.5)/float(n), range(n)))
    return(result)

def EstNduck(sf,shows,QVals=None,npoint=100):
    '''EstNduck(sf,shows,QVals=None,npoint=100)
    Use the negative binomal distribution to generate equi-probable values
     of the total number of geoducks give the show-factor and the number of shows.
    *sf is the show factor
    *shows is the numbr of shows
    *QVals is a list of equiprobably q-vals 0<1.
      - if QVals==None, the values are calculated according to npoint
    *npoint is the number of equiprobably values to estimate
      - npoint is ignored if values are given for Qvals'''
    if (QVals==None):QVals=GenQvals(n=npoint)
    if isinstance(QVals,float):
        result=GenSF(shows, ducks,QVals=[QVals])
        return(result[0])

    G=list(map(lambda y:shows+nbinom.isf(1-y,shows,sf),QVals))
    return(G)
def GenDucks(shows1,ducks1,shows2,QVals=None,npoint=100):
    
    '''GenDucks(shows1,ducks1,shows2,QVals=None,npoint=100)
    Estimate the number of geoducks given the number of shows and corresponding data
       from a show-factor plot.
    *shows1 is the numbr of shows in the show-factor plot
    *ducks1 is the estimated number of ducks in the show-fator plot
    *shows2 is the current numbr of shows
    *QVals is a list of equiprobably q-vals 0<1.
      - if QVals==None, the values are calculated according to npoint
    *npoint is the number of equiprobably values to estimate
      - npoint is ignored if values are given for Qvals'''
    if (QVals==None):QVals=GenQvals(n=npoint)

    ProbSF=FastBeta.InvCDF(shows1+1, ducks1-shows1+1,QVals=QVals)
    ducks2=[]
    for psf in ProbSF:
        #ducks2+=EstNduck(psf,shows2,QVals=QVals)
        try:
            ducks2+=list(FastNBinom.InvCDF(1.-array(psf),shows2,QVals))
        except:
            print('NegBinom_Beta 23, psf,shows2, len(QVals)', psf,shows2, len(QVals))
            print('type(ducks2), type(FastNBinom.InvCDF(psf,shows2,QVals)) ',type(ducks2), type(FastNBinom.InvCDF(psf,shows2,QVals)))
            print('ducks2\n',ducks2)
            print('FastNBinom.InvCDF(psf,shows2,QVals)\n',FastNBinom.InvCDF(psf,shows2,QVals))
            ducks2+=FastNBinom.InvCDF(psf,shows2,QVals)
    ducks2=list(shows2+array(mquantiles(ducks2,prob=QVals)))
    return(ducks2)
def GenSFCorr(shows1,ducks1,shows2,QVals=None,npoint=100):
    
    '''GenSFCorr(shows1,ducks1,shows2,QVals=None,npoint=100)
    Estimate the correction factor to convert the number of shows in the
    density survey to equiprobable values for the number of geoducks.
    *shows1 is the numbr of shows in the show-factor plot(s)
    *ducks1 is the estimated number of ducks in the show-fator plot(s)
    *shows2 is the current numbr of shows in the density data
    *QVals is a list of equiprobably q-vals 0<1.
      - if QVals==None, the values are calculated according to npoint
    *npoint is the number of equiprobably values to estimate
      - npoint is ignored if values are given for Qvals'''
    nducks=GenDucks(shows1,ducks1,shows2,QVals=QVals,npoint=npoint)
    SFcorr=list(map(lambda t:  float(t)/float(shows2),nducks))
    return(SFcorr)

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    shows1=95
    ducks1=100
    shows2=950
    npoint=100
    QVals=GenQvals(n=npoint)

    
    g3=GenDucks(shows1,ducks1,shows2,QVals=QVals,npoint=npoint)
    #sf4=beta.rvs( shows1+1,ducks1-shows1+1,size=npoint*npoint)
    #g4=shows2+nbinom.rvs(shows2,sf4,size=len(sf4))
    #g4=mquantiles(g4,prob=QVals)
    
    #print('\n'FastBeta.InvCDF(shows1+1, ducks1-shows1+1,QVals=QVals))
    #print('\n',FastNBinom.InvCDF(1.-.95,shows2,QVals))
    
    bins=list(map(lambda i:950+5*i,range(21)))
    plt.hist(g3,fc='r',alpha=0.25,bins=bins)
    #plt.hist(g4,fc='b',alpha=0.25,bins=bins)
    print('done')
    plt.show()
