import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from ADO import adoBaseClass as OpenDB
from norm import norm
from numpy import ndarray,array
from numpy.random import shuffle
import pdb 
class ADOWeightVal():
    '''Weight statistics as for values taken form the geoduck-bio database'''
    def __init__(self,ODB,SurveyTitle,Year,SurveySite=None):
        '''ADOWeightVal(ODB,HeaderValues)
           * ODB is an open geoduck bio-database'''
        
        self.ODB=ODB

        query ="select "
        query+="SiteAnalysisData.MeanWeight as EstMeanWeight, SiteAnalysisData.MeanWeightSE, SiteAnalysisData.MeanWeightSource  from SiteAnalysisData "
        query+=self.WhereQuery(SurveyTitle,Year,SurveySite)
        query+=";"
        ODB.execute(query)
        self.EstMeanWeight    =ODB.GetVariable('EstMeanWeight')
        self.MeanWeightSE     =ODB.GetVariable('MeanWeightSE')
        self.MeanWeightSource =ODB.GetVariable('MeanWeightSource')
        if isinstance(self.EstMeanWeight,(list,ndarray)):self.EstMeanWeight=self.EstMeanWeight[0]
        if isinstance(self.MeanWeightSE ,(list,ndarray)):self.MeanWeightSE =self.MeanWeightSE[0]
        if isinstance(self.MeanWeightSource ,(list,ndarray)):self.MeanWeightSource =self.MeanWeightSource[0]
        if self.EstMeanWeight==None:self.EstMeanWeight=-1.
        if self.MeanWeightSE==None:self.MeanWeightSE=0.
        if self.MeanWeightSource==None:self.MeanWeightSource='Unknown'
        if self.MeanWeightSource=='':self.MeanWeightSource='Unknown'
        self.RandSource=norm(self.EstMeanWeight,self.MeanWeightSE)
        

    def WhereQuery(self,SurveyTitle,Year,SurveySite):
        query ="Where( "
        query+=     "(SiteAnalysisData.SurveyTitle ='"+SurveyTitle+ "') and "
        query+=     "(SiteAnalysisData.Year        = "+str(Year)  + " ) and "
        if SurveySite!=None:
          query+=   "(SiteAnalysisData.SurveySite  = "+str(SurveySite)  + " ) "
        else:
          query+=   "(SiteAnalysisData is not null)"
        query+=")"
        
        return(query)

    def Randval(self,n=None,EquiProb=True):
      '''ADOWeightVal.Randval(self,n=None,EquiProb=True)
      if n=None, returns a single random value
      if EquiProb, returned values are equiprobable- but in a random order'''
      if n==None:return(self.RandSource.rvs())
		
      if not(EquiProb):
        try:
          return(self.RandSource.rvs(n))
        except:
          pdb.set_trace()
          return(self.RandSource.rvs(n))

      # EquiProb is true
      p=array(list(map(lambda i:(i+.5)/n,range(n) )))
      EPV=self.RandSource.isf(p)
      shuffle(EPV)
      return(EPV)


if __name__ == "__main__":
    databasepath='H:\AnalysisPrograms2013\PyFunctions\Geoduck\SampleAIP\Geoduck_Bio2.mdb'
    ODB=OpenDB(databasepath)
    SurveyTitle='Malcolm Island, 2013'
    Year=2013
    SurveySite=2
    test=ADOWeightVal(ODB,SurveyTitle,Year,SurveySite=SurveySite)
    print('test.EstMeanWeight',test.EstMeanWeight)
    print('test.MeanWeightSE',test.MeanWeightSE)
    print('test.RandVal()',test.Randval())
    print('test.RandVal(n=5)',test.Randval(n=5))
