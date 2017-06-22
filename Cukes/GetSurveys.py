import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from ADO import adoBaseClass as OpenDB
 
class AllSurveys:
    def __init__(self,ODB):
        '''AllSurveys(ODB)
        ODB (open database) is an instance of the ADO class'''

        self.ODB=ODB
        query ="SELECT DISTINCT Headers.Project as SurveyTitle, Headers.Year "
        query+="FROM Headers "
        query+="WHERE ( "
        query+="((Headers.Project) Is Not Null)  "
        query+="AND ((Headers.Year) Is Not Null) "
        query+=") "
        query+="ORDER BY Headers.Project, Headers.Year;"
        try:
            self.ODB.execute(query)
        except:
            print('GetSurveys 21\n query')
            print(query)
    def GetSurvey(self):
        result=self.ODB.GetVariable('SurveyTitle')
        return(result)
    def GetYear(self):
        result=self.ODB.GetVariable('Year')
        return(result)
    
    def GetCombo(self):
        result=list(map(lambda x:x[0]+' '+str(x[1]), self.ODB.GetALL()))
        return(result)
if __name__ == "__main__":
    databasepath='h:\SampleMDB\SeaCuke_Bio_97_NoLink.mdb'
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
    
