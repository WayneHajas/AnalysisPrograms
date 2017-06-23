'''A program to copy data from a Cuke-biodatabase to a new database.
The data to copy will be specified according to Project and Year.

Data will be copied from the following tables:
    Headers
    Densities
    
The same table-structure will be used in the new-copy of the data as in the sourc-copy.
The new database will be useable as a data-source for the cuke-Analysis Program.

It is anticipated that eventually, this functionality will be incorporated into the cuke analysis program.'''

from NewMDB import NewMDB   

import sys
sys.path.append('..\common')
from CopyHeaders import OldHeaders,KeyFromHeaders,SourceTables 
from ADO import adoBaseClass as OpenDB


def CopyMDB(SourceMDB,newmdb,ProjectYear):
    
    
    #Do the Headers next
    
    oHeaders=SourceTables(SourceMDB,TableName='Headers',keyName=['Project','Year'] )
    oHeaders.CreateHeadersTable(newmdb)
    oHeaders.CopyRecordToNew(newmdb,key=ProjectYear)   
    #Add a record of NULLs because sometimes the last record disappears from the table.
    oHeaders.AppendNullRecord(newmdb)
    
    #Get the key-values from 
    keys=oHeaders.GetVariable('Key')
    
    #Start the new tables for Densities and ShowFactor
    oDensities=SourceTables(SourceMDB,TableName='Densities',keyName='HKey')
    oDensities.CreateHeadersTable(newmdb)
      
    #Densities data are written transect-by-transect
    for k in keys:
        oDensities.CopyRecordToNew(newmdb,key=k)    
    #Add a record of NULLs because sometimes the last record disappears from the table.
    oDensities.AppendNullRecord(newmdb)

if __name__ == "__main__":
    
    import os
    databasepath='t:\\SeaCuke_Bio.mdb'
    SourceMDB=OpenDB(databasepath)   
    
    OUTmdbName='d:\\scratch\\test.mdb'
    if os.path.exists (OUTmdbName):os.remove (OUTmdbName)
    newmdb=NewMDB('d:/scratch/test.mdb')
    
    #Indicate specific surveys through a list of dictionaries
    ProjectYear=[\
        {'Project':'Laredo Channel','Year':2013},\
        {'Project':'Sidney Sooke','Year':2014}]
        #,\
        #{'Project':'Gardner Canal','Year':2014}]
        
    CopyMDB(SourceMDB,newmdb,ProjectYear)