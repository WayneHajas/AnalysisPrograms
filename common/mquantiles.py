from numpy import interp,inf

def mquantiles(probSample,prob=[.025,.975]):
    '''For some reason, scipy.mstats wouldn't work with cx_freeze.
    Therefore I am making my own interpolation method'''
    if isinstance(prob,(float)):return(mquantiles(probSample,prob=[prob]))
    if isinstance(probSample,(float,int)):return(None)

    oldy=sorted(probSample)
    n=len(oldy)
    oldx=list(map(lambda t: (t+.5)/float(n),range(n)))
    result=interp(prob,oldx,oldy)
    
    for i in range(len(prob)):
        if prob[i]<=0:result[i]=-inf
        if prob[i]>=1:result[i]= inf
    
    return (result)

if __name__ == "__main__":
    probSample=list(map(lambda t: (t+.5)/10.,range(10)))
    prob=list(map(lambda t:(t-.5)/20.,range(22)))
    q= mquantiles(probSample,prob=prob)

    print('\n',probSample,'\n')

    for i in range(len(prob)):
        print (i, prob[i],q[i])
        
    probSample=list(map(lambda t: (t+.5)/20.,range(10)))
    prob=list(map(lambda t:(t-.5)/20.,range(10,22)))+list(map(lambda t:(t-.5)/20.,range(10)))
    q= mquantiles(probSample,prob=prob)

    print('\n',probSample,'\n')

    for i in range(len(prob)):
        print (i, prob[i],q[i])
          
    
