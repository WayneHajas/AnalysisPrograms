'''
2016-01-29 Modify to use standard form of allometric instead of alpha-30
2015-11-23 Modify to use CopyMDB.

2017-06-26
Coordinate stat-area and sub-area as transect characteristics.  If sub-area is selected, stat-area is automatically selected as well.

'''

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Thu Jun 13 08:20:51 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from numpy.random import seed
from numpy import inf,iinfo,int16
MinInt=iinfo(int16).min
import pdb

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QAbstractListModel,QModelIndex
from PyQt4.QtGui import QListWidgetItem

from MetaTransectClass import MetaTransectClass
import GSUQueryFunc as QueryFunc
from GSUQueryFunc import AlloEqn

import sys,os
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from GetSurveys import AllSurveys
from ADO import adoBaseClass as OpenDB
from GSUTransectClass import transectclass
from NewMDB import NewMDB
from InputOutputMDB import dataODB,resultODB
from CopyMDB import CopyMDB

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
        self.CalculateAllometric = QtGui.QCheckBox(Dialog)
        self.CalculateAllometric.setGeometry(QtCore.QRect(320, 160, 241, 61))
        self.CalculateAllometric.setStyleSheet(_fromUtf8("font: 12pt \"MS Shell Dlg 2\";"))
        self.CalculateAllometric.setObjectName(_fromUtf8("CalculateAllometric"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(320, 440, 321, 61))
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.intcpt = QtGui.QPlainTextEdit(Dialog)
        self.intcpt.setGeometry(QtCore.QRect(320, 230, 191, 31))
        self.intcpt.setObjectName(_fromUtf8("intcpt"))
        self.intcptLabel = QtGui.QLabel(Dialog)
        self.intcptLabel.setGeometry(QtCore.QRect(520, 230, 131, 31))
        self.intcptLabel.setObjectName(_fromUtf8("intcptLabel"))
        self.sdintcptLabel = QtGui.QLabel(Dialog)
        self.sdintcptLabel.setGeometry(QtCore.QRect(520, 270, 131, 31))
        self.sdintcptLabel.setObjectName(_fromUtf8("sdintcptLabel"))
        self.sdintcpt = QtGui.QPlainTextEdit(Dialog)
        self.sdintcpt.setGeometry(QtCore.QRect(320, 270, 191, 31))
        self.sdintcpt.setObjectName(_fromUtf8("sdintcpt"))
        self.sigmabetaLabel = QtGui.QLabel(Dialog)
        self.sigmabetaLabel.setGeometry(QtCore.QRect(520, 350, 131, 31))
        self.sigmabetaLabel.setObjectName(_fromUtf8("sigmabetaLabel"))
        self.mubetaLabel = QtGui.QLabel(Dialog)
        self.mubetaLabel.setGeometry(QtCore.QRect(520, 310, 131, 31))
        self.mubetaLabel.setObjectName(_fromUtf8("mubetaLabel"))
        self.sigmabeta = QtGui.QPlainTextEdit(Dialog)
        self.sigmabeta.setGeometry(QtCore.QRect(320, 350, 191, 31))
        self.sigmabeta.setObjectName(_fromUtf8("sigmabeta"))
        self.mubeta = QtGui.QPlainTextEdit(Dialog)
        self.mubeta.setGeometry(QtCore.QRect(320, 310, 191, 31))
        self.mubeta.setObjectName(_fromUtf8("mubeta"))
        self.sigmaepsilon = QtGui.QPlainTextEdit(Dialog)
        self.sigmaepsilon.setGeometry(QtCore.QRect(320, 390, 191, 31))
        self.sigmaepsilon.setObjectName(_fromUtf8("sigmaepsilon"))
        self.sigmaepsilonLabel = QtGui.QLabel(Dialog)
        self.sigmaepsilonLabel.setGeometry(QtCore.QRect(520, 390, 131, 31))
        self.sigmaepsilonLabel.setObjectName(_fromUtf8("sigmaepsilonLabel"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 284, 131, 201))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.NumberBootstrapLabel = QtGui.QLabel(Dialog)
        self.NumberBootstrapLabel.setGeometry(QtCore.QRect(130, 560, 131, 41))
        self.NumberBootstrapLabel.setWordWrap(True)
        self.NumberBootstrapLabel.setObjectName(_fromUtf8("NumberBootstrapLabel"))
        self.NumberBootstrap = QtGui.QPlainTextEdit(Dialog)
        self.NumberBootstrap.setGeometry(QtCore.QRect(20, 560, 101, 31))
        self.NumberBootstrap.setObjectName(_fromUtf8("NumberBootstrap"))
        self.RandomSeed = QtGui.QPlainTextEdit(Dialog)
        self.RandomSeed.setGeometry(QtCore.QRect(310, 560, 101, 31))
        self.RandomSeed.setObjectName(_fromUtf8("RandomSeed"))
        self.RandomSeedLabel = QtGui.QLabel(Dialog)
        self.RandomSeedLabel.setGeometry(QtCore.QRect(420, 560, 131, 31))
        self.RandomSeedLabel.setObjectName(_fromUtf8("RandomSeedLabel"))
        self.USB39 = QtGui.QRadioButton(Dialog)
        self.USB39.setGeometry(QtCore.QRect(51, 431, 41, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.USB39.setFont(font)
        self.USB39.setAutoExclusive(False)
        self.USB39.setObjectName(_fromUtf8("USB39"))
        self.USB24 = QtGui.QRadioButton(Dialog)
        self.USB24.setGeometry(QtCore.QRect(51, 460, 41, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.USB24.setFont(font)
        self.USB24.setAutoExclusive(False)
        self.USB24.setObjectName(_fromUtf8("USB24"))
        self.USB54 = QtGui.QRadioButton(Dialog)
        self.USB54.setGeometry(QtCore.QRect(51, 402, 41, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.USB54.setFont(font)
        self.USB54.setAutoExclusive(False)
        self.USB54.setObjectName(_fromUtf8("USB54"))
        self.USB1000 = QtGui.QRadioButton(Dialog)
        self.USB1000.setGeometry(QtCore.QRect(51, 315, 59, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.USB1000.setFont(font)
        self.USB1000.setAutoExclusive(False)
        self.USB1000.setObjectName(_fromUtf8("USB1000"))
        self.USB84 = QtGui.QRadioButton(Dialog)
        self.USB84.setGeometry(QtCore.QRect(51, 344, 41, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.USB84.setFont(font)
        self.USB84.setAutoExclusive(False)
        self.USB84.setObjectName(_fromUtf8("USB84"))
        self.USB69 = QtGui.QRadioButton(Dialog)
        self.USB69.setGeometry(QtCore.QRect(51, 373, 41, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.USB69.setFont(font)
        self.USB69.setAutoExclusive(False)
        self.USB69.setObjectName(_fromUtf8("USB69"))
        self.AvailSurveys = QtGui.QListWidget(Dialog)
        self.AvailSurveys.setGeometry(QtCore.QRect(21, 35, 256, 192))
        self.AvailSurveys.setObjectName(_fromUtf8("AvailSurveys"))
        self.TransectCharacteristics = QtGui.QListWidget(Dialog)
        self.TransectCharacteristics.setGeometry(QtCore.QRect(320, 35, 256, 101))
        self.TransectCharacteristics.setObjectName(_fromUtf8("TransectCharacteristics"))
        self.DoCalcs = QtGui.QPushButton(Dialog)
        self.DoCalcs.setGeometry(QtCore.QRect(190, 610, 91, 41))
        self.DoCalcs.setObjectName(_fromUtf8("DoCalcs"))
        self.QuitBttn = QtGui.QPushButton(Dialog)
        self.QuitBttn.setGeometry(QtCore.QRect(320, 610, 91, 41))
        self.QuitBttn.setObjectName(_fromUtf8("QuitBttn"))
        self.MinDepthLabel = QtGui.QLabel(Dialog)
        self.MinDepthLabel.setGeometry(QtCore.QRect(130, 510, 131, 31))
        self.MinDepthLabel.setWordWrap(True)
        self.MinDepthLabel.setObjectName(_fromUtf8("MinDepthLabel"))
        self.MinDepth = QtGui.QPlainTextEdit(Dialog)
        self.MinDepth.setGeometry(QtCore.QRect(20, 510, 101, 31))
        self.MinDepth.setObjectName(_fromUtf8("MinDepth"))
        self.MaxDepth = QtGui.QPlainTextEdit(Dialog)
        self.MaxDepth.setGeometry(QtCore.QRect(310, 510, 101, 31))
        self.MaxDepth.setObjectName(_fromUtf8("MaxDepth"))
        self.MaxDepthLabel = QtGui.QLabel(Dialog)
        self.MaxDepthLabel.setGeometry(QtCore.QRect(420, 510, 131, 31))
        self.MaxDepthLabel.setWordWrap(True)
        self.MaxDepthLabel.setObjectName(_fromUtf8("MaxDepthLabel"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Green Sea Urchin Analysis Program", None))
        self.AllSurveys.setText(_translate("Dialog", "Do All Surveys?", None))
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Survey</span></p></body></html>", None))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Transect Characteristics</span></p></body></html>", None))
        self.CalculateAllometric.setText(_translate("Dialog", "Attempt to Estimate\n"
"Allometric Relationship\n"
"from Data?", None))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:8pt;\">W=exp(alpha+beta*log(L)+epsilon)</span></p><p><span style=\" font-size:8pt;\">log(alpha)~N(mu</span><span style=\" font-size:8pt; vertical-align:sub;\">alpha</span><span style=\" font-size:8pt;\">,sigma</span><span style=\" font-size:8pt; vertical-align:sub;\">alpha</span><span style=\" font-size:8pt; vertical-align:super;\">2</span><span style=\" font-size:8pt;\">)    beta~N(mu</span><span style=\" font-size:8pt; vertical-align:sub;\">beta</span><span style=\" font-size:8pt;\">,sigma</span><span style=\" font-size:8pt; vertical-align:sub;\">beta</span><span style=\" font-size:8pt; vertical-align:super;\">2</span><span style=\" font-size:8pt;\">)    epsilon~N(0,sigma</span><span style=\" font-size:8pt; vertical-align:sub;\">epsilon</span><span style=\" font-size:8pt; vertical-align:super;\">2</span><span style=\" font-size:8pt;\">)</span></p></body></html>", None))
        self.intcptLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">mu</span><span style=\" font-size:12pt; vertical-align:sub;\">alpha</span></p></body></html>", None))
        self.sdintcptLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">sigma</span><span style=\" font-size:12pt; vertical-align:sub;\">alpha</span></p></body></html>", None))
        self.sigmabetaLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">sigma</span><span style=\" font-size:12pt; vertical-align:sub;\">beta</span></p></body></html>", None))
        self.mubetaLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">mu</span><span style=\" font-size:12pt; vertical-align:sub;\">beta</span></p></body></html>", None))
        self.sigmaepsilonLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">sigma</span><span style=\" font-size:12pt; vertical-align:sub;\">epsilon</span></p></body></html>", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Upper Size Bounds (mm)", None))
        self.NumberBootstrapLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Number of Bootstrap Repititions</span></p></body></html>", None))
        self.RandomSeedLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Random Seed</span></p></body></html>", None))
        self.USB39.setToolTip(_translate("Dialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.USB39.setText(_translate("Dialog", "39", None))
        self.USB24.setToolTip(_translate("Dialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.USB24.setText(_translate("Dialog", "24", None))
        self.USB54.setToolTip(_translate("Dialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.USB54.setText(_translate("Dialog", "54", None))
        self.USB1000.setToolTip(_translate("Dialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.USB1000.setText(_translate("Dialog", "1000", None))
        self.USB84.setToolTip(_translate("Dialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.USB84.setText(_translate("Dialog", "84", None))
        self.USB69.setToolTip(_translate("Dialog", "<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.USB69.setText(_translate("Dialog", "69", None))
        self.DoCalcs.setText(_translate("Dialog", "Do\n"
"Calculations", None))
        self.QuitBttn.setText(_translate("Dialog", "Quit", None))
        self.MinDepthLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Minimum Depth (m)</span></p></body></html>", None))
        self.MaxDepthLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Maximum Depth (m)</span></p></body></html>", None))
    def FillSurveys(self):
        self.AS=AllSurveys(self.ODB)
        FullName=self.AS.GetCombo()
        for fn in FullName:
            item=QListWidgetItem(fn)
            self.AvailSurveys.addItem(item)
        self.AvailSurveys.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

    def FillTranChar(self):
        for fieldname in ['SurveyTitle','SubSampleLocation','Year','StatArea','SubArea']:
            item=QListWidgetItem(fieldname)
            self.TransectCharacteristics.addItem(item)
        #pdb.set_trace()
        self.TransectCharacteristics.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

    def MakeConnect(self):
        #pdb.set_trace()
        self.DoCalcs.clicked.connect(self.Calculations)
        self.QuitBttn.clicked.connect(self.QuitCalcs)
        self.AllSurveys.stateChanged.connect(self.DoAllSurveys)
        self.TransectCharacteristics.itemSelectionChanged.connect(self.CoordStatAreaSubArea)

    def Calculations(self):
        print ('\nCalculations Started')
        seed(int(self.RandomSeed.document().toPlainText()))
        self.GetSelectedSurveys()
        self.GetSelectedTranChar()
        self.GetSelectedUppSizeBound()
        self.CalcAllometric=self.CalculateAllometric.isChecked()
        self.GetAlloParam()
        self.TranClassChar=MetaTransectClass(self.ODB,\
                                             self.SelectedSurveys,\
                                             self.SelectedTranchar,\
                                             CalcAllo=self.CalcAllometric,
                                             DefaultAllo=AlloEqn(intcpt=self.AlloParam['intcpt'],\
                                                                 sdintcpt=self.AlloParam['sdintcpt'],\
                                                                 mnbeta=self.AlloParam['mubeta'],\
                                                                 sdbeta=self.AlloParam['sigmabeta'],\
                                                                 sigmawithin=self.AlloParam['sigmaepsilon']))
        self.PrepOUTmdb()
        dictSelectedSurveys=self.SelectedSurveystoDict()
        CopyMDB(self.ODB,self.OUTmdb,dictSelectedSurveys)
        
        CB=[99,95,90,75,50]
        nboot=int(self.NumberBootstrap.document().toPlainText())

        for i in range(self.TranClassChar.nclass):
                
            FTC=self.TranClassChar.FormatTranClass(i)
            if self.TranClassChar.TranClass!=[[]]:
                print('\nSurveyTitle: ',FTC['SurveyTitle'] )
                print('SubSampleLocation: ',FTC['SubSampleLocation'] )
                if FTC['Year'    ]!=MinInt: print('Year:     ',FTC['Year'    ])
                if FTC['StatArea']!=MinInt: print('StatArea: ',FTC['StatArea'] )
                if FTC['SubArea' ]!=MinInt: print('SubArea:  ',FTC['SubArea' ] )
            print(len(self.TranClassChar.key[i]), ' transects')
            
            tc=transectclass(self.ODB,self.TranClassChar.key[i],self.TranClassChar.Allo[i],QueryFunc,\
                                          SizeBound=self.UppSizeBnd,\
                                          MinDepth=float(self.MinDepth.document().toPlainText()),\
                                          MaxDepth=float(self.MaxDepth.document().toPlainText()))
            CurDeterm=tc.GetFormatEstVal()
            CurCB=tc.GetPctCB(CB,nboot=nboot)

            
            #Transect Classes
            self.OUTmdb.ADDTo_TranChar(FTC['SurveyTitle'],FTC['SubSampleLocation'],FTC['Year'],FTC['StatArea'],FTC['SubArea'],FTC['InBed'],FTC['NumTran'],\
                                  tc.GetSurveyedArea(),\
                                  tc.GetNumSurveyedQuadInDepthRange(),
                                  tc.AlloSource.intcpt,tc.AlloSource.sdintcpt,\
                                  tc.AlloSource.mnbeta,tc.AlloSource.sdbeta,
                                  tc.AlloSource.sigmawithin)
            tck=self.OUTmdb.GetTranCharKey(FTC['SurveyTitle'],FTC['SubSampleLocation'],FTC['Year'],FTC['StatArea'],FTC['SubArea'],FTC['InBed'])            
            tc.WriteTransectResults(self.OUTmdb,tck)


            #The confidence bounds
            for cbResult in CurCB:
                CBval=cbResult['CB']
                SN=list(filter(lambda x:x!='CB', cbResult.keys()))
                for sn in SN:                             
                        CurSize=cbResult[sn]
                        SK=self.OUTmdb.GetSizeRangeKey(CurSize['SizeLimit'][-1])

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

    def GetAlloParam(self):
        #pdb.set_trace()
        self.AlloParam={}
        try:
            self.AlloParam['intcpt']=float(self.intcpt.document().toPlainText()  )
        except:
            print ('MainWindow 267,type(self.intcpt.document().toPlainText() )',type(self.intcpt.document().toPlainText() ),self.intcpt.document().toPlainText() )
            self.AlloParam['intcpt']=None 
        try:
            self.AlloParam['sdintcpt']=float(self.sdintcpt.document().toPlainText())
        except:
            self.AlloParam['sdintcpt']=None 
        try:
            self.AlloParam['mubeta']=float(self.mubeta.document().toPlainText() )
        except:
            self.AlloParam['mubeta']=None 
        try:
            self.AlloParam['sigmabeta']=float(self.sigmabeta.document().toPlainText() )
        except:
            self.AlloParam['sigmabeta']=None 
        try:
            self.AlloParam['sigmaepsilon']=float(self.sigmaepsilon.document().toPlainText() )
        except:
            self.AlloParam['sigmaepsilon']=None 
            
            

    def GetSelectedUppSizeBound(self):
        self.UppSizeBnd=[]
        if self.USB24.isChecked():self.UppSizeBnd+=[24] 
        if self.USB39.isChecked():self.UppSizeBnd+=[39] 
        if self.USB54.isChecked():self.UppSizeBnd+=[54] 
        if self.USB69.isChecked():self.UppSizeBnd+=[69] 
        if self.USB84.isChecked():self.UppSizeBnd+=[84] 
        self.UppSizeBnd+=[inf] 

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
            
    def CoordStatAreaSubArea(self):
        '''Make sure statarea and subarea are coherent'''
        #Update list of selected transect-characteristics
        self.GetSelectedTranChar()
        
        #if subarea is selected, force statarea to be selected        
        if ('SubArea' in self.SelectedTranchar) and not('StatArea' in self.SelectedTranchar) :
            for index in range(self.TransectCharacteristics.count()):
                if self.TransectCharacteristics.item(index).text()=='StatArea':
                    self.TransectCharacteristics.item(index).setSelected(True)
                    self.GetSelectedTranChar()
            
        
    def QuitCalcs(self):
        print ('No Calculations')
        sys.exit(app.exec_())

    def DefaultSettings(self):
        self.intcpt.insertPlainText('-6.8664802585167077')
        self.sdintcpt.insertPlainText('0.034723646241811214')
        self.mubeta.insertPlainText('2.7276732805478963')
        self.sigmabeta.insertPlainText('0.0088232364135380891')
        self.sigmaepsilon.insertPlainText('0.15967472910118682')
        self.NumberBootstrap.insertPlainText('10000')
        self.RandomSeed.insertPlainText('756')
        self.MinDepth.insertPlainText('-1000')
        self.MaxDepth.insertPlainText('1000')
        
        
        self.CalculateAllometric.setChecked(True)
        self.USB1000.setDisabled(True)
        self.USB1000.setChecked(True)
        self.USB54.setChecked(True)
        self.USB24.autoExclusive=False

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
            self.OUTmdb.ADDTo_SurveyUsed(sy[0],sy[1])
            
           
    def SelectedSurveystoDict(self):
        '''Convert self.SelectedSurveys as a list of dictionaries'''
        if isinstance(self.SelectedSurveys[0],dict):
            return(self.SelectedSurveys)
        result=[{'SurveyTitle':t[0], 'Year':t[1]}  for t in self.SelectedSurveys]
        return(result)

       


if __name__ == "__main__":
    import sys
    inMDB=dataODB(prompt="Select input database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")
    resultODB=resultODB(prompt="Select output database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")

    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    
   
    
    ui = Ui_Dialog(Dialog,inMDB,resultODB)
    Dialog.show()
    sys.exit(app.exec_())

