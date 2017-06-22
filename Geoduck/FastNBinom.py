from numpy import sqrt

import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from InterpProd import WCHinterp


def InvCDF(p,r,QVals):
    '''InvCDF(p,r,QVals)
       A fast way to generate many inverse-CDFs for the beta-distribution.
       * p correspond to the show factor
       * r corresponds to the number of shows
       * QVals 0 to 1.  are the cumulative probabilities for which we want to find the corresponding x-values

       Note that the results correspond to the CDF for the number of non-showing ducks.
       To get the estimated number of all ducks (showing and non-showing) you have to add r.
       The parameterization of the negative binomial distribution has a couple variations.  Beware!

       
       '''
    Kmod=int(r*p/(1.-p))#Approximate mode of estimate
    EstSD=sqrt(r*p)/(1.-p)#Approximation of standard deviation of the number of non-shows

    Klow=max([0,int(Kmod-3.*EstSD)])#Establish upper and lower bounds for the number of non-showing ducks that will be considered
    Kupp=       int(Kmod+3.*EstSD)

    #Arbitrarily set the pdf at the mode to 1.   Will normalize later.
    PDF=[1.]*(Kupp-Klow+1)

    for k in range(Kmod+1,Kupp+1):
        PDF[k-Klow]=PDF[k-1-Klow]*(k+r-1)*p/k
    for k in range(Kmod-1,Klow-2,-1):
        PDF[k-Klow]=PDF[k-Klow+1]*(k+1)/p/(k+r)

    #Convert to cumulative sum
    for k in range(1,len(PDF)):
        PDF[k]+=PDF[k-1]
            

    #Normalize
    sumPDF=PDF[-1]
    CDF=list(map(lambda x:x/sumPDF,PDF))
    newx=WCHinterp(CDF,list(range(Klow,Kupp+1)),QVals)
    return(newx)

def GenQvals(n=100):
    result=list(map(lambda i: (i+.5)/float(n), range(n)))
    return(result)
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from scipy.stats import nbinom
    from numpy import array
    

    shows1=900
    sf=0.90   
    npoint=100
    QVals=GenQvals(n=npoint)
    test=InvCDF(1.-sf,shows1,QVals)
    ref=nbinom.isf(1.-array(QVals),shows1,sf)
    
    plt.plot(test,QVals,'r*')
    plt.plot(ref,QVals,'k-',linewidth=5,alpha=0.25)
    plt.show()
    
