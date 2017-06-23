'''2015-11-17 Modified MetaTransectClass.QueryTranClass to ensure that 
transects will always be orderd by Headers.key'''

from numpy import ndarray
from numpy import iinfo,int16
MinInt=iinfo(int16).min
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from ADO import adoBaseClass as OpenDB
from SiteInfo import SiteInfo

class MetaTransectClass:
    def __init__(self,ODB,SelectedSurveyYears,SelectedTranChar):
        '''MetaTransectClass(SelectedSurveyYears,SelectedTranChar,CalcAllo=False)

          ODB is an ADO connection to a database
          SelectedSurveyYears are the cominations of Location and Year
          SelectedTranChar are the transect characteristics that are supposed to be used
          CalcAllo indicates that an attempt should be made to estimate allometric parameters from length-weight data

          All the information you need to generate a full transect class!
          '''
        self.SelectedSurveyYears=SelectedSurveyYears
        self.ODB=ODB
        self.SelectedTranChar=SelectedTranChar
        self.nchar=len(self.SelectedTranChar)
        
        self.WhereSurveyYear()
        self.DefineTranClass()
        self.key=list(map(lambda i: self.GetKey(i)  ,range(self.nclass)))

        
    def WhereSurveyYear(self):
        CurSurvey=self.SelectedSurveyYears[0]
        self.SpecSurvey =' ('
        self.SpecSurvey+='( (Headers.Year='
        self.SpecSurvey+=str(CurSurvey[1])
        self.SpecSurvey+=') AND (Headers.Project="'
        self.SpecSurvey+=CurSurvey[0]
        self.SpecSurvey+='"))'

        for CurSurvey in self.SelectedSurveyYears[1:]:
            self.SpecSurvey+=' or '
                
            self.SpecSurvey+='( (Headers.Year='
            self.SpecSurvey+=str(CurSurvey[1])
            self.SpecSurvey+=') AND (Headers.Project="'
            self.SpecSurvey+=CurSurvey[0]
            self.SpecSurvey+='"))'
        self.SpecSurvey+= ' ) '

    def DefineTranClass(self):
        #Trivial Case
        if len(self.SelectedTranChar)==0:
            self.TranClass=[[]]
            self.nclass=1
            ClassKey=self.GetKey()
            self.SI=SiteInfo(nsite=self.nclass,TransectNumber=ClassKey,TranChar=self.TranClass)
            self.SI.exec()
            self.TranClass[0].append(self.SI.result[0])
            return
            
        query ='SELECT DISTINCT Headers.'
        query+=self.SelectedTranChar[0]
        for stc in self.SelectedTranChar[1:]:
            query+=', Headers.'
            query+=stc
            query+='  '
        query=query.replace('Headers.Location' , 'Headers.Project')
        query=query.replace('Headers.SubSampleLocation','Headers.Site')
        query+='  FROM Densities INNER JOIN Headers ON Densities.HKey = Headers.Key  Where( '
        query+=self.SpecSurvey
        query+=' );'
        try:
            self.ODB.execute(query)
            self.TranClass=self.ODB.GetALL()
            self.nclass=len(self.TranClass)
        except:
            print('\nMetaTransectClass 72')
            print('query',query)
            self.ODB.execute(query)
            self.TranClass=self.ODB.GetALL()
            self.nclass=len(self.TranClass)
        ClassKey=self.GetKey()
        self.SI=SiteInfo(nsite=self.nclass,TransectNumber=ClassKey,TranChar=self.TranClass)
        self.SI.exec()

        for i in range(self.nclass):self.TranClass[i].append(self.SI.result[i])
           

    def FormatTranClass(self,index):
        CurSpec=self.TranClass[index]

        #Default Values
        result={'Project':'Combined','Site':MinInt,\
                'Year':MinInt,'StatArea':MinInt,'SubArea':MinInt,\
                'InBed':MinInt,'NumTran':MinInt,'NumQuad':MinInt}
        result['NumTran']=len(  self.key[index])
        for c in range(len(self.SelectedTranChar)):
            try:
                if self.SelectedTranChar[c]=='Project':
                    result['Project']=CurSpec[c]
                elif self.SelectedTranChar[c]=='Site':
                    result['Site']=CurSpec[c]
                elif self.SelectedTranChar[c]=='Year':
                    result['Year']=CurSpec[c]
                elif self.SelectedTranChar[c]=='StatArea':
                    result['StatArea']=CurSpec[c]
                elif self.SelectedTranChar[c]=='SubArea':
                    result['SubArea']=CurSpec[c]
            except:
                print ('\nMetaTransect 99 index,len(self.nclass)',index,self.nclass)
                print ('c,len(CurSpec)',c,len(CurSpec))
                print('CurSpec',CurSpec)
                print('self.SelectedTranChar',self.SelectedTranChar)
                if self.SelectedTranChar[c]=='Project':
                    result['Project']=CurSpec[c]
                elif self.SelectedTranChar[c]=='Site':
                    result['Site']=CurSpec[c]
                elif self.SelectedTranChar[c]=='Year':
                    result['Year']=CurSpec[c]
                elif self.SelectedTranChar[c]=='StatArea':
                    result['StatArea']=CurSpec[c]
                elif self.SelectedTranChar[c]=='SubArea':
                    result['SubArea']=CurSpec[c]
                
        return(result)
            
        

    def SpecClass(self,index):
        CurSpec=self.TranClass[index]
        byChar=self.SingleChar(self.SelectedTranChar,CurSpec)
        result=' ( '+byChar[0]
        for bc in byChar[1:]:
            result+=' and '+bc
        result+=' ) '
        return(result)
        

    def SingleChar(self,char,val):
        if isinstance(char,(list,ndarray)):
            return(list(map(lambda c,v: self.SingleChar(c,v)    ,char,val)))
        if val==None:
            result='(Headers.'+char+' Is Null) '
            return(result)
            
        result='(Headers.'+char+'='
        if (char=='Project') :
            result+='"'+val+'")'

        else:
            result+=str(val)+')'
        result=result.replace('Headers.Location','Headers.Project')
        result=result.replace('Headers.SubSampleLocation','Headers.Site')
        return(result)

        

    def QueryTranClass(self,i):
        query ='Select distinct Headers.Key, Headers.Transect, '
        query+='FALSE as Omit, "" as ReasonOmit ,'
        query+='Headers.Year, Headers.Month,Headers.Day ,Headers.Comments ' 
        query+='FROM Densities INNER JOIN Headers ON Densities.HKey = Headers.Key '
        query+='Where( '
        query+=self.SpecSurvey
        if self.nclass>1:
            query+=' and '
            query+=self.SpecClass(i)
        query+=') order by Headers.Key;'
        return(query)

    def GetKey(self,i=None):
        if i==None:return(list(map(lambda i:self.GetKey(i=i),range(self.nclass))))
        if isinstance(i, (list,ndarray)): return(list(map(lambda j:self.GetKey(i=j),i)))
        query=self.QueryTranClass(i)
        try:
            self.ODB.execute(query)
            result=self.ODB.GetALL()
        except:
            print('MetaTransectClass 150')
            print ('i',i)
            print ('query',query)
            print('self.TranClass[i]',self.TranClass[i])
            self.ODB.execute(query)
            result=self.ODB.GetALL()
        return(result)

if __name__ == "__main__":


    databasepath='H:\SampleMDB\SeaCuke_Bio_97_NoLink.mdb'
    ODB=OpenDB(databasepath)

    SelectedSurveyYears=[['West Aristazabal',2012],['Howe Sound',2012]]
    SelectedTranChar=['Site','Year','SubArea','Project']


    print ('done Define Classes')
