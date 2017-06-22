#Routines for a generic quadrat.
#Should be good for urchins,cukes and geoducks.
#Cukes and urchins will have a single size class and no measured animals.

from numpy.random import dirichlet,multinomial
from UnMeasAnimals import UnMeasAnimals
from MeasAnimals   import MeasAnimals

class quadrat:
    def __init__(self,QuadNum,Depth,NumCount=0,SizeMeas=None,SizeBound=None):
        '''quadrat(QuadNum,Depth,NumCount,SizeMeas=None,SizeBound=None)
        int(QuadNum) is the quadrat number.  Also used to mark distance along the transect
        float(Depth) is the depth asigned to the quadrat.  Usually this corresponds to Chart-depth in metres.
        list(numeric(SizeMeas)) is a list of size-measurements(floating or integer).  None indicates that there are no measurements
        list(numeric(SizeBound) is a list of upper bounds(integer or float) corresponding to size-classes.  None indicates that there are no size classes
        '''
        self.QuadNum=QuadNum
        self.Depth=Depth
        self.NumCount=NumCount
        self.SizeBound=SizeBound
        self.UnMeas=UnMeasAnimals(self.NumCount,SizeBound=SizeBound)
        self.AddSizeMeas(SizeMeas,NewSizeBound=self.SizeBound)
        

    def AddSizeMeas(self,NewSizeMeas,NewSizeBound=None):
        if NewSizeBound!=None:self.Sizebound=NewSizeBound
        self.Meas=None
        if NewSizeMeas!=None:
            try:
                self.Meas=MeasAnimals(SizeMeas=NewSizeMeas,SizeBound=self.SizeBound)
            except:
                print('quadrat line 31 NewSizeMeas,self.SizeBound\n',NewSizeMeas,'\n',self.SizeBound)
                self.Meas=MeasAnimals(SizeMeas=NewSizeMeas,SizeBound=self.SizeBound)
            self.NumCount=max([self.NumCount,self.Meas.Nanimal])

            #Update unmeasured animals to deterministic values
            try:
                self.UnMeas=UnMeasAnimals(self.NumCount-self.Meas.Nanimal,\
                                      SizeProb=self.Meas.ResampSizeProb(UseDeterm=True),\
                                         SizeBound= self.Sizebound)
            except:
                print ('\nquadrat line 42')
                print ('self.QuadNum',self.QuadNum)
                print ('self.SizeBound',self.SizeBound)
                print ('NewSizeMeas',NewSizeMeas)
                
                self.UnMeas=UnMeasAnimals(self.NumCount-self.Meas.Nanimal,\
                                      SizeProb=self.Meas.ResampSizeProb(UseDeterm=True),\
                                         SizeBound= self.Sizebound)
                    

    def RandomizeUnMeas(self,NewSizeProb=None):

        #Do nothing if there are no size-classes
        if Meas.nSizeClass==1:return
        #Do nothing if there are no unmeasured animals.
        if UnMeas.nAnimals==0:return

        #If possible, generate probabilities from the measured animals
        ProbSizeClass=self.Meas.ResampSizeProb()
        if ProbSizeClass==None:ProbSizeClass=NewSizeProb
        self.UnMeas.SetSizeProb(ProbSizeClass)

    def GetUnMeasAbundance(self,AvgWeight=None,SizeProb=None):
        return(self.UnMeas.GetAbundance(AvgWeight=AvgWeight,SizeProb=SizeProb))

    def GetMeasAbundance(self,AE):
        '''quadrat.GetMeasAbundance(AE)
        AE(L)is the allometric equation relating Length to Weight)
        Returns a 2-d list.  Each row represents a size-class.
        First column gives the number of animals in the size-class.
        Second column gives biomass estimated for the size-class'''
        if self.Meas==None:
            result={}
            for sb in self.SizeBound:
                kname='USL'+str(sb)
                result[kname]={'Pop':0,'Bmass':0.}
            return(result)
        try:
            return(self.Meas.GetAbundance(AE))
        except:
            print('\nquadrat line 72,self.QuadNum,self.Meas',self.QuadNum,self.Meas)

       
 
    
if __name__ == "__main__":

    q1=quadrat(34,3.457)
    q2=quadrat(34,3.457,NumCount= 5)
    q3=quadrat(34,3.457,NumCount= 5,SizeMeas=[10.,15,16,17,20,23,26,27,35,55],SizeBound=[54,30])

    print ('\n')
    def AE(L):return(2*L)
    for x in q3.GetMeasAbundance(AE):
        print (x)

    
    print('done')
