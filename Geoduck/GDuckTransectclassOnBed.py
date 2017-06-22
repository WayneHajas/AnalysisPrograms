# Class to represent geoduck-transects - but only those that are on a bed
from GDuckTransectclass import GDuckTransectclass

class GDuckTransectclassOnBed(GDuckTransectclass):
    def __init__(oriTransectSet):
        '''oriTransectSet is an instance of GDuckTransectclass.
           All we are going to do is filter out transects that are not on a transect'''

        self.ODB=oriTransectSet.ODB
        self.SFData=oriTransectSet.SFData
        self.MinDepth=oriTransectSet.MinDepth
        self.MaxDepth=oriTransectSet.MaxDepth
        self.AlloSource=oriTransectSet.AlloSource
        self.AE=oriTransectSet.AE

        #Only pick up the transects that are used for calculations involving oriTransectSet
        self.transects=list(map(lambda i:oriTransectSet.transect[i],oriTransectSet.IndexKeyUse))
        #Take out the off-bed transects.
        self.transects=list(filter(lambda t:t.OnBed,self.transects))
        self.ntransect=len(self.transects)
        self.IndexKeyUse=oriTransectSet.IndexKeyUse

if __name__ == "__main__":

    from numpy import inf
    import geoduckQueryFunc as QueryFunc
    databasepath='H:\AnalysisPrograms2013\PyFunctions\Geoduck\SampleAIP\Geoduck_BioNew.mdb'
    from ADO import adoBaseClass as OpenDB
    ODB=OpenDB(databasepath)
    AlloSource=QueryFunc.AlloEqn()  
    TranClassChar={'SurveyTitle':"Millar and Russell Channels",'Year':2007,'SurveySite':1,'MeanWeight':100,'StErrWeight':10,'CoastLengthM':1000,'StErrCLM':10}

    key=list(range(10819,10890))
    IndexKeyUse=1

  
    test=GDuckTransectclass(ODB,key,IndexKeyUse,TranClassChar,AlloSource,QueryFunc,SizeBound=None,MinDepth=-999,MaxDepth=999)
    print (test.GetSurveyedArea())
    print (test.ntransect)
    
        

        
