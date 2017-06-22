# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RSUAP.ui'
#
# Created: Mon Jul 15 07:33:40 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!
from numpy.random import seed
from numpy import inf
import pdb

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QAbstractListModel,QModelIndex
from PyQt4.QtGui import QListWidgetItem

from MetaTransectClass import MetaTransectClass
import RSUQueryFunc as QueryFunc
from RSUQueryFunc import AlloEqn

import sys,os
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from GetSurveys import AllSurveys
from ADO import adoBaseClass as OpenDB
from transectclass import transectclass
from NewMDB import NewMDB
from InputOutputMDB import dataODB,resultODB

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Dialog(object):

    def __init__(self,Dialog,ODB,OUTmdb):
        self.setupUi(Dialog)

        self.inMDB=ODB
        self.resultODB=OUTmdb
        self.OUTmdb=self.resultODB.ODB
        self.ODB=self.inMDB.ODB
        #pdb.set_trace()
        self.FillSurveys()
        self.FillTranChar()
        self.MakeConnect()
        self.DefaultSettings()
        
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(692, 769)
        font = QtGui.QFont()
        font.setPointSize(12)
        #pdb.set_trace()
        Dialog.setFont(font)

        
        self.AllSurveys = QtGui.QCheckBox(Dialog)
        self.AllSurveys.setGeometry(QtCore.QRect(30, 224, 141, 41))
        self.AllSurveys.setStyleSheet(_fromUtf8("font: 12pt \"MS Shell Dlg 2\";"))
        self.AllSurveys.setObjectName(_fromUtf8("AllSurveys"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 4, 241, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(290, 4, 241, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 284, 131, 241))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.USB50 = QtGui.QRadioButton(self.groupBox_2)
        self.USB50.setGeometry(QtCore.QRect(30, 210, 41, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.USB50.setFont(font)
        self.USB50.setAutoExclusive(False)
        self.USB50.setObjectName(_fromUtf8("USB50"))
        self.NumberBootstrapLabel = QtGui.QLabel(Dialog)
        self.NumberBootstrapLabel.setGeometry(QtCore.QRect(430, 290, 131, 41))
        self.NumberBootstrapLabel.setWordWrap(True)
        self.NumberBootstrapLabel.setObjectName(_fromUtf8("NumberBootstrapLabel"))
        self.NumberBootstrap = QtGui.QPlainTextEdit(Dialog)
        self.NumberBootstrap.setGeometry(QtCore.QRect(320, 290, 101, 31))
        self.NumberBootstrap.setObjectName(_fromUtf8("NumberBootstrap"))
        self.RandomSeed = QtGui.QPlainTextEdit(Dialog)
        self.RandomSeed.setGeometry(QtCore.QRect(320, 340, 101, 31))
        self.RandomSeed.setObjectName(_fromUtf8("RandomSeed"))
        self.RandomSeedLabel = QtGui.QLabel(Dialog)
        self.RandomSeedLabel.setGeometry(QtCore.QRect(430, 340, 131, 31))
        self.RandomSeedLabel.setObjectName(_fromUtf8("RandomSeedLabel"))
        self.USB89 = QtGui.QRadioButton(Dialog)
        self.USB89.setGeometry(QtCore.QRect(51, 431, 41, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.USB89.setFont(font)
        self.USB89.setAutoExclusive(False)
        self.USB89.setObjectName(_fromUtf8("USB89"))
        self.USB69 = QtGui.QRadioButton(Dialog)
        self.USB69.setGeometry(QtCore.QRect(51, 460, 41, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.USB69.setFont(font)
        self.USB69.setAutoExclusive(False)
        self.USB69.setObjectName(_fromUtf8("USB69"))
        self.USB99 = QtGui.QRadioButton(Dialog)
        self.USB99.setGeometry(QtCore.QRect(51, 402, 41, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.USB99.setFont(font)
        self.USB99.setAutoExclusive(False)
        self.USB99.setObjectName(_fromUtf8("USB99"))
        self.USB1000 = QtGui.QRadioButton(Dialog)
        self.USB1000.setGeometry(QtCore.QRect(51, 315, 59, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.USB1000.setFont(font)
        self.USB1000.setAutoExclusive(False)
        self.USB1000.setObjectName(_fromUtf8("USB1000"))
        self.USB140 = QtGui.QRadioButton(Dialog)
        self.USB140.setGeometry(QtCore.QRect(51, 344, 51, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.USB140.setFont(font)
        self.USB140.setAutoExclusive(False)
        self.USB140.setObjectName(_fromUtf8("USB140"))
        self.USB119 = QtGui.QRadioButton(Dialog)
        self.USB119.setGeometry(QtCore.QRect(51, 373, 51, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.USB119.setFont(font)
        self.USB119.setAutoExclusive(False)
        self.USB119.setObjectName(_fromUtf8("USB119"))
        self.AvailSurveys = QtGui.QListWidget(Dialog)
        self.AvailSurveys.setGeometry(QtCore.QRect(21, 35, 256, 192))
        self.AvailSurveys.setObjectName(_fromUtf8("AvailSurveys"))
        self.TransectCharacteristics = QtGui.QListWidget(Dialog)
        self.TransectCharacteristics.setGeometry(QtCore.QRect(320, 35, 256, 111))
        self.TransectCharacteristics.setObjectName(_fromUtf8("TransectCharacteristics"))
        self.DoCalcs = QtGui.QPushButton(Dialog)
        self.DoCalcs.setGeometry(QtCore.QRect(190, 440, 91, 41))
        self.DoCalcs.setObjectName(_fromUtf8("DoCalcs"))
        self.QuitBttn = QtGui.QPushButton(Dialog)
        self.QuitBttn.setGeometry(QtCore.QRect(320, 440, 91, 41))
        self.QuitBttn.setObjectName(_fromUtf8("QuitBttn"))
        self.MinDepthLabel = QtGui.QLabel(Dialog)
        self.MinDepthLabel.setGeometry(QtCore.QRect(430, 180, 131, 31))
        self.MinDepthLabel.setWordWrap(True)
        self.MinDepthLabel.setObjectName(_fromUtf8("MinDepthLabel"))
        self.MinDepth = QtGui.QPlainTextEdit(Dialog)
        self.MinDepth.setGeometry(QtCore.QRect(320, 180, 101, 31))
        self.MinDepth.setObjectName(_fromUtf8("MinDepth"))
        self.MaxDepth = QtGui.QPlainTextEdit(Dialog)
        self.MaxDepth.setGeometry(QtCore.QRect(320, 230, 101, 31))
        self.MaxDepth.setObjectName(_fromUtf8("MaxDepth"))
        self.MaxDepthLabel = QtGui.QLabel(Dialog)
        self.MaxDepthLabel.setGeometry(QtCore.QRect(430, 230, 131, 31))
        self.MaxDepthLabel.setWordWrap(True)
        self.MaxDepthLabel.setObjectName(_fromUtf8("MaxDepthLabel"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Red Sea Urchin Analysis Program", None))
        self.AllSurveys.setText(_translate("Dialog", "Do All Surveys?", None))
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Survey</span></p></body></html>", None))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Transect Characteristics</span></p></body></html>", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Upper Size Bounds (mm)", None))
        self.USB50.setToolTip(_translate("Dialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.USB50.setText(_translate("Dialog", "50", None))
        self.NumberBootstrapLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Number of Bootstrap Repititions</span></p></body></html>", None))
        self.RandomSeedLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Random Seed</span></p></body></html>", None))
        self.USB89.setToolTip(_translate("Dialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.USB89.setText(_translate("Dialog", "89", None))
        self.USB69.setToolTip(_translate("Dialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.USB69.setText(_translate("Dialog", "69", None))
        self.USB99.setToolTip(_translate("Dialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.USB99.setText(_translate("Dialog", "99", None))
        self.USB1000.setToolTip(_translate("Dialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.USB1000.setText(_translate("Dialog", "1000", None))
        self.USB140.setToolTip(_translate("Dialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.USB140.setText(_translate("Dialog", "140", None))
        self.USB119.setToolTip(_translate("Dialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.USB119.setText(_translate("Dialog", "119", None))
        self.DoCalcs.setText(_translate("Dialog", "Do\n"
"Calculations", None))
        self.QuitBttn.setText(_translate("Dialog", "Quit", None))
        self.MinDepthLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Minimum Depth (m)</span></p></body></html>", None))
        self.MaxDepthLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Maximum Depth (m)</span></p></body></html>", None))

    def FillSurveys(self):
        self.AS=AllSurveys(self.ODB)
        FullName=self.AS.GetSurvey()
        for fn in FullName:
            item=QListWidgetItem(fn)
            self.AvailSurveys.addItem(item)
        self.AvailSurveys.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

    def FillTranChar(self):
        for fieldname in ['SurveyTitle','Location','SiteNum','Year','StatArea','SubArea','InBed']:
            item=QListWidgetItem(fieldname)
            self.TransectCharacteristics.addItem(item)
        #pdb.set_trace()
        self.TransectCharacteristics.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

    def MakeConnect(self):
        #pdb.set_trace()
        self.DoCalcs.clicked.connect(self.Calculations)
        self.QuitBttn.clicked.connect(self.QuitCalcs)
        self.AllSurveys.stateChanged.connect(self.DoAllSurveys)

    def Calculations(self):
        print ('Calculations Started')
        seed(int(self.RandomSeed.document().toPlainText()))
        self.GetSelectedSurveys()
        self.GetSelectedTranChar()
        self.GetSelectedUppSizeBound()
        #pdb.set_trace()
        self.TranClassChar=MetaTransectClass(self.ODB,\
                                             self.SelectedSurveys,\
                                             self.SelectedTranchar   )
                                             
        self.PrepOUTmdb()
        #print ('\nRSUAP 237 about to start stats, self.TranClassChar.key')
        #for x in self.TranClassChar.key:print(x)
       
        CB=[99,95,90,75,50]
        nboot=int(self.NumberBootstrap.document().toPlainText())

        for i in range(self.TranClassChar.nclass):
            
            tc=transectclass(self.ODB,self.TranClassChar.key[i],self.TranClassChar.Allo[i],QueryFunc,\
                                          SizeBound=self.UppSizeBnd,\
                                          MinDepth=float(self.MinDepth.document().toPlainText()),\
                                          MaxDepth=float(self.MaxDepth.document().toPlainText()))
            CurDeterm=tc.GetFormatEstVal()
            CurCB=tc.GetPctCB(CB,nboot=nboot)

            FTC=self.TranClassChar.FormatTranClass(i)
            #Transect Classes
            self.OUTmdb.ADDTo_TranChar(FTC['SurveyTitle'],FTC['Location'],FTC['SiteNum'],FTC['Year'],FTC['StatArea'],FTC['SubArea'],FTC['InBed'],FTC['NumTran'],\
                                  tc.GetSurveyedArea(),tc.GetNumSurveyedQuadInDepthRange())
            tck=self.OUTmdb.GetTranCharKey(FTC['SurveyTitle'],FTC['Location'],FTC['SiteNum'],FTC['Year'],FTC['StatArea'],FTC['SubArea'],FTC['InBed'])

            #The confidence bounds
            for cbResult in CurCB:
                CBval=cbResult['CB']
                SN=list(filter(lambda x:x!='CB', cbResult.keys()))
                for sn in SN:                             
                        CurSize=cbResult[sn]
                        SK=self.OUTmdb.GetSizeRangeKey(CurSize['SizeLimit'][-1])
                        #pdb.set_trace()

                        self.OUTmdb.ADDTo_ConfInterval(\
                            tck,SK,\
                            CBval,\
                           CurSize['linear']['Pop'][0], CurSize['linear']['Pop'][1], \
                           CurSize['spatial']['Pop'][0], CurSize['spatial']['Pop'][1], \
                            
                           CurSize['linear']['Bmass'][0], CurSize['linear']['Bmass'][1], \
                           CurSize['spatial']['Bmass'][0], CurSize['spatial']['Bmass'][1])
                                
               
            #The estimated values
            for sn in CurDeterm.keys():
                CurSize=CurDeterm[sn]
                SK=self.OUTmdb.GetSizeRangeKey(CurSize['SizeLimit'][-1])
                self.OUTmdb.ADDTo_EstDens(\
                    CurSize['linear']['Pop'],CurSize['spatial']['Pop'],\
                    CurSize['linear']['Bmass'],CurSize['spatial']['Bmass'],\
                    TranCharKey=tck,SizeKey=SK)
                
        print('\ndone MainWindow Line 274')

             
            

    def GetSelectedUppSizeBound(self):
        self.UppSizeBnd=[]
        if self.USB50.isChecked() :self.UppSizeBnd+=[50 ] 
        if self.USB69.isChecked() :self.UppSizeBnd+=[69 ] 
        if self.USB89.isChecked() :self.UppSizeBnd+=[89 ] 
        if self.USB99.isChecked() :self.UppSizeBnd+=[99 ] 
        if self.USB119.isChecked():self.UppSizeBnd+=[119] 
        if self.USB140.isChecked():self.UppSizeBnd+=[140] 
        self.UppSizeBnd+=[inf] 

    def GetSelectedTranChar(self):
        self.SelectedTranchar=[]
        for index in range(self.TransectCharacteristics.count()):
            if self.TransectCharacteristics.item(index).isSelected():
                self.SelectedTranchar+=[self.TransectCharacteristics.item(index).text()]
        
        
    def GetSelectedSurveys(self):
        self.SelectedSurveys=[]
        survey=self.AS.GetSurvey()
        for index in range(self.AvailSurveys.count()):
            if self.AvailSurveys.item(index).isSelected():
                try:
                  self.SelectedSurveys+=[survey[index]]
                except:
                  pdb.set_trace()
                  self.SelectedSurveys+=[survey[index]]
                
    def DoAllSurveys(self):
        if self.AllSurveys.isChecked():
            for index in range(self.AvailSurveys.count()):
                self.AvailSurveys.item(index).setSelected(True)
        else:
            for index in range(self.AvailSurveys.count()):
                self.AvailSurveys.item(index).setSelected(False)
            
        
    def QuitCalcs(self):
        print ('No Calculations')
        sys.exit(app.exec_())

    def DefaultSettings(self):
        self.NumberBootstrap.insertPlainText('1000')
        self.RandomSeed.insertPlainText('756')
        self.MinDepth.insertPlainText('-1000')
        self.MaxDepth.insertPlainText('1000')
        
        self.USB1000.setDisabled(True)
        self.USB1000.setChecked(True)
        self.USB89.setChecked(True)

    def PrepOUTmdb(self):
        '''Put information into output.  Not the stats - just the metadata'''
        self.OUTmdb.ADDTo_Analysis(int(self.NumberBootstrap.document().toPlainText()),\
                                   int(self.RandomSeed.document().toPlainText()),\
                                   float(self.MinDepth.document().toPlainText()),\
                                   float(self.MaxDepth.document().toPlainText()))
        self.OUTmdb.ADDTo_SizeRange(0,self.UppSizeBnd[0])
        for x in range(1,len(self.UppSizeBnd)):
            self.OUTmdb.SizeRangeKey.Increment()
            self.OUTmdb.ADDTo_SizeRange(1+self.UppSizeBnd[x-1],self.UppSizeBnd[x]  )

        for sy in self.SelectedSurveys:
            self.OUTmdb.ADDTo_SurveyUsed(sy)

       


if __name__ == "__main__":
    import sys
    inMDB=dataODB(prompt="Select input database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")
    resultODB=resultODB(prompt="Select output database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")

    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    
   
    
    ui = Ui_Dialog(Dialog,inMDB,resultODB)
    Dialog.show()
    sys.exit(app.exec_())

