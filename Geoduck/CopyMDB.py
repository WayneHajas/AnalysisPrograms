'''A program to copy data from a geoduck-biodatabase to a new database.
The data to copy will be specified according to SurveyTitle and Year.

Data will be copied from the following tables:
    Headers
    Density
    ShowFactor
    SiteAnalysisData
    SiteSummary
    
The same table-structure will be used in the new-copy of the data as in the sourc-copy.
The new database will be useable as a data-source for the Geoduck-Analysis Program.

It is anticipated that eventually, this functionality will be incorporated into the geoduck analysis program.'''

import sys,os

sys.path.append('D:\Coding\AnalysisPrograms2013\Fossil\working\Geoduck')
from NewMDB import NewMDB   


sys.path.append('D:\Coding\AnalysisPrograms2013\Fossil\working\common')
from CopyHeaders import OldHeaders,KeyFromHeaders,SourceTables 
from ADO import adoBaseClass as OpenDB


def CopyMDB(SourceMDB,newmdb,SurveyYear):
    
    #SiteAnalysisData and SiteSummary don't have any keys to link them to other tables.  Use SurveyTitle and Year directly
    oSiteAnalysisData=SourceTables(SourceMDB,TableName='SiteAnalysisData',keyName=['SurveyTitle','Year'] )
    oSiteAnalysisData.CreateHeadersTable(newmdb)
    oSiteAnalysisData.CopyRecordToNew(newmdb,key=SurveyYear)  
    #Add a record of NULLs because sometimes the last record disappears from the table.
    oSiteAnalysisData.AppendNullRecord(newmdb)
    
    oSiteSummary=SourceTables(SourceMDB,TableName='SiteSummary',keyName=['SurveyTitle','Year'] )
    oSiteSummary.CreateHeadersTable(newmdb)
    oSiteSummary.CopyRecordToNew(newmdb,key=SurveyYear) 
    #Add a record of NULLs because sometimes the last record disappears from the table.
    oSiteSummary.AppendNullRecord(newmdb)
    
    #Do the Headers next
    
    oHeaders=SourceTables(SourceMDB,TableName='Headers',keyName=['SurveyTitle','Year'] )
    oHeaders.CreateHeadersTable(newmdb)
    oHeaders.CopyRecordToNew(newmdb,key=SurveyYear)
    #Add a record of NULLs because sometimes the last record disappears from the table.
    oHeaders.AppendNullRecord(newmdb)
    
    #Get the key-values 
    keys=oHeaders.GetVariable('Key')
    
    #Start the new tables for Density and ShowFactor
    oDensity=SourceTables(SourceMDB,TableName='Density',keyName='HKey')
    oDensity.CreateHeadersTable(newmdb)
    
    oShowFactor=SourceTables(SourceMDB,TableName='ShowFactor',keyName='HKey')
    oShowFactor.CreateHeadersTable(newmdb)
    
    #ShowFactor and Density data are written transect-by-transect
    for k in keys:
        oDensity.CopyRecordToNew(newmdb,key=k)    
        oShowFactor.CopyRecordToNew(newmdb,key=k)
    #Add a record of NULLs because sometimes the last record disappears from the table.
    oDensity.AppendNullRecord(newmdb)
    oShowFactor.AppendNullRecord(newmdb)

if __name__ == "__main__":
    
    
    databasepath='t:\Geoduck_Bio.mdb'
    SourceMDB=OpenDB(databasepath)   
    
    OUTmdbName='d:\scratch\FromCopyMDB.mdb'
    if os.path.exists (OUTmdbName):os.remove (OUTmdbName)
    newmdb=NewMDB(OUTmdbName)
    
    #Indicate specific surveys through a list of dictionaries
    
    SurveyYear=[\
        {'SurveyTitle':'Flamingo and Louscoone Inlets','Year':2013}]
    CopyMDB(SourceMDB,newmdb,SurveyYear)