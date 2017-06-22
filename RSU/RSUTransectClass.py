import sys,os

from numpy import iinfo,int16
MinInt=iinfo(int16).min


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from transectclass import transectclass as GenericTransectClass

class transectclass(GenericTransectClass):
    '''Identical to the generic TransectClass except that I am adding a function to write transect results'''
    def __init__(self,ODB,key,AlloSource,QueryFunc,SizeBound=None,MinDepth=-999,MaxDepth=999):
        super().__init__(ODB,key,AlloSource,QueryFunc,SizeBound=SizeBound,MinDepth=MinDepth,MaxDepth=MaxDepth) 


    def WriteTransectResults(self,OUTmdb,tck):
        
        self.RandomizeSizeProb(UseDeterm=True)#Set Deterministic
        self.AE=self.AlloSource.AvgWgtDetermAE()#Set Average weights.
    
        
        for i in range(self.ntransect):
            CurTransect=self.transects[i]
            TranAbund=CurTransect.GetAbundance(AverageWeight=self.GetAvgWeight(),UseDeterm=True)     
         
            #size-names            
            SBname=list(map(lambda SB: 'USL'+str(SB),CurTransect.SizeBound  ))
            nsize=len(SBname)  
        
            #size-keys
            sk=OUTmdb.GetSizeRangeKey(CurTransect.SizeBound)
 
            
            for s in range(nsize):
                
                try:
                    Bmass=TranAbund[SBname[s]]['Bmass']
                except:
                    Bmass=MinInt
                try:
                    Population=TranAbund[SBname[s]]['Pop']
                except:
                    PopDens=MinInt    
                
                
                #def ADDTo_Transect(TranCharKey,SizeRangeKey,HeaderKey,  TranLength,NumQuadrats,Population,Biomass):
                OUTmdb.ADDTo_Transect(tck,sk[s],CurTransect.key,\
                                    CurTransect.GetTranLength(),\
                                    Population,\
                                    Bmass)
