import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from ADO import adoBaseClass as OpenDB
import pdb
 
class AllSurveys:
    def __init__(self,ODB):
        '''AllSurveys(ODB)
        ODB (open database) is an instance of the ADO class'''

        self.ODB=ODB
        query ="SELECT DISTINCT Headers.SurveyTitle as SurveyTitle, Headers.Year "
        query+="FROM Headers "
        query+="WHERE ( "
        query+="((Headers.SurveyTitle) Is Not Null)  "
        query+="AND ((Headers.Year) Is Not Null) "
        query+=") "
        query+="ORDER BY Headers.SurveyTitle, Headers.Year;"
        try:
            self.ODB.execute(query)
        except:
            print('GetSurveys 23\n query')
            print(query)
    def GetSurvey(self):
        result=self.ODB.GetVariable('SurveyTitle')
        return(result)
    def GetYear(self):
        result=self.ODB.GetVariable('Year')
        return(result)
    
    def GetCombo(self):
        try:
            result=list(map(lambda x:x[0]+' '+str(x[1]), self.ODB.GetALL()))
        except:
            print('\nGetSurveys 34, self.ODB.GetALL()  ',self.ODB.GetALL() )
            result=list(map(lambda x:x[0]+' '+str(x[1]), self.ODB.GetALL()))
        return(result)
if __name__ == "__main__":
    databasepath='H:\AnalysisPrograms2013\PyFunctions\Geoduck\SampleAIP\Geoduck_Bio.mdb'
    ODB=OpenDB(databasepath)

    AS=AllSurveys(ODB)
    Survey=AS.GetSurvey()
    for x in Survey:print(x)
    
    y=AS.GetYear()
    print('year')
    for x in y:print(x)
    
    c=AS.GetCombo()
    print('combo')
    for x in c:print(x)
    
