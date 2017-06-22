# for column types, see http://www.w3schools.com/ado/ado_datatypes.asp
from numpy import ndarray
import os, sys
from win32com.client import Dispatch
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from KeyValues import MinInt,KeyValues

class NewMDB:
    def __init__(self,OUTmdbName,\
                 InitAnalysisKey=MinInt,\
                 InitTranCharKey=MinInt,\
                 InitSizeRangeKey=MinInt):

        if os.path.exists (OUTmdbName):os.remove (OUTmdbName)
        adox = Dispatch ("ADOX.Catalog")
        CONNECTION_STRING = "Provider=Microsoft.Jet.OLEDB.4.0; data Source=%s" % OUTmdbName
        try:
            adox.Create (CONNECTION_STRING)
        except:
            print('\nNewMDB 20,CONNECTION_STRING\n',CONNECTION_STRING)
            adox.Create (CONNECTION_STRING)
                  
        

        self.DB = Dispatch ('ADODB.Connection')
        self.DB.Open (CONNECTION_STRING)

        #self.DB=DB
        self.Create_Results_Analysis()
        self.Create_Results_ConfInterval()
        self.Create_Results_EstDens()
        self.Create_Results_SizeRange()
        self.Create_Results_TranChar()
        self.Create_Results_SurveyUsed()

        self.AnalysisKey=KeyValues(InitValue=InitAnalysisKey)
        self.TranCharKey=KeyValues(InitValue=InitTranCharKey)
        self.SizeRangeKey=KeyValues(InitValue=InitSizeRangeKey)

    def Create_Results_Analysis(self):
        CreateStatement ='Create TABLE Results_Analysis ('
        CreateStatement+='AnalysisKey LONG,'
        CreateStatement+='AnalysisDate TIME, '
        CreateStatement+='nReps INT, '
        CreateStatement+='rSeed INT, '
        CreateStatement+='MinDepth DOUBLE, '
        CreateStatement+='MaxDepth DOUBLE) '
        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print ('\nNewMDB line 51\n',CreateStatement)
            self.DB.Execute(CreateStatement )            

    def ADDTo_Analysis(self,nReps,rSeed,MinDepth,MaxDepth):
        query ="insert INTO Results_Analysis(AnalysisKey,AnalysisDate,nReps,rSeed,MinDepth,MaxDepth) "
        query+="Values("
        query+=str(self.AnalysisKey.GetValue())
        query+=","
        query+="NOW()"
        query+=","
        query+=str(nReps)
        query+=","
        query+=str(rSeed)
        query+=","
        query+=str(MinDepth)
        query+=","
        query+=str(MaxDepth)
        query+=");"
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 72 query\n',query)
            self.DB.Execute(query)
 
    def Create_Results_ConfInterval(self):
        CreateStatement ='Create TABLE Results_ConfInterval ('
        CreateStatement+='TranCharKey LONG,'
        CreateStatement+='SizeRangeKey LONG,'
        CreateStatement+='pcConfidenceLevel INT,'
        CreateStatement+='lowPopLinear DOUBLE, '
        CreateStatement+='uppPopLinear DOUBLE, '
        CreateStatement+='lowPopSpatial DOUBLE, '
        CreateStatement+='uppPopSpatial DOUBLE, '
        CreateStatement+='lowBmassLinear DOUBLE, '
        CreateStatement+='uppBmassLinear DOUBLE, '
        CreateStatement+='lowBmassSpatial DOUBLE, '
        CreateStatement+='uppBmassSpatial DOUBLE) '
        self.DB.Execute(CreateStatement )
        
    def ADDTo_ConfInterval(self,TranCharKey,SizeRangeKey,\
                           pcConfidenceLevel,\
                           lowPopLinear,    uppPopLinear,\
                           lowPopSpatial,   uppPopSpatial,\
                           lowBmassLinear,  uppBmassLinear,\
                           lowBmassSpatial, uppBmassSpatial):
        query ="insert INTO Results_ConfInterval(TranCharKey,SizeRangeKey,pcConfidenceLevel, "
        query+=     "lowPopLinear,    uppPopLinear, "
        query+=     "lowPopSpatial,   uppPopSpatial, "
        query+=     "lowBmassLinear,  uppBmassLinear, "
        query+=     "lowBmassSpatial, uppBmassSpatial) "
        query+="Values("
        query+=str(TranCharKey)
        query+=","
        query+=str(SizeRangeKey)
        query+=","
        query+=str(pcConfidenceLevel)
        query+=","
        query+=str(lowPopLinear)
        query+=","
        query+=                 str(uppPopLinear)
        query+=","
        query+=str(lowPopSpatial)
        query+=","
        query+=                 str(uppPopSpatial)
        query+=","
        query+=str(lowBmassLinear/1000.)
        query+=","
        try:
            query+=             str(uppBmassLinear/1000.)
        except:
            query+=             str(MinInt)
        query+=","
        try:
            query+=str(lowBmassSpatial/1000.)
        except:
            query+=str(MinInt)
        query+=","
        try:
            query+=             str(uppBmassSpatial/1000.)
        except:
            query+=             str(MinInt)

        query+=");"
        query=query.replace('None',str(MinInt))
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 119 query\n',query)
            self.DB.Execute(query)

    def Create_Results_EstDens(self):
        CreateStatement ='Create TABLE Results_EstDens ('
        CreateStatement+='TranCharKey LONG,'
        CreateStatement+='SizeRangeKey LONG,'
        CreateStatement+='PopLinear DOUBLE, '
        CreateStatement+='PopSpatial DOUBLE, '
        CreateStatement+='BmassLinear DOUBLE, '
        CreateStatement+='BmassSpatial DOUBLE) '
        self.DB.Execute(CreateStatement )

    def ADDTo_EstDens(self,PopLinear, PopSpatial,BmassLinear,BmassSpatial,TranCharKey=None,SizeKey=None):
        skey=SizeKey
        if skey==None:skey=self.SizeRangeKey.GetValue()
        tckey=TranCharKey
        if tckey==None:tckey=self.TranCharKey.GetValue()
        query ="insert INTO Results_EstDens(TranCharKey,SizeRangeKey, "
        query+=     "PopLinear,   PopSpatial, BmassLinear, BmassSpatial) "
        query+="Values("
        query+=str(tckey)
        query+=","
        query+=str(skey)
        query+=","
        query+=str(PopLinear)
        query+=","
        query+=str(PopSpatial)
        query+=","
        try:
            query+=str(BmassLinear/1000.)
        except:
            query+=str(MinInt)
        query+=","
        try:
            query+=str(BmassSpatial/1000.)
        except:
            query+=str(MinInt)
        query+=");"
        query=query.replace('None',str(MinInt))
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 181 query\n',query)
            self.DB.Execute(query)

        
    def Create_Results_SizeRange(self):
        CreateStatement ='Create TABLE Results_SizeRange ('
        CreateStatement+='AnalysisKey LONG,'
        CreateStatement+='SizeRangeKey LONG,'
        CreateStatement+='MinSize DOUBLE, '
        CreateStatement+='MaxSize DOUBLE) '
        self.DB.Execute(CreateStatement )
        self.SizeMap={}

    def ADDTo_SizeRange(self, MinSize,MaxSize):
        query ="insert INTO Results_SizeRange(AnalysisKey,SizeRangeKey, "
        query+=     "MinSize,MaxSize) "
        query+="Values("
        query+=str(self.AnalysisKey.GetValue())
        query+=","
        query+=str(self.SizeRangeKey.GetValue())
        query+=","
        query+=str(MinSize)
        query+=","
        query+=str(MaxSize)
        query+=");"
        query=query.replace('inf','1000')
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 187 query\n',query)
            self.DB.Execute(query)
        self.SizeMap[MaxSize]= self.SizeRangeKey.GetValue()

    def GetSizeRangeKey(self,MaxSize):
        if isinstance(MaxSize,(list,ndarray)):return(list(map(lambda ms:self.GetSizeRangeKey(ms),MaxSize)))
        result=self.SizeMap[MaxSize]
        return(result)

    def Create_Results_SurveyUsed(self):
        CreateStatement ='Create TABLE Results_SurveyUsed ('
        CreateStatement+='AnalysisKey LONG,'
        CreateStatement+='Location varchar,'        
        CreateStatement+='Yr INT );'        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print('\nNewMDB line 101 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement )

    def ADDTo_SurveyUsed(self, Location,Year):
        query ="insert INTO Results_SurveyUsed(AnalysisKey,Location,Yr) "
        query+="Values("
        query+=str(self.AnalysisKey.GetValue())
        query+=",'"
        query+=Location
        query+="',"
        query+=str(Year)
        query+=");"
        query=query.replace('inf','1000')
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 219 query\n',query)
            self.DB.Execute(query)
            

    def Create_Results_TranChar(self):
        CreateStatement ='Create TABLE Results_TranChar ('
        CreateStatement+='AnalysisKey LONG,'
        CreateStatement+='TranCharKey LONG,'
        CreateStatement+='Location varchar,'        
        CreateStatement+='SubSampleLocation varchar,'        
        CreateStatement+='Yr INT,'
        CreateStatement+='StatArea INT ,'
        CreateStatement+='SubArea INT ,'
        CreateStatement+='InBed INT ,'
        CreateStatement+='NumTran INT ,'
        CreateStatement+='TransectArea DOUBLE ,'
        CreateStatement+='mu30 DOUBLE ,'
        CreateStatement+='sigma30 DOUBLE ,'
        CreateStatement+='mubeta DOUBLE ,'
        CreateStatement+='sigmabeta DOUBLE ,'
        CreateStatement+='sigmaepsilon DOUBLE );'
        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print('\nNewMDB line 120 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement )
        self.TranCharMap=[]

    def ADDTo_TranChar(self, Location,SubSampleLocation,Year,StatArea,SubArea,InBed,NumTran,\
                       TransectArea,mu30,sigma30,mubeta,sigmabeta,sigmaepsilon):
        query ="insert INTO Results_TranChar(AnalysisKey,TranCharKey,Location,SubSampleLocation,Yr,StatArea,SubArea,InBed,"
        query+="NumTran,TransectArea,mu30,sigma30,mubeta,sigmabeta,sigmaepsilon) "
        query+="Values("
        query+=str(self.AnalysisKey.GetValue())
        query+=","
        query+=str(self.TranCharKey.GetValue())
        query+=",'"
        query+=Location
        query+="','"
        query+=SubSampleLocation
        query+="',"
        query+=str(Year)
        query+=","
        query+=str(StatArea)
        query+=","
        query+=str(SubArea)
        query+=","
        query+=str(InBed)
        query+=","
        query+=str(NumTran)
        query+=","
        query+=str(TransectArea)
        query+=","
        query+=str(mu30)
        query+=","
        query+=str(sigma30)
        query+=","
        query+=str(mubeta)
        query+=","
        query+=str(sigmabeta)
        query+=","
        query+=str(sigmaepsilon)
        query+=");"
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 263 query\n',query)
            self.DB.Execute(query)
        self.TranCharMap+=[[Location,SubSampleLocation,Year,StatArea,SubArea,InBed,self.TranCharKey.GetValue() ]]   
        self.TranCharKey.Increment()


    def GetTranCharKey(self,Location,SubSampleLocation,Year,StatArea,SubArea,InBed):
        index=list(range(len(self.TranCharMap)))

        #Trivial cases
        if len(index)==0: return(None)
        if len(index)==1: return(self.TranCharMap[0][-1])

        try:
            x=list(filter(lambda t:self.TranCharMap[t][:6]==[Location,SubSampleLocation,Year,StatArea,SubArea,InBed],range(len(self.TranCharMap))))[0]
            result= self.TranCharMap[x][-1]
            return(result)
        except:
            print('\nNewMDB 310')
            print('[Location,SubSampleLocation,Year,StatArea,SubArea,InBed]',[Location,SubSampleLocation,Year,StatArea,SubArea,InBed])
            for x in self.TranCharMap:print(x)

        





        

if __name__ == "__main__":


    from PyQt4 import QtGui
    from PyQt4.QtCore import *

    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    prompt="Select OutPut database file"
    DefaultDirec="H:\\"
    FileExt="Access Files (*.mdb *.accdb)"


    mdbfile = QtGui.QFileDialog.getSaveFileName(w, prompt,DefaultDirec,FileExt)
    testdb=NewMDB(mdbfile)
    testdb.ADDTo_Analysis(1000,125,0.12,100.6)


    testdb.ADDTo_ConfInterval(123,456,\
                           95,\
                           1,    2,\
                           3,   4,\
                           5,  6,\
                           7, 8)
    testdb.ADDTo_EstDens(200, 20,400,40)
    testdb.ADDTo_SizeRange(25,54)
    testdb.ADDTo_SurveyUsed(' Location',1963)
    testdb.ADDTo_TranChar( 'Location','SubSampleLocation',1962,12,3,'NULL',10,\
                           100,1,2,3,4,5)
    del testdb

    print('done')
