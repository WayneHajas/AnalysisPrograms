# -*- coding: utf-8 -*-

"""
Module implementing MainWindow and Dialog
"""

from PyQt4.QtGui import QMainWindow, QDialog,QListWidgetItem
from PyQt4.QtCore import pyqtSignature
from PyQt4 import QtCore, QtGui


from RejectDialog import RejectDialog

import pdb



class ReasonOmit(QDialog, RejectDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.MakeConnect()
        self.SetDefaultValues()
        
    def SetDefaultValues(self):
        self.UserReason.insertPlainText('')

       
       
    def GetValues(self):
        self.result=self.UserReason.document().toPlainText()#pdb.set_trace()
        


    def MakeConnect(self):
        self.NoAnimals.clicked.connect(self.OnNoAnimals)
        self.NotHarvestable.clicked.connect(self.OnNotHarvestable)
        self.PoorQuality.clicked.connect(self.OnPoorQuality)
        self.SeparateAnalysis.clicked.connect(self.OnSeparateAnalysis)

        self.Finished.clicked.connect(self.OnFinished)


    def OnNoAnimals(self):
        #pdb.set_trace()
        self.UserReason.clear()
        self.UserReason.insertPlainText('No animals')
        return
    def OnNotHarvestable(self):
        self.UserReason.clear()
        self.UserReason.insertPlainText('Animals are not harvestable')
        return
    def OnPoorQuality(self):
        self.UserReason.clear()
        self.UserReason.insertPlainText('Poor quality animals')
        return
    def OnSeparateAnalysis(self):
        self.UserReason.clear()
        self.UserReason.insertPlainText('To be analyzed separately')
        return


    def OnFinished(self):
        #pdb.set_trace()
        self.GetValues()
        self.close()
        return



    def NoTran(self):
        if self.OmitAll.isChecked():
            for index in range(self.ExcludeTransects.count()):
                self.ExcludeTransects.item(index).setSelected(True)
            self.IncludeAll.setChecked(False)
        
    def AllTran(self):
        if self.IncludeAll.isChecked():
            for index in range(self.ExcludeTransects.count()):
                self.ExcludeTransects.item(index).setSelected(False)
            self.OmitAll.setChecked(False)
    def SetTransectNumber(self,TransectNumber=None):
        #pdb.set_trace()
        if TransectNumber==None:
            self.TransectHeading.setText('All Transects')
        elif TransectNumber=='':
            self.TransectHeading.setText('All Transects')
        elif TransectNumber==[]:
            self.TransectHeading.setText('All Transects')
        elif isinstance(TransectNumber,str):
            self.TransectHeading.setText(TransectNumber)
        else:
            try:
                self.TransectHeading.setText('Transect number '+str(TransectNumber))
            except:
                print('\nReason Omit 94')
                print('TransectNumber',TransectNumber)
                self.TransectHeading.setText('Transect number '+str(TransectNumber))
        
       
       



      
if __name__ == "__main__":
    import sys
    TransectNumber=[[1,2],[3,4]]
    TranChar=['A survey', 'over there','sometime',2013,6,12]
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = ReasonOmit(nsite=3,TransectNumber=3*[TransectNumber],TranChar=3*[TranChar])
    #ui.setupUi(Dialog)
    ui.show()
    sys.exit(app.exec_())

