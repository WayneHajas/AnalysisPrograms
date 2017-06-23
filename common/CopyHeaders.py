'''
2015-11-23. Created and applied BuildOrderByQuery.  Now there is a specific order to results.


2015-04-29.  Modified BuildWhereQuery to accomodate keyName as an array'''

from numpy import ndarray
from ADO import adoBaseClass as OpenDB
from FieldTypeIndex import GetTextCode
from PrepForMDB import PrepForMDB
import gc

class OldHeaders(OpenDB):
    def __init__(self, databasepath,TableName='Headers',keyName='key'):
        '''OldHeaders(databasepath,TableName='Headers',keyName='key')
        'keyName' is the name of the key-field in the Headers Table
        Inherits from adoBaseClass.
        Specialized to facilitate the copying of information from one Table to another.
        Developed specifically for the Headers-tables - but should be more flexible than that.
        '''
        self.TableName=TableName        
        
        #Force square brackets to make the sql-commands more robust        
        if self.TableName[0]!='[':
            self.TableName='['+self.TableName
        if self.TableName[-1]!=']':
            self.TableName=self.TableName+']'
        self.keyName=keyName        
        self.keys=None

        self.keyName=keyName        
        self.keys=None
 
        WhereQuery=self.BuildWhereQuery()
        SQL_query='Select * from '+self.TableName +' '+WhereQuery+';'
        super().__init__(databasepath,SQL_query=SQL_query)
        self.DefineFieldType()
        self.DefineFieldSize()
        self.nField=len(self.Fname)

    def BuildOrderByQuery(self):
        if (self.keyName is None) or (self.keyName=='')or (self.keyName==[]):
            return('')
        
        if (isinstance(self.keyName,str)):
            result=' order by '+self.TableName+'.'+self.keyName+' '
            return(result)
        
        if (isinstance(self.keyName,(list,ndarray))):
            result=' order by '+self.TableName+'.'+self.keyName[0]+' '
            for k in self.keyName[1:]:
                result+=', '+k+' '
            return(result)
            

    
    def BuildCase(self,PreppedValues,keyName):
        
         #Selection by just one field
        if isinstance(PreppedValues,str) :  
            result= ' ( '+self.TableName+'.'+keyName+' = '+PreppedValues +' ) '
            return(result)   
            
        #A dictionary indicates that multiple fields are to be used to define a case    
        if isinstance(PreppedValues,dict):
            ByField=list(map(lambda kN:self.BuildCase(PreppedValues[kN],kN)  ,keyName))
            result='('+ ' and '.join(ByField)  +')'
            return(result)
        
        #Catch an error
        print('\ncopyheaders 14  keyname\n',keyname,'\nPreppedValues',PreppedValues)
    
    def BuildWhereQuery(self):
        '''No key-values specified'''        
        if self.keys==None:
            return('')
            
        PreppedValues=PrepForWhereQuery(self.keys)    
        
        result='Where( '
        
        #A single allowable state
        if isinstance(PreppedValues,(dict,str)) :
            result+=self.BuildCase(PreppedValues,self.keyName) +' ) '
            return (result)
        
        #Multiple allowed stats
        PossState=list(map(lambda t: self.BuildCase(t,self.keyName)   ,PreppedValues))
        result+= ' or '.join(PossState) + ' ) '
        return(result)
            
      
        
    def SetKeys(self,keys): 
        '''Execute query to get targetted records'''
        self.keys=keys 
        WhereQuery=self.BuildWhereQuery()
        OrderByQuery=self.BuildOrderByQuery()
        SQL_query='Select * from '+self.TableName +' '+WhereQuery+' '+OrderByQuery+';'  
        self.execute(SQL_query)
    
    def DefineFieldType(self):
       'Get field types and put them in a list'
       try:
           self.Type=[f.Type for f in self.rs.Fields]
       except:
           print('CopyHeaders line 40')
           self.Type=[f.Type for f in self.rs.Fields]
    
       return       
    def DefineFieldSize(self):
       'Get field sizes and put them in a list'
       try:
           self.Size=[f.DefinedSize for f in self.rs.Fields]
       except:
           print('CopyHeaders line 49')
           self.Size=[f.DefinedSize for f in self.rs.Fields]
    
       return       
     
    def GetValuesAsChar(self, key=None):
         '''OldHeaders.GetValuesAsChar(self, key)'''
         
         #Revise the current query to reflect the current keys
         self.SetKeys(key)
         if self.Nrec==0:
             return([])
          
         #All relevent records
         result=[]             
         self.rs.MoveFirst()
         while(not(self.CheckEOF() )):
            CurRec=self.Get()
            CurAsChar=PrepForMDB(CurRec)
            result+=[CurAsChar] 
         #self.close()
         return(result)
         
    def CheckEOF(self): 
        return(self.rs.EOF)
        
    def CreateHeadersTable(self, DestinyMDB):
        '''OldHeaders.CreateHeadersTable(DestinyMDB)
        DestinyMDB is a connection to the database that is going to get a HeadersTable'''
        chType=GetTextCode(self.Type)        
        
        CreateStatement ='Create TABLE '+self.TableName+'( '
        for i in range(self.nField-1):
            CreateStatement+= '['+self.Fname[i]+ '] '+chType[i]+', '
        i=self.nField-1
        CreateStatement+= '['+self.Fname[i]+ '] '+chType[i]+') '        
        
        try:
            DestinyMDB.DB.Execute(CreateStatement )
        except:
            print ('CopyHeaders line 95\n',CreateStatement)
            DestinyMDB.DB.Execute(CreateStatement )            
    
    
    def AppendNullRecord(self,DestinyMDB):
        '''OldHeaders.AppendNullRecord(DestinyMDB)
        
        Final written record occasionally gets lost. Put a record of nulls in
        so that useful data is kept.'''
            
        query ='insert into '+self.TableName+ '(['+self.Fname[0]+']'
        for fn in self.Fname[1:]:
            query+=',['+fn+']'
        query+=') '
        query+='values( NULL'
        for fn in self.Fname[1:]:
            query+=', NULL'
        query+=' );'
        DestinyMDB.DB.Execute(query )            
            
    def CopyRecordToNew(self,DestinyMDB,key=None):
        '''OldHeaders.CopyRecordToNew(DestinyMDB,key=None)
        
           copies records from current table to one in DestinyMDB.
           Table-name is the same in the destination-file as it is in the source table.
           
           key is used to specify the records to copy.  if key==None, then all records are copied.
           The field-name corresponding to key was specified in the initialization of OldHeaders.
           So far key has always corresponded to key-values of the database.  Should work with other datatypes.'''
           
        chValues=self.GetValuesAsChar(key=key)
        if chValues==[]: 
            return
           
        for chv in chValues:    
            query ='insert into '+self.TableName+ '(['+self.Fname[0]+']'
            for fn in self.Fname[1:]:
                query+=',['+fn+']'
            query+=') '
            try:
                query+='values( '+chv[0]
                for c in chv[1:]:
                    query+=','+c
                query+=' );'   
            except:
                print('\nCopyHeaders 123')
                query+='values( '+chv[0]
                for c in chv[1:]:
                    query+=','+c
                query+=' );'   
            
            try:
                DestinyMDB.DB.Execute(query )
            except:
                print ('CopyHeaders line 126\n',query)
                DestinyMDB.DB.Execute(query )            
  
class SourceTables(OldHeaders):
    '''This class is intended to work the same as OldHeaders except that a connnection to the data-source is given
       insted of the name of the data-file.'''
       
    def __init__(self,adodbConnect,TableName='Headers',keyName='key'):
        self.adodbConnect=adodbConnect
        self.TableName=TableName

        #Force square brackets to make the sql-commands more robust        
        if self.TableName[0]!='[':
            self.TableName='['+self.TableName
        if self.TableName[-1]!=']':
            self.TableName=self.TableName+']'
        self.keyName=keyName        
        self.keys=None
 
        WhereQuery=self.BuildWhereQuery()
        SQL_query='Select * from '+self.TableName +' '+WhereQuery+';'
        self.execute(SQL_query)
        self.rs=self.adodbConnect.rs   
        self.Get=self.adodbConnect.Get 
        self.GetVariable=self.adodbConnect.GetVariable
        
        self.DefineFieldType()
        self.DefineFieldSize()
        self.Fname=self.adodbConnect.Fname
        self.nField=len(self.Fname)
        
    def execute(self,SQL_query):
        self.adodbConnect.execute(SQL_query)
        self.Nrec=self.adodbConnect.Nrec
         
    def CheckEOF(self): 
        return(self.adodbConnect.rs.EOF)   
    def GetVariable(self,name):
        
        if not name in self.adodbConnect.rs.Fname:
            return (None)
        if (self.adodbConnect.rs.Nrec==0):return([])
        self.adodbConnect.rs.rs.MoveFirst()
        result=[]
        while(not(self.adodbConnect.rs.rs.EOF )):
            result+=[self.adodbConnect.rs.rs.Fields(name).Value]
            self.adodbConnect.rs.rs.MoveNext()
        self.adodbConnect.rs.rs.MoveFirst()
        return(result)
        

def KeyFromHeaders(databasepath,TableName='Headers',keyName='key'):      
     SQL_query='Select distinct ' + keyName+ ' from '+TableName +' order by '+keyName +' ;'
     
     #databasepath is a file name
     if isinstance(databasepath,str):
         SourceData=OpenDB(databasepath)
         SourceData.execute(SQL_query)
     #databasepath is NewMDB
     else:
         dbp=databasepath.OUTmdbName
         SourceData=OpenDB(dbp)
         SourceData.execute(SQL_query)
     
     result= SourceData.GetVariable(keyName)
     print('copyheaders 242', result)
     return(result)

        
def PrepForWhereQuery(orivalue):
    '''Change a data-value into something useable in the where-section of an sql-query'''
    
    #An array of values    
    if isinstance(orivalue,(list,ndarray)):
        result=list(map(lambda t:PrepForWhereQuery(t),orivalue  ))
        return(result)
    #A numerical value
    if isinstance(orivalue,(float,int)): 
        result=str(int(orivalue))
        return(result)
    #A string value
    if isinstance(orivalue,str): 
        result="'"+orivalue+"'"
        return(result)
    #A dictionary of values
    if isinstance(orivalue,dict): 
        result={}
        for t in orivalue.keys():
            result[t]=PrepForWhereQuery(orivalue[t])
        return(result)

        
        
if __name__ == "__main__":
    databasepath='t:\RedUrchin_Bio.mdb'
    
    test5=OldHeaders(databasepath,keyName='Key')    
    x=test5.GetValuesAsChar(339)
    y=test5.Type
    z=test5.Fname
    w=test5.Size
    for i in range(len(x)):
        print(z[i],y[i],x[i],w[i])
    import sys
    sys.path.append('d:\scratch')
    sys.path.append('../RSU')
    from NewMDB import NewMDB
    newmdb=NewMDB('d:/scratch/test.mdb')
    test5.CreateHeadersTable(newmdb)
    test5.CopyRecordToNew(newmdb,[332,333,366,13431,13391,13207,11974])
    del newmdb,test5