# -*- coding: utf-8 -*-

"""
Module implementing MainWindow and Dialog
"""

from PyQt4.QtGui import QMainWindow, QDialog,QListWidgetItem
from PyQt4.QtCore import pyqtSignature
from PyQt4 import QtCore, QtGui


from SiteDialog import SiteDialog
from ReasonOmit import ReasonOmit




class SiteInfo(QDialog, SiteDialog):
    def __init__(self,nsite=1,TransectNumber=[[]],TranChar=[[]],parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.TransectNumber=TransectNumber
        self.TranChar=TranChar
        self.MakeConnect()
        self.nsite=nsite
        self.SetDefaultValues()
        self.SiteIndex=0
        self.FillScreenValues()        
        self.setCharacteristics(self.SiteIndex)
        self.RO=ReasonOmit()
        self.NoMore=False #A logical flag that freezes the display of transects-to-omit
        
    def SetDefaultValues(self):
        self.result=list(map(lambda x:{},self.TranChar))
        for i in range(self.nsite):
            r=self.result[i]
            k=self.TransectNumber[i]
            r['MeanWeight']=266.
            r['StErrWeight']=26.6
            r['CoastLengthM']=10000
            r['StErrCLM']=1000
            r['KeysToUse']=k

    def FillScreenValues(self):
        self.NoMore=True #A logical flag that freezes the display of transects-to-omit
        self.PreviousSite.setDisabled(self.SiteIndex<=0)
        self.NextSite.setDisabled(self.SiteIndex>=(self.nsite-1))

        self.CoastLengthM.clear()
        self.CoastLengthK.clear()
        self.StErrCLM.clear()
        self.StErrCLK.clear()
        self.MeanWeight.clear()
        self.StErrWeight.clear()
        
        CurVal=self.result[self.SiteIndex]
        self.CoastLengthM.insertPlainText(str(CurVal['CoastLengthM']))
        self.StErrCLM.insertPlainText(str(CurVal['StErrCLM']))
        self.MeanWeight.insertPlainText(str(CurVal['MeanWeight']))
        self.StErrWeight.insertPlainText(str(CurVal['StErrWeight']))
        self.FixCoastLengthK()
        self.FixStErrCLK()

        self.FillTransectNumber()
        self.NoMore=False #A logical flag that freezes the display of transects-to-omit
        
        
        

    def FillTransectNumber(self):
        while self.ExcludeTransects.count()>0:
            dummy=self.ExcludeTransects.takeItem(0)
            del dummy
            
        self.ExcludeTransects.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        if self.TransectNumber[self.SiteIndex]==None:return
        if self.TransectNumber[self.SiteIndex]==[]:return
        for t in range(len(self.TransectNumber[self.SiteIndex])):
            try:
                item=QListWidgetItem('{:20d} {:20d}'.format(self.TransectNumber[self.SiteIndex][t][0],self.TransectNumber[self.SiteIndex][t][1]    ))
                self.ExcludeTransects.addItem(item)
                if self.TransectNumber[self.SiteIndex][t][2]:
                    self.ExcludeTransects.item(t).setSelected(True)
            except:
                print('\nSiteInfo 93')
                print('self.SiteIndex,t, len(self.TransectNumber[self.SiteIndex])', self.SiteIndex,t, len(self.TransectNumber[self.SiteIndex]))
                print('self.TransectNumber[self.SiteIndex][t]',self.TransectNumber[self.SiteIndex][t])

                item=QListWidgetItem('{:20d} {:20d}'.format(self.TransectNumber[self.SiteIndex][t][0],self.TransectNumber[self.SiteIndex][t][1]    ))
                self.ExcludeTransects.addItem(item)
                if self.TransectNumber[self.SiteIndex][t][2]:
                    self.ExcludeTransects.item(t).setSelected(True)
                    
       

    def setCharacteristics(self,i):
       if (self.TranChar==None) or (self.TranChar==[]) or (self.TranChar==''):   
           self.TransectCharacteristic.setText("all")
           return
       if (self.TranChar[i]==None) or (self.TranChar[i]==[]) or (self.TranChar[i]==''):   
           self.TransectCharacteristic.setText("all")
           return
       if isinstance(self.TranChar[i],(str,int)):   
           self.TransectCharacteristic.setText(str(self.TranChar))
           return
       txt=str(self.TranChar[i][0])
       for t in self.TranChar[i][1:]:
            txt+='\n'+str(t)
       self.TransectCharacteristic.setText(txt)

    
       
    def GetValues(self):
        CurVal=self.result[self.SiteIndex]
        CurVal['MeanWeight']=float(self.MeanWeight.document().toPlainText())
        CurVal['StErrWeight']=float(self.StErrWeight.document().toPlainText())
        CurVal['CoastLengthM']=float(self.CoastLengthM.document().toPlainText())
        CurVal['StErrCLM']=float(self.StErrCLM.document().toPlainText())
        self.GetKeysToUse()
    	
    def GetKeysToUse(self):
        KeysToUse=[]        
        for index in range(self.ExcludeTransects.count()):
          if not(self.ExcludeTransects.item(index).isSelected()):
            key,TransectNum=str(self.ExcludeTransects.item(index).text()).split()
            KeysToUse+=[[int(key),int(TransectNum)]]
        self.result[self.SiteIndex]['KeysToUse']=KeysToUse

    def MakeConnect(self):
        self.CoastLengthM.textChanged.connect(self.FixCoastLengthK)
        self.CoastLengthK.textChanged.connect(self.FixCoastLengthM)

        self.StErrCLM.textChanged.connect(self.FixStErrCLK)
        self.StErrCLK.textChanged.connect(self.FixStErrCLM)

        self.MeanWeight.textChanged.connect(self.CheckMeanWeight)
        self.StErrWeight.textChanged.connect(self.CheckStErrWeight)

        self.OmitAll.clicked.connect(self.NoTran)
        self.IncludeAll.clicked.connect(self.AllTran)

        self.ExcludeTransects.itemSelectionChanged.connect(self.ExcludeTransectsChanged)

        self.NextSite.clicked.connect(self.OnNext)
        self.PreviousSite.clicked.connect(self.OnPrev)
        self.QuitAnal.clicked.connect(self.OnQuit)

    def FixCoastLengthK(self):
        if self.CoastLengthM.document().toPlainText()=='':return         
        if self.CoastLengthM.document().toPlainText()=='.':return         
        try: 
           CoastLengthM=float(self.CoastLengthM.document().toPlainText())
           CoastLengthK=0.001*CoastLengthM  
           if self.CoastLengthK.document().toPlainText()=='':
               self.CoastLengthK.insertPlainText(str(CoastLengthK))
           elif CoastLengthK!=float(self.CoastLengthK.document().toPlainText()):
               self.CoastLengthK.clear()
               self.CoastLengthK.insertPlainText(str(CoastLengthK))
           
        except:
            print('\nSiteInfo 136 ')
            print('CoastLengthM',CoastLengthM )
            print('CoastLengthK',CoastLengthK )
            print('str(CoastLengthK)',str(CoastLengthK) )
            print('self.CoastLengthM.document().toPlainText()',self.CoastLengthM.document().toPlainText() )
            print('self.CoastLengthK.document().toPlainText()',self.CoastLengthK.document().toPlainText() )
            self.CoastLengthM.clear()
            self.CoastLengthK.clear()
            self.CoastLengthM.insertPlainText('10000')
            self.CoastLengthK.insertPlainText('10')

    def FixCoastLengthM(self):
        if self.CoastLengthK.document().toPlainText()=='':return
        if self.CoastLengthK.document().toPlainText()=='.':return
        try:
           CoastLengthK=float(self.CoastLengthK.document().toPlainText())
           CoastLengthM=1000.*CoastLengthK
           if self.CoastLengthM.document().toPlainText()=='':
               self.CoastLengthM.insertPlainText(str(CoastLengthM))
           elif CoastLengthM!=float(self.CoastLengthM.document().toPlainText()):
               self.CoastLengthM.clear()
               self.CoastLengthM.insertPlainText(str(CoastLengthM))
        except:
            print('\nSiteInfo 158 ')
            print('self.CoastLengthK.document().toPlainText()',self.CoastLengthK.document().toPlainText() )
            print('self.CoastLengthM.document().toPlainText()',self.CoastLengthM.document().toPlainText() )
            self.CoastLengthM.clear()
            self.CoastLengthK.clear()
            self.CoastLengthM.insertPlainText('10000')
            self.CoastLengthK.insertPlainText('10')

    def FixStErrCLK(self):
        if self.StErrCLM.document().toPlainText()=='':return
        if self.StErrCLM.document().toPlainText()=='.':return
        try:
           StErrCLM=float(self.StErrCLM.document().toPlainText())
           StErrCLK=0.001*StErrCLM
           if self.StErrCLK.document().toPlainText()=='':
               self.StErrCLK.insertPlainText(str(StErrCLK))
           elif StErrCLK!=float(self.StErrCLK.document().toPlainText()):
               self.StErrCLK.clear()
               self.StErrCLK.insertPlainText(str(StErrCLK))
        except:
            self.StErrCLM.clear()
            self.StErrCLK.clear()

            self.StErrCLM.insertPlainText('1000')
            self.StErrCLK.insertPlainText('1')

    def FixStErrCLM(self):
        if self.StErrCLK.document().toPlainText()=='':return
        if self.StErrCLK.document().toPlainText()=='.':return
        try:
           StErrCLK=float(self.StErrCLK.document().toPlainText())
           StErrCLM=1000.*StErrCLK
           if self.StErrCLM.document().toPlainText()=='':
               self.StErrCLM.insertPlainText(str(StErrCLM))
           if StErrCLM!=float(self.StErrCLM.document().toPlainText()):
               self.StErrCLM.clear()
               self.StErrCLM.insertPlainText(str(StErrCLM))
        except:
            self.StErrCLM.clear()
            self.StErrCLK.clear()

            self.StErrCLM.insertPlainText('1000')
            self.StErrCLK.insertPlainText('1')
            
    def CheckMeanWeight(self):
        if self.MeanWeight.document().toPlainText()=='':return
        if self.MeanWeight.document().toPlainText()=='.':return
        try:
            dummy=float(self.MeanWeight.document().toPlainText())
        except:
            self.MeanWeight.clear()
            self.MeanWeight.insertPlainText('266')

    def CheckStErrWeight(self):
        if self.StErrWeight.document().toPlainText()=='':return
        if self.StErrWeight.document().toPlainText()=='.':return
        try:
            dummy=float(self.StErrWeight.document().toPlainText())
        except:
            self.StErrWeight.clear()
            self.StErrWeight.insertPlainText('26.6')

    def OnNext(self):
        self.GetValues()
        self.SiteIndex+=1
        self.NoMore=False #A logical flag that freezes the display of transects-to-omit
        self.FillScreenValues()
        self.setCharacteristics(self.SiteIndex)

    def OnPrev(self):
        self.GetValues()
        self.SiteIndex-=1
        self.NoMore=False #A logical flag that freezes the display of transects-to-omit
        self.FillScreenValues()
        self.setCharacteristics(self.SiteIndex)
        self.OmitAll.setChecked(False)
        self.IncludeAll.setChecked(False)

    def OnQuit(self):
        self.GetValues()
        self.close()
        
    def NoTran(self):
        '''No transects are omitted.  Or conversely, all are incorporated into calculations.'''
        if self.NoMore:return
        self.NoMore=True

        for t in range(len(self.TransectNumber[self.SiteIndex])):
            self.TransectNumber[self.SiteIndex][t][3]=''
            self.TransectNumber[self.SiteIndex][t][2]=False
            self.ExcludeTransects.item(t).setSelected(False)
        self.IncludeAll.setChecked(False)
        self.OmitAll.setChecked(False)
        self.NoMore=False
        
    def AllTran(self):
        '''All transects are omitted.  Or conversely, none are incorporated into calculations.'''
        if self.NoMore:return
        self.NoMore=True
       
        self.RO.SetTransectNumber('')
        self.RO.exec()
        reason=self.RO.result
        for t in range(len(self.TransectNumber[self.SiteIndex])):
            self.TransectNumber[self.SiteIndex][t][3]=reason
            self.TransectNumber[self.SiteIndex][t][2]=True
            self.ExcludeTransects.item(t).setSelected(True)
        self.IncludeAll.setChecked(False)
        self.OmitAll.setChecked(False)
        self.NoMore=False

    def ExcludeTransectsChanged(self):
        if self.NoMore:return
        self.NoMore=True
        for t in range(len(self.TransectNumber[self.SiteIndex])):
            try:
                if self.ExcludeTransects.item(t).isSelected()!=self.TransectNumber[self.SiteIndex][t][2]:
                   self.TransectNumber[self.SiteIndex][t][2]= self.ExcludeTransects.item(t).isSelected()
                   if self.ExcludeTransects.item(t).isSelected():
                       self.RO.SetTransectNumber(self.TransectNumber[self.SiteIndex][t][1])
                       self.RO.exec()
                       self.TransectNumber[self.SiteIndex][t][3]=self.RO.result
                   else:
                        self.TransectNumber[self.SiteIndex][t][3]=''
                       
            except:
                print('\nSiteInfo 296')
                print(' self.SiteIndex, t, len(self.TransectNumber[self.SiteIndex]  ',  self.SiteIndex, t, len(self.TransectNumber[self.SiteIndex]))
                print(' self.TransectNumber[self.SiteIndex][t] ', self.TransectNumber[self.SiteIndex][t] )
                print(' self.ExcludeTransects.count()',self.ExcludeTransects.count())
                print(' self.ExcludeTransects.item(t).isSelected())',self.ExcludeTransects.item(t).isSelected())
                
                if self.ExcludeTransects.item(t).isSelected()==self.TransectNumber[self.SiteIndex][t][2]:
                   self.TransectNumber[self.SiteIndex][t][2]= not(self.ExcludeTransects.item(t).isSelected())
                   if self.ExcludeTransects.item(t).isSelected():
                       self.RO.SetTransectNumber(self.TransectNumber[self.SiteIndex][t][1])
                       self.RO.exec()
                       self.TransectNumber[self.SiteIndex][t][3]=self.RO.result
                   else:
                        self.TransectNumber[self.SiteIndex][t][3]=''
        self.NoMore=False
                       
        


      
if __name__ == "__main__":
    import sys
    TransectNumber=[[1,2],[3,4]]
    TranChar=['A survey', 'over there','sometime',2013,6,12]
    TransectNumber=[[[52, 112, 0, '', 2013, 8, 31, 'Cukes deeper = N'], \
                [53, 111, 0, '', 2013, 8, 31, 'Cukes deeper = Y'], \
                [55, 110, 0, '', 2013, 8, 31, 'Cukes deeper = Y'], \
                [56, 109, 0, '', 2013, 8, 31, 'Cukes deeper = N'], \
                [57, 108, 0, '', 2013, 8, 31, 'Cukes deeper = Y'], \
                [58, 107, 0, '', 2013, 8, 31, 'Cukes deeper = N.  Halfway across']], \
                [[63, 113, 0, '', 2013, 8, 31, 'Cukes deeper = Y'], \
                [64, 114, 0, '', 2013, 8, 31, 'Cukes deeper = Y. Very small cukes, many just above juvenile size.'] ]]
    TranChar=[[11], [12] ]
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = SiteInfo(nsite=2,TransectNumber=TransectNumber,TranChar=TranChar)
    #ui.setupUi(Dialog)
    ui.show()
    sys.exit(app.exec_())

