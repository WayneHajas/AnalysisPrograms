#Class to represent Unmeasured Animals in a quadrat
from numpy.random import multinomial
from numpy import ndarray,inf
import pdb


class UnMeasAnimals:
    def __init__(self,nAnimals,SizeBound=None,SizeProb=None,AvgWeight=None):
        '''UnMeasAnimals(nAnimals,SizeBound=None,SizeProb=None,AvgWeight=None)
        nAnimals is the number of unmeasured animals
        nSizeClass is the number of size classes
        list(numeric(SizeProb)) is the probability associated with each size-class
        list(numeric(AvgWeight) is the average weight associated with each size-class
        '''
        self.SizeBound=SizeBound
        if (self.SizeBound==None):self.SizeBound=[inf]
        if isinstance(self.SizeBound,(float,int)):self.SizeBound=[self.SizeBound,inf]
        if max(self.SizeBound)<(inf):self.SizeBound+=[inf]

        self.SizeBound.sort()
        self.nSizeClass=len(self.SizeBound)

        self.nAnimals=nAnimals
        self.SizeProb=SizeProb
        self.AvgWeight=AvgWeight
        if (self.SizeProb==None) :self.SizeProb=list(map(lambda t:1./float(self.nSizeClass),range(self.nSizeClass)))
        try:
            self.SetSizeProb(self.SizeProb)
        except:
            print ('\nUnMeasAnimals line 31')
            print ('self.nAnimals',self.nAnimals)
            print ('self.SizeProb',self.SizeProb)
            print ('self.nSizeClass',self.nSizeClass)
            #pdb.set_trace()
            self.SetSizeProb(self.SizeProb)
            dummy=1./0.
        self.SetAvgWeight(self.AvgWeight)

    def SetSizeProb(self,SizeProb):
        self.SizeProb=SizeProb
        if isinstance(self.SizeProb,(int,float)):
           self.SizeProb=[1.0]
           self.nSizeClass=1
           return
        if self.SizeProb==None:   
           self.SizeProb=[1.0]
           self.nSizeClass=1
           return
        if self.SizeProb==[]:   
           self.SizeProb=self.nSizeClass*[1.0/float(self.nSizeClass)]
           return

         
        #Make sure probabilities sum to one
        sumProb=sum(self.SizeProb)
        if (sumProb!=1.0) and (sumProb!=0.0):
            SP=map(lambda x: x/sumProb,self.SizeProb)
            self.SizeProb=list(SP)

    def SetAvgWeight(self,AvgWeight):
        self.AvgWeight=AvgWeight
        if isinstance(self.AvgWeight,(float,int)):self.AvgWeight=[self.AvgWeight]

    def GetAbundance(self, AvgWeight=None,SizeProb=None,UseDeterm=False):
        #pdb.set_trace()
        if self.nAnimals==0:
            result={}
            for USL in self.SizeBound:
                kname='USL'+str(USL)
                result[kname]={'Pop':0,'Bmass':0.}
            return(result)
            
        if AvgWeight!=None:self.SetAvgWeight(AvgWeight)
        if isinstance(self.AvgWeight,(list,ndarray)):
            AllNone=list(map(lambda x:x==None,self.AvgWeight))
            if all(AllNone):self.AvgWeight=None
        if self.AvgWeight!=None:
            if len(self.AvgWeight)!=self.nSizeClass:
                print ('\nUnMeasAnimals 80')
                print (' number of size classes is ',self.nSizeClass,self.SizeBound)
                print ('number of average-weights is ',len(self.AvgWeight),self.AvgWeight)
                print ('self.SizeProb',self.SizeProb)
                print ('AvgWeight',AvgWeight)
                print ('self.SizeBound',self.SizeBound)
                print ('self.nAnimals',self.nAnimals)
                dummy=1./0.
                      
        if (SizeProb!=None):self.SetSizeProb(SizeProb)

        
        #pdb.set_trace()
        if self.nSizeClass==1:RandomFreq=[self.nAnimals]
        else:RandomFreq=list(multinomial(self.nAnimals,self.SizeProb))
        if UseDeterm:RandomFreq=list(map(lambda x:x*float(self.nAnimals), self.SizeProb))
        #pdb.set_trace()
        if self.AvgWeight!=None:
            try:
                result={}
                for i in range(self.nSizeClass):                        
                    kname='USL'+str(self.SizeBound[i])
                    if RandomFreq[i]==0:
                        result[kname]={'Pop':0,'Bmass':0.}
                    else:
                    	if isinstance(self.AvgWeight,dict):
                    	  result[kname]={'Pop':RandomFreq[i],'Bmass':float(RandomFreq[i])*float(self.AvgWeight[kname])}
                    	else:
                    	  result[kname]={'Pop':RandomFreq[i],'Bmass':float(RandomFreq[i])*float(self.AvgWeight[i])}
                return(result)
            except:
                print('\nUnMeasAnimals 90, ')
                print('RandomFreq\n',RandomFreq)
                print('self.AvgWeight\n',self.AvgWeight)
                print('self.nSizeClass\n',self.nSizeClass)
                print('self.nAnimals',self.nAnimals)
                print ('self.SizeProb',self.SizeProb)
                print ('self.SizeBound',self.SizeBound)
                dummy=1./0.

        #No information for average weight
        try:
            result={}
            for i in range(self.nSizeClass):
                kname='USL'+str(self.SizeBound[i])
                result[kname]={'Pop':RandomFreq[i],'Bmass':None}
            return(result)
        except:
            print('\nUnMeasAnimals 109, ')
            print('RandomFreq\n',RandomFreq)
            print('self.AvgWeight\n',self.AvgWeight)
            print('self.nSizeClass\n',self.nSizeClass)
            print('self.SizeBound\n',self.SizeBound)
            return(None)

        return(None)
        
if __name__ == "__main__":
    uma1=UnMeasAnimals(1,sizeBound=[89,inf])
    uma2=UnMeasAnimals(10,nSizeClass=3)
    uma3=UnMeasAnimals(10,nSizeClass=3,SizeProb=[.15,.15,.3])
    uma4=UnMeasAnimals(10,nSizeClass=3,SizeProb=[.15,.15,.3],AvgWeight=[10,100,1000])
        

    print ('\n')
    for x in uma4.GetAbundance(): print (x)
    print ('\ndone')
