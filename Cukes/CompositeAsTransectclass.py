'''
2015-11-24
Created to gracefully handle instances where analysis is done on a single transect-class.
The overall-stats will match the stats for the transect-class
'''

from CukeTransectclass import CukeTransectclass


import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))



class CompositeAsTransectclass(CukeTransectclass):
    def __init__(self,oriTranClass,SampAvgDensity):
        self.TranClassChar=oriTranClass.TranClassChar
        self.ClassIndex=oriTranClass.ClassIndex
                
        self.IndexTranUse=oriTranClass.IndexTranUse
        self.MinDepth,self.MaxDepth=oriTranClass.MinDepth,oriTranClass.MaxDepth
        self.transects=oriTranClass.transects
        self.ntransect=oriTranClass.ntransect
        self.AlloSource=oriTranClass.AlloSource
        self.AE=oriTranClass.AE   
        self.SampAvgDensity=SampAvgDensity
        
 
    def WriteResults(self,OUTmdb,FMT,MeanWtSource):
        CoastLength=self.TranClassChar.SI.result[self.ClassIndex]['CoastLengthM']
        MeanWt=self.TranClassChar.SI.result[self.ClassIndex]['MeanWeight']

        Density=self.GetAbundance()['USLinf']['Pop']/self.GetSurveyedWidth()
        Population=Density*CoastLength
        BiomassPerM=Density*MeanWt
        SiteBioMass=BiomassPerM*CoastLength
 
        OUTmdb.ADDTo_Results_Overall(Density,Population,BiomassPerM,SiteBioMass) 
        return()
                             
  

    def WriteCB(self,OUTmdb,FMT,CB=[99,95,90,75,50]):
        nboot=len(self.SampAvgDensity)
        SampPopDensity=self.SampAvgDensity
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
            OUTmdb.ADDTo_Results_OverallConfBounds(CB[i],\
                           CBPopDensity[i][0],   CBPopDensity[i][1],  \
                           CBPop[i][0],          CBPop[i][1],  \
                           CBBMDensity[i][0],    CBBMDensity[i][1],  \
                           CBBM[i][0],           CBBM[i][1])


      
        return()
       
                




if __name__ == "__main__":

    from numpy import inf
    
    print ('\ndone CompositeAsTransectclass class')
