'''
2016-01-12
Modified the progress-messages that appear on the console.  Site number, if defined, will appear.
'''

from numpy.random import seed
from numpy import inf,iinfo,int16,sqrt
MinInt=iinfo(int16).min


from PyQt4.QtGui import QMainWindow, QDialog,QListWidgetItem
from PyQt4.QtCore import pyqtSignature
from PyQt4 import QtCore, QtGui


from MetaTransectClass import MetaTransectClass
from CukeTransectclass import CukeTransectclass
from ParamLevelCombo import CalcOverallStats
from CopyMDB import CopyMDB
from CompositeAsTransectclass import CompositeAsTransectclass
from BCA import Naive_CB

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from GetSurveys import AllSurveys
from ADO import adoBaseClass as OpenDB
from MainWin import Ui_MainWindow

class SCmain(QMainWindow, Ui_MainWindow):

    def __init__(self,ODB,OUTmdb,parent = None):
        self.inMDB=ODB
        self.resultODB=OUTmdb
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.MakeConnect()
        
        self.OUTmdb=self.resultODB.ODB
        self.ODB=self.inMDB.ODB
        self.FillSurveys()
        self.FillTranChar()
        self.MakeConnect()
        self.DefaultSettings()

   

        
    def FillSurveys(self):
        self.AS=AllSurveys(self.ODB)
        FullName=self.AS.GetCombo()
        for fn in FullName:
            item=QListWidgetItem(fn)
            self.AvailSurveys.addItem(item)
        self.AvailSurveys.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

    def FillTranChar(self):
        for fieldname in ['Project','Site','Year','StatArea','SubArea']:
            item=QListWidgetItem(fieldname)
            self.TransectCharacteristics.addItem(item)
        self.TransectCharacteristics.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

    def MakeConnect(self):
        self.DoCalcs.clicked.connect(self.Calculations)
        self.QuitBttn.clicked.connect(self.QuitCalcs)
        self.AllSurveys.stateChanged.connect(self.DoAllSurveys)
        

    def Calculations(self):

        #Do nothing unless some surveys are selected
        if self.AvailSurveys.count()==0:return
        
        seed(int(self.RandomSeed.document().toPlainText()))
        try:
            self.GetSelectedSurveys()
        except:
            self.QuitCalcs()
            
        #copy stubs of input tables to the output file.
        dictSelectedSurveys=self.SelectedSurveystoDict()
        CopyMDB(self.ODB,self.OUTmdb,dictSelectedSurveys)
        
        print ('\nCalculations Started')
        self.GetSelectedTranChar()
        self.TranClassChar=MetaTransectClass(self.ODB,\
                                             self.SelectedSurveys,\
                                             self.SelectedTranchar)
       
        CB=[99,95,90,75,50]
        self.Comments=self.RunComments.document().toPlainText()
        self.nboot=int(self.NumberBootstrap.document().toPlainText())
        self.seed=int(self.RandomSeed.document().toPlainText())
        self.LeastDepth=float(self.MinDepth.document().toPlainText())
        self.MostDepth=float(self.MaxDepth.document().toPlainText())

        self.SourceMeanWeight='LogBook'
        if self.MarketSample.isChecked():self.SourceMeanWeight='MarketSample'
        if self.Biodata.isChecked():self.SourceMeanWeight='Biodata'

        self.species='californicus'
        import californicusQueryFunc as QueryFunc
        if self.miniata.isChecked():
            self.species='miniata'
            import miniataQueryFunc as QueryFunc
        if self.pallida.isChecked():
            self.species='pallida'
            import pallidaQueryFunc as QueryFunc
        AlloSource=QueryFunc.AlloEqn()  
        self.PrepOUTmdb()      

        SiteCB =[]
        SiteEst=[]
        for i in range(self.TranClassChar.nclass):
            FMT=self.TranClassChar.FormatTranClass(i)

            print('\n' )
            if FMT['Project' ]!='Combined': print('Project:  ',FMT['Project' ])
            if FMT['Site'    ]!=MinInt:     print('Site:     ',FMT['Site' ])
            if FMT['Year'    ]!=MinInt:     print('Year:     ',FMT['Year'    ])
            if FMT['StatArea']!=MinInt:     print('StatArea: ',FMT['StatArea'] )
            if FMT['SubArea' ]!=MinInt:     print('SubArea:  ',FMT['SubArea' ] )
            print ('Reading Data')

            CTC=CukeTransectclass(self.ODB,i,self.TranClassChar,AlloSource,QueryFunc,MinDepth=self.LeastDepth,MaxDepth=self.MostDepth)
            print('NumTran:  ',len(CTC.IndexTranUse) )

            self.OUTmdb.ADDTo_TranChar(FMT['Project'],FMT['Site'],FMT['Year'],FMT['StatArea'],FMT['SubArea'],FMT['NumTran'],\
                                  CTC.GetSurveyedArea())
            print('Writing results for individual transects')
            CTC.WriteTransectResults(self.OUTmdb, FMT)
            print('Writing estimated values')
            SiteEst+=[CTC.WriteSiteResults(self.OUTmdb,FMT,self.SourceMeanWeight)]
            print('Calculating confidence bounds')
            SiteCB +=[CTC.WriteSiteCB(self.OUTmdb,FMT,nboot=self.nboot,CB=CB)]
            self.OUTmdb.TranCharKey.Increment()



        print ('\nCombined')
        if self.TranClassChar.nclass>1:
            self.WriteOverall(SiteEst,SiteCB,CB)
        else:
            FMT=self.TranClassChar.FormatTranClass(0)
            dummy=CompositeAsTransectclass(CTC,SiteCB[0]['SampPopDensity'])
            dummy.WriteCB(self.OUTmdb,FMT,CB=CB)
            dummy.WriteResults(self.OUTmdb,FMT,self.SourceMeanWeight)
        
        print('\ndone MainWindow Line 147')
        return

    def WriteOverall(self,SiteEst,SiteCB,CB,nlevel=100):
        nsite=len(SiteCB)

        #Estimated Values
        EstPop=sum(list(map(lambda x:x['EstPop'],SiteEst)))
        EstBma=sum(list(map(lambda x:x['EstBma'],SiteEst)))
        CL    =sum(list(map(lambda x:x['CL'    ],SiteEst)))
        PopDens=EstPop/CL
        BmaDens=EstBma/CL
        self.OUTmdb.ADDTo_Results_Overall(PopDens,EstPop,BmaDens,EstBma)

        #Confidence Bounds
        CBoverall=CalcOverallStats(SiteCB, newq=None,randomize=True,CB=CB,nlevel=nlevel)
        if nsite==1:
            CBoverall['PopDensCB']=Naive_CB(SiteEst[0]['PopDens'],CB=CB)
            CBoverall['BmaDens']  =Naive_CB(SiteEst[0]['BmaDens'],CB=CB)
        for i in range(len(CB)):
            self.OUTmdb.ADDTo_Results_OverallConfBounds(CB[i],\
                           CBoverall['PopDensCB'][i][0],    CBoverall['PopDensCB'][i][1],\
                           CBoverall['TotaPopCB'][i][0],    CBoverall['TotaPopCB'][i][1],\
                           CBoverall['BmaDensCB'][i][0],    CBoverall['BmaDensCB'][i][1],\
                           CBoverall['TotaBmaCB'][i][0],    CBoverall['TotaBmaCB'][i][1])
                                     

    def GetSelectedTranChar(self):
        self.SelectedTranchar=[]
        for index in range(self.TransectCharacteristics.count()):
            if self.TransectCharacteristics.item(index).isSelected():
                self.SelectedTranchar+=[self.TransectCharacteristics.item(index).text()]
        
        
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

    def DefaultSettings(self):
        self.NumberBootstrap.insertPlainText('10000')
        self.RandomSeed.insertPlainText('756')
        self.MinDepth.insertPlainText('-1000')
        self.MaxDepth.insertPlainText('1000')
        self.californicus.setChecked(True)
        self.MarketSample.setChecked(True)
        

    def PrepOUTmdb(self):
        '''Put information into output.  Not the stats - just the metadata'''
        self.OUTmdb.ADDTo_Results_Header(self.Comments,self.species,str(self.nboot),str(self.seed),str(self.LeastDepth),str(self.MostDepth))
        for ss in self.SelectedSurveys:
            self.OUTmdb.ADDTo_SurveyUsed(ss[0],str(ss[1]))

       
    def SelectedSurveystoDict(self):
        '''Convert self.SelectedSurveys as a list of dictionaries'''
        if isinstance(self.SelectedSurveys[0],dict):
            return(self.SelectedSurveys)
        result=[{'Project':t[0], 'Year':t[1]}  for t in self.SelectedSurveys]
        return(result)


if __name__ == "__main__":
    import sys
    inMDB=dataODB(prompt="Select input database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")
    resultODB=resultODB(prompt="Select output database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")

    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    
   
    
    ui = MainWindow(Dialog,inMDB,resultODB)
    Dialog.show()
    sys.exit(app.exec_())
