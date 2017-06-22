#Class to represent a 'class' of transects that will be used to represent an entity.  Typically, all the transects in a site.

from numpy import iinfo,int16,average,array
MinInt=iinfo(int16).min
from numpy.random import choice

import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from mquantiles import mquantiles
from transectclass import transectclass
from SumAbundance import SumAbundance,CalcDensity,CalcAvgWeight
from wchNorm import *
from InterpProd import WCHinterp
from BCA import BCA_CB
import pdb


class CukeTransectclass(transectclass):
    def __init__(self,ODB,ClassIndex,TranClassChar,AlloSource,QueryFunc,SizeBound=None,MinDepth=-999,MaxDepth=999):
        self.TranClassChar=TranClassChar
        self.ClassIndex=ClassIndex
        try:
            key=list(map(lambda k:k[0],  self.TranClassChar.SI.TransectNumber[self.ClassIndex]))
        except:
            print('\nCukeTransectClass 24 ')
            print('self.TranClassChar.SI.TransectNumber[self.ClassIndex]')
                
        self.IndexTranUse=list(filter(lambda i: self.TranClassChar.SI.TransectNumber[self.ClassIndex][i][2] ==0     ,range(len(self.TranClassChar.SI.TransectNumber[self.ClassIndex]))))                 
        super().__init__(ODB,key,AlloSource,QueryFunc,MinDepth=MinDepth,MaxDepth=MaxDepth) 
        '''CukeTransectclass(ODB,key,QueryFunc,SizeBound=None)
        ODB (open database) is an instance of the ADO class
        key is a list of values from the headers table
        AlloSource is an entity that generates allometric functions
        QueryFunc is library of function to create species-specific functions and data
        SizeBound is a list of upper bounds on the size-classes'''
        
      

  
    def GetAbundance(self,AverageWeight=None,UseDeterm=False):
        if (AverageWeight==None):
            if UseDeterm:
                self.AE=self.AlloSource.AvgWgtDetermAE()
            else:
                self.AE=self.AlloSource.AvgWgtRndAE()
            AverageWeight=self.GetAvgWeight()
        byTran=list(map(lambda t:self.transects[t].GetAbundance(AverageWeight=AverageWeight,UseDeterm=UseDeterm),self.IndexTranUse))
        try:
            result=SumAbundance(byTran)
        except:
            print ('transectclass 48 byTran\n',byTran)
            result=SumAbundance(byTran)
        return(result)

    def GetSurveyedArea(self):
        #result=sum(list(map(lambda t:t.GetQuadArea(),self.transects)))
        result=sum(list(map(lambda t:self.transects[t].GetQuadArea(),self.IndexTranUse)))
        return(result)

    def GetSurveyedWidth(self):
        result=sum(list(map(lambda t:self.transects[t].GetTranWidth(),self.IndexTranUse)))
        return(result)

    def WriteTransectResults(self,OUTmdb,FMT):
        TranCharKey=OUTmdb.GetTranCharKey(FMT['Project'],FMT['Site'],FMT['Year'],FMT['StatArea'],FMT['SubArea'])
        for i in range(self.ntransect):
            CurTransect=self.transects[i]
            try:
                Bmass=CurTransect.GetAbundance()['USLinf']['Pop']*self.TranClassChar.SI.result[self.ClassIndex]['MeanWeight']
            except:
                Bmass=MinInt
            try:
                PopDens=CurTransect.GetAbundance()['USLinf']['Pop']/CurTransect.GetTranLength()/CurTransect.GetTranWidth()
            except:
                PopDens=MinInt
            OUTmdb.ADDTo_Transect(TranCharKey,\
                                self.TranClassChar.SI.TransectNumber[self.ClassIndex][i][1],\
                                self.TranClassChar.SI.TransectNumber[self.ClassIndex][i][0],\
                                self.TranClassChar.SI.TransectNumber[self.ClassIndex][i][4],\
                                self.TranClassChar.SI.TransectNumber[self.ClassIndex][i][5],\
                                self.TranClassChar.SI.TransectNumber[self.ClassIndex][i][6],\
                                self.MinDepth,self.MaxDepth,\
                                CurTransect.GetTranLength(),\
                                CurTransect.GetNumQuad(),\
                                CurTransect.GetAbundance()['USLinf']['Pop'],\
                                PopDens,\
                                Bmass,\
                                self.TranClassChar.SI.TransectNumber[self.ClassIndex][i][2],\
                                self.TranClassChar.SI.TransectNumber[self.ClassIndex][i][3],\
                                self.TranClassChar.SI.TransectNumber[self.ClassIndex][i][7])

    def WriteSiteResults(self,OUTmdb,FMT,MeanWtSource):
        ResultKey=OUTmdb.AnalysisKey.GetValue()
        SiteKey=OUTmdb.GetTranCharKey(FMT['Project'],FMT['Site'],FMT['Year'],FMT['StatArea'],FMT['SubArea'])
        SubSite=SampleTransect(self,replace=False)
        TranLen=list(map(lambda t: t.GetTranLength(),SubSite.transects))
        MeanTranLength=average(TranLen)
        CoastLength=self.TranClassChar.SI.result[self.ClassIndex]['CoastLengthM']
        CoastLengthSE=self.TranClassChar.SI.result[self.ClassIndex]['StErrCLM']
        MeanWt=self.TranClassChar.SI.result[self.ClassIndex]['MeanWeight']
        MeanWtSE=self.TranClassChar.SI.result[self.ClassIndex]['StErrWeight']
        #MeanWtSource
        NumberTransects=len(TranLen)
        Density=self.GetAbundance()['USLinf']['Pop']/self.GetSurveyedWidth()
        Population=Density*CoastLength
        BiomassPerM=Density*MeanWt
        SiteBioMass=BiomassPerM*CoastLength

        OUTmdb.ADDTo_EstDens(OUTmdb.TranCharKey.GetValue(),FMT,
                             MeanTranLength,CoastLength,CoastLengthSE,MeanWt,MeanWtSE,MeanWtSource,
                             NumberTransects,Density,Population,\
                            BiomassPerM,SiteBioMass)
        results={'PopDens':Density,'BmaDens':BiomassPerM,'EstPop':Population,'EstBma':SiteBioMass,'CL':CoastLength}
        return(results)
                             
    def SampAvgDensity(self,nboot=1000):
        if nboot!=None:
            result=list(map(lambda dummy:self.SampAvgDensity(nboot=None),range(nboot)))
            return(result)
        #pdb.set_trace()
        SampTran=SampleTransect(self,replace=True)
        result=SampTran.GetAvgAbundance()['linear']['USLinf']['Pop']
        return(result)

    def GetJackAbund(self):
        self.RandomizeSizeProb(UseDeterm=True)
        result=[]
        for i in range(len(self.IndexTranUse)):
            CurJack=JackKnife(self,i)
            result+=[CurJack.MeanAbund]
        if result==[]:result=[self.DetermMeanAbund()]
        if result==[None]:result=[self.DetermMeanAbund()]
        return(result)
    


    def GetJackAvgDensity(self):
        #pdb.set_trace()
        result=list(map(lambda t:t['linear']['USLinf']['Pop'], self.GetJackAbund()))
        return(result)

    def CBAvgDensity(self,nboot=1000,AvgDensity=None,JackAvgDensity=None,CB=[99,95,90,75,50]):

        if isinstance(CB,(float,int)):cb=CB/100.
        else:cb=list(map(lambda x:x/100.,CB))
        
        useAvgDensity=AvgDensity
        if useAvgDensity==None:useAvgDensity=sorted(self.SampAvgDensity(nboot=nboot))

        useJackAvgDensity=JackAvgDensity
        if useJackAvgDensity==None:useJackAvgDensity=sorted(self.GetJackAvgDensity())

        determEst=self.DetermMeanAbund()['linear']['USLinf']['Pop']
        result=BCA_CB(determEst,useAvgDensity,useJackAvgDensity,cb)
       
        return(result)

    def SampBiomassDensity(self,nboot=1000,AvgDensity=None):
        MeanWeight=self.TranClassChar.SI.result[self.ClassIndex]['MeanWeight']
        StErrWeight=self.TranClassChar.SI.result[self.ClassIndex]['StErrWeight']
        pval=list(map(lambda i:(i+.5)/float(nboot),range(nboot)))

        #Weight values
        w=array(list(map(lambda i: InvNorm( i),pval)))
        w*=StErrWeight
        w+=MeanWeight

        #pdb.set_trace()
        #Populations
        if AvgDensity!=None:
            p=AvgDensity
        else:
            p=array(self.SampAvgDensity(nboot=nboot))

        bd=w.reshape(len(w),1)*p
        bd=bd.reshape(1,len(w)*len(p))[0]    
        result=mquantiles(bd,pval)
        return(result)

    def GetJackBiomassDensity(self,JackAvgDensity=None):
        useJackAvgDensity=JackAvgDensity
        if useJackAvgDensity==None:useJackAvgDensity=sorted(self.GetJackAvgDensity())
        MeanWeight=self.TranClassChar.SI.result[self.ClassIndex]['MeanWeight']
        result=list(map(lambda x:x*MeanWeight, useJackAvgDensity))
        return(result)

    def CBBiomassDensity(self,nboot=1000,AvgDensity=None,BiomassDensity=None,JackBiomassDensity=None,JackAvgDensity=None,CB=[99,95,90,75,50]):

        if isinstance(CB,(float,int)):cb=CB/100.
        else:cb=list(map(lambda x:x/100.,CB))

        useBiomassDensity=BiomassDensity
        if useBiomassDensity==None:useBiomassDensity=sorted(self.SampBiomassDensity(nboot=nboot,AvgDensity=AvgDensity))

        useJackBiomassDensity=JackBiomassDensity
        if useJackBiomassDensity==None:useJackBiomassDensity=self.GetJackBiomassDensity(JackAvgDensity=JackAvgDensity)

        MeanWeight=self.TranClassChar.SI.result[self.ClassIndex]['MeanWeight']
        determEst=MeanWeight*self.DetermMeanAbund()['linear']['USLinf']['Pop']
        result=BCA_CB(determEst,useBiomassDensity,useJackBiomassDensity,cb)
       
        return(result)
         

    def SampPop(self,nboot=1000,AvgDensity=None):
        CoastLengthM=self.TranClassChar.SI.result[self.ClassIndex]['CoastLengthM']
        StErrCLM=self.TranClassChar.SI.result[self.ClassIndex]['StErrCLM']
        pval=list(map(lambda i:(i+.5)/float(nboot),range(nboot)))

        #Coast-Length values
        w=array(list(map(lambda i: InvNorm( i),pval)))
        w*=StErrCLM
        w+=CoastLengthM

        #Populations
        if AvgDensity!=None:
            p=AvgDensity
        else:
            p=array(self.SampAvgDensity(nboot=nboot))

        bd=w.reshape(len(w),1)*p
        bd=bd.reshape(1,len(w)*len(p))[0]
        result=mquantiles(bd,pval)
        return(result)
    
    def GetJackPop(self,JackAvgDensity=None):
        useJackAvgDensity=JackAvgDensity
        if useJackAvgDensity==None:useJackAvgDensity=sorted(self.GetJackAvgDensity())
        CoastLengthM=self.TranClassChar.SI.result[self.ClassIndex]['CoastLengthM']
        result=list(map(lambda x:x*CoastLengthM, useJackAvgDensity))
        return(result)

    def CBPop(self,nboot=1000,PopDensity=None,AvgDensity=None,JackPop=None,JackAvgDensity=None,CB=[99,95,90,75,50]):
        if isinstance(CB,(float,int)):cb=CB/100.
        else:cb=list(map(lambda x:x/100.,CB))

        usePopDensity=PopDensity
        if usePopDensity==None:usePopDensity=sorted(self.SampPop(nboot=nboot,AvgDensity=AvgDensity))

        useJackPop=JackPop
        if useJackPop==None:useJackPop=self.GetJackPop(JackAvgDensity=JackAvgDensity)
        
        CoastLengthM=self.TranClassChar.SI.result[self.ClassIndex]['CoastLengthM']
        determEst=CoastLengthM*self.DetermMeanAbund()['linear']['USLinf']['Pop']
        result=BCA_CB(determEst,usePopDensity,useJackPop,cb)
        return(result)
      
    def SampBiomass(self,nboot=1000,BiomassDensity=None,AvgDensity=None):
        CoastLengthM=self.TranClassChar.SI.result[self.ClassIndex]['CoastLengthM']
        StErrCLM=self.TranClassChar.SI.result[self.ClassIndex]['StErrCLM']
        pval=list(map(lambda i:(i+.5)/float(nboot),range(nboot)))

        #Coast-length values
        cl=array(list(map(lambda i: InvNorm( i),pval)))
        cl*=StErrCLM
        cl+=CoastLengthM

        #Biomass density
        if BiomassDensity!=None:
            bmd=BiomassDensity
        else:
            bmd=array(self.SampBiomassDensity(nboot=nboot,AvgDensity=AvgDensity))

        bd=cl.reshape(len(cl),1)*bmd
        bd=bd.reshape(1,nboot*nboot)[0]
        bd.sort()
        oldx=list(map(lambda i: (i+.5)/nboot/nboot,range(nboot*nboot)))
        result=WCHinterp(oldx,bd,pval)
        return(result)

    def GetJackBiomass(self,JackAvgDensity=None):
        useJackAvgDensity=JackAvgDensity
        if useJackAvgDensity==None:useJackAvgDensity=sorted(self.GetJackAvgDensity())
        MeanWeight=self.TranClassChar.SI.result[self.ClassIndex]['MeanWeight']
        CoastLengthM=self.TranClassChar.SI.result[self.ClassIndex]['CoastLengthM']
        result=list(map(lambda x:x*MeanWeight*CoastLengthM, useJackAvgDensity))
        return(result)

       
    def CBBiomass(self,nboot=1000,AvgDensity=None,BiomassDensity=None,Biomass=None,\
                  JackBiomass=None,JackAvgDensity=None,CB=[99,95,90,75,50]):

        if isinstance(CB,(float,int)):cb=CB/100.
        else:cb=list(map(lambda x:x/100.,CB))

        useBiomass=Biomass
        if useBiomass==None:useBiomass=sorted(self.SampBiomass(nboot=nboot,BiomassDensity=BiomassDensity,AvgDensity=AvgDensity))

        useJackBiomass=JackBiomass
        if useJackBiomass==None:useJackBiomass=self.GetJackBiomass(JackAvgDensity=JackAvgDensity)

        MeanWeight=self.TranClassChar.SI.result[self.ClassIndex]['MeanWeight']
        CoastLengthM=self.TranClassChar.SI.result[self.ClassIndex]['CoastLengthM']
        determEst=MeanWeight*CoastLengthM*self.DetermMeanAbund()['linear']['USLinf']['Pop']
        result=BCA_CB(determEst,useBiomass,useJackBiomass,cb)
        return(result)

    def WriteSiteCB(self,OUTmdb,FMT,nboot=1000,CB=[99,95,90,75,50]):
        TranCharKey=OUTmdb.GetTranCharKey(FMT['Project'],FMT['Site'],FMT['Year'],FMT['StatArea'],FMT['SubArea'])
        
        SampPopDensity=self.SampAvgDensity(nboot=nboot)
        SampBMDensity=self.SampBiomassDensity(nboot=nboot,AvgDensity=SampPopDensity)
        SampPop=self.SampPop(nboot=nboot,AvgDensity=SampPopDensity)
        SampBM=self.SampBiomass(nboot=nboot,BiomassDensity=SampBMDensity,AvgDensity=SampPopDensity)

        JackPopDensity=self.GetJackAvgDensity()
        JackBiomassDensity=self.GetJackBiomassDensity(JackAvgDensity=JackPopDensity)
        JackPop=self.GetJackPop(JackAvgDensity=JackPopDensity)
        JackBM=self.GetJackBiomass(JackAvgDensity=JackPopDensity)

        CBPopDensity=self.CBAvgDensity(nboot=nboot,AvgDensity=SampPopDensity,JackAvgDensity=JackPopDensity,CB=CB)
        CBBMDensity=self.CBBiomassDensity(nboot=nboot,BiomassDensity=SampBMDensity,JackBiomassDensity=JackBiomassDensity,CB=CB)
        CBPop=self.CBPop(nboot=nboot,PopDensity=SampPop,JackPop=JackPop,CB=CB)
        CBBM=self.CBBiomass(nboot=nboot,Biomass=SampBM,JackBiomass=JackBM,CB=CB)
        for i in range(len(CB)):
            OUTmdb.ADDTo_ConfInterval(TranCharKey,CB[i],\
                                      CBPopDensity[i][0],CBPopDensity[i][1],\
                                      CBBMDensity[i][0],CBBMDensity[i][1],\
                                      CBPop[i][0],CBPop[i][1],\
                                      CBBM[i][0],CBBM[i][1])
        result={'SampPopDensity':SampPopDensity,\
                'CL':[self.TranClassChar.SI.result[self.ClassIndex]['CoastLengthM'],self.TranClassChar.SI.result[self.ClassIndex]['StErrCLM']],\
                'MW':[self.TranClassChar.SI.result[self.ClassIndex]['MeanWeight'],self.TranClassChar.SI.result[self.ClassIndex]['StErrWeight']]}
            
        return(result)
       
                

class SampleTransect(CukeTransectclass):
    def __init__(self,tc,ntransect=None,replace=True):
        '''SampleTransect(tc,SampleSize=None,replace=True)
        tc is an instance of transectclass
        SampleSize is the number of transects in the resample - will default to the same number as in tc
        replace indicates if sampling is done with replacement'''
        #pdb.set_trace()
        self.ntransect= ntransect
        if self.ntransect==None:self.ntransect=len(tc.IndexTranUse)

        #For some reason, numpy.choice wasn't very random when it sampled transects.
        #I am going to sample indeces and then bring in the transects accordingly.

        self.transects=list(map(lambda t: tc.transects[t]   ,tc.IndexTranUse))
        if replace:
            index=choice( tc.IndexTranUse,self.ntransect,replace=replace)
            self.transects=list(map(lambda t: tc.transects[t],index))

        self.AlloSource=tc.AlloSource
        self.AE=self.AlloSource.AvgWgtRndAE()
        self.RandomizeSizeProb()
        self.IndexTranUse=list(range(self.ntransect))

class JackKnife(CukeTransectclass):
    def __init__(self,tc,i):

        #Get a deep copy of the list of transects
        self.transects=list(map(lambda t:tc.transects[t],tc.IndexTranUse))
        dummy=self.transects.pop(i)
        self.ntransect= len(self.transects)
        self.IndexTranUse=list(range(self.ntransect))
        self.AlloSource=tc.AlloSource
        self.AE=self.AlloSource.AvgWgtRndAE()
        if self.ntransect==0:
            self.MeanAbund=None
        else:
            self.MeanAbund=self.GetAvgAbundance(UseDeterm=True)


if __name__ == "__main__":

    from numpy import inf
    import GSUQueryFunc as QueryFunc
    databasepath='d:\scratch\GreenUrchin_NoLink00.mdb'
    ODB=OpenDB(databasepath)

    key=[9009, 9012]
    key=[11725, 11726, 11727, 11728, 11729]#, 11730, 11731, 11732, 11733, 11734, 11735, 11736, 11737, 11738, 11739]
    key=[10895]
    AlloSource=QueryFunc.AlloEqn()
    p=[.025,.975]

    tc=transectclass(ODB,key,AlloSource,QueryFunc,SizeBound=[54])
    print  ('\ntc.GetAbundance(UseDeterm=True)',tc.GetAbundance(UseDeterm=True))
    print  ('\ntc.GetAvgWeight()',tc.GetAvgWeight())
    print  ('\ntc.DetermMeanAbund()',tc.DetermMeanAbund())
    print  ('\ntc.GetAbundance(UseDeterm=True)',tc.GetAbundance(UseDeterm=True))
    print  ('\ntc.GetAvgAbundance(UseDeterm=True)',tc.GetAvgAbundance(UseDeterm=True))
    print  ('\ntc.GetPctCB([95],nboot=100)', tc.GetPctCB([95],nboot=5))
    print ('\ndone transect class')
