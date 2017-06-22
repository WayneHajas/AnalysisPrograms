# for column types, see http://www.w3schools.com/ado/ado_datatypes.asp

#Edited 2014-06-18 so that in output, site-area is given in hectares (previously was metres-squared)

# 2014-0720
# In write-transectcs, GIS_Code is left blank if there is no value from the Headers Table.

from numpy import ndarray
import datetime
import os, sys
from win32com.client import Dispatch
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from KeyValues import MinInt,KeyValues
import pdb

class NewMDB:
    def __init__(self,OUTmdbName,\
                 InitAnalysisKey=MinInt,\
                 InitTranCharKey=MinInt):

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

        self.OUTmdbName=OUTmdbName
        self.Create_Results_Header()
        self.Create_Results_SiteConfBound()
        self.Create_Results_Site()
        self.Create_Results_Transect()
        self.Create_Results_Overall()
        self.Create_Results_OverallConfBounds()

        self.AnalysisKey=KeyValues(InitValue=InitAnalysisKey)
        self.TranCharKey=KeyValues(InitValue=InitTranCharKey)
        self.ROKey=KeyValues(InitValue=InitTranCharKey)
        self.OverallCBKey=KeyValues(InitValue=InitTranCharKey)
        self.SiteKey=KeyValues(InitValue=InitTranCharKey)
        self.SiteCBKey=KeyValues(InitValue=InitTranCharKey)
        self.TransectKey=KeyValues(InitValue=InitTranCharKey)


    def Create_Results_Header(self):
        CreateStatement ='Create TABLE Results_Header ('
        CreateStatement+='ResultKey LONG,'
        CreateStatement+='Region varchar,'
        CreateStatement+='SurveyTitle varchar,'
        CreateStatement+='[Year] INT, '# Com does not like "year" as a field name
        CreateStatement+='RunNumber INT, '
        CreateStatement+='RunComments varchar,'
        CreateStatement+='YearRun INT, '
        CreateStatement+='MonthRun INT, '
        CreateStatement+='DayRun INT, '
        CreateStatement+='SurveyArea DOUBLE, '
        CreateStatement+='NumberTransects INT, '
        CreateStatement+='Species varchar,'
        CreateStatement+='BootstrappingUsed YesNo,'        
        CreateStatement+='NumberIterations INT, '        
        CreateStatement+='RandomSeed Long, '        
        CreateStatement+='MinDepth DOUBLE, '
        CreateStatement+='MaxDepth DOUBLE); '
        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print ('\nNewMDB line 68\n',CreateStatement)
            self.DB.Execute(CreateStatement )            

    def ADDTo_Results_Header(self,\
                             TranClassChar,RunNumber,RunComments,SurveyArea,\
                             NumberTransects,NumberIterations,RandomSeed,\
                             MinDepth,MaxDepth):
        ct=datetime.datetime.now()
        y,m,d=ct.year,ct.month,ct.day
        
        #SurveyArea=MinInt
        #if RunNumber==2:SurveyArea
        query ="insert INTO Results_Header("
        query+=     "ResultKey,Region,SurveyTitle,[Year],RunNumber,RunComments,YearRun,MonthRun,DayRun,"
        query+=      "SurveyArea,NumberTransects, "
        query+=     "Species,BootstrappingUsed, NumberIterations,RandomSeed,MinDepth,MaxDepth) "
        query+="Values("
        query+=str(self.AnalysisKey.GetValue())
        query+=","
        try:
            query+="'"+TranClassChar.GetUniqueVal('GeographicArea')+"'"
        except:
            pdb.set_trace()
            query+="'"+TranClassChar.GetUniqueVal('GeographicArea')+"'"
        query+=","
        try:
            query+="'"+TranClassChar.GetUniqueVal('SurveyTitle')+"'"
        except:
            pdb.set_trace()
            query+="'"+TranClassChar.GetUniqueVal('SurveyTitle')+"'"
        query+=","
        query+=str(TranClassChar.GetUniqueVal('Year'))
        query+=","
        query+=str(RunNumber)
        query+=","
        query+="'"+RunComments+"'"
        query+=","
        query+=str(y)
        query+=","
        query+=str(m)
        query+=","
        query+=str(d)
        query+=","
        query+=str(SurveyArea/10000) #Convert to hectares
        query+=","
        query+=str(NumberTransects)
        query+=","
        query+="'"+'84C'+"'"
        query+=","
        query+=str(int(True)) 
        query+=","
        query+=str(NumberIterations)
        query+=","
        query+=str(RandomSeed)
        query+=","
        query+=str(MinDepth)
        query+=","
        query+=str(MaxDepth)
        query+=");"
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 104 query\n',query)
            self.DB.Execute(query)
 
    def Create_Results_SiteConfBound(self):
        CreateStatement ='Create TABLE Results_SiteConfBound ('
        CreateStatement+='SiteKey LONG,'
        CreateStatement+='ResultKey LONG,'
        CreateStatement+='ConfidenceLevel INT,'
        CreateStatement+='DensityLow DOUBLE,  DensityHigh DOUBLE, '
        CreateStatement+='PopulationLow DOUBLE,        PopulationHigh DOUBLE, '
        CreateStatement+='BiomassPerMLow DOUBLE,BiomassPerMHigh DOUBLE, '
        CreateStatement+='SiteBiomassLow DOUBLE,      SiteBiomassHigh DOUBLE) '
        self.DB.Execute(CreateStatement )
        
    def ADDTo_SiteConfBound(self,\
                           pcConfidenceLevel,\
                           DensityLow,      DensityHigh,\
                           PopulationLow,   PopulationHigh,\
                           BiomassPerMLow,  BiomassPerMHigh,\
                           SiteBiomassLow,  SiteBiomassHigh\
                           ):
        query ="insert INTO Results_SiteConfBound(SiteKey,ResultKey,ConfidenceLevel, "
        query+=     "DensityLow,     DensityHigh, "
        query+=     "PopulationLow,  PopulationHigh, "
        query+=     "BiomassPerMLow, BiomassPerMHigh, "
        query+=     "SiteBiomassLow, SiteBiomassHigh "
        query+=") "
        query+="Values("
        query+=str(self.SiteKey.GetValue())
        query+=","
        query+=str(self.AnalysisKey.GetValue())
        query+=","+str(pcConfidenceLevel)
        
        query+="," + str(DensityLow)         +  "," +  str(DensityHigh)
        query+="," + str(PopulationLow)      +  "," +  str(PopulationHigh)
        
        try:
            query+="," + str(BiomassPerMLow/1000.) +  "," +  str(BiomassPerMHigh/1000.)
        except:
            query+="," + '-32767'                  +  "," +  '-32767'
        try:
            query+="," + str(SiteBiomassLow/1000.) +  "," +  str(SiteBiomassHigh/1000.)
        except:
            query+="," + '-32767'                  +  "," +  '-32767'
        query+=");"
        query=query.replace('None','-32767')
        query=query.replace('-inf','-32767')
        query=query.replace('inf','-32767')
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 156 query\n',query)
            self.DB.Execute(query)

    def Create_Results_Site(self):
        CreateStatement ='Create TABLE Results_Site ('
        CreateStatement+='ResultKey LONG,'
        CreateStatement+='SiteKey LONG,'
        CreateStatement+='SiteNumber INT,'
        CreateStatement+='LOBF INT,'
        CreateStatement+='MeanTranLength DOUBLE, '
        CreateStatement+='SiteArea DOUBLE, '
        CreateStatement+='SiteAreaSE DOUBLE, '
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
            print('\nNewMDB 180 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement)

    def ADDTo_Results_Site(self,SiteNum,LOBF,MeanTranLength,SiteArea,SiteAreaSE,\
                      MeanWt,MeanWtSE,MeanWtSource,\
                      NumberTransects,Density,Population,\
                      BiomassPerM,SiteBioMass):
        query =    "insert INTO Results_Site(ResultKey, SiteKey, SiteNumber, LOBF, MeanTranLength, "
        query+=    "SiteArea,SiteAreaSE,MeanWt,MeanWtSE,MeanWtSource,NumberTransects,Density, "
        query+=    "Population,BiomassPerM,SiteBioMass) "
        query+="Values("
        query+=str(self.AnalysisKey.GetValue())
        query+=","+str(self.SiteKey.GetValue(IncrementFirst=True))
        query+=","+str(SiteNum)
        query+=","+str(LOBF)
        query+=","+str(MeanTranLength)
        query+=","+str(SiteArea/10000.)
        query+=","+str(SiteAreaSE/10000.)
        query+=","+str(MeanWt)
        query+=","+str(MeanWtSE)
        query+=",'"+str(MeanWtSource)+"'"
        query+=","+str(NumberTransects)
        query+=","+str(Density)
        query+=","+str(Population)
        query+=","+str(BiomassPerM/1000.)#Convert from grams to kilogram
        query+=","+str(SiteBioMass/1000./1000.)#Convert from grams to tonnes
        
        query+=");"
        query=query.replace('None','-32767')
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 219 query\n',query)
            print(' MeanWtSource ', )
            self.DB.Execute(query)

        

    def Create_Results_SurveyUsed(self):
        CreateStatement ='Create TABLE Results_SurveyUsed ('
        CreateStatement+='AnalysisKey LONG,'
        CreateStatement+='Location varchar,'        
        CreateStatement+='[Year] INT'
        CreateStatement+=');'        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print('\nNewMDB line 233 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement )

    def ADDTo_SurveyUsed(self, Location,Year):
        query ="insert INTO Results_SurveyUsed(AnalysisKey,Location,[Year]) "
        query+="Values("
        query+=str(self.AnalysisKey.GetValue())
        query+=",'"+Location+"',"
        query+=str(Year)
        query+=");"
        query=query.replace('inf','1000')
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 247 query\n',query)
            self.DB.Execute(query)
            

    def Create_Results_Transect(self):
        CreateStatement ='Create TABLE Results_Transect ('
        CreateStatement+='TransectKey LONG,'
        CreateStatement+='SiteKey LONG,'
        CreateStatement+='TransectNumber INT ,'        
        CreateStatement+='HeaderKey LONG,'
        CreateStatement+='[Year] INT, '
        CreateStatement+='[Month] INT, '
        CreateStatement+='[Day] INT, '
        CreateStatement+='MinDepth DOUBLE, '
        CreateStatement+='MaxDepth DOUBLE, '  
        CreateStatement+='TranLength INT, '     
        CreateStatement+='NumQuadrats INT,'
        CreateStatement+='NumAnimals INT,'
        CreateStatement+='Density DOUBLE, '
        CreateStatement+='BiomassPerM DOUBLE, '
        CreateStatement+='ShowFactor DOUBLE, '       
        CreateStatement+='DailyFixed varchar,'
        CreateStatement+='OmitTransect YesNo, '
        CreateStatement+='OmitTransectReason varchar ,'
        CreateStatement+='TransectComments varchar,  '
        CreateStatement+='GIS_Code LONG );'
        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print('\nNewMDB line 280 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement )

    def ADDTo_Results_Transect(self, TransectKey,SiteKey,TransectNumber,HeaderKey,SurveyDate,MinDepth,MaxDepth,\
                               TranLength,NumQuadrats,NumAnimals,Density ,BiomassPerM ,ShowFactor,\
                               DailyFixed ,OmitTransect ,OmitTransectReason,TransectComments,GIS_Code):
        #Make the rounding match old version of analysis program
        iTranLength=int(round(TranLength+1e-6))
        
        query ="insert INTO Results_Transect(TransectKey,SiteKey,TransectNumber,HeaderKey, "
        query+="[Year],[Month],[Day],MinDepth,MaxDepth, "
        query+="TranLength,NumQuadrats,NumAnimals,Density,BiomassPerM ,ShowFactor, "
        query+="DailyFixed,OmitTransect,OmitTransectReason ,TransectComments "

        #GIS_Code left blank if there is no value
        if GIS_Code!=None: query+=",GIS_Code "
        
        query+=") "
        query+="Values("
        query+=str(TransectKey)
        query+=","
        query+=str(SiteKey)
        query+=","
        query+=str(TransectNumber)
        query+=","
        query+=str(HeaderKey)
        query+=","
        query+=str(SurveyDate.year)+","+str(SurveyDate.month)+","+str(SurveyDate.day)
        query+=","
        query+=str(MinDepth)
        query+=","
        query+=str(MaxDepth)
        query+=","
        query+=str(iTranLength)
        query+=","
        query+=str(NumQuadrats)
        query+=","
        query+=str(NumAnimals)
        query+=","
        query+=str(Density)
        query+=","
        query+=str(BiomassPerM)
        query+=","
        query+=str(ShowFactor)
        query+=","
        query+="'"+DailyFixed+"'"
        query+=","
        query+=str(OmitTransect)
        query+=","
        query+="'"+OmitTransectReason+"'"
        query+=","
        query+="'"+TransectComments+"'"
        if GIS_Code!=None:
          query+=","
          query+=str(GIS_Code)
        query+=");"
        query=query.replace('None','-32767')
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 322 query\n',query)
            self.DB.Execute(query)
       
   


    def Create_Results_Overall(self):
        CreateStatement ='Create TABLE Results_Overall('
        CreateStatement+='ROKey LONG,'
        CreateStatement+='ResultKey LONG,'
        CreateStatement+='Density DOUBLE, '
        CreateStatement+='Population DOUBLE, '
        CreateStatement+='BiomassPerM DOUBLE, '
        CreateStatement+='SurveyBioMass DOUBLE  );'
        
        try:
            self.DB.Execute(CreateStatement )
        except:
            print('\nNewMDB line 341 CreateStatement\n',CreateStatement)
            self.DB.Execute(CreateStatement )

    def ADDTo_Results_Overall(self,Density,Population,BiomassPerM,SurveyBioMass):
        query ="insert INTO Results_Overall(ROKey, ResultKey,Density,Population,BiomassPerM,SurveyBioMass) "
        query+="Values("
        query+=    str(self.ROKey.GetValue(IncrementFirst=True))
        query+=","+str(self.AnalysisKey.GetValue())
        query+=","+str(Density)
        query+=","+str(Population)
        query+=","+str(BiomassPerM/1000.)
        query+=","+str(SurveyBioMass/1000000.)
        query+=");"
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 357 query\n',query)
            self.DB.Execute(query)
 
    def Create_Results_OverallConfBounds(self):
        CreateStatement ='Create TABLE Results_OverallConfBounds ('
        CreateStatement+='ROKey LONG,' 
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
        query ="insert INTO Results_OverallConfBounds(ROKey,ConfidenceLevel, "
        query+=     "DensityLow,    DensityHigh, "
        query+=     "PopulationLow,  PopulationHigh, "
        query+=     "BiomassPerMLow,  BiomassPerMHigh, "
        query+=     "SurveyBiomassLow,        SurveyBiomassHigh "
        query+=") "
        query+="Values("
        query+=str(self.ROKey.GetValue())
        query+="," + str(pcConfidenceLevel)
        query+="," + str(DensityLow)         +  "," +  str(DensityHigh)
        query+="," + str(PopulationLow)         +  "," +  str(PopulationHigh)
        
        try:
            query+="," + str(BiomassPerMLow/1000.) +  "," +  str(BiomassPerMHigh/1000.)
        except:
            query+="," + '-32767'                  +  "," +  '-32767'
        try:
            query+="," + str(SurveyBiomassLow/1000000.) +  "," +  str(SurveyBiomassHigh/1000000.)
        except:
            query+="," + '-32767'                  +  "," +  '-32767'
       
        query+=");"
        query=query.replace('None','-32767')
        try:
            self.DB.Execute(query)
        except:
            print('\nNewMDB 407 query\n',query)
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
            print('\nNewMDB 429')
            print('[Location,SubSampleLocation,Yr,StatArea,SubArea]',[Location,SiteNum,Year,StatArea,SubArea])
            for x in self.TranCharMap:print(x)

        





        

if __name__ == "__main__":


    from PyQt4 import QtGui
    from PyQt4.QtCore import *

    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    prompt="Select OutPut database file"
    DefaultDirec="H:\\AnalysisPrograms2013\\PyFunctions\\Geoduck\\SampleData"
    FileExt="Access Files (*.mdb *.accdb)"


    mdbfile = QtGui.QFileDialog.getSaveFileName(w, prompt,DefaultDirec,FileExt)
    testdb=NewMDB(mdbfile)
    import datetime
    SurveyDate=datetime.datetime.now()
    testdb.ADDTo_Results_Transect( 1,2,3,4,SurveyDate,6,7,\
                               8,9,10,11 ,12 ,0.5,\
                               'DailyFixed' ,True ,'OmitTransectReason','TransectComments',13)

    testdb.ADDTo_Results_Header('SelectedSurveys',4,'Run comments',1000,756,3,100)

    SelectedSurveys,RunNumber,RunComments,\
                             NumberIterations,RandomSeed,MinDepth,MaxDepth


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
