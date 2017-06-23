
from datetime import datetime
from numpy import ndarray,average
from sys import maxsize as inf

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from ADO import adoBaseClass as OpenDB
from transect import transect


class GDtransect(transect):
    '''GDtransect(ODB,key,QueryFunc,SizeBound=None,MinDepth=-999,MaxDepth=999)

    ODB (open database) is an instance of the ADO class
    key is the key-value from the headers table

    Significant differences between transect and GDtransect
    *GDtransect keeps survey-date as a characteristic of the transect
    *GDtransect incorporates show-factor into abundance.
    *GDtransect uses averages from surveyed quadrats to estimate abundance
    Previous version in H:\AnalysisPrograms2013\PyFunctions.20140218\Geoduck 
    '''
    def __init__(self,ODB,key,QueryFunc,SizeBound=None,MinDepth=-999,MaxDepth=999):
        self.key=key
        self.ODB=ODB
        self.MinDepth,self.MaxDepth=MinDepth,MaxDepth
        self.QueryFunc=QueryFunc

        #self.SizeBound is maintained to be compatible with common code
        self.SizeBound=SizeBound
        if self.SizeBound==None:self.SizeBound=[inf]
        if self.SizeBound==inf:self.SizeBound=[inf]
        if isinstance(self.SizeBound,(float,int)):self.SizeBound=[self.SizeBound,inf]
        if (len(self.SizeBound)==1) and (self.SizeBound[0]!=inf):self.SizeBound.append(inf)
        self.SizeBound.sort()
        self.MeasAbund=None
        query=self.QueryFunc.QnumDepthCount(self.key)
        try:
            ODB.execute(query)
        except:
            print('\ntransect line 30')
            print('query\n',query)
        self.c=self.ODB.GetVariable('CountTotal')#Number of counted animals#Quadrat Number
        self.q=self.ODB.GetVariable('QuadNum')#Quadrat Number
        self.d=self.ODB.GetVariable('Depth')#Depth
        self.AdjustForDepthRange()
        self.MeanShowDens=average(self.c)
        self.GetSurveyDate_BedNum()
        self.TranLen*=self.FracInDepthRange
        self.EstNumShow=self.MeanShowDens*self.nquad
        
    def AdjustForDepthRange(self):
        self.nquad=len(self.q)
        iquad=range(self.nquad)
        iInDepthRange=list(filter(lambda i: (self.d[i] >=self.MinDepth) and (self.d[i]<=self.MaxDepth),iquad))
        self.FracInDepthRange=1.
        nInDepthRange=len(iInDepthRange)
        if nInDepthRange==self.nquad:return
        
        self.FracInDepthRange=float(nInDepthRange)/float(self.nquad)
        self.nquad=nInDepthRange
        self.c=list(map(lambda i:self.c[i],iInDepthRange))
        self.d=list(map(lambda i:self.d[i],iInDepthRange))
        self.q=list(map(lambda i:self.q[i],iInDepthRange))


    def GetNumQuad(self):
        return(self.nquad)

    def GetSurveyDate_BedNum(self):
        query= "Select Headers.Year, Headers.Month, Headers.Day,Headers.BedNum, "
        query+="Headers.Transect,Headers.CommentsGeneral,Headers.CommentsData, "
        query+="Headers.GIS_Code,  Headers.TransectLength "
        query+="From Headers  "
        query+="Where Headers.Key= "+str(self.key)+" ;"
        self.ODB.execute(query)
        try:
            record=self.ODB.GetALL()[0]
            y,m,d=record[:3]
            if d==0:d=1
            self.SurveyDate=datetime(y,m,d)
            BedNum=record[3]
            self.OnBed=(BedNum!=None)
            self.TransectNumber=record[4]
            self.TransectComments=''
            if record[5]!=None:
              self.TransectComments+=record[5]
            if (record[5]!=None) and (record[6]!=None):
              self.TransectComments+=' '
            if record[6]!=None:
              self.TransectComments+=record[6]
            #take out quotes so they don't confuse things later on
            self.TransectComments=self.TransectComments.replace('\'',' ')
            self.TransectComments=self.TransectComments.replace('"',' ')
            self.GIS_Code=record[7]
            recTranLen=record[8]
            self.TranLen=recTranLen#Unadusted for depth-range
        except:
            print('\n GDtransect 34 self.ODB.GetALL()\n',self.ODB.GetALL())
            print('query',query)
            print('self.ODB.GetALL() ',self.ODB.GetALL())
            record=self.ODB.GetALL()[0]
            y,m,d=record[:3]
            self.SurveyDate=datetime(y,m,d)
            BedNum=record[3]
            self.OnBed=(BedNum!=None)
            self.TransectNumber=record[4]
            self.TransectComments=record[5]+' '+record[6]
            self.GIS_Code=records[7]
            
    def GetAbundance(self,  sfp,CalcNumDuck=True,Randomize=True):
        '''Note that this is going return abundance based upon average
           population-densities of surveyed quadrats.

           A previous version of this function used interpolated quadrat-densities.
           We might change back at a later time.'''
       
        #Old calculation of NumShow
        #NumShow=transect.GetAbundance(self)['USLinf']['Pop']

        #New calculation of NumShow
        NumShow=self.EstNumShow



        try:
            sf=sfp.EstSF(date=self.SurveyDate)
            result=float(NumShow)/sf
        except:
            print('GDtransect 70')
            print (self.SurveyDate,NumShow)
            sf=sfp.EstSF(date=self.SurveyDate)
            result=float(NumShow)/sf
        return(result)

    def GetDepthRangeOccur(self):
        d=self.d
        d=list(filter(lambda x:(x>=self.MinDepth) and (x<=self.MaxDepth),d))
        if len(d)==0:return[None,None]
        if len(d)==1:return(2*d)
        d.sort()
        return([d[0],d[-1]])
        
    def GetTranLength(self):
        return(self.TranLen)


if __name__ == "__main__":
    databasepath='H:\AnalysisPrograms2013\PyFunctions\Geoduck\SampleData\Geoduck_Bio.mdb'
    ODB=OpenDB(databasepath)
    key=14106
    import geoduckQueryFunc as QueryFunc
    from ADOSFdate import dumbSFplot
    sfp=dumbSFplot(sf=0.886)
    
    gdt=GDtransect(ODB,key,QueryFunc,SizeBound=None,MinDepth=-999,MaxDepth=999)
    print( '\n gdt.GetAbundance(sfp,CalcNumDuck=True,Randomize=True)' ,  gdt.GetAbundance(sfp,CalcNumDuck=True,Randomize=True))

    print('sfp.EstSF(date=gdt.SurveyDate) ' , sfp.EstSF(date=gdt.SurveyDate) )
           

    print( '/n gdt.GetTranLength() ' ,gdt.GetTranLength() )

  
