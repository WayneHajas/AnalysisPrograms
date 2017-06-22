#Class to represent Measured Animals in a quadrat

from numpy.random import dirichlet
from numpy import inf,ndarray

class MeasAnimals:
    def __init__(self,SizeMeas=None,SizeBound=None):
        '''MeasAnimals(SizeMeas=None,SizeBound=None)
        list(numeric(SizeMeas)) is a list of size-measurements(floating or integer).  None indicates that there are no measurements
        list(numeric(SizeBound) is a list of upper bounds(integer or float) corresponding to size-classes.  None indicates that there are no size classes.'''

        self.SizeBound=SizeBound
        if (self.SizeBound==None):self.SizeBound=[inf]
        if isinstance(self.SizeBound,(float,int)):self.SizeBound=[self.SizeBound]
        if max(self.SizeBound)<(inf):self.SizeBound+=[inf]

        self.SizeBound.sort()
        self.nSizeClass=len(self.SizeBound)

        self.Nanimal=0
        if isinstance(SizeMeas,(float,int)):self.Nanimal=1.
        if isinstance(SizeMeas,(list,ndarray)):self.Nanimal=len(SizeMeas)
        
        self.SizeFreq=None
        if self.Nanimal==0:self.SizeFreq=[0]*self.nSizeClass
        self.SizeMeas=SizeMeas
        if (SizeMeas!=None) and (self.Nanimal>0):
            self.SizeMeas=[list(filter(lambda x:x<=self.SizeBound[0],SizeMeas))]
            self.SizeMeas+=list(map(lambda i:list(filter(lambda x:(x<=self.SizeBound[i])and(x>self.SizeBound[i-1]),SizeMeas)),   range(1,self.nSizeClass)))
            self.SizeFreq=list(map(lambda x: len(x),self.SizeMeas))

    def ResampSizeProb(self,UseDeterm=False):
        if self.nSizeClass==1:return([1.0])
        if self.Nanimal==0:return(self.nSizeClass*[0.])
        if not(UseDeterm):return(list(dirichlet(self.SizeFreq)))
        #Deterministic
        return(list(map(lambda x:float(x)/float(self.Nanimal),self.SizeFreq   )))

    def GetAbundance(self,AE):
        '''GetAbundance(AE)
        AE(L)is the allometric equation relating Length to Weight)
        Returns a 2-d list.  Each row represents a size-class.
        First column gives the number of animals in the size-class.
        Second column gives biomass estimated for the size-class'''

        #There is no data
        if (self.SizeMeas==None) or (self.SizeMeas==[]):
            result={}
            for i in range(self.nSizeClass):
                kname='USL'+str(self.SizeBound[i])
                result[kname]={'Pop':0,'Bmass':0.}
            return(result)

        #There is data
        result={}
        for i in range(self.nSizeClass):
            x=self.SizeMeas[i]
            kname='USL'+str(self.SizeBound[i])
            if len(x)==0:
                result[kname]={'Pop':0,'Bmass':0.}
            else:
                pop=len(x)
                if pop==0:
                    bmass=0.
                else:
                    if AE==None:
                        bmass=None
                    else:
                        try:
                            bmass=sum(list(map(lambda y:AE(y),x)))
                        except:
                            print('MeasAnimals 72,x\n',x )
                            print(AE)
                            print(help(AE))
                            print(AE(54))
                            print(x[0],AE(x[0]))
                            print ('AE(x)', list(map(lambda y:AE(y),x)) )
                            bmass=sum(list(map(lambda y:AE(y),x)))
                            
                result[kname]={'Pop':pop,'Bmass':bmass}
        return(result)
        
        
if __name__ == "__main__":


    from numpy import exp,log
    def AE(L):return(exp(2.4175+2.754*log(L/30.)+.5*.1222*.1222))

    q3=MeasAnimals(SizeMeas=[10,20,60,100,30,40],SizeBound=54)
    print (q3.SizeBound)
    for x in q3.SizeMeas:
        print (x)
    print ('\n')

    print('q3.GetAbundance(AE)', q3.GetAbundance(AE))
    print ('\n')
