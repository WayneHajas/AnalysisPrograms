from numpy import ndarray,array,hstack,dot
from scipy.stats import norm
from InterpProd import WCHinterp

class ProdOfProb:
    def __init__(self,EquiProbVals,mu,sigma,nresult=None):
        self.nresult=nresult
        if self.nresult==None:self.nresult=len(EquiProbVals)

        EquiProbVal1=array(list(filter(lambda epv:epv!=None,EquiProbVals)))
        EquiProbVal1=EquiProbVal1.reshape(len(EquiProbVal1),1)
        
        self.pval=array(list(map(lambda i:(i+.5)/float(self.nresult),range(self.nresult)))).reshape(1,self.nresult)
        if sigma==0.:
            EquiProbVal2=array(self.nresult*[mu]).reshape(1,self.nresult)
            
        else:
            try:
                EquiProbVal2=norm.isf(1-self.pval,mu,sigma)
            except:
                print('\nProdOfProb 21')
                print('self.pval',self.pval)
                print('mu,sigma',mu,sigma)

        try:
            oldy=hstack(dot(EquiProbVal1,EquiProbVal2))
            oldy.sort()
            nold=len(oldy)
        except:
            print('\nProdOfProb 30')
            print('EquiProbVal1',EquiProbVal1)
            print('EquiProbVal2',EquiProbVal2)
            print('oldy',oldy)
        oldx=list(map(lambda i:(i+.5)/float(nold),range(nold)))

        
        self.EquiProbVal=WCHinterp(oldx,oldy,self.pval)

def ProdAll(EquiProbVals,params,nresult=None):
    if params==[]:return(EquiProbVals)
    if isinstance(params[0],(list,ndarray)):
        POP1=ProdOfProb(EquiProbVals,params[0][0],params[0][1] ,nresult=nresult)
        try:
            result=ProdAll(hstack(POP1.EquiProbVal), params[1:])
        except:
            print('\nProdOfProb 46')
            print('hstack(POP1.EquiProbVal)',hstack(POP1.EquiProbVal))
            print('params[1:]',params[1:])
        return(result)

    POP1=ProdOfProb(EquiProbVals,params[0],params[1],nresult=nresult)
    return(POP1.EquiProbVal)

    
        
if __name__ == "__main__":
    mu=5
    sigma=.1
    EquiProbVals=norm.rvs(4,.1,20)
    EPV2=ProdOfProb(EquiProbVals,mu,sigma,nresult=None)
    print (ProdAll(EquiProbVals,[mu,sigma]))
    print (ProdAll(EquiProbVals,[[mu,sigma]]))
    print (ProdAll(EquiProbVals,[[mu,sigma],[mu,0]]))
    print (ProdAll(EquiProbVals,[[mu,sigma],[mu,0],[0,1]]))
