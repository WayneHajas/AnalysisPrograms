'''
20160129
Change field-names to reflect change to allometric equation (mu30 to intcpt)

20151130
Include version-date in Results_Analysis table.

Use PrepforMDB to convert values to character-strings that can incorporated into
write-queries
'''


# for column types, see http://www.w3schools.com/ado/ado_datatypes.asp
from numpy import ndarray
import datetime
import os, sys
from win32com.client import Dispatch
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from KeyValues import MinInt,KeyValues
import UnitSuffixes as US
from PrepForMDB import PrepForMDB
from VersionTime import VersionTime


class NewMDB:
    def __init__(self,OUTmdbName,\
                 InitAnalysisKey=MinInt,\
                 InitTranCharKey=MinInt,\
                 InitSizeRangeKey=MinInt):

        self.OUTmdbName=OUTmdbName        
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
        self.Create_Results_Transect()


        self.AnalysisKey=KeyValues(InitValue=InitAnalysisKey)
        self.TranCharKey=KeyValues(InitValue=InitTranCharKey)
        self.SizeRangeKey=KeyValues(InitValue=InitSizeRangeKey)

    def Create_Results_Analysis(self):
        CreateStatement ='Create TABLE Results_Analysis ('
        CreateStatement+='AnalysisKey LONG,'
        CreateStatement+='AnalysisDate TIME, '
        CreateStatement+='nReps INT, '
        CreateStatement+='rSeed INT, '        
        CreateStatement+='MinDepth'+US.Metres+ ' DOUBLE, '
        CreateStatement+='MaxDepth'+US.Metres+ ' DOUBLE, '
        CreateStatement+='VersionDate TIME) '
        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print ('\nNewMDB line 51\n',CreateStatement)
            self.DB.Execute(CreateStatement )            

    def ADDTo_Analysis(self,nReps,rSeed,MinDepth,MaxDepth):
        VersionDate=VersionTime()
        vy,vm,vd=VersionDate.year,VersionDate.month,VersionDate.day
        ct=datetime.datetime.now()
        y,m,d=ct.year,ct.month,ct.day
        
        query ="insert INTO Results_Analysis(AnalysisKey,AnalysisDate,nReps,rSeed,"        
        query+='MinDepth'+US.Metres+ ',MaxDepth'+US.Metres+ ',VersionDate ) '
        query+="Values("
        query+=PrepForMDB(self.AnalysisKey.GetValue())
        query+=","
        query+="NOW()"
        query+=","
        query+=PrepForMDB(nReps)
        query+=","
        query+=PrepForMDB(rSeed)
        query+=","
        query+=PrepForMDB(MinDepth)
        query+=","
        query+=PrepForMDB(MaxDepth)
        query+=","
        query+="DateSerial( "+PrepForMDB(vy)+","+PrepForMDB(vm)+","+PrepForMDB(vd)+")"
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
        CreateStatement+='lowPopLinear'+US.PerMetre+ ' DOUBLE, '
        CreateStatement+='uppPopLinear'+US.PerMetre+ ' DOUBLE, '
        CreateStatement+='lowPopSpatial'+US.PerMetreSquared+ ' DOUBLE, '
        CreateStatement+='uppPopSpatial'+US.PerMetreSquared+ ' DOUBLE, '
        CreateStatement+='lowBmassLinear'+US.KgPerMetre+ ' DOUBLE, '
        CreateStatement+='uppBmassLinear'+US.KgPerMetre+ ' DOUBLE, '
        CreateStatement+='lowBmassSpatial'+US.KgPerMetreSquared+ ' DOUBLE, '
        CreateStatement+='uppBmassSpatial'+US.KgPerMetreSquared+ ' DOUBLE) '
        self.DB.Execute(CreateStatement )
        
    def ADDTo_ConfInterval(self,TranCharKey,SizeRangeKey,\
                           pcConfidenceLevel,\
                           lowPopLinear,    uppPopLinear,\
                           lowPopSpatial,   uppPopSpatial,\
                           lowBmassLinear,  uppBmassLinear,\
                           lowBmassSpatial, uppBmassSpatial):
        query ="insert INTO Results_ConfInterval(TranCharKey,SizeRangeKey,pcConfidenceLevel, "        
        query+=     'lowPopLinear'+US.PerMetre+ ',    uppPopLinear'+US.PerMetre+ ', '
        query+=     'lowPopSpatial'+US.PerMetreSquared+ ',   uppPopSpatial'+US.PerMetreSquared+ ', '
        query+=     'lowBmassLinear'+US.KgPerMetre+ ',  uppBmassLinear'+US.KgPerMetre+ ', '
        query+=     'lowBmassSpatial'+US.KgPerMetreSquared+ ', uppBmassSpatial'+US.KgPerMetreSquared+ ') '
        query+="Values("
        query+=PrepForMDB(TranCharKey)
        query+=","
        query+=PrepForMDB(SizeRangeKey)
        query+=","
        query+=PrepForMDB(pcConfidenceLevel)
        query+=","
        query+=PrepForMDB(lowPopLinear)
        query+=","
        query+=                 PrepForMDB(uppPopLinear)
        query+=","
        query+=PrepForMDB(lowPopSpatial)
        query+=","
        query+=                 PrepForMDB(uppPopSpatial)
        query+=","
        query+=PrepForMDB(lowBmassLinear/1000.)
        query+=","
        try:
            query+=             PrepForMDB(uppBmassLinear/1000.)
        except:
            query+=             PrepForMDB(MinInt)
        query+=","
        try:
            query+=PrepForMDB(lowBmassSpatial/1000.)
        except:
            query+=PrepForMDB(MinInt)
        query+=","
        try:
            query+=             PrepForMDB(uppBmassSpatial/1000.)
        except:
            query+=             PrepForMDB(MinInt)

        query+=");"
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 119 query\n',query)
            self.DB.Execute(query)

    def Create_Results_EstDens(self):
        CreateStatement ='Create TABLE Results_EstDens ('
        CreateStatement+='TranCharKey LONG,'
        CreateStatement+='SizeRangeKey LONG,'        
        CreateStatement+='PopLinear'+US.PerMetre+ ' DOUBLE, '
        CreateStatement+='PopSpatial'+US.PerMetreSquared+ ' DOUBLE, '
        CreateStatement+='BmassLinear'+US.KgPerMetre+ ' DOUBLE, '
        CreateStatement+='BmassSpatial'+US.KgPerMetreSquared+ ' DOUBLE) '

        self.DB.Execute(CreateStatement )

    def ADDTo_EstDens(self,PopLinear, PopSpatial,BmassLinear,BmassSpatial,TranCharKey=None,SizeKey=None):
        skey=SizeKey
        if skey==None:skey=self.SizeRangeKey.GetValue()
        tckey=TranCharKey
        if tckey==None:tckey=self.TranCharKey.GetValue()
        query ="insert INTO Results_EstDens(TranCharKey,SizeRangeKey, "
        query+=     'PopLinear'+US.PerMetre+ ',   PopSpatial'+US.PerMetreSquared+ ', BmassLinear'+US.KgPerMetre+ ', BmassSpatial'+US.KgPerMetreSquared+ ') '
        query+="Values("
        query+=PrepForMDB(tckey)
        query+=","
        query+=PrepForMDB(skey)
        query+=","
        query+=PrepForMDB(PopLinear)
        query+=","
        query+=PrepForMDB(PopSpatial)
        query+=","
        try:
            query+=PrepForMDB(BmassLinear/1000.)
        except:
            query+=PrepForMDB(MinInt)
        query+=","
        try:
            query+=PrepForMDB(BmassSpatial/1000.)
        except:
            query+=PrepForMDB(MinInt)
        query+=");"
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 181 query\n',query)
            self.DB.Execute(query)

        
    def Create_Results_SizeRange(self):
        CreateStatement ='Create TABLE Results_SizeRange ('
        CreateStatement+='AnalysisKey LONG,'
        CreateStatement+='SizeRangeKey LONG,'
        CreateStatement+='MinSize'+US.Mm+ ' DOUBLE, '
        CreateStatement+='MaxSize'+US.Mm+ ' DOUBLE) '
        self.DB.Execute(CreateStatement )
        self.SizeMap={}

    def ADDTo_SizeRange(self, MinSize,MaxSize):
        query ="insert INTO Results_SizeRange(AnalysisKey,SizeRangeKey, "
        query+=     'MinSize'+US.Mm+ ',MaxSize'+US.Mm+ ') '
        query+="Values("
        query+=PrepForMDB(self.AnalysisKey.GetValue())
        query+=","
        query+=PrepForMDB(self.SizeRangeKey.GetValue())
        query+=","
        query+=PrepForMDB(MinSize)
        query+=","
        query+=PrepForMDB(MaxSize)
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
        CreateStatement+='SurveyTitle varchar,'        
        CreateStatement+='Yr INT );'        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print('\nNewMDB line 101 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement )

    def ADDTo_SurveyUsed(self, SurveyTitle,Year):
        query ="insert INTO Results_SurveyUsed(AnalysisKey,SurveyTitle,Yr) "
        query+="Values("
        query+=PrepForMDB(self.AnalysisKey.GetValue())
        query+=",'"
        query+=SurveyTitle
        query+="',"
        query+=PrepForMDB(Year)
        query+=");"
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 267 query\n',query)
            self.DB.Execute(query)
    

            

    def Create_Results_TranChar(self):
        CreateStatement ='Create TABLE Results_TranChar ('
        CreateStatement+='AnalysisKey LONG,'
        CreateStatement+='TranCharKey LONG,'
        CreateStatement+='SurveyTitle varchar,'        
        CreateStatement+='Location varchar,'        
        CreateStatement+='SiteNum INT,'
        CreateStatement+='[Year] INT,'
        CreateStatement+='StatArea INT ,'
        CreateStatement+='SubArea INT ,'
        CreateStatement+='InBed INT ,'
        CreateStatement+='Transect_Count INT ,'
        CreateStatement+='TransectArea'+US.MetresSquared+ ' DOUBLE  ,'
        CreateStatement+='SurveyedQuadCount INT );'
        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print('\nNewMDB line 245 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement )
        self.TranCharMap=[]

            

    def Create_Results_TranChar(self):
        CreateStatement ='Create TABLE Results_TranChar ('
        CreateStatement+='AnalysisKey LONG,'
        CreateStatement+='TranCharKey LONG,'
        CreateStatement+='SurveyTitle varchar,'        
        CreateStatement+='SubSampleLocation varchar,'        
        CreateStatement+='Yr INT,'
        CreateStatement+='StatArea INT ,'
        CreateStatement+='SubArea INT ,'
        CreateStatement+='InBed INT ,'
        CreateStatement+='Transect_Count INT ,'
        CreateStatement+='TransectArea'+US.MetresSquared+'  DOUBLE ,'     
        CreateStatement+='SurveyedQuadCount INT , '
        CreateStatement+='intcpt DOUBLE ,'
        CreateStatement+='sdintcpt DOUBLE ,'
        CreateStatement+='mubeta DOUBLE ,'
        CreateStatement+='sigmabeta DOUBLE ,'
        CreateStatement+='sigmaepsilon DOUBLE );'        

        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print('\nNewMDB line 120 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement )
        self.TranCharMap=[]

    def ADDTo_TranChar(self, SurveyTitle,SubSampleLocation,Year,StatArea,SubArea,InBed,Transect_Count,\
                       TransectArea,SurveyedQuadCount,intcpt,sdintcpt,mubeta,sigmabeta,sigmaepsilon):
        query ="insert INTO Results_TranChar(AnalysisKey,TranCharKey,SurveyTitle,SubSampleLocation,Yr,StatArea,SubArea,InBed,"
        query+='Transect_Count,TransectArea'+US.MetresSquared+ ",SurveyedQuadCount,intcpt,sdintcpt,mubeta,sigmabeta,sigmaepsilon) "
        query+="Values("
        query+=PrepForMDB(self.AnalysisKey.GetValue())
        query+=","
        query+=PrepForMDB(self.TranCharKey.GetValue())
        query+=",'"
        query+=SurveyTitle
        query+="','"
        query+=SubSampleLocation
        query+="',"
        query+=PrepForMDB(Year)
        query+=","
        query+=PrepForMDB(StatArea)
        query+=","
        query+=PrepForMDB(SubArea)
        query+=","
        query+=PrepForMDB(InBed)
        query+=","
        query+=PrepForMDB(Transect_Count)
        query+=","
        query+=PrepForMDB(TransectArea)
        query+=","
        query+=PrepForMDB(SurveyedQuadCount)
        query+=","
        query+=PrepForMDB(intcpt)
        query+=","
        query+=PrepForMDB(sdintcpt)
        query+=","
        query+=PrepForMDB(mubeta)
        query+=","
        query+=PrepForMDB(sigmabeta)
        query+=","
        query+=PrepForMDB(sigmaepsilon)
        query+=");"
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 263 query\n',query)
            self.DB.Execute(query)
        self.TranCharMap+=[[SurveyTitle,SubSampleLocation,Year,StatArea,SubArea,InBed,self.TranCharKey.GetValue() ]]   
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

 

    def Create_Results_Transect(self):
        CreateStatement ='Create TABLE Results_Transect('
        CreateStatement+='TranCharKey LONG,'
        CreateStatement+='SizeRangeKey LONG,'
        CreateStatement+='HeaderKey LONG,'
        CreateStatement+='TranLength'+US.Metres+ ' INT, '
        CreateStatement+='Population DOUBLE, '
        CreateStatement+='Biomass'+US.Kilograms+ ' DOUBLE  );'
        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print('\nNewMDB line 340 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement )
   


    def ADDTo_Transect(self, TranCharKey,SizeRangeKey,HeaderKey,\
                       TranLength,Population,Biomass):
        query ="insert INTO Results_Transect(TranCharKey,SizeRangeKey,HeaderKey, "
        query+='TranLength'+US.Metres+ ',Population,Biomass'+US.Kilograms+ ') '
        
        query+="Values("
        query+=PrepForMDB(TranCharKey)
        query+=","+PrepForMDB(SizeRangeKey)
        query+=","+PrepForMDB(HeaderKey)
        query+=","+PrepForMDB(TranLength)
        query+=","+PrepForMDB(Population)
        query+=","+PrepForMDB(Biomass/1000) #convert from grams to kilograms
        query+=");"
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 379 query\n',query)
            self.DB.Execute(query)
       





        

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
    testdb.ADDTo_SurveyUsed(' SurveyTitle',1963)
    testdb.ADDTo_TranChar( 'SurveyTitle','SubSampleLocation',1962,12,3,'NULL',10,\
                           100,1,2,3,4,5)
    del testdb

    print('done')
