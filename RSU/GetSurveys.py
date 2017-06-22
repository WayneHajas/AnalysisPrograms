import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from ADO import adoBaseClass as OpenDB
 
class AllSurveys:
    def __init__(self,ODB):
        '''AllSurveys(ODB)
        ODB (open database) is an instance of the ADO class'''

        self.ODB=ODB
        query ="SELECT DISTINCT Headers.SurveyTitle as SurveyTitle "
        query+="FROM Headers "
        query+="WHERE ( "
        query+="((Headers.SurveyTitle) Is Not Null)  "
        query+=") "
        query+="ORDER BY Headers.SurveyTitle;"
        self.ODB.execute(query)
        self.SurveyTitle=self.ODB.GetVariable('SurveyTitle')
    def GetSurvey(self):
        result=self.SurveyTitle
        return(result)
if __name__ == "__main__":
    databasepath='h:\SampleMDB\GreenUrchin_NoLink.mdb'
    ODB=OpenDB(databasepath)

    AS=AllSurveys(ODB)
    Survey=AS.GetSurvey()
    print('survey')
    for x in Survey:print(x)
    
    y=AS.GetYear()
    print('year')
    for x in y:print(x)
    
    c=AS.GetCombo()
    print('combo')
    for x in c:print(x)
    
