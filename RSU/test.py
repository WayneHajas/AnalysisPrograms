import os,sys
import win32com.client
from ADOX import Catalog as cat

databasepath='d:/scratch/test.mdb'
SQL_query='select * from Results_SurveyUsed;'


oRS=None #Will be given a value when an query is submitted
Nrec=None
#
oConn = win32com.client.Dispatch('ADODB.Connection')
oConn.ConnectionString = "Provider=Microsoft.ACE.OLEDB.12.0;Data source="+databasepath+";"
oConn.Open()
#oConn.CreateQueryDef('testQuer',SQL_query)


cat.ActiveConnection=oConn
cat.Views.Append('testQuer',SQL_query)


oRS = win32com.client.Dispatch('ADODB.Command')
oRS.ActiveConnection = oConn    # Set the recordset to connect thru oConn
oRS.CommandText = SQL_query        
oRS.Execute()

print(dir(oRS))
oRS.CreateQueryDef('testQuer',SQL_query)
oRS.Execute()