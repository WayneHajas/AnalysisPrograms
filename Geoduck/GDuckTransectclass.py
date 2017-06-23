'''2015-11-03
If a random seed is specified, then it is used as the basis for generating (not randomly)
a seed for every iteration of transect sampling.'''  


#Class to represent a 'class' of transects that will be used to represent an entity.  Typically, all the transects in a site.

from numpy import iinfo,int16,average,array,average
MinInt=iinfo(int16).min
from numpy.random import shuffle
from wchchoice import choice
from numpy.random import seed
from copy import deepcopy
#from scipy.stats import randint

import os,sys
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from wchmquantile import mquantiles
from GDtransect import GDtransect
from transectclass import transectclass
from SumAbundance import SumAbundance,CalcDensity,CalcAvgWeight
from wchNorm import *
from InterpProd import WCHinterp
from BCA import BCA_CB,BCA, Naive_CB
from ADOSFdate import GetShowPlotNum,dumbSFplot,ADOmultiSFplot
from SiteSize import SiteSize,CopySiteSize
from ADOWeightVal import ADOWeightVal
from ArithSamples import Multiply



class GDuckTransectclass(transectclass):
    def __init__(self,ODB,ClassIndex,TranClassChar,AlloSource,QueryFunc,\
                 SizeBound=None,MinDepth=-999,MaxDepth=999,ShowFactor=None,OnlyOnBed=False,curseed=None):
        '''GDuckTransectclass(ODB,ClassIndex,TranClassChar,AlloSource,QueryFunc,SizeBound=None,MinDepth=-999,MaxDepth=999,ShowFactor=None)
        ODB (open database) is an instance of the ADO class
        ClassIndex is an index used within TranClassChar to specify the class of transects
        TranClassChar is an instance of MetaTransectClass
        AlloSource is an entity that generates allometric functions.  Ignored for geoducks
        QueryFunc is library of function to create species-specific functions and data
        SizeBound is a list of upper bounds on the size-classes'''
        self.ODB=ODB
        self.TranClassChar=TranClassChar
        self.ClassIndex=ClassIndex
        self.curseed=curseed
        seed(self.curseed)
        self.key=TranClassChar.TranClass[self.ClassIndex]['AllKey']
        self.key.sort()
        
        #super().__init__(ODB,key,AlloSource,QueryFunc,MinDepth=MinDepth,MaxDepth=MaxDepth)
        self.MinDepth,self.MaxDepth=MinDepth,MaxDepth
        try:
            self.transects=list(map(lambda k:\
                GDtransect(ODB,k[0],QueryFunc,SizeBound=SizeBound,MinDepth=self.MinDepth,MaxDepth=self.MaxDepth),\
                self.key))
            if OnlyOnBed:self.ReduceToOnBed()
        except:
            print('\ntransectclass 49')
            print (self.key[:5])
            print('dir(QueryFunc)', dir(QueryFunc))
            print('type(QueryFunc)', type(QueryFunc))
            self.transects=list(map(lambda k:\
                GDtransect(ODB,k[0],QueryFunc,SizeBound=SizeBound,MinDepth=self.MinDepth,MaxDepth=self.MaxDepth),\
                self.key))
            if OnlyOnBed:self.ReduceToOnBed()
        self.ntransect=len(self.transects)
        self.AlloSource=AlloSource
        self.AE=self.AlloSource.AvgWgtDetermAE()
        self.survey=self.TranClassChar.GetChar(ClassIndex,'SurveyTitle')
        self.year  =self.TranClassChar.GetChar(ClassIndex,'Year')
        self.site  =self.TranClassChar.GetChar(ClassIndex,'SurveySite')
        self.SiteSize=SiteSize(self.ODB,self.survey,self.year,self.site,ListTransects=self.transects)
        self.MeanWeight=ADOWeightVal(self.ODB,self.survey,self.year,self.site)
        
        #Something to get the show-factor data
        if ShowFactor!=None:
            self.SFData=dumbSFplot(SF=ShowFactor)
        else:
            self.GetSFData(ODB)#Try to get show-factor data
        self.offtransects=[]#So far no transects identified as off-bed
    def ReduceToOnBed(self):
        self.offtransects=list(filter(lambda t: not(t.OnBed),self.transects))
        self.transects=list(filter(lambda t: t.OnBed,self.transects))
        self.ntransect=len(self.transects)
        self.SiteSize=SiteSize(self.ODB,self.survey,self.year,self.site,ListTransects=self.transects)


    def GetTranAbundance(self,UseDeterm=False):
        '''Abundance in the surveyed transects'''
        byTran=list(map(lambda t:t.GetAbundance( sfp=self.SFData,CalcNumDuck=False,Randomize=False),self.transects))
        try:
            result=SumAbundance(byTran)
        except:
            print ('transectclass 67 byTran\n',byTran)
            result=SumAbundance(byTran)
        return(result)

    def GetSurveyedArea(self):
        result=sum(list(map(lambda t:t.GetQuadArea(),self.transects)))
        return(result)

    def GetAvgDensity(self,UseDeterm=False):
        '''This could be finessed a little more.
           Currently, the calculations reflect the surveyed-area of the transects.
           For the purpose of weighting, the recorded transectllengths (from the Headers file)
           could be incorporated'''
        if self.ntransect<=0:return(MinInt)
        TranDens=list(map(lambda t:t.MeanShowDens                                       ,self.transects))
        TranLeng=list(map(lambda t:t.TranLen                                            ,self.transects))
        sf=      list(map(lambda t:self.SFData.EstSF(date=t.SurveyDate,CalcNumDuck=True),self.transects))

        sumprd=sum(list(map(lambda a,b,sf:a*b/sf,TranDens,TranLeng,sf)))
        sumlen=sum(TranLeng)
        if sumlen<1:return(MinInt)
        
        result=sumprd/sumlen/10 #Convert from quadrats to square-metres
        return(result)
    def GetAvgAbundance(self,UseDeterm=True):return(self.GetAvgDensity(UseDeterm=UseDeterm))

    def GetSurveyedWidth(self):
        result=sum(list(map(lambda t:t.GetTranWidth(),self.transects)))
        return(result)

    def WriteTransectResults(self,OUTmdb,RemoveOffBed=True):
        TranCharKey=self.key
        for i in range(self.ntransect):
            CurTransect=self.transects[i]
            tranSF=self.SFData.EstSF(date=CurTransect.SurveyDate,CalcNumDuck=True)
            tranArea=CurTransect.GetQuadArea()
            MeanWeight=self.MeanWeight.EstMeanWeight
            MinDepth,MaxDepth=CurTransect.GetDepthRangeOccur()
            Density=average(CurTransect.c)/CurTransect.QueryFunc.QuadArea/tranSF 
            BiomassPerM=Density*MeanWeight
            Biomass=BiomassPerM*tranArea
            
            #Only use transects on bed
            if RemoveOffBed:
            	OmitReason=''
            	UseTransect=CurTransect.OnBed
            	if not(UseTransect):OmitReason='Not On Bed'
            
            #Use all transects
            else:
            	OmitReason=''
            	UseTransect=True

            DailyFixed=self.SFData.GetDailyFixed()
            OUTmdb.ADDTo_Results_Transect(\
                                OUTmdb.TransectKey.GetValue(IncrementFirst=True),\
                                #Originally SiteKey was off by one in the results.  So one is added here.
                                OUTmdb.SiteKey.GetValue()+1,\
                                CurTransect.TransectNumber,\
                                CurTransect.key,\
                                CurTransect.SurveyDate,\
                                MinDepth,MaxDepth,\
                                CurTransect.GetTranLength(),\
                                len(CurTransect.d),\
                                sum(CurTransect.c),\
                                Density,\
                                BiomassPerM/1000,\
                                tranSF,\
                                DailyFixed,\
                                not(CurTransect.OnBed),\
                                OmitReason,\
                                CurTransect.TransectComments,\
                                CurTransect.GIS_Code)
        '''Mean Density and mean biomass-density will be slightly than occured
               in the older (C++) version of GAP.  In the older version, mean density
               is based upon the surveyed quadrats.  In the current version, mean density
               is based upon surveyed quadrats plus quadrats where the number of shows
               is an interpolated quantity.  In the new version, quadrats at the tips
               of a transect have less influence than those in the middle'''

        #Repeat for transects already identified as off-bed
        n=len(self.offtransects)
        for i in range(n):
            CurTransect=self.offtransects[i]
            try:
              tranSF=self.SFData.EstSF(date=CurTransect.SurveyDate,CalcNumDuck=True)
            except:
              tranSF=self.SFData.EstSF(date=CurTransect.SurveyDate,CalcNumDuck=True)
            tranArea=CurTransect.GetQuadArea()
            MeanWeight=self.MeanWeight.EstMeanWeight
            MinDepth,MaxDepth=CurTransect.GetDepthRangeOccur()
            Density=average(CurTransect.c)/CurTransect.QueryFunc.QuadArea/tranSF 
            BiomassPerM=Density*MeanWeight
            Biomass=BiomassPerM*tranArea
            
            #Only use transects on bed
            if RemoveOffBed:
            	OmitReason=''
            	UseTransect=CurTransect.OnBed
            	if not(UseTransect):OmitReason='Not On Bed'
            
            #Use all transects
            else:
            	OmitReason=''
            	UseTransect=True

            DailyFixed=self.SFData.GetDailyFixed()
            OUTmdb.ADDTo_Results_Transect(\
                                OUTmdb.TransectKey.GetValue(IncrementFirst=True),\
                                #Originally SiteKey was off by one in the results.  So one is added here.
                                OUTmdb.SiteKey.GetValue()+1,\
                                CurTransect.TransectNumber,\
                                CurTransect.key,\
                                CurTransect.SurveyDate,\
                                MinDepth,MaxDepth,\
                                CurTransect.GetTranLength(),\
                                len(CurTransect.d),\
                                sum(CurTransect.c),\
                                Density,\
                                BiomassPerM/1000,\
                                tranSF,\
                                DailyFixed,\
                                not(CurTransect.OnBed),\
                                OmitReason,\
                                CurTransect.TransectComments,\
                                CurTransect.GIS_Code)


                             
    def GetSampAvgDensity(self,nboot=1000,iterseed=None):
        '''iterseed is ignored for multiple samples.'''

        if self.ntransect<=0:return(nboot*[MinInt])
        if nboot!=None:
            if self.curseed!=None:
                #set a new seed for every re-sample
                result1=[self.GetSampAvgDensity(nboot=None,iterseed=self.curseed+i)   for i in range(nboot)]
            else:
                #rely on random sampling as initiated in a previous call to numpy.random.seed                
                result1=[self.GetSampAvgDensity(nboot=None,iterseed=None)   for i in range(nboot)]
            return(result1)
 
        SampTran=SampleTransect(self,replace=True,curseed=iterseed)
        try:
            result=SampTran.GetAvgDensity(UseDeterm=False)
        except:
            print('\nGDuckTransectclass 138, SampTran.GetAvgDensity() ', SampTran.GetAvgDensity())
            result=SampTran.GetAvgDensity(self,UseDeterm=False) 
        return(result)

    
    def GetJackAvgDensity(self):
        result=[]
        for i in range(self.ntransect):
            CurJack=JackKnife(self,i)
            result+=[CurJack.GetAvgDensity(UseDeterm=True)]
        if result==[]:result=[self.GetAvgDensity(UseDeterm=True)]
        if result==[None]:result=[self.GetAvgDensity(UseDeterm=True)]
        return(result)
    

    def CBAvgDensity(self,nboot=1000,SampAvgDensity=None,JackAvgDensity=None,CB=[99,95,90,75,50]):
        if self.ntransect<=0:
            if isinstance(CB,(float,int)):return([MinInt,MinInt ])
            return(len(CB)*[[MinInt,MinInt]])
       
        if isinstance(CB,(float,int)):cb=CB/100.
        else:cb=list(map(lambda x:x/100.,CB))
        
        useAvgDensity=SampAvgDensity
        if useAvgDensity==None:useAvgDensity=sorted(self.GetSampAvgDensity(nboot=nboot))

        useJackAvgDensity=JackAvgDensity
        if useJackAvgDensity==None:useJackAvgDensity=sorted(self.GetJackAvgDensity())

        try:
            determEst=self.GetAvgDensity(UseDeterm=True)
        except:
            print('\nGDuckTransectclass 201 GetAvgDensity(UseDeterm=True) ', GetAvgDensity(UseDeterm=True))
            determEst=GetAvgDensity(UseDeterm=True)
        result=BCA_CB(determEst,useAvgDensity,useJackAvgDensity,cb)       
        return(result)
    
    def EquiProbDensity(self,n=100,SampAvgDensity=None,JackAvgDensity=None):
        
        if self.ntransect<=0:return(n*[MinInt])
        p =list(map(lambda i:(i+5)/float(n),range(n)))
        
        useAvgDensity=SampAvgDensity
        if useAvgDensity==None:useAvgDensity=sorted(self.GetSampAvgDensity(nboot=nboot))

        useJackAvgDensity=JackAvgDensity
        if useJackAvgDensity==None:useJackAvgDensity=sorted(self.GetJackAvgDensity())

        determEst=self.GetAvgDensity(UseDeterm=True)
        result=BCA(determEst,useAvgDensity,useJackAvgDensity,p)
        return(result)


    def GetSampBiomassDensity(self,nboot=1000,EquiProb=None,SampleWeight=None):
        '''results are sorted'''

        if self.ntransect<=0:return(nboot*[MinInt*nboot])
        nsqrt=int(sqrt(nboot))

        useEquiProb=EquiProb
        if useEquiProb==None:
           useEquiProb =self.EquiProbDensity(n=nsqrt) 

        #Weight values
        try:
         w=sorted(SampleWeight)
        except:
         w=self.MeanWeight.RandSource.EquiProbVal(nsqrt)
        
        result=Multiply(w,useEquiProb)
        return(result)


    def CBBiomassDensity(self,nboot=1000,SampAvgDensity=None,BiomassDensity=None,SampleWeight=None,CB=[99,95,90,75,50]):
        '''assume that SampAvgDensity/BiomassDensity are already BCA adjusted and ordered'''
        if self.ntransect<=0:
            if isinstance(CB,(float,int)):return([MinInt*1000,MinInt*1000 ])
            return(len(CB)*[[MinInt*1000,MinInt*1000]])
        nsqrt=int(sqrt(nboot))

        if isinstance(CB,(float,int)):cb=CB/100.
        else:cb=list(map(lambda x:x/100.,CB))

        useBiomassDensity=BiomassDensity
        if useBiomassDensity==None:
            useBiomassDensity=self.GetSampBiomassDensity(nboot=nboot,EquiProb=SampAvgDensity,SampleWeight=SampleWeight)
        result=Naive_CB(useBiomassDensity,CB=cb)       
        return(result)
         

    def GetSampPop(self,nboot=1000,EquiProbDensity=None,RunNumber=4,Area=None):
        '''Assume EquiProbDensity is an equiprobable-ordered set of values.  CBa operations have already occured'''

        #Average densities    
        if self.ntransect<=0:return(nboot*[MinInt])
        nsqrt=int(sqrt(nboot))
        pval=list(map(lambda i:(i+.5)/nsqrt,range(nsqrt)))


        #Site-Area values
        A=Area
        if A==None:
            if RunNumber==4: #Digitized area
                A=self.SiteSize.GetEquiProbArea(nsqrt,Digitized=True)
            elif RunNumber==2:#Area based on mean-transect-length and line-of-best-fit
                A=self.SiteSize.GetEquiProbArea(nsqrt,Digitized=False)
            else:
                print('GDuckTransectclass 249')
                print(' Do not know what to do with RunNumber=',RunNumber)
                print('Setting area to 1.0')
                A=1.0
        if isinstance(A,(int,float)):A=[A]
        try:
            if A.mu<0:return(nboot*[MinInt])
        except:
            dummy=True
        try:
            if A<0:return(nboot*[MinInt])
        except:
            dummy=True
        try:
            A=Area.GetEquiProbArea(nsqrt,Digitized=(RunNumber==4))
        except:
            dummy=True

        useEquiProbDensity=EquiProbDensity
        if useEquiProbDensity==None:
           useEquiProbDensity =self.EquiProbDensity(n=nsqrt)
        else:
            useEquiProbDensity.sort()

       #Population density
        result=Multiply(A,useEquiProbDensity)
        return(result)
    

    def CBPop(self,nboot=1000,SampAvgDensity=None,SampPop=None,\
              CB=[99,95,90,75,50],Area=None,RunNumber=4):
        if self.ntransect<=0:
            if isinstance(CB,(float,int)):return([MinInt,MinInt ])
            return(len(CB)*[[MinInt,MinInt]])
       
        if isinstance(CB,(float,int)):cb=CB/100.
        else:cb=list(map(lambda x:x/100.,CB))

        useSampPop=SampPop
        if useSampPop==None:
            useSampPop=self.GetSampPop(nboot=nboot,EquiProbDensity=SampAvgDensity,RunNumber=RunNumber,Area=Area)
        result=Naive_CB(useSampPop,CB=cb)
        return(result)
      
    def GetSampBiomass(self,nboot=1000,SampAvgDensity=None,SampPop=None,SampleWeight=None,RunNumber=4,Area=None):
        '''Assume SampAvgDensity/SampPop area equiprobable and BCa corrected'''
        if self.ntransect<=0:return(nboot*[MinInt*1000000])
        nsqrt=int(sqrt(nboot))

        pval=list(map(lambda i:(i+.5)/float(nsqrt),range(nsqrt)))

        useSampPop=SampPop
        if useSampPop==None:
           useSampPop=self.GetSampPop(nboot=nsqrt,EquiProbDensity=SampAvgDensity,RunNumber=RunNumber,Area=Area) 
        if max(useSampPop)<0:return(nboot*[MinInt*1000000])
        
        w=SampleWeight
        if w==None:
          w=self.MeanWeight.RandSource.EquiProbVal(nsqrt)
            
        #Biomass Estimates
        result=Multiply(useSampPop,w)
        return(result)

                      
    def CBBiomass(self,SampBiomass=None,nboot=1000,SampAvgDensity=None,SampPop=None,\
                  SampleWeight=None,RunNumber=4,CB=[99,95,90,75,50],Area=None):
        if self.ntransect<=0:
            if isinstance(CB,(float,int)):return([MinInt*1000000,MinInt*1000000 ])
            return(len(CB)*[[MinInt*1000000,MinInt*1000000]])
        if isinstance(CB,(list,ndarray)):
            if max(CB)>1:
                useCB=list(map(lambda t:t/100.,CB))
            else:
                useCB=CB
        else:  #CB is a single value
            if CB>1:
                useCB=[CB/100.]
            else:
                useCB=[CB]
        nsqrt=sqrt(nboot)       
        useSampBiomass=SampBiomass
        if useSampBiomass==None:
           useSampBiomass =self.GetSampBiomass(nboot=nboot,SampAvgDensity=SampAvgDensity,SampPop=SampPop,\
                                               SampleWeight=SampleWeight,RunNumber=RunNumber,Area=Area)
        determEst=self.GetAvgAbundance()*self.SiteSize.GetEstArea(Digitized=(RunNumber==4))*self.MeanWeight.EstMeanWeight
        result=Naive_CB(useSampBiomass,useCB)
                
        return(result)


    def WriteSiteCB(self,OUTmdb,nboot=1000,CB=[99,95,90,75,50],\
                    RunNumber=4,SampPopDens=None,Area=None,SampleWeight=None,MakeBCaCorrection=True):
        if isinstance(CB,(float,int)):cb=CB/100.
        else:cb=list(map(lambda x:x/100.,CB))

        #Sample of population densities
        SampAvgPopDens=SampPopDens
        if SampAvgPopDens==None: SampAvgPopDens=self.GetSampAvgDensity(nboot=nboot)

        #Sample of average-weight values
        SW=SampleWeight
        if SW==None:SW=self.MeanWeight.RandSource.EquiProbVal(nboot)

        #Site-Area values for sampling
        A=Area
        if (A==None):
            if RunNumber==4: #Digitized area
                try:
                  A=self.SiteSize.DigitizedArea.EquiProbVal(nboot,LowBound=self.SiteSize.TranArea)
                except:
                  print('\nGDuckTransectclass 398 ')
                  print('self.SiteSize.GetDigitizedArea()  ',self.SiteSize.GetDigitizedArea()   )
                  A=self.SiteSize.GetDigitizedArea().mu
            elif RunNumber==2:#Area based on mean-transect-length and line-of-best-fit
                A=self.SiteSize.LOBFarea.EquiProbVal(nboot,LowBound=self.SiteSize.TranArea)

            else:
                print('GDuckTransectclass 249')
                print(' Do not know what to do with RunNumber=',RunNumber)
                print('Setting area to 1.0')
                A=1.0

        determAvgPopDens=   self.GetAvgDensity()
        JackAvgPopDens=  self.GetJackAvgDensity()


        SampAvgPopDens2=SampAvgPopDens
        if MakeBCaCorrection:
            #Attempt a BCA correction on the density sample.
            p=list(map(lambda i: (i+.5)/float(nboot),range(nboot)))
            SampAvgPopDens2=BCA(determAvgPopDens,   SampAvgPopDens, JackAvgPopDens,p=p)
        
        SampPop=self.GetSampPop(nboot=nboot,EquiProbDensity=SampAvgPopDens2,RunNumber=RunNumber,Area=A)
        SampBioDensity=self.GetSampBiomassDensity(nboot=nboot,EquiProb=SampAvgPopDens2,SampleWeight=SW)
        SampBiomass=self.GetSampBiomass(nboot=nboot,SampAvgDensity=SampAvgPopDens2,RunNumber=RunNumber,Area=A)    
    

        CBAvgPopDens=Naive_CB( SampAvgPopDens2,    CB) #BCA correction already made
        CBBioDens=self.CBBiomassDensity(nboot=nboot,BiomassDensity=SampBioDensity,CB=CB)
        
        CBPop       =self.CBPop(nboot=nboot,SampPop=SampPop,CB=CB,Area=A,RunNumber=RunNumber)
        CBBiomass=self.CBBiomass(SampBiomass=SampBiomass,nboot=nboot,RunNumber=RunNumber,CB=CB,Area=A)

        for i in range(len(CB)):
            OUTmdb.ADDTo_SiteConfBound(CB[i],\
                                      CBAvgPopDens[i][0],CBAvgPopDens[i][1],\
                                      CBPop[i][0],CBPop[i][1],\
                                      CBBioDens[i][0],CBBioDens[i][1],\
                                      CBBiomass[i][0]/1000,CBBiomass[i][1]/1000)
        result={'Area':A,'SampPop':SampPop,'SampBiomass':SampBiomass,'SampleWeight':SW,\
                'SampAvgPopDens':SampAvgPopDens2,'SampBioDensity':SampBioDensity}
            
        return(result)

    def GetSFData(self,ODB):
        self.SFData=ADOmultiSFplot(self.ODB,self.survey,self.year,SurveySite=self.site)
        return

    def GetAvgWeight(self):
        return (self.MeanWeight.EstMeanWeight)

    def GetRandomArea(self,n=1000,RunNumber=4):
        result=self.SiteSize(n=n,RunNumber=RunNumber)
        return(result)
                

class SampleTransect(GDuckTransectclass):
    def __init__(self,tc,ntransect=None,replace=True,curseed=None):
        '''SampleTransect(tc,SampleSize=None,replace=True)
        tc is an instance of transectclass
        SampleSize is the number of transects in the resample - will default to the same number as in tc
        replace indicates if sampling is done with replacement'''
        
        self.SFData=tc.SFData
        self.SFData.Randomize(deterministic=False)
        
        self.ntransect= len(tc.transects)
        #For some reason, numpy.choice wasn't very random when it sampled transects.
        #I am going to sample indeces and then bring in the transects accordingly.
        index=choice(self.ntransect,self.ntransect,replace=True,curseed=curseed)
        self.transects=[tc.transects[i] for i in index ]        
        

        self.AlloSource=tc.AlloSource
        self.AE=self.AlloSource.AvgWgtRndAE()
        #self.RandomizeSizeProb()
        self.SiteSize=CopySiteSize(tc.SiteSize,self.transects)

class JackKnife(GDuckTransectclass):
    def __init__(self,tc,i):

        
        self.SFData=tc.SFData
        self.SFData.Randomize(deterministic=True)

        #Get a deep copy of the list of transects
        self.transects=list(map(lambda t:t,tc.transects))
        dummy=self.transects.pop(i)
        self.ntransect= len(self.transects)
        self.AlloSource=tc.AlloSource
        self.AE=self.AlloSource.AvgWgtRndAE()
        if self.ntransect==0:
            self.MeanAbund=None
        else:
            self.MeanAbund=self.GetAvgAbundance(UseDeterm=True)
        self.SiteSize=CopySiteSize(tc.SiteSize,self.transects)
            


if __name__ == "__main__":

    from numpy import inf
    import geoduckQueryFunc as QueryFunc
    from MetaTransectClass import MetaTransectClass
    databasepath='t:\Geoduck_Bio.mdb'
    from ADO import adoBaseClass as OpenDB
    ODB=OpenDB(databasepath)
    AlloSource=QueryFunc.AlloEqn()  
    key=list(range(14341,14346))
    ClassIndex=4
    
    TranClassChar=MetaTransectClass(ODB,\
                                             [["Flamingo and Louscoone Inlets",2013]])
    #test=GDuckTransectclass(ODB,key,IndexKeyUse,TranClassChar,AlloSource,QueryFunc,SizeBound=None,MinDepth=-999,MaxDepth=999)
    test=GDuckTransectclass(ODB,ClassIndex,TranClassChar,AlloSource,QueryFunc,SizeBound=None,MinDepth=-999,MaxDepth=999,ShowFactor=None)
    A=test.SiteSize.DigitizedArea.EquiProbVal(1000,LowBound=test.SiteSize.TranArea)
    
    print(mquantiles(A))

    print ('\ndone GDuckTransect class')
