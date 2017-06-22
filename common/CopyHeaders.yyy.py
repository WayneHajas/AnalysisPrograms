from numpy import ndarray
from ADO import adoBaseClass as OpenDB
from FieldTypeIndex import GetTextCode

class OldHeaders(OpenDB):
    def __init__(self, databasepath,keyName='key',keys=None):
        '''OldHeaders(databasepath,keyName='key')
        'keyName' is the name of the key-field in the Headers Table
        Inherits from adoBaseClass.
        Specialized to facilitate the copying of information from the Headers Table in one of the biodata databases.
        '''
        self.keyName=keyName        
        self.keys=keys
 
        WhereQuery=self.BuildWhereQuery()
        SQL_query='Select * from Headers '+WhereQuery+';'
        super().__init__(databasepath,SQL_query=SQL_query)
        self.DefineFieldType()
        self.DefineFieldSize()
        self.nField=len(self.Fname)
        
    def BuildWhereQuery(self):
        '''No key-values specified'''        
        if self.keys==None:
            return('')
        '''A single key-value specified'''
        if isinstance(self.keys,(str,float,int)):
            result= ' Where ( Headers.'+self.keyName+'='+str(int(self.keys))+' ) '
            return(result)
        '''An array or list of values'''
        result =' Where ( '
        result+=    '( Headers.'+self.keyName+'='+str(int(self.keys[0]))+' ) '
        for k in self.keys[1:]:
            result+=    'or ( Headers.'+self.keyName+'='+str(int(k))+' ) ' 
        result+= ') '
        return(result)
    
    def DefineFieldType(self):
       'Get field types and put them in a list'
       try:
           self.Type=[f.Type for f in self.rs.Fields]
       except:
           print('CopyHeaders line 40')
           self.Type=[f.Type for f in self.rs.Fields]
    
       return       
    def DefineFieldSize(self):
       'Get field types and put them in a list'
       try:
           self.Size=[f.DefinedSize for f in self.rs.Fields]
       except:
           print('CopyHeaders line 49')
           self.Size=[f.DefinedSize for f in self.rs.Fields]
    
       return       
     
    def GetValuesAsChar(self, key=None):
         if self.Nrec==0:
             return([])
         if (key==None) :
             result=self.GetALL()
             return(result)
         if isinstance(key,(list,ndarray)):
            result=list(map(lambda k:self.GetValuesAsChar(key=k)     ,key ))
            return(result)
        
         strkey=str(key)
         keyindex=list(filter(lambda i:self.Fname[i]==self.keyName    ,range(len(self.Fname))))[0]
         self.rs.MoveFirst()
         while(not(self.rs.EOF )):
            test=self.Get()
            if str(test[keyindex])==strkey:
                for i in range(len(test)): 
                    if test[i]==None:
                        test[i]=''
                    else:
                        test[i]=str(test[i])
                return(test)
         return([])
 
    def CreateHeadersTable(self, DestinyMDB):
        '''OldHeaders.CreateHeadersTable(DestinyMDB)
        DestinyMDB is a connection to the database that is going to get a HeadersTable'''
        chType=GetTextCode(self.Type)        
        
        CreateStatement ='Create TABLE Headers( '
        for i in range(self.nField-1):
            CreateStatement+= '['+self.Fname[i]+ '] '+chType[i]+', '
        i=self.nField-1
        CreateStatement+= '['+self.Fname[i]+ '] '+chType[i]+') '        
        
        try:
            DestinyMDB.DB.Execute(CreateStatement )
        except:
            print ('CopyHeaders line 95\n',CreateStatement)
            DestinyMDB.DB.Execute(CreateStatement )            


 
    def CopyRecordToNew(self,DestinyMDB,keys):
        '''Any values stored as time in the original table will appear as NULL in the new table.
        A lot of finicky syntax would be required to copy over the time-values.  I just didn't think it was worth the effort at this time.'''
        if isinstance(keys,(list,ndarray)):
            for k in keys:
                self.CopyRecordToNew(DestinyMDB,k)
            return
        chValues=self.GetValuesAsChar(keys)
        if chValues==[]: 
            return
        query ='insert into '+self.TableName+ '(['+self.Fname[0]+']'
        for fn in self.Fname[1:]:
            query+=',['+fn+']'
        query+=') '
        query+='values( '+chValues[0]
        for chv in chValues[1:]:
            query+=','+chv
        query+=' );'    
        
        try:
            DestinyMDB.DB.Execute(query )
        except:
            print ('CopyHeaders line 116\n',query)
            DestinyMDB.DB.Execute(query )            
        
        
        
               
        
        
   
        
if __name__ == "__main__":
    databasepath='D:\scratch\RedUrchin_Bio.mdb'
    
    x=test5.GetValuesAsChar(339)
    y=test5.Type
    z=test5.Fname
    w=test5.Size
    for i in range(len(x)):
        print(z[i],y[i],x[i],w[i])
    sys.path.append()