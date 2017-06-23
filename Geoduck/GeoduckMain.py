'''2015-11-25
In Combined-sites, recognize the special case where there is a single-site.
Combined-results will exactly replicate results for single-site.  Less confusion that way.
'''

# change made 20140717
#    Transects used for run number 2 (LOBF-based site-area)
#    Previously, only tranects with a BedNum-value from the Headers table were
#       used in the calculations.
#    After this change, all transects are used for run number 2

# For run number 4, deterministic site-area is now the expectation value.
#  This affects population-estimates and biomass estimates for site and combined-sites
#  Through BCA, this also affects confidence bounds for run number 4.

from numpy.random import seed,uniform
from numpy import inf,iinfo,int16,sqrt,array
MinInt=iinfo(int16).min


from PyQt4.QtGui import QMainWindow, QDialog,QListWidgetItem
from PyQt4.QtCore import pyqtSignature
from PyQt4 import QtCore, QtGui


from MetaTransectClass import MetaTransectClass
from GDuckTransectclass import GDuckTransectclass
from ParamLevelCombo import CalcOverallStats
from mquantiles import mquantiles
from ArithSamples import Add,Divide,DivideByAverage

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from GetSurveys import AllSurveys
from ADO import adoBaseClass as OpenDB
from GeoduckDialog import GeoduckDialog
import geoduckQueryFunc as QueryFunc
from CopyMDB import CopyMDB

class GeoduckMain(QMainWindow, GeoduckDialog):

    def __init__(self,ODB,OUTmdb,parent = None):
        self.inMDB=ODB
        self.resultODB=OUTmdb
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.MakeConnect()
        
        self.OUTmdb=self.resultODB.ODB
        self.ODB=self.inMDB.ODB
        self.FillSurveys()
        self.DefaultSettings()
        self.setFocus()

    def MakeConnect(self):
        self.DoCalcs.clicked.connect(self.Calculations)
        self.QuitBttn.clicked.connect(self.QuitCalcs)
        self.AllSurveys.stateChanged.connect(self.DoAllSurveys)
   

        
    def FillSurveys(self):
        self.AS=AllSurveys(self.ODB)
        FullName=self.AS.GetCombo()
        for fn in FullName:
            item=QListWidgetItem(fn)
            self.AvailSurveys.addItem(item)
        self.AvailSurveys.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)


    def DefaultSettings(self):
        self.NumberBootstrap.insertPlainText('10000')
        self.RandomSeed.insertPlainText('756')
        self.MinDepth.insertPlainText('3')
        self.MaxDepth.insertPlainText('1000')    

    def Calculations(self):

        #Do nothing unless some surveys are selected
        if self.AvailSurveys.count()==0:return
        try:
            self.GetSelectedSurveys()
        except:
            self.QuitCalcs()
        print ('\nCalculations Started')
        self.TranClassChar=MetaTransectClass(self.ODB,\
                                             self.SelectedSurveys)
       
        CB=[99,95,90,75,50]
        self.Comments=self.RunComments.document().toPlainText()
        self.nboot=int(self.NumberBootstrap.document().toPlainText())
        self.seed=int(self.RandomSeed.document().toPlainText())
        self.LeastDepth=float(self.MinDepth.document().toPlainText())
        self.MostDepth=float(self.MaxDepth.document().toPlainText())        
        
        AlloSource=QueryFunc.AlloEqn()  
        SiteSamp =[]
        SiteEst=[]
        SampSite=[]
        TranClass=[]

        #Beginning of run 2 ###
        #Results based on LOBF as a basis for esitmating site-area
        print('\nResults based on Line Of Best Fit')
        self.OUTmdb.AnalysisKey.Increment()
        SiteSamp2 =[]
        for i in range(self.TranClassChar.nclass):
            print("\nSurvey: ",self.TranClassChar.GetChar(i,'SurveyTitle'))
            print("Year:   ",self.TranClassChar.GetChar(i,'Year'))
            print("Site:",self.TranClassChar.GetChar(i,'SurveySite'))

            #Random seeds will be manually gernerated for each sample of transects
            curseed=self.seed+i*self.nboot
 
            print ('Reading Data')
            CTC=GDuckTransectclass(self.ODB,i,self.TranClassChar,AlloSource,QueryFunc,\
                                   MinDepth=self.LeastDepth,MaxDepth=self.MostDepth,\
                                   OnlyOnBed=False,curseed=curseed)
            TranClass+=[CTC] 
            SiteEst+=[{'ntransect':CTC.ntransect,'MeanWeight':CTC.MeanWeight,'SiteSize':CTC.SiteSize}]

            SiteEst[i]['Area'   ]=SiteEst[i]['SiteSize'].GetEstArea(Digitized=False)
            SiteEst[i]['PopDens'   ]=CTC.GetAvgAbundance()
            SiteEst[i]['Pop'    ]=SiteEst[i]['Area']*SiteEst[i]['PopDens']
            SiteEst[i]['BiomassDens'   ]=CTC.GetAvgAbundance()*CTC.MeanWeight.EstMeanWeight
            SiteEst[i]['Biomass']=SiteEst[i]['Area']*SiteEst[i]['BiomassDens']

                        
            print("Number of Transects: ",CTC.ntransect)
            print('Writing results for individual transects')
            SiteSize=CTC.SiteSize
            MeanWeight=CTC.MeanWeight
            CTC.WriteTransectResults(self.OUTmdb,RemoveOffBed=False)

            SiteSize=CTC.SiteSize
            MeanWeight=CTC.MeanWeight

            self.OUTmdb.ADDTo_Results_Site(CTC.site,
                                       SiteSize.LOBF,
                                       SiteSize.GetMeanTranLen().mu,
                                       SiteSize.GetEstArea(Digitized=False),
                                       SiteSize.GetSEEstArea(Digitized=False),
                                       MeanWeight.EstMeanWeight/1000,    
                                       MeanWeight.MeanWeightSE/1000,
                                       MeanWeight.MeanWeightSource,
                                       CTC.ntransect,
                                       CTC.GetAvgAbundance(),
                                       CTC.GetAvgAbundance()*SiteSize.LOBFarea.mu,
                                       CTC.GetAvgAbundance()*CTC.MeanWeight.EstMeanWeight ,
                                       CTC.GetAvgAbundance()*CTC.MeanWeight.EstMeanWeight*SiteSize.LOBFarea.mu)
                                           


            print('Calculating Confidence Bounds')
            Area=CTC.SiteSize.GetRandomArea(n=self.nboot,RunNumber=2)
            SiteSamp2+=[CTC. WriteSiteCB(self.OUTmdb,nboot=self.nboot,\
                                         CB=CB,RunNumber=2) ]           
        print ('\nCombined')
        
        #Reduce datasets to sites that should be combined into overall results
        SiteEst,SiteSamp2= SelectGood(self.TranClassChar.AnalyzeSite, SiteEst),SelectGood(self.TranClassChar.AnalyzeSite, SiteSamp2)
        
        self.WriteOverall(SiteEst,SiteSamp2,CB)
        SurveyArea=sum(list(map(lambda x:x['Area'], SiteEst)))
        ntransect=sum(list(map(lambda x:x['ntransect'], SiteEst)))
        self.OUTmdb.ADDTo_Results_Header(self.TranClassChar,2,self.Comments,SurveyArea,\
             ntransect,self.nboot,self.seed, self.LeastDepth,self.MostDepth )
        #End of run 2 ################



        #Beginning of run number 4 #################
        dummy=self.OUTmdb.AnalysisKey.GetValue(IncrementFirst=True)#increment key for sets of analyses
        SiteEst=[]
        for i in range(self.TranClassChar.nclass):
            

            print('\n' )
            print("Survey: ",self.TranClassChar.GetChar(i,'SurveyTitle'))
            print("Year:   ",self.TranClassChar.GetChar(i,'Year'))
            print("Site:",self.TranClassChar.GetChar(i,'SurveySite'))
            print ('Reading Data')

            CTC=TranClass[i]
            CTC.ReduceToOnBed()#CTC.SiteSize is corrected here
            print("Number of Transects: ",CTC.ntransect)
            print('Writing results for individual transects')
            CTC.WriteTransectResults(self.OUTmdb,RemoveOffBed=False)
            print('Number of transects onbed: ',CTC.ntransect)
            SiteSize=CTC.SiteSize
            MeanWeight=CTC.MeanWeight
            
            #Use Digitized Area
            print('Writing estimated values - digitized area')

            #Later change could use the expectation value for Area.
            #Area=SiteSize.DigitizedArea.mu
            Area=SiteSize.GetEstArea(Digitized=True)
            PopDens=CTC.GetAvgAbundance()
            Pop    =PopDens*Area
            BmaDens=PopDens*CTC.MeanWeight.EstMeanWeight
            Bma    =Pop    *CTC.MeanWeight.EstMeanWeight
            if CTC.ntransect<=0:
                PopDens=MinInt
                Pop    =MinInt
                BmaDens=MinInt*1000
                Bma    =MinInt*1000000
            ###Area=SiteSize.GetDigitizedArea().mu
            if Area<0:
                Pop    =MinInt
                Bma    =MinInt*1000000
   
            self.OUTmdb.ADDTo_Results_Site(CTC.site,
                                       0,# LOBF is irrelevent for run#4
                                       SiteSize.GetMeanTranLen().mu,
                                       Area,
                                       SiteSize.GetSEEstArea(Digitized=True),
                                       MeanWeight.EstMeanWeight/1000,
                                       MeanWeight.MeanWeightSE/1000,
                                       MeanWeight.MeanWeightSource,
                                       CTC.ntransect,
                                       PopDens,
                                       Pop,
                                       BmaDens ,
                                       Bma) 
         
            SiteEst+=[{'PopDens':PopDens,\
                       'Pop':Pop,\
                       'BiomassDens':BmaDens,
                       'Biomass':Bma,
                       'Area':Area,\
                       'ntransect':CTC.ntransect,'MeanWeight':CTC.MeanWeight,'SiteSize':CTC.SiteSize}]
            
            print('Calculating Confidence Bounds')

            SiteSamp+=[CTC. WriteSiteCB(self.OUTmdb,nboot=self.nboot,CB=CB,RunNumber=4,Area=None)]
            
        print ('\nCombined')
        
        #Reduce datasets to sites that should be combined into overall results
        SiteEst,SiteSamp2= SelectGood(self.TranClassChar.AnalyzeSite, SiteEst),SelectGood(self.TranClassChar.AnalyzeSite, SiteSamp2)
        
        self.WriteOverall(SiteEst,SiteSamp,CB)
        SurveyArea=sum(list(map(lambda x:x['Area'], SiteEst)))
        ntransect=sum(list(map(lambda x:x['ntransect'], SiteEst)))
        self.OUTmdb.ADDTo_Results_Header(self.TranClassChar,4,self.Comments,SurveyArea,\
             ntransect,self.nboot,self.seed, self.LeastDepth,self.MostDepth )
        #End of run 4 ###############

        dictSelectedSurveys=self.SelectedSurveystoDict()
        CopyMDB(self.ODB,self.OUTmdb,dictSelectedSurveys)

        print('\nResults are in ',self.OUTmdb.OUTmdbName)
        return

    def WriteOverall(self,SiteEst,SiteSamp,CB):
        nsite=len(SiteSamp)

        #Deterministic Estimates
        MinArea=min(list(map(lambda x: ValorMax(x['Area'])  ,SiteEst)))
        if MinArea<0:#There is an undefined area
            EstPop=MinInt
            EstBma=MinInt*1000000
            Area  =MinInt
            PopDens=MinInt
            BmaDens=MinInt*1000
        else:
            EstPop=sum(list(map(lambda x:x['Pop'],SiteEst)))
            EstBma=sum(list(map(lambda x:x['Biomass'],SiteEst)))
            Area  =sum(list(map(lambda x:x['Area'  ],SiteEst)))
            PopDens=EstPop/Area
            BmaDens=EstBma/Area


        
        self.OUTmdb.ADDTo_Results_Overall(PopDens,EstPop,BmaDens,EstBma)

        #Confidence Bounds
        CBoverall=CombineSites(SiteSamp, CB)
        for i in range(len(CB)):
            self.OUTmdb.ADDTo_Results_OverallConfBounds(CB[i],\
                           CBoverall['PopDens'][i][1],    CBoverall['PopDens'][i][2],\
                           CBoverall['SitePop'][i][1],    CBoverall['SitePop'][i][2],\
                           CBoverall['BioDens'][i][1],    CBoverall['BioDens'][i][2],\
                           CBoverall['SiteBioM'][i][1],    CBoverall['SiteBioM'][i][2])
                                     

        
    def GetSelectedSurveys(self):
        self.SelectedSurveys=[]
        year=self.AS.GetYear()
        survey=self.AS.GetSurvey()
        for index in range(self.AvailSurveys.count()):
            if self.AvailSurveys.item(index).isSelected():
                 self.SelectedSurveys+=[[survey[index],year[index]]]
               
                    
                
    def DoAllSurveys(self):
        if self.AllSurveys.isChecked():
            for index in range(self.AvailSurveys.count()):
                self.AvailSurveys.item(index).setSelected(True)
        else:
            for index in range(self.AvailSurveys.count()):
                self.AvailSurveys.item(index).setSelected(False)
            
        
    def QuitCalcs(self):
        print ('\nBye Bye')
        os._exit(0)
        quit()
        sys.exit(app.exec_())

        

    def PrepOUTmdb(self):
        '''Put information into output.  Not the stats - just the metadata'''
        RunNumber=-1
        for ss in self.SelectedSurveys:
            self.OUTmdb.ADDTo_SurveyUsed(ss[0],str(ss[1]))
            
           
    def SelectedSurveystoDict(self):
        '''Convert self.SelectedSurveys as a list of dictionaries'''
        if isinstance(self.SelectedSurveys[0],dict):
            return(self.SelectedSurveys)
        result=[{'SurveyTitle':t[0], 'Year':t[1]}  for t in self.SelectedSurveys]
        return(result)

def ValorMax(x):
    try:
        return(min(x))
    except:
        return(x)
       
def CombineSites(SiteSamp,CB):
    '''Assuming CB is a percentage'''
    if isinstance(CB,(float,int)):cb=CB/100.
    else:cb=sorted(list(map(lambda x:x/100.,CB)),reverse=True)

    MinArea=min(list(map(lambda x: ValorMax(x['Area'])  ,SiteSamp)))
    if MinArea<0:#There is an undefined area
       SumPop=SumArea=PopDens=list(map(lambda t:MinInt, SiteSamp[0]['SampPop']))
       BioDens=list(map(lambda t:MinInt*1000, SiteSamp[0]['SampPop']))
       SumBioM=BioDens=list(map(lambda t:MinInt*1000, SiteSamp[0]['SampPop']))
       
    else:#All areas are defined
        SumArea=array(SiteSamp[0]['Area'])
        SumPop =array(SiteSamp[0]['SampPop'])
        SumBioM=array(SiteSamp[0]['SampBiomass'])
        
        #For a single site, just reuse the densities        
        if len(SiteSamp)==1:
            PopDens=array(SiteSamp[0]['SampAvgPopDens'])
            BioDens=array(SiteSamp[0]['SampBioDensity'])
        
        #For multiple sites, add up biomass and population amd divide by mean areaa        
        else:
            for x in SiteSamp[1:]:
                SumArea=Add(SumArea,x['Area'])  
                SumPop =Add(SumPop,x['SampPop'])  
                SumBioM=Add(SumBioM,x['SampBiomass'])
    
            '''Divide by the average because uncertainty in the area has already contributed
            to variability in total-population and total-biomass.  This is the way population and 
            biomass denisties were estimated in previous versions of GAP.
            
            With lots of effort, something better could be created.  Lots more cpu and memory 
            would be required.  I will stick with this for now.'''
            
            
            PopDens=DivideByAverage(SumPop   ,SumArea)
            BioDens=DivideByAverage(SumBioM,SumArea)

    if isinstance( CB,(float,int)):
        p=[.5-CB/200.,.5+CB/200]
    else:
        p=[]
        for x in CB:p+=[ .5-x/200.,.5+x/200 ]
        p.sort()
    pSitePop =mquantiles(SumPop,p)
    pSiteBioM=mquantiles(SumBioM,p)
    pPopDens =mquantiles(PopDens,p)
    pBioDens =mquantiles(BioDens,p)
    result={'SitePop':[],'SiteBioM':[],'PopDens':[],'BioDens':[] }
    try:
        for i in range(int(len(p)/2)):
            result['SitePop' ]+=[[CB[i],pSitePop[i] ,pSitePop[-i-1]  ]]
            result['SiteBioM']+=[[CB[i],pSiteBioM[i],pSiteBioM[-i-1] ]]
            result['PopDens' ]+=[[CB[i],pPopDens[i] ,pPopDens[-i-1]  ]]
            result['BioDens' ]+=[[CB[i],pBioDens[i] ,pBioDens[-i-1]  ]]
    except:
        print('\nGeoduckMain 372')
        for i in range(int(len(p)/2)):
            result['SitePop' ]+=[[CB[i],pSitePop[i] ,pSitePop[-i-1]  ]]
            result['SiteBioM']+=[[CB[i],pSiteBioM[i],pSiteBioM[-i-1] ]]
            result['PopDens' ]+=[[CB[i],pPopDens[i] ,pPopDens[-i-1]  ]]
            result['BioDens' ]+=[[CB[i],pBioDens[i] ,pBioDens[-i-1]  ]]
    return(result)

def SelectGood(criteria, orilist):
    n=len(criteria)
    result=[orilist[i] for i in range(n) if criteria[i]   ]
    return(result)

if __name__ == "__main__":
    import sys
    from InputOutputMDB import dataODB,resultODB
    from NewMDB import NewMDB
    inMDB=dataODB(prompt="Select input database file",DefaultDirec="H:\AnalysisPrograms2013\PyFunctions\Geoduck\SampleAIP", FileExt="Access Files (*.mdb *.accdb)")
    resultODB=resultODB(prompt="Select output database file",DefaultDirec="H:\AnalysisPrograms2013\PyFunctions\Geoduck\SampleAIP", FileExt="Access Files (*.mdb *.accdb)")

    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    
   
    
    ui = MainWindow(Dialog,inMDB,resultODB)
    Dialog.show()
    sys.exit(app.exec_())
