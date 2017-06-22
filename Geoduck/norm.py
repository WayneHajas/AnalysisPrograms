import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from wchNorm import InvNorm
from numpy.random import normal
from numpy import ndarray,array
import pdb

class norm():
    '''This class is a proxy for scipy.stats.norm.
    cx_freeze has trouble with scipy.stats.norm
    cx_freeze seems to deal with numpy.random.normal'''

    def __init__(self,mu,sigma):
        self.mu=mu
        self.sigma=sigma

    def rvs(self,n=None):
        if self.sigma<1.e-6:
            if n==None:return(self.mu)
            return(array(n*[self.mu]))
        try:
            return(normal(self.mu,self.sigma,size=n))
        except:
            print('\n norm 21')
            pdb.set_trace()
            return(normal(self.mu,self.sigma,size=n))
            

    def isf(self,p):
        if isinstance(p,(list,ndarray)):
            z=list(map(lambda t:self.mu+self.sigma*InvNorm(1-t),p))
            if isinstance(p,ndarray):z=array(z)
            return(z)
        else:
            z=self.mu+self.sigma*InvNorm(1-p)
            return(z)
    def EquiProbVal(self,n):
        p =list(map(lambda i:(i+.5)/float(n),range(n)))
        result=self.isf(p)
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
    RandSource=norm(1,0.)
    print(RandSource.rvs())
    print(RandSource.rvs(n=3))
    print(RandSource.isf(.5))
    print(RandSource.isf(p))

    
    
