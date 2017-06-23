import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from ADO import adoBaseClass as OpenDB
from datetime import datetime,timedelta
from numpy import ndarray

from SFdate import SFMeas,SFQuad,SFplot,multiSFplot

        
class ADOSFQuad(SFQuad):
    def __init__(self,ODB,SurveyName,SurveyYear,SFPlotNum,SFQuadNum):
        '''ADOSFQuad(ODB,SurveyName,SurveyYear,SFPlotNum,SFQuadNum)
           *ODB is an instance of adoBaseClass
           '''
        super().__init__()
        query ="SELECT Headers.Year,Headers.Month,Headers.Day,"
        query+=     "ShowFactor.ShowL, ShowFactor.TotalFlagL, ShowFactor.ShowR, ShowFactor.TotalFlagR "
        query+="FROM Headers INNER JOIN ShowFactor ON Headers.Key = ShowFactor.HKey "
        query+="WHERE ( "
        query+=           "(Headers.SurveyTitle='"
        query+=                                   SurveyName
        query+=                                               "') AND "
        query+=           "(Headers.Year="
        query+=                                   str(SurveyYear)
        query+=                                               ") AND "
        query+=           "(Headers.ShowPlotNum="
        query+=                                   str(SFPlotNum)
        query+=                                               ") AND "
        query+=           "(ShowFactor.Quadrat="
        query+=                                   str(SFQuadNum)
        query+=                                               ") ) "
        query+="order by Headers.Year,Headers.Month,Headers.Day ; "
        ODB.execute(query)
        data=ODB.GetALL()
        for r in data:
            qleft=SFMeas([r[0],r[1],r[2]], Nshow=r[3],Nduck=r[4]) 
            qright=SFMeas([r[0],r[1],r[2]], Nshow=r[5],Nduck=r[6])
            qleft.Add(qright)
            self.append(qleft)      

class ADOSFplot(SFplot):
    def __init__(self,ODB,SurveyName,SurveyYear,SFPlotNum):
        '''ADOSFplot(ODB,SurveyName,SurveyYear,SFPlotNum)
           *ODB is an instance of adoBaseClass
           '''
        super().__init__()
        self.ODB=ODB
        self.SurveyName=SurveyName
        self.SurveyYear=SurveyYear
        self.SFPlotNum=SFPlotNum
        self.GetQuadNum()
        for q in self.QuadNum:
            quad=ADOSFQuad(self.ODB,self.SurveyName,self.SurveyYear,self.SFPlotNum,q)
            self.quad.append(quad)

    def GetQuadNum(self):
        query ="SELECT DISTINCT ShowFactor.Quadrat "
        query+="FROM Headers INNER JOIN ShowFactor ON Headers.Key = ShowFactor.HKey "
        query+="WHERE ( "
        query+=           "(Headers.SurveyTitle='"
        query+=                                   self.SurveyName
        query+=                                               "') AND "
        query+=           "(Headers.Year="
        query+=                                   str(self.SurveyYear)
        query+=                                               ") AND "
        query+=           "(Headers.ShowPlotNum="
        query+=                                   str(self.SFPlotNum)
        query+=                                               "))  "
        query+="ORDER BY  ShowFactor.Quadrat;"
        self.ODB.execute(query)
        self.QuadNum=self.ODB.GetVariable('Quadrat')

    def GetDailyFixed(self):#Corresponds to DailyFixed field in Results_Transect
        return(self.DailyFixed)            

class ADOmultiSFplot(multiSFplot):
    def __init__(self, ODB,SurveyName,SurveyYear,SurveySite=None,SFPlotNum=None):
        '''ADOmultiSFplot(ODB,SurveyName,SurveyYear,SFPlotNum)
        * SFPlotNum is a list of plot numbers)'''

        SFPlotNum=GetShowPlotNum(ODB,SurveyName,SurveyYear)
        if SFPlotNum['FixedSFValue']!=None:
            self.lSFplot=[dumbSFplot(sf=SFPlotNum['FixedSFValue'])]
            self.DailyFixed='Fixed'
        elif SFPlotNum['ShowPlotNum']!=[]:
            self.lSFplot=\
                list(map(lambda i:
                    ADOSFplot(ODB,SurveyName,SurveyYear,i),SFPlotNum['ShowPlotNum']))
            self.DailyFixed='Daily'

        #There is no useful information
        else:
            self.lSFplot=[dumbSFplot(sf=1.0)]
            self.DailyFixed='Fixed'
        multiSFplot.__init__(self,self.lSFplot)

    def GetDailyFixed(self):#Corresponds to DailyFixed field in Results_Transect
        return(self.DailyFixed)            

class dumbSFplot():
    '''dumbSFplot()
    This is a dumb version of the show-factor plots.
    The only possible show-factor plot is sf.
    There is no show-factor data.
    There are the right functions so that dumbSFplot can be used as a proxy for ADOmultiSFplot.
    '''
    def __init__(self, sf=1.0):
        self.SetSF(sf=sf)

    def SetSF(self,sf=1):
        if sf==None:
            self.sf=1
            return
        if isinstance(sf,str):
            try:
                sf2=float(sf)
                self.SetSF(sf=sf2)
                return
            except:
                self.sf=1.0
                return
        if (sf<0):
            self.sf=1
            return
        if (sf>1):
            self.sf=1
            return
        try:
            self.sf=sf
        except:
            self.sf=1.0
        return
            
    def EstSF(self, date=None,CalcNumDuck=True):
        return(self.sf)
    def RandSF(self, date=None,CalcNumDuck=True,Randomize=True):
        return(self.sf)
    def Randomize(self,deterministic=False,CalcNumDuck=True):
        return
    def GetNumDuck(self):
        return(1.0)
    def GetNumShow(self, date=None):
        return(self.sf)
    def GetDateRange(self):
        MaxDate=datetime.now()
        MinDate=datetime.now()#+timedelta(days=-1000*365)
        return([MinDate,MaxDate])
    def GetDailyFixed(self):#Corresponds to DailyFixed field in Results_Transect
        return(self.DailyFixed)


def GetShowPlotNum(ODB,SurveyName,SurveyYear,SurveySite=None):    
    query ="SELECT DISTINCT  SiteAnalysisData.ShowPlotToUse1, SiteAnalysisData.ShowPlotToUse2, "
    query+="SiteAnalysisData.ShowPlotToUse3, SiteAnalysisData.ShowPlotToUse4, "
    query+="SiteAnalysisData.FixedSFValue "
    query+="FROM  SiteAnalysisData "
    query+="WHERE ( "
    query+=           "(SiteAnalysisData.SurveyTitle='"
    query+=                                   SurveyName
    query+=                                               "') AND "
    query+=           "(SiteAnalysisData.Year="
    query+=                                   str(SurveyYear)
    if SurveySite!=None:
        query+=                                            ") AND "
        query+=        "(SiteAnalysisData.SurveySite="
        query+=                                str(SurveySite)
    query+=                                               ") ); "
    ODB.execute(query)

    FixedSFValue=ODB.GetVariable('FixedSFValue')
    if len(FixedSFValue)==0:#There is no show-factor information
        result={'FixedSFValue':None  ,"ShowPlotNum":[]}
        return(result)
        
    FixedSFValue=FixedSFValue[0]
    if FixedSFValue!=None:#There is  a show-factor value
        result={'FixedSFValue':FixedSFValue  ,"ShowPlotNum":[]}
        return(result)
    ShowPlotNum=ODB.GetALL()[0][:-1]
    
    ShowPlotNum=list(filter(lambda x:x!=None,ShowPlotNum))
    result={'FixedSFValue':None  ,"ShowPlotNum":ShowPlotNum}
    return(result)


if __name__ == "__main__":
    databasepath='H:\AnalysisPrograms2013\PyFunctions\Geoduck\SampleData\Geoduck_Bio.mdb'
    ODB=OpenDB(databasepath)
    SurveyName='Millar and Russell Channels'
    SurveyYear=2007
    SFPlotNum=1
    SFQuadNum=7

    print('\n', 'GetShowPlotNum(ODB,"Millar and Russell Channels",2007,1)', GetShowPlotNum(ODB,"Millar and Russell Channels",2007,1) )

    sfp1=ADOSFplot(ODB,"Millar and Russell Channels",2007,1)
    sfp2=ADOmultiSFplot(ODB,"Millar and Russell Channels",2007,0.75)

    
    drange=sfp1.GetDateRange()
    print('\nGetNumShow', sfp1.GetNumShow(date=drange[0]))
    print('\nGetNumDuck', sfp1.GetNumDuck())
    print('\nEstSF ',sfp1.EstSF(date=drange[0]))
    for d in range(-3,18):
        d1=drange[0]+timedelta(days=d)
        print(d1, sfp1.GetNumShow(date=d1),sfp1.GetNumDuck(),sfp1.EstSF(date=d1))
    for d in range(-3,18):
        d1=drange[0]+timedelta(days=d)
        try:
           print(d1, sfp2.GetNumShow(date=d1),sfp2.GetNumDuck(),sfp2.EstSF(date=d1),sfp2.RandSF(date=d1,CalcNumDuck=False))
        except:
            print ('d1',d1)
            print('sfp2.GetNumShow(date=d1)',sfp2.GetNumShow(date=d1))
            print('sfp2.GetNumDuck()',sfp2.GetNumDuck())
            print('sfp2.EstSF(date=d1)',sfp2.EstSF(date=d1))
            print('sfp2.RandSF(date=d1,CalcNumDuck=False)',sfp2.RandSF(date=d1,CalcNumDuck=False))
    
    d= datetime(2001,7,6)
    for lsfp in sfp2.lSFplot:
        print('lsfp.GetNumShow(date=d)',lsfp.GetNumShow(date=d) )
    print(type(sfp2))
    print(dir(sfp2))
