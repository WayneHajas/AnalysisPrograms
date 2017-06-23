'''
2015-11-27 Change biomass units to kg for overall results

2015-11-18 Modified to use PrepForMDB instead of str'''


# for column types, see http://www.w3schools.com/ado/ado_datatypes.asp
from numpy import ndarray
import os, sys
from win32com.client import Dispatch
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from KeyValues import MinInt,KeyValues
from VersionTime import VersionTime
from PrepForMDB import PrepForMDB

class NewMDB:
    def __init__(self,OUTmdbName,\
                 InitAnalysisKey=MinInt,\
                 InitTranCharKey=MinInt):
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
        self.Create_Results_Header()
        self.Create_Results_ConfInterval()
        self.Create_Results_EstDens()
        self.Create_Results_TranChar()
        self.Create_Results_SurveyUsed()
        self.Create_Results_Transect()
        self.Create_Results_Overall()
        self.Create_Results_OverallConfBounds()

        self.AnalysisKey=KeyValues(InitValue=InitAnalysisKey)
        self.TranCharKey=KeyValues(InitValue=InitTranCharKey)


    def Create_Results_Header(self):
        CreateStatement ='Create TABLE Results_Header ('
        CreateStatement+='ResultKey LONG,'
        CreateStatement+='AnalysisDate TIME, '
        CreateStatement+='RunComments varchar,'
        CreateStatement+='Species varchar,'
        CreateStatement+='nReps INT, '
        CreateStatement+='rSeed INT, '
        CreateStatement+='MinDepth DOUBLE, '
        CreateStatement+='MaxDepth DOUBLE, '
        CreateStatement+='VersionDate TIME) '
        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print ('\nNewMDB line 55\n',CreateStatement)
            self.DB.Execute(CreateStatement )            

    def ADDTo_Results_Header(self,RunComments,Species,nReps,rSeed,MinDepth,MaxDepth):
        VersionDate=VersionTime()
        y,m,d=VersionDate.year,VersionDate.month,VersionDate.day
        
        query ="insert INTO Results_Header(ResultKey,AnalysisDate,RunComments,Species,nReps,rSeed,MinDepth,MaxDepth,VersionDate) "
        query+="Values("
        query+=PrepForMDB(self.AnalysisKey.GetValue())
        query+=","
        query+="NOW()"
        query+=","
        query+="'"+RunComments+"'"
        query+=","
        query+="'"+Species+"'"
        query+=","
        query+=PrepForMDB(nReps)
        query+=","
        query+=PrepForMDB(rSeed)
        query+=","
        query+=PrepForMDB(MinDepth)
        query+=","
        query+=PrepForMDB(MaxDepth)
        query+=","
        query+="DateSerial( "+str(y)+","+str(m)+","+str(d)+")"
        query+=");"
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 76 query\n',query)
            self.DB.Execute(query)
 
    def Create_Results_ConfInterval(self):
        CreateStatement ='Create TABLE Results_ConfInterval ('
        CreateStatement+='TranCharKey LONG,'
        CreateStatement+='pcConfidenceLevel INT,'
        CreateStatement+='lowPopLinear DOUBLE,  uppPopLinear DOUBLE, '
        CreateStatement+='lowBmassLinear DOUBLE,uppBmassLinear DOUBLE, '
        CreateStatement+='lowPop DOUBLE,        uppPop DOUBLE, '
        CreateStatement+='lowBmass DOUBLE,      uppBmass DOUBLE) '
        self.DB.Execute(CreateStatement )
        
    def ADDTo_ConfInterval(self,TranCharKey,\
                           pcConfidenceLevel,\
                           lowPopLinear,    uppPopLinear,\
                           lowBmassLinear,  uppBmassLinear,\
                           lowPop,          uppPop,\
                           lowBmass,        uppBmass\
                           ):
        query ="insert INTO Results_ConfInterval(TranCharKey,pcConfidenceLevel, "
        query+=     "lowPopLinear,    uppPopLinear, "
        query+=     "lowBmassLinear,  uppBmassLinear, "
        query+=     "lowPop, uppPop, "
        query+=     "lowBmass, uppBmass "
        query+=") "
        query+="Values("
        query+=str(TranCharKey)
        query+=","
        query+=str(pcConfidenceLevel)
        query+="," + str(lowPopLinear)         +  "," +  str(uppPopLinear)
        try:
            query+="," + str(lowBmassLinear/1000.) +  "," +  str(uppBmassLinear/1000.)#Calculations are done in grams.  Divide by 1000 to get kg
        except:
            query+="," + '-32767'                  +  "," +  '-32767'
        query+="," + str(lowPop)         +  "," +  str(uppPop)
        try:
            query+="," + str(lowBmass/1000.) +  "," +  str(uppBmass/1000.)#Calculations are done in grams.  Divide by 1000 to get kg
        except:
            query+="," + '-32767'                  +  "," +  '-32767'
        query+=");"
        query=query.replace('None','-32767')
        query=query.replace('-inf','-32767')
        query=query.replace('inf','-32767')
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 123 query\n',query)
            self.DB.Execute(query)

    def Create_Results_EstDens(self):
        CreateStatement ='Create TABLE Results_EstDens ('
        CreateStatement+='TranCharKey LONG,'
        CreateStatement+='Location varchar,'
        CreateStatement+='SiteNum INT,'
        CreateStatement+='Yr INT,'
        CreateStatement+='StatArea INT,'
        CreateStatement+='SubArea INT,'
        CreateStatement+='MeanTranLength DOUBLE, '
        CreateStatement+='CoastLength DOUBLE, '
        CreateStatement+='CoastLengthSE DOUBLE, '
        CreateStatement+='MeanWt DOUBLE, '
        CreateStatement+='MeanWtSE DOUBLE, '
        CreateStatement+='MeanWtSource varchar,'
        CreateStatement+='NumberTransects INT,'
        CreateStatement+='Density DOUBLE, '
        CreateStatement+='Population DOUBLE, '
        CreateStatement+='BiomassPerM DOUBLE, '
        CreateStatement+='SiteBioMass DOUBLE); '
        try:
            self.DB.Execute(CreateStatement)
        except:
            print('\nNewMDB 134 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement)

    def ADDTo_EstDens(self,SiteKey,FMT,MeanTranLength,\
                      CoastLength,CoastLengthSE,\
                      MeanWt,MeanWtSE,MeanWtSource,\
                      NumberTransects,Density,Population,\
                      BiomassPerM,SiteBioMass):
        query =    "insert INTO Results_EstDens(TranCharKey,"
        query+=        "Location,SiteNum,Yr,StatArea,SubArea,"
        query+=        "MeanTranLength,CoastLength,CoastLengthSE,"
        query+=        "MeanWt,MeanWtSE,MeanWtSource,"
        query+=        "NumberTransects,Density,Population,"
        query+=        "BiomassPerM,SiteBioMass) "
        query+="Values("+str(SiteKey)
        query+= ",'"+str(FMT['Project'])+"'"
        query+= ","+str(FMT['Site'])
        query+= ","+str(FMT['Year'])
        query+= ","+str(FMT['StatArea'])
        query+= ","+str(FMT['SubArea'])
        query+= ","+str(MeanTranLength)
        query+= ","+str(CoastLength)
        query+= ","+str(CoastLengthSE)
        query+= ","+str(MeanWt)
        query+= ","+str(MeanWtSE)
        query+= ",'"+str(MeanWtSource)+"'"
        query+= ","+str(NumberTransects)
        query+= ","+str(Density)
        query+= ","+str(Population)
        query+= ","+str(BiomassPerM/1000)#Calculations are done in grams.  Divide by 1000 to get kg
        query+= ","+str(SiteBioMass/1000)
        
        query+=");"
        query=query.replace('None','-32767')
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 170 query\n',query)
            self.DB.Execute(query)

        

    def Create_Results_SurveyUsed(self):
        CreateStatement ='Create TABLE Results_SurveyUsed ('
        CreateStatement+='AnalysisKey LONG,'
        CreateStatement+='Location varchar,'        
        CreateStatement+='Yr INT'
        CreateStatement+=');'        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print('\nNewMDB line 168 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement )

    def ADDTo_SurveyUsed(self, Location,Year):
        query ="insert INTO Results_SurveyUsed(AnalysisKey,Location,Yr) "
        query+="Values("
        query+=str(self.AnalysisKey.GetValue())
        query+=",'"+Location+"',"
        query+=str(Year)
        query+=");"
        query=query.replace('inf','1000')
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 186 query\n',query)
            self.DB.Execute(query)
            

    def Create_Results_TranChar(self):
        CreateStatement ='Create TABLE Results_TranChar ('
        CreateStatement+='AnalysisKey LONG,'
        CreateStatement+='TranCharKey LONG,'
        CreateStatement+='Location varchar,'        
        CreateStatement+='SiteNum INT,'
        CreateStatement+='Yr INT,'
        CreateStatement+='StatArea INT ,'
        CreateStatement+='SubArea INT ,'
        CreateStatement+='NumTran INT ,'
        CreateStatement+='TransectArea DOUBLE );'
        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print('\nNewMDB line 204 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement )
        self.TranCharMap=[]

    def ADDTo_TranChar(self, Location,SiteNum,Year,StatArea,SubArea,NumTran,\
                       TransectArea):
        CurSiteNum=SiteNum
        if CurSiteNum==None: CurSiteNum=MinInt
        query ="insert INTO Results_TranChar(AnalysisKey,TranCharKey,Location,SiteNum,Yr,StatArea,SubArea,"
        query+="NumTran,TransectArea) "
        query+="Values("
        query+=str(self.AnalysisKey.GetValue())
        query+=","
        query+=str(self.TranCharKey.GetValue())
        query+=",'"
        query+=Location
        query+="','"
        query+=str(CurSiteNum)
        query+="',"
        query+=str(Year)
        query+=","
        query+=str(StatArea)
        query+=","
        query+=str(SubArea)
        query+=","
        query+=str(NumTran)
        query+=","
        query+=str(TransectArea)
        query+=");"
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 237 query\n',query)
            self.DB.Execute(query)
        self.TranCharMap+=[[Location,SiteNum,Year,StatArea,SubArea,self.TranCharKey.GetValue() ]] 
        #self.TranCharKey.Increment()
   

    def Create_Results_Transect(self):
        CreateStatement ='Create TABLE Results_Transect('
        CreateStatement+='TranCharKey LONG,'
        CreateStatement+='TransectNumber INT ,'
        CreateStatement+='HeaderKey LONG,'
        CreateStatement+='SurveyDate TIME, '# DateSerial( Headers.Year,Headers.Month,Headers.Day) as SurveyDate 
        CreateStatement+='MinDepth DOUBLE, '
        CreateStatement+='MaxDepth DOUBLE, '
        CreateStatement+='TranLength INT, '
        CreateStatement+='NumQuadrats INT, '
        CreateStatement+='NumAnimals DOUBLE, '
        CreateStatement+='Density DOUBLE, '
        CreateStatement+='Biomass DOUBLE, '
        CreateStatement+='OmitTransect YesNo, '
        CreateStatement+='OmitTransectReason varchar ,'
        CreateStatement+='TransectComments varchar  );'
        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print('\nNewMDB line 258 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement )
   


    def ADDTo_Transect(self, TranCharKey,TransectNumber,HeaderKey,y,m,d,MinDepth,MaxDepth,\
                       TranLength,NumQuadrats,NumAnimals,Density,Biomass,\
                      OmitTransect,OmitTransectReason,TransectComments):
        query ="insert INTO Results_Transect(TranCharKey,TransectNumber,HeaderKey, "
        query+="SurveyDate,MinDepth,MaxDepth,TranLength,NumQuadrats,NumAnimals,Density,Biomass, "
        query+="OmitTransect,OmitTransectReason,TransectComments) "
        
        query+="Values("
        query+=str(TranCharKey)
        query+=","+str(TransectNumber)
        query+=","+str(HeaderKey)
        query+=",DateSerial( "+str(y)+","+str(m)+","+str(d)+")"
        query+=","+str(MinDepth)
        query+=","+str(MaxDepth)
        query+=","+str(TranLength)
        query+=","+str(NumQuadrats)
        query+=","+str(NumAnimals)
        query+=","+str(Density)
        query+=","+str(Biomass)
        query+=","+str(OmitTransect)
        if (OmitTransectReason==None) or (OmitTransectReason==''):
            query+=",''"
        else:
            OmitTransectReason=OmitTransectReason.replace("'"," ")
            query+=",'"+OmitTransectReason+"'"
        if (TransectComments==None) or (TransectComments==''):
            query+=",''"
        else:
            TransectComments=TransectComments.replace("'"," ")
            query+=",'"+TransectComments+"'"
        query+=");"
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 288 query\n',query)
            print('type(OmitTransectReason),OmitTransectReason', type(OmitTransectReason),OmitTransectReason)
            print('type(TransectComments),TransectComments', type(TransectComments),TransectComments)
            self.DB.Execute(query)
   

    def Create_Results_Overall(self):
        CreateStatement ='Create TABLE Results_Overall('
        CreateStatement+='ResultKey LONG,'
        CreateStatement+='Density DOUBLE, '
        CreateStatement+='Population DOUBLE, '
        CreateStatement+='BiomassPerM DOUBLE, '
        CreateStatement+='SurveyBioMass DOUBLE  );'
        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print('\nNewMDB line 305 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement )

    def ADDTo_Results_Overall(self,Density,Population,BiomassPerM,SurveyBioMass):
        query ="insert INTO Results_Overall(ResultKey,Density,Population,BiomassPerM,SurveyBioMass) "
        query+="Values("
        query+=str(self.AnalysisKey.GetValue())
        query+=","+str(Density)
        query+=","+str(Population)
        query+=","+str(BiomassPerM/1000.)  #Calculations are done in grams.  Divide by 1000 to get kg
        query+=","+str(SurveyBioMass/1000.)
        query+=");"
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 320 query\n',query)
            self.DB.Execute(query)
 
    def Create_Results_OverallConfBounds(self):
        CreateStatement ='Create TABLE Results_OverallConfBounds ('
        CreateStatement+='ResultKey LONG,'
        CreateStatement+='ConfidenceLevel INT,'
        CreateStatement+='DensityLow DOUBLE,  DensityHigh DOUBLE, '
        CreateStatement+='PopulationLow DOUBLE,PopulationHigh DOUBLE, '
        CreateStatement+='BiomassPerMLow DOUBLE,        BiomassPerMHigh DOUBLE, '
        CreateStatement+='SurveyBiomassLow DOUBLE,      SurveyBiomassHigh DOUBLE) '
        self.DB.Execute(CreateStatement )

    def ADDTo_Results_OverallConfBounds(self,\
                           pcConfidenceLevel,\
                           DensityLow,    DensityHigh,\
                           PopulationLow,  PopulationHigh,\
                           BiomassPerMLow,  BiomassPerMHigh,\
                           SurveyBiomassLow,        SurveyBiomassHigh\
                           ):
        query ="insert INTO Results_OverallConfBounds(ResultKey,ConfidenceLevel, "
        query+=     "DensityLow,    DensityHigh, "
        query+=     "PopulationLow,  PopulationHigh, "
        query+=     "BiomassPerMLow,  BiomassPerMHigh, "
        query+=     "SurveyBiomassLow,        SurveyBiomassHigh "
        query+=") "
        query+="Values("
        query+=str(self.AnalysisKey.GetValue())
        query+=","
        query+=str(pcConfidenceLevel)
        query+="," + str(DensityLow)         +  "," +  str(DensityHigh)
        query+="," + str(PopulationLow)         +  "," +  str(PopulationHigh)
        
        try:
            query+="," + str(BiomassPerMLow/1000.) +  "," +  str(BiomassPerMHigh/1000.)#Calculations are done in grams.  Divide by 1000 to get kg
        except:
            query+="," + '-32767'                  +  "," +  '-32767'
        try:
            query+="," + str(SurveyBiomassLow/1000.) +  "," +  str(SurveyBiomassHigh/1000.)
        except:
            query+="," + '-32767'                  +  "," +  '-32767'
       
        query+=");"
        query=query.replace('None','-32767')
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 403 query\n',query)
            self.DB.Execute(query)
        

    def GetTranCharKey(self,Location,SiteNum,Year,StatArea,SubArea):
        index=list(range(len(self.TranCharMap)))

        #Trivial cases
        if len(index)==0: return(None)
        if len(index)==1: return(self.TranCharMap[0][-1])

        try:
            x=list(filter(lambda t:self.TranCharMap[t][:5]==[Location,SiteNum,Year,StatArea,SubArea],range(len(self.TranCharMap))))[0]
            result= self.TranCharMap[x][-1]
            return(result)
        except:
            print('\nNewMDB 310')
            print('[Location,SubSampleLocation,Yr,StatArea,SubArea]',[Location,SiteNum,Year,StatArea,SubArea])
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
    testdb.ADDTo_Results_Header('Run comments','species',1000,756,3,100)


    testdb.ADDTo_ConfInterval(-3127,95,\
                           101,    102,\
                           103.,   104.4,\
                           105.,  106.9555555,\
                           107.00001, 108.3333)
    testdb.ADDTo_EstDens(200, 20,400,40)
    testdb.ADDTo_SurveyUsed('Location',1963)
    testdb.ADDTo_TranChar( 'Location',62,1962,12,3,10,100)
    testdb.ADDTo_Transect(1000,6,1001,2013,7,23,3.5,10.,\
                       65,13,100,6.5,13.8,\
                      False,'OmitTransectReason','TransectComments',1111)

    
    del testdb

    print('done NewMDB')
    ADDTo_Transect(self, TranCharKey,TransectNumber,HeaderKey,y,m,d,MinDepth,MaxDepth,\
                       TranLength,NumQuadrats,NumAnimals,Density,Biomass,\
                      OmitTransect,OmitTransectReason,TransectComments,GIS_Code)
