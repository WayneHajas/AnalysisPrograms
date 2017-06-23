'''Wrapper to numpy.random.choice.  If a seed is specified, then that seed 
will be implemented before numpy.random.choice is implemented.

Randomization process was getting corrupted.  This will help'''


from numpy.random import seed
from numpy.random import choice as numpychoice

def choice(a,size=None,curseed=None,replace=True,p=None):
    
    if curseed!=None:
        seed(curseed)
    result=numpychoice(a, size=size,replace=replace,p=p)
    return(result)
    
    
if __name__ == "__main__":
    
    seed(756)
    
    x=['q','w','e','r','t','y','u','i']
    sampsize=len(x)
    
    
    print(choice(x,sampsize))
     
     
    niter=100000
    
    seed(756)
    samp1=[choice(x,sampsize) for i in range(niter)  ]
    
    seed(756)
    samp2=[choice(x,sampsize) for i in range(niter)  ]
    
    def MatchSample(x,y):
        result=all([x[i]==y[i] for i in range(sampsize)   ])
        return(result)
        
    print(MatchSample(samp1[0],samp2[0]))
    print(MatchSample(samp1[1],samp2[0]))
    print('\n')
    
    fullMatch=[MatchSample(samp1[i],samp2[i])   for i in range(niter)]
    
    
    print(sum(fullMatch)/niter)