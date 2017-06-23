import sys
from numpy import average,std,sqrt,array,iinfo,int16,pi
MinInt=iinfo(int16).min
from numpy.random import choice
from norm import norm
from numpy.random import shuffle

class SiteSize():
    def __init__(self,ODB,survey,year,site,ListTransects=None):
        
        '''SiteSize(ODB,survey,year,site,ListTransects=None)
        ODB (open database) is an instance of the ADO class
        survey corresponds to field in Headers table
        year corresponds to field in Headers table
        site corresponds to field in Headers table
        ListTransects is a list of transect (or GDtransect) objects.

        One estimate of SiteSize is based upon bed-areas and the other is
        based on estimated-mean transect length and the length of the line-of-best-fit'''

        self.ODB=ODB
        self.survey=survey
        self.year=year
        self.site=site
        self.ListTransects=ListTransects
        self.CalcDigitizedArea()
        self.AreaFromLOBF()
        
        #Area of surveyed transects in the depth-range.  Includes unsurveyed transects.
        self.TranArea=sum(list(map(lambda t: t.GetQuadArea(),self.ListTransects)))

    def ReviseTranLen(self,ListTransects=None):
        self.ListTransects=ListTransects
        self.GetMeanTranLen()
        
    def FromSiteAnalysisData(self):
        '''Try to calculate site-area from data in the AnalysisData table'''
        query ='SELECT DISTINCT SiteAnalysisData.DigitizedArea '
        query+='FROM SiteAnalysisData '
        query+='WHERE (((SiteAnalysisData.SurveyTitle)="'
        query+=self.survey
        query+='") AND ((SiteAnalysisData.Year)= '
        query+=str(self.year)
        query+=') AND ((SiteAnalysisData.SurveySite)= '
        query+=str(self.site)
        query+='));'

        try:
          self.ODB.execute(query)
          area=self.ODB.GetVariable('DigitizedArea')[0]*10000#convert hectares to square metres
          self.DigitizedArea=norm(area,area/10.)
          if area<0:
              self.DigitizedArea=norm(MinInt*10000,0.)
        except:
          self.DigitizedArea=norm(MinInt*10000,0.)
    def FromSiteSummary(self):
        '''Try to calculate site-area from data in the SiteSummary table'''
        query ='SELECT DISTINCT SiteSummary.Survey '
        query+='FROM SiteSummary '
        query+='WHERE (((SiteSummary.SurveyTitle)="'
        query+=self.survey
        query+='") AND ((SiteSummary.Year)= '
        query+=str(self.year)
        query+=') AND ((SiteSummary.SurveySite)= '
        query+=str(self.site)
        query+='));'

        try:
          self.ODB.execute(query)
          area=ODB.GetVariable('SurveySiteArea')
          self.DigitizedArea=norm(sum(area),0.)
        except:
          self.DigitizedArea=None

    def CalcDigitizedArea(self):
        self.FromSiteAnalysisData()
        if self.DigitizedArea!=None:
            return
        self.FromSiteSummary()
        if self.DigitizedArea!=None:
            return
        self.DigitizedArea=norm(MinInt,0.)
        return
    def GetDigitizedArea(self):
        return(self.DigitizedArea)

    def GetLOBF(self):
        query ='SELECT DISTINCT SiteAnalysisData.LOBF '
        query+='FROM SiteAnalysisData '
        query+='WHERE (((SiteAnalysisData.SurveyTitle)="'
        query+=self.survey
        query+='") AND ((SiteAnalysisData.Year)= '
        query+=str(self.year)
        query+=') AND ((SiteAnalysisData.SurveySite)= '
        query+=str(self.site)
        query+='));'
        try:
            self.ODB.execute(query)
            self.LOBF=self.ODB.GetVariable('LOBF')[0]
        except:
            print('\nSiteSize 81')
            print(query)
            self.ODB.execute(query)
            print("self.ODB.GetVariable('LOBF') ", self.ODB.GetVariable('LOBF'))
            self.LOBF=self.ODB.GetVariable('LOBF')[0]
        return

    def GetMeanTranLen(self):
        TranLen=list(map(lambda t: t.GetTranLength()  ,self.ListTransects))
        n=len(TranLen)
        if n<1:return(norm(-sys.maxsize,-sys.maxsize))
        try:
          mu=average(TranLen)
        except:
            mu=average(TranLen)
        if n>1:
            sigma=std(TranLen,ddof=1)
            sterr=sigma/sqrt(n)
        else:
            sigma=-sys.maxsize
            sterr=-sys.maxsize
        result=norm(mu,sterr)
        return(result)
    def AreaFromLOBF(self):
        self.GetLOBF()
        if self.LOBF==None:
          self.LOBFarea=norm(MinInt,0.)
          return
        MTL=self.GetMeanTranLen()
        try:
            if(len(self.ListTransects)>1):
                self.LOBFarea=norm(MTL.mu*self.LOBF,MTL.sigma*self.LOBF)
                return
        except:
            print('SiteSize 117')
            print('MTL',MTL)
            print('len(self.ListTransects) ' , len(self.ListTransects) )
            if(len(self.ListTransects)>1):
                self.LOBFarea=norm(MTL[0]*self.LOBF,MTL[1]*self.LOBF)
                return

        if(len(self.ListTransects)>0):
                self.LOBFarea=norm(MTL.mu*self.LOBF,0.)
                return

        self.LOBFarea=norm(MinInt,0.)
    def RandAreaFromLOBF(self,n=None):
        return(self.LOBFarea.rvs(n,LowBound=self.TranArea))
        
    def GetArea(self,Digitized=True):
        if Digitized: return(self.GetDigitizedArea())
        return(self.LOBFarea)
    def GetEstArea(self,Digitized=True):
        if not(Digitized):return(self.LOBFarea.mu)

        #Digitized area
        return(self.DigitizedArea.mu)

        
    def GetDigitizedEquiProb(self,n):
        p=list(map(lambda i: (i+.5)/float(n),range(n)))
        result=self.DigitizedArea.isf(p)
        return(result)
    def GetEquiProbArea(self,n,Digitized=True):
        if Digitized:return(self.DigitizedArea.EquiProbVal(n,LowBound=self.TranArea))

        #Area based on line-of-best-fit
        return(self.LOBFarea.EquiProbVal(n,LowBound=self.TranArea))
                            
        
        
    def GetSEEstArea(self,Digitized=True):
        if Digitized:return(self.DigitizedArea.sigma)
        return(self.LOBFarea.sigma)
    def GetRandomArea(self,n=1000,RunNumber=4,EquiProb=True):
            if RunNumber==4:return(self.DigitizedArea.rvs(n=n,LowBound=self.TranArea))
            elif RunNumber==2:return(self.LOBFarea.rvs(n=n,LowBound=self.TranArea))
            if n==None:return(MinInt)
            return(array(n*[MinInt]))
        

class CopySiteSize(SiteSize):
    def __init__(self,oriSiteSize,ListTransects):
        self.ODB=oriSiteSize.ODB
        self.survey=oriSiteSize.survey
        self.year=oriSiteSize.year
        self.site=oriSiteSize.site
        self.LOBF=oriSiteSize.LOBF
        self.DigitizedArea=oriSiteSize.DigitizedArea
        self.ListTransects=ListTransects
        self.AreaFromLOBF()
        self.TranArea=oriSiteSize.TranArea

if __name__ == "__main__":

    from GDuckTransectclass import GDuckTransectclass  
    from GDtransect import GDtransect
    from numpy import inf
    import geoduckQueryFunc as QueryFunc
    from GDuckTransectclass import GDuckTransectclass
    from MetaTransectClass import MetaTransectClass
    databasepath='H:/AnalysisPrograms2013/PyFunctions/Geoduck/SampleData/2013MalcolmIsWorking.mdb'  
    databasepath='t:Geoduck_Bio.mdb'  
    from ADO import adoBaseClass as OpenDB
    ODB=OpenDB(databasepath)
    AlloSource=QueryFunc.AlloEqn()  
    key=list(range(10819,10890))
    ClassIndex=0
    survey="Malcolm Island, 2013"
    key=[14143,14144,14146,14146]
    ListTransects=list(map(lambda k:GDtransect(ODB,k,QueryFunc,SizeBound=None,MinDepth=3,MaxDepth=999)   ,key))
    test=SiteSize(ODB,survey,2013,6,ListTransects=ListTransects)
          
            
        
   
