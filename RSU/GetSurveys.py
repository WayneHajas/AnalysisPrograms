import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from ADO import adoBaseClass as OpenDB
 
class AllSurveys:
    def __init__(self,ODB):
        '''AllSurveys(ODB)
        ODB (open database) is an instance of the ADO class'''

        self.ODB=ODB
        query ="SELECT DISTINCT Headers.Source,Headers.Year,Headers.Location  "
        query+="FROM Headers "
        query+="WHERE ( "
        query+="((Headers.Location) Is Not Null)  "
        query+="AND ((Headers.Year) Is Not Null) "
        query+=") "
        query+="ORDER BY Headers.Source,Headers.Location , Headers.Year;"
        self.ODB.execute(query)

    def GetSurvey(self):
        result=self.ODB.GetVariable('Location')
        return(result)
    def GetYear(self):
        result=self.ODB.GetVariable('Year')
        return(result)
    
    def GetCombo(self):
        result=list(map(lambda x:x[0]+' '+str(x[1])+' '+x[2], self.ODB.GetALL()))
        if len(result)==0:
        
        	print('GetSurveys 30\nNo Surveys Found')
	        
	        print('\nself.ODB.GetALL() is: \n', self.ODB.GetALL())
	        result=list(map(lambda x:x[0]+' '+str(x[1])+''+x[2], self.ODB.GetALL()))
        
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
    
