'''A program to copy data from a Cuke-biodatabase to a new database.
The data to copy will be specified according to SurveyTitle and Year.

Data will be copied from the following tables:
    Headers
    Density
    Dissection
    SF
    
The same table-structure will be used in the new-copy of the data as in the sourc-copy.
The new database will be useable as a data-source for the cuke-Analysis Program.

It is anticipated that eventually, this functionality will be incorporated into the cuke analysis program.'''

import sys,os


sys.path.append('D:\Coding\AnalysisPrograms2013\Fossil\working\common')
from CopyHeaders import SourceTables 
from ADO import adoBaseClass as OpenDB

sys.path.append('D:\Coding\AnalysisPrograms2013\Fossil\working\GSU')
from NewMDB import NewMDB   



def CopyMDB(SourceMDB,newmdb,SurveyYear):
    
    
    #Do the Headers next
    
    oHeaders=SourceTables(SourceMDB,TableName='Headers',keyName=['SurveyTitle','Year'] )
    oHeaders.CreateHeadersTable(newmdb)
    oHeaders.CopyRecordToNew(newmdb,key=SurveyYear)
    #Add a record of NULLs because sometimes the last record disappears from the table.
    oHeaders.AppendNullRecord(newmdb)
    
    #Get the key-values from the new Headers-table
    keys=oHeaders.GetVariable('Key')
    
    #Start the new tables for Density and Dissection and SF
    oDensity=SourceTables(SourceMDB,TableName='Density',keyName='HKey')
    oDensity.CreateHeadersTable(newmdb)
    oDissection=SourceTables(SourceMDB,TableName='Dissection',keyName='HKey')
    oDissection.CreateHeadersTable(newmdb)
    oSF=SourceTables(SourceMDB,TableName='SF',keyName='HKey')
    oSF.CreateHeadersTable(newmdb)
      
    #Disection, SF and Density data are written transect-by-transect
    for k in keys:
        oDensity.CopyRecordToNew(newmdb,key=k)    
        oDissection.CopyRecordToNew(newmdb,key=k)    
        oSF.CopyRecordToNew(newmdb,key=k)  
    
    #Add a record of NULLs because sometimes the last record disappears from the table.
    oDensity.AppendNullRecord(newmdb)
    oDissection.AppendNullRecord(newmdb)
    oSF.AppendNullRecord(newmdb)

if __name__ == "__main__":
    
    
    databasepath='d:\\scratch\\CopyGreenUrchin_Bio.mdb'
    databasepath='d:\\scratch\\ORI.mdb'
    SourceMDB=OpenDB(databasepath)   
    
    OUTmdbName='d:\\scratch\\ORI.mdb'
    OUTmdbName='d:\\scratch\\test.mdb'
    if os.path.exists (OUTmdbName):os.remove (OUTmdbName)
    newmdb=NewMDB(OUTmdbName)
    
    #Indicate specific surveys through a list of dictionaries
    SurveyYear=[\
        {'SurveyTitle':'Nov04Stephenson','Year':2004},\
        {'SurveyTitle':'Oct12Stephenson','Year':2012},\
        {'SurveyTitle':'Mar14FulfordReef','Year':2014}]
        
    CopyMDB(SourceMDB,newmdb,SurveyYear)
    del newmdb