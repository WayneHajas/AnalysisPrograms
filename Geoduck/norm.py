import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from wchNorm import InvNorm
from numpy.random import normal
from numpy import ndarray,array

class norm():
    '''This class is a proxy for scipy.stats.norm.
    cx_freeze has trouble with scipy.stats.norm
    cx_freeze seems to deal with numpy.random.normal'''

    def __init__(self,mu,sigma):
        self.mu=mu
        self.sigma=sigma

    def rvs(self,n=None,LowBound=None):
        if self.sigma<1.e-6:
            if (n==None) and (LowBound!=None):return(max([self.mu,LowBound]))
            if (n==None) and (LowBound==None):return(self.mu)
            if (self.mu>LowBound):return(array(n*[self.mu]))
            return(array(n*[LowBound]))
            
        Unbounded=normal(self.mu,self.sigma,size=n)
        if LowBound==None:return(Unbounded)
        result=list(map(lambda t:max([t,LowBound])   ,Unbounded))
        return(result)
   
       
      

    def isf(self,p):
        if isinstance(p,(list,ndarray)):
            z=list(map(lambda t:self.mu+self.sigma*InvNorm(1-t),p))
            if isinstance(p,ndarray):z=array(z)
            return(z)
        else:
            z=self.mu+self.sigma*InvNorm(1-p)
            return(z)
    def EquiProbVal(self,n,LowBound=None):
        p =list(map(lambda i:(i+.5)/float(n),range(n)))
        Unbounded=self.isf(p)
        result=Unbounded
        if LowBound!=None:
            result=list(map(lambda t:max(t,LowBound)  ,Unbounded))
        
        return(result)

           
if __name__ == "__main__":

    mu=0
    sigma=1
    p=[.025,.05,.5,.95,.975]
    RandSource=norm(mu,sigma)
    print('\n')
    print(RandSource.rvs())
    print(RandSource.rvs(n=3))
    print('\n')
    RandSource=norm(1,sigma)
    print(RandSource.isf(.5))
    print(RandSource.isf(p))
    print('\n')
    RandSource=norm(0,1.)
    print(RandSource.rvs())
    print('\n')
    print(RandSource.EquiProbVal(n=10))
    print(RandSource.EquiProbVal(n=10,LowBound=0))
    print('\n')
    print(RandSource.isf(.5))
    print(RandSource.isf(p))

    
    
