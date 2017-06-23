'''A program to copy data from a Cuke-biodatabase to a new database.
The data to copy will be specified according to SurveyTitle and Year.

Data will be copied from the following tables:
    Headers
    Density
    SF
    
The same table-structure will be used in the new-copy of the data as in the sourc-copy.
The new database will be useable as a data-source for the cuke-Analysis Program.

It is anticipated that eventually, this functionality will be incorporated into the cuke analysis program.'''

import sys,os

sys.path.append('D:\Coding\AnalysisPrograms2013\Fossil\working\RSU')
from NewMDB import NewMDB   


sys.path.append('D:\Coding\AnalysisPrograms2013\Fossil\working\common')
from CopyHeaders import SourceTables 
from ADO import adoBaseClass as OpenDB


def CopyMDB(SourceMDB,newmdb,LocationYear):
    
    
    #Do the Headers next
    
    oHeaders=SourceTables(SourceMDB,TableName='Headers',keyName=['Location','Year'] )
    oHeaders.CreateHeadersTable(newmdb)
    oHeaders.CopyRecordToNew(newmdb,key=LocationYear)
    #Add a record of NULLs because sometimes the last record disappears from the table.
    oHeaders.AppendNullRecord(newmdb)
    
    #Get the key-values
    keys=oHeaders.GetVariable('Key')
    
    #Start the new tables for Density and SF
    oDensity=SourceTables(SourceMDB,TableName='Density',keyName='HKey')
    oDensity.CreateHeadersTable(newmdb)
    oSF=SourceTables(SourceMDB,TableName='SF',keyName='HKey')
    oSF.CreateHeadersTable(newmdb)
      
    #Disection, SF and Density data are written transect-by-transect
    for k in keys:
        oDensity.CopyRecordToNew(newmdb,key=k)    
        oSF.CopyRecordToNew(newmdb,key=k)  
    
    #Add a record of NULLs because sometimes the last record disappears from the table.
    oDensity.AppendNullRecord(newmdb)
    oSF.AppendNullRecord(newmdb) 

if __name__ == "__main__":
    
    
    databasepath='t:\\RedUrchin_Bio.mdb'
    SourceMDB=OpenDB(databasepath)   
    
    OUTmdbName='H:\\scratch\\RedSample.mdb'
    if os.path.exists (OUTmdbName):os.remove (OUTmdbName)
    newmdb=NewMDB(OUTmdbName)
    
    #Indicate specific surveys through a list of dictionaries
    LocationYear=[\
        {'Location':'Bamfield','Year':2013},\
        {'Location':'Louise Island','Year':2012},\
        {'Location':'Louise Island','Year':2013},\
        {'Location':'Okisollo Channel','Year':2012},\
        {'Location':'Tofino','Year':2012},\
        {'Location':'Hippa Island','Year':2014},\
        {'Location':'Carpenter Bay','Year':2014}]
        

        
    CopyMDB(SourceMDB,newmdb,LocationYear)
    del newmdb