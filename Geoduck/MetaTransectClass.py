'''2015-11-17.  Modified MetaTransectClass.QueryTranClass to ensure that 
transects will always be orderd by Headers.key

2016-04-19
    Require that SiteAnalysisData.AnalyzeSite is a transect-characterisic.  
'''

from numpy import ndarray
from numpy import iinfo,int16
MinInt=iinfo(int16).min
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from ADO import adoBaseClass as OpenDB

class MetaTransectClass:
    def __init__(self,ODB,SelectedSurveyYears):
        '''MetaTransectClass(SelectedSurveyYears)

          ODB is an ADO connection to a database
          SelectedSurveyYears are the cominations of Location and Year
          SelectedTranChar are fixed at ['Project','Year','Site']
          stics that are supposed to be used

          All the information you need to generate a full transect class!
          '''
        self.SelectedSurveyYears=SelectedSurveyYears
        self.ODB=ODB
        self.SelectedTranChar=['GeographicArea','SurveyTitle','Year','SurveySite']
        self.nchar=len(self.SelectedTranChar)
        
        self.WhereSurveyYear()
        self.DefineTranClass()
        
        #Logical array to indicate which sites are supposed to be used in overall statistics
        self.AnalyzeSite=[ t['AnalyzeSite'] for t in self.TranClass ]

        
    def WhereSurveyYear(self):
        CurSurvey=self.SelectedSurveyYears[0]
        self.SpecSurvey =' ('
        self.SpecSurvey+='((Headers.Year='
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
            self.TranClass=[[{'AllKey':self.GetKey()}]]
            self.nclass=1

            
        query ='SELECT DISTINCT Headers.'
        query+=self.SelectedTranChar[0]
        for stc in self.SelectedTranChar[1:]:
            query+=', Headers.'
            query+=stc
            query+='  '
        query+=',SiteAnalysisData.AnalyzeSite '
        query+='  FROM SiteAnalysisData INNER JOIN (Density INNER JOIN Headers ON Density.HKey = Headers.Key) ON '
        query+='        (SiteAnalysisData.SurveySite = Headers.SurveySite) AND '
        query+='        (SiteAnalysisData.SurveyTitle = Headers.SurveyTitle) AND '
        query+='        (SiteAnalysisData.Year = Headers.Year) '
        
        query+='  Where( '
        query+=self.SpecSurvey
        query+=' );'
        try:
            self.ODB.execute(query)
            TabTranClass=self.ODB.GetALL()
        except:
            print('\nMetaTransectClass 68')
            print('query',query)
            self.ODB.execute(query)
            TabTranClass=self.ODB.GetALL()
            return
        self.nclass=len(TabTranClass)

        #A list of dictionaries will define the classes of transect
        self.TranClass=[]
        for i in range(self.nclass):
            CurClass={}
            for j in range(self.nchar):
                CurClass[self.SelectedTranChar[j]]=TabTranClass[i][j]
            CurClass['AnalyzeSite']= (TabTranClass[i][-1]!='n')&(TabTranClass[i][-1]!='N')
            self.TranClass.append(CurClass)
            self.TranClass[-1]['AllKey']=self.GetKey(i=i)
           
                 

    def FormatTranClass(self,index):
        '''Essentially converts the information into a dictionary'''
        CurSpec=self.TranClass[index]

        #Default Values
        result={'SurveyTitle':'Combined','GeographicArea':'Combined','SurveySite':MinInt,\
                'Year':MinInt,'NumTran':MinInt,'NumQuad':MinInt}
        for c in range(len(self.SelectedTranChar)):
            try:
                if self.SelectedTranChar[c]=='GeographicArea':
                    result['GeographicArea']=CurSpec['GeographicArea']
                elif self.SelectedTranChar[c]=='SurveyTitle':
                    result['SurveyTitle']=CurSpec['SurveyTitle']
                elif self.SelectedTranChar[c]=='SurveySite':
                    result['SurveySite']=CurSpec['SurveySite']
                elif self.SelectedTranChar[c]=='Year':
                    result['Year']=CurSpec['Year']
            except:
                print('MetaTransectClass 104')
        result['Key']=self.TranClass[index]['AllKey']
        result['NumTran']=len(result['Key'])
        return(result)
            
        

    def SpecClass(self,index):
        CurSpec=self.TranClass[index]
        CharName=list(CurSpec.keys())

        CurCharName=CharName[0]
        if CurCharName=='AllKey':return(None)
        query='( ( Headers.'+CurCharName
        value=CurSpec[CurCharName]
        if value==None:
            query+=        " is Null ) "
        elif isinstance(value,str):
            query+=        "='"+value+"' ) "
        elif isinstance(value,(int,float)):
            query+=        "="+str(value)+" ) "
        else:
            print('\nMetaTransectClass 119\nCould not figure it out')
            print('\nCurCharName',CurCharName)
            print('\nvalue',value)
            print('\nself.TranClass',self.TranClass)

       
            
        for CurCharName in list(filter(lambda x:x!='AllKey',CharName[1:])):
            query+='and ( Headers.'+CurCharName
            value=CurSpec[CurCharName]
            if value==None:
                query+=        " is Null ) "
            elif isinstance(value,str):
                query+=        "='"+value+"' ) "
            elif isinstance(value,(int,float)):
                query+=        "="+str(value)+" ) "
            else:
                print('MetaTransectClass 135\nCould not figure it out')
                print('CurCharName',CurCharName)
                print('CharName',CharName)
                print('value',value)
        query+= ")"
        return(query)
        

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
        result=result.replace('Headers.Location','Headers.SurveyTitle')
        result=result.replace('Headers.SubSampleLocation','Headers.SurveySite')
        return(result)

        

    def QueryTranClass(self,i):
        query ='Select distinct Headers.Key, Headers.Transect '
        query+='FROM Density INNER JOIN Headers ON Density.HKey = Headers.Key '
        query+='Where( '
        query+=self.SpecSurvey
        if self.nclass>1:
            SC=self.SpecClass(i)
            if SC!=None:
              query+=' and '
              query+=self.SpecClass(i)
        query+=') order by Headers.Key ;'
        return(query)

    def GetKey(self,i=None):
        if i==None:return(list(map(lambda i:self.GetKey(i=i),range(self.nclass))))
        if isinstance(i, (list,ndarray)): return(list(map(lambda j:self.GetKey(i=j),i)))
        query=self.QueryTranClass(i)
        try:
            self.ODB.execute(query)
            result=self.ODB.GetALL()
        except:
            print('MetaTransectClass 180')
            print ('i',i)
            print ('query',query)
            print('self.TranClass[i]',self.TranClass[i])
            self.ODB.execute(query)
            result=self.ODB.GetALL()

        return(result)

    def GetChar(self,index,CharName):
        '''Gets value corresponding to an index and the name of a charcteristic'''
        try:
            CurSpec=self.TranClass[index]
        except:
            print('MetaTransectClass 198')
            print('index is ',index)
            print('Maximum value is ',-1+len(self.TranClass))
            return(None)
        try:
            return(CurSpec[CharName])
        except:
            print('MetaTransectClass 205')
            print('CharName is ',CharName)
            print('Possible values are ',CurSpec.key())
            return(None)

    def GetUniqueVal(self,CharName):
        AllVal=list(map(lambda x:x[CharName],self.TranClass))
        AllVal=uniq(AllVal)
        if len(AllVal)==1:return(AllVal[0])

        AllVal.sort()
        if isinstance(AllVal[0],(int,float)):return(MinInt)
        result=','.join(AllVal) #assuming we have strings
        return(result)
        
     
  

 
def uniq(input):
  output = []
  for x in input:
    if x not in output:
      output.append(x)
  return output
             
        

if __name__ == "__main__":

    databasepath='H:\AnalysisPrograms2013\PyFunctions\Geoduck\SampleData\Geoduck_Bio.mdb'
    ODB=OpenDB(databasepath)
    
    SelectedSurveyYears=[['Principe Channel, 2012',2012],['West Laredo Channel, 2012',2012]]


    test=MetaTransectClass(ODB,SelectedSurveyYears)
    print('test.TranClass[0]', test.TranClass[0])
    print('test.TranClass[1]', test.TranClass[1])
    print('test.GetChar(0,"SurveyTitle")  ', test.GetChar(0,"SurveyTitle") )

    print('Done MetaTransectClass')
