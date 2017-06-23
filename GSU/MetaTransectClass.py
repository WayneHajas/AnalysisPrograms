'''
2016-01-29.  Modify some variable names to reflect the change from alpha-30 to intcpt

2015-11-17.  Modified MetaTransectClass.QueryTranClass to ensure that 
transects will always be orderd by Headers.key'''

from numpy import ndarray
from numpy import iinfo,int16
MinInt=iinfo(int16).min
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from ADO import adoBaseClass as OpenDB
from DataAllometric import DataAllometric
from GSUQueryFunc import AlloEqn
import pdb

class MetaTransectClass:
    def __init__(self,ODB,SelectedSurveyYears,SelectedTranChar,CalcAllo=False,DefaultAllo=None):
        '''MetaTransectClass(SelectedSurveyYears,SelectedTranChar,CalcAllo=False,DefaultAllo=None)

          ODB is an ADO connection to a database
          SelectedSurveyYears are the cominations of Location and Year
          SelectedTranChar are the transect characteristics that are supposed to be used
          CalcAllo indicates that an attempt should be made to estimate allometric parameters from length-weight data
          DefaultAllo is a default instance of AlloEqn that gives the allometric equation.

          All the information you need to generate a full transect class!
          '''
        
        self.SelectedSurveyYears=SelectedSurveyYears
        self.ODB=ODB
        self.SelectedTranChar=SelectedTranChar
        self.nchar=len(self.SelectedTranChar)
        self.DefaultAllo=DefaultAllo
        
        self.WhereSurveyYear()
        self.DefineTranClass()
        self.key=list(map(lambda i: self.GetKey(i)  ,range(self.nclass)))

        #Establish default allometric
        DA=DefaultAllo
        if DA==None:DA=AlloEqn()
        self.Allo=list(map(lambda k: DA,self.key))
        #pdb.set_trace()
        if CalcAllo:
            for k in range(len(self.key)):
                DataAllo=DataAllometric(self.ODB,self.key[k]).Allo
                if DataAllo.intcpt!=None:
                    self.Allo[k]=DataAllo
        
    def WhereSurveyYear(self):
        CurSurvey=self.SelectedSurveyYears[0]
        self.SpecSurvey =' ('
        self.SpecSurvey+='( (Headers.Year='
        self.SpecSurvey+=str(CurSurvey[1])
        self.SpecSurvey+=') AND (Headers.SurveyTitle="'
        self.SpecSurvey+=CurSurvey[0]
        self.SpecSurvey+='"))'

        for CurSurvey in self.SelectedSurveyYears[1:]:
            self.SpecSurvey+=' or '
                
            self.SpecSurvey+='( (Headers.Year='
            self.SpecSurvey+=str(CurSurvey[1])
            self.SpecSurvey+=') AND (Headers.SurveyTitle="'
            self.SpecSurvey+=CurSurvey[0]
            self.SpecSurvey+='"))'
        self.SpecSurvey+= ' ) '

    def DefineTranClass(self):
        #Trivial Case
        if len(self.SelectedTranChar)==0:
            self.TranClass=[[]]
            self.nclass=1
            return
            
        query ='SELECT DISTINCT Headers.'
        query+=self.SelectedTranChar[0]
        for stc in self.SelectedTranChar[1:]:
            query+=', Headers.'
            query+=stc
            query+='  '
        query+='  FROM Density INNER JOIN Headers ON Density.HKey = Headers.Key  Where( '
        query+=self.SpecSurvey
        query+=' );'
        try:
            self.ODB.execute(query)
            self.TranClass=self.ODB.GetALL()
            self.nclass=len(self.TranClass)
        except:
            print('\nMetaTransectClass 74')
            print('query',query)
            self.ODB.execute(query)
            self.TranClass=self.ODB.GetALL()
            self.nclass=len(self.TranClass)

    def FormatTranClass(self,index):
        CurSpec=self.TranClass[index]

        #Default Values
        result={'SurveyTitle':'Combined','SubSampleLocation':'Combined',\
                'Year':MinInt,'StatArea':MinInt,'SubArea':MinInt,\
                'InBed':MinInt,'NumTran':MinInt,'NumQuad':MinInt}
        result['NumTran']=len(  self.key[index])
        for c in range(len(CurSpec)):
            try:
                if self.SelectedTranChar[c]=='SurveyTitle':
                    result['SurveyTitle']=CurSpec[c]
                elif self.SelectedTranChar[c]=='SubSampleLocation':
                    result['SubSampleLocation']=CurSpec[c]
                elif self.SelectedTranChar[c]=='Year':
                    result['Year']=CurSpec[c]
                elif self.SelectedTranChar[c]=='StatArea':
                    result['StatArea']=CurSpec[c]
                elif self.SelectedTranChar[c]=='SubArea':
                    result['SubArea']=CurSpec[c]
            except:
                print ('\nMetaTransect 94 index,len(self.nclass)',index,self.nclass)
                print ('c,len(CurSpec)',c,len(CurSpec))
                print('CurSpec',CurSpec)
                print('self.SelectedTranChar',self.SelectedTranChar)
                
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
        result='(Headers.'+char+'='
        if (char=='SurveyTitle') or (char=='SubSampleLocation'):
            result+='"'+val+'")'

        else:
            result+=str(val)+')'
        result=result.replace('Headers.Location','Headers.SurveyTitle')
        return(result)

        

    def QueryTranClass(self,i):
        query ='Select distinct Headers.Key FROM Density INNER JOIN Headers ON Density.HKey = Headers.Key '
        query+='Where( '
        query+=self.SpecSurvey
        if self.nclass>1:
            query+=' and '
            query+=self.SpecClass(i)
        query+=') order by Headers.Key ;'
        return(query)

    def GetKey(self,i):
        query=self.QueryTranClass(i)             
        self.ODB.execute(query)
        result=self.ODB.GetVariable('Key')
        return(result)

if __name__ == "__main__":


    databasepath='h:\SampleMDB\GreenUrchin_NoLink.mdb'
    ODB=OpenDB(databasepath)

    SelectedSurveyYears=[['Sep03ActivePass',2003],['Oct12Stephenson',2012]]
    SelectedTranChar=['SubSampleLocation','Year','SubArea','SurveyTitle']
    test=MetaTransectClass(ODB,SelectedSurveyYears,SelectedTranChar,CalcAllo=False)    
    print(test.key)
    for t in test.Allo:print (t.intcpt)
    print('\n')
    for t in test.TranClass:print (t)
    print('\n')
    print ('test.nclass',test.nclass)
    for t in range(test.nclass):print (test.FormatTranClass(t))

    print ('done Define Classes')
