# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BySite.ui'
#
# Created: Mon Aug 12 10:40:31 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

'''
2015-04-23
I have adjusted the window to distinguish between the column of key-numbers from the Header-Table and the column of transect-numbers.
A couple of text boxes have been added.  Other items on the window have been re-sized to make room for the new headings.'''


from PyQt4 import QtCore, QtGui

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


class SiteDialog(object):

    
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(731, 382)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 141, 141))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.TransectCharacteristic = QtGui.QLabel(self.groupBox_2)
        self.TransectCharacteristic.setGeometry(QtCore.QRect(10, 20, 141, 101))
        self.TransectCharacteristic.setObjectName(_fromUtf8("TransectCharacteristic"))
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(190, 10, 231, 131))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.MaxDepthLabel = QtGui.QLabel(self.groupBox_3)
        self.MaxDepthLabel.setGeometry(QtCore.QRect(120, 70, 81, 31))
        self.MaxDepthLabel.setWordWrap(True)
        self.MaxDepthLabel.setObjectName(_fromUtf8("MaxDepthLabel"))
        self.StErrWeight = QtGui.QPlainTextEdit(self.groupBox_3)
        self.StErrWeight.setGeometry(QtCore.QRect(10, 70, 101, 31))
        self.StErrWeight.setObjectName(_fromUtf8("StErrWeight"))
        self.MeanWeight = QtGui.QPlainTextEdit(self.groupBox_3)
        self.MeanWeight.setGeometry(QtCore.QRect(10, 20, 101, 31))
        self.MeanWeight.setObjectName(_fromUtf8("MeanWeight"))
        self.MinDepthLabel = QtGui.QLabel(self.groupBox_3)
        self.MinDepthLabel.setGeometry(QtCore.QRect(120, 20, 81, 31))
        self.MinDepthLabel.setWordWrap(True)
        self.MinDepthLabel.setObjectName(_fromUtf8("MinDepthLabel"))
        self.groupBox_4 = QtGui.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 170, 411, 111))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.MaxDepthLabel_2 = QtGui.QLabel(self.groupBox_4)
        self.MaxDepthLabel_2.setGeometry(QtCore.QRect(120, 70, 81, 31))
        self.MaxDepthLabel_2.setWordWrap(True)
        self.MaxDepthLabel_2.setObjectName(_fromUtf8("MaxDepthLabel_2"))
        self.StErrCLM = QtGui.QPlainTextEdit(self.groupBox_4)
        self.StErrCLM.setGeometry(QtCore.QRect(10, 70, 101, 31))
        self.StErrCLM.setObjectName(_fromUtf8("StErrCLM"))
        self.CoastLengthM = QtGui.QPlainTextEdit(self.groupBox_4)
        self.CoastLengthM.setGeometry(QtCore.QRect(10, 20, 101, 31))
        self.CoastLengthM.setObjectName(_fromUtf8("CoastLengthM"))
        self.MinDepthLabel_2 = QtGui.QLabel(self.groupBox_4)
        self.MinDepthLabel_2.setGeometry(QtCore.QRect(120, 20, 81, 31))
        self.MinDepthLabel_2.setWordWrap(True)
        self.MinDepthLabel_2.setObjectName(_fromUtf8("MinDepthLabel_2"))
        self.CoastLengthK = QtGui.QPlainTextEdit(self.groupBox_4)
        self.CoastLengthK.setGeometry(QtCore.QRect(220, 20, 101, 31))
        self.CoastLengthK.setObjectName(_fromUtf8("CoastLengthK"))
        self.MaxDepthLabel_3 = QtGui.QLabel(self.groupBox_4)
        self.MaxDepthLabel_3.setGeometry(QtCore.QRect(330, 70, 81, 31))
        self.MaxDepthLabel_3.setWordWrap(True)
        self.MaxDepthLabel_3.setObjectName(_fromUtf8("MaxDepthLabel_3"))
        self.StErrCLK = QtGui.QPlainTextEdit(self.groupBox_4)
        self.StErrCLK.setGeometry(QtCore.QRect(220, 70, 101, 31))
        self.StErrCLK.setObjectName(_fromUtf8("StErrCLK"))
        self.MinDepthLabel_3 = QtGui.QLabel(self.groupBox_4)
        self.MinDepthLabel_3.setGeometry(QtCore.QRect(330, 20, 81, 31))
        self.MinDepthLabel_3.setWordWrap(True)
        self.MinDepthLabel_3.setObjectName(_fromUtf8("MinDepthLabel_3"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(460, -1, 191, 31))
        self.label.setObjectName(_fromUtf8("label"))
        
        self.OmitAll = QtGui.QPushButton(Dialog)
        self.OmitAll.setGeometry(QtCore.QRect(460, 275, 200, 24))
        self.OmitAll.setStyleSheet(_fromUtf8("font: 8pt \"MS Shell Dlg 2\";"))
        self.OmitAll.setObjectName(_fromUtf8("OmitAll"))

        self.IncludeAll = QtGui.QPushButton(Dialog)
        self.IncludeAll.setGeometry(QtCore.QRect(460, 299, 200, 24))
        self.IncludeAll.setStyleSheet(_fromUtf8("font: 8pt \"MS Shell Dlg 2\";"))
        self.IncludeAll.setObjectName(_fromUtf8("IncludeAll"))


        self.ExcludeTransects = QtGui.QListWidget(Dialog)
        self.ExcludeTransects.setGeometry(QtCore.QRect(460, 70, 190, 201)) ##460, 90, 190, 181###
        self.ExcludeTransects.setObjectName(_fromUtf8("ExcludeTransects"))

        self.PreviousSite = QtGui.QPushButton(Dialog)
        self.PreviousSite.setGeometry(QtCore.QRect(240, 300, 75, 23))
        self.PreviousSite.setObjectName(_fromUtf8("PreviousSite"))

        self.NextSite = QtGui.QPushButton(Dialog)
        self.NextSite.setGeometry(QtCore.QRect(380, 300, 75, 23))
        self.NextSite.setObjectName(_fromUtf8("NextSite"))
        self.QuitAnal = QtGui.QPushButton(Dialog)
        self.QuitAnal.setGeometry(QtCore.QRect(310, 300, 75, 23))
        self.QuitAnal.setObjectName(_fromUtf8("QuitAnal"))

        self.ExcludeTransectHeader = QtGui.QGroupBox(Dialog)
        self.ExcludeTransectHeader.setGeometry(QtCore.QRect(460, 12, 191, 55)) #460, 8, 191, 40
        self.ExcludeTransectHeader.setObjectName(_fromUtf8("ExcludeTransectHeader"))
        self.splitter = QtGui.QSplitter(self.ExcludeTransectHeader)
        self.splitter.setGeometry(QtCore.QRect(10, 10, 112, 11)) 
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.TransectNumber = QtGui.QLabel(self.splitter)
        self.TransectNumber.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.TransectNumber.setFont(font)
        self.TransectNumber.setScaledContents(True)
        self.TransectNumber.setAlignment(QtCore.Qt.AlignCenter)
        self.TransectNumber.setWordWrap(True)
        self.TransectNumber.setIndent(0)
        self.TransectNumber.setObjectName(_fromUtf8("TransectNumber"))
        self.splitter_2 = QtGui.QSplitter(self.ExcludeTransectHeader)
        self.splitter_2.setGeometry(QtCore.QRect(30, 20, 125, 26))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.HeadersKey = QtGui.QLabel(self.splitter_2)
        self.HeadersKey.setMinimumSize(QtCore.QSize(50, 20))#50, 25
        font = QtGui.QFont()
        font.setPointSize(10)
        self.HeadersKey.setFont(font)
        self.HeadersKey.setAlignment(QtCore.Qt.AlignCenter)
        self.HeadersKey.setWordWrap(True)
        self.HeadersKey.setIndent(0)
        self.HeadersKey.setObjectName(_fromUtf8("HeadersKey"))
        self.TransectNumber_2 = QtGui.QLabel(self.splitter_2)
        self.TransectNumber_2.setMinimumSize(QtCore.QSize(75, 20)) #75, 30
        font = QtGui.QFont()
        font.setPointSize(10)
        self.TransectNumber_2.setFont(font)
        self.TransectNumber_2.setAlignment(QtCore.Qt.AlignCenter)
        self.TransectNumber_2.setWordWrap(True)
        self.TransectNumber_2.setIndent(0)
        self.TransectNumber_2.setObjectName(_fromUtf8("TransectNumber_2"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Site Information", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Transect Characteristics", None))
        self.TransectCharacteristic.setText(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">TransectCharacteristic 1</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">TransectCharacteristic 2</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">TransectCharacteristic 3</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">TransectCharacteristic 4</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">TransectCharacteristic 5</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.groupBox_3.setTitle(_translate("Dialog", "Mean Weight", None))
        self.MaxDepthLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Standard Error (grams)</span></p></body></html>", None))
        self.MinDepthLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Estimated Value(grams)</span></p></body></html>", None))
        self.groupBox_4.setTitle(_translate("Dialog", "Coast Length", None))
        self.MaxDepthLabel_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Standard Error (metres)</span></p></body></html>", None))
        self.MinDepthLabel_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Estimated Value(metres)</span></p></body></html>", None))
        self.MaxDepthLabel_3.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">(kilometres)</span></p></body></html>", None))
        self.MinDepthLabel_3.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">(kilometres)</span></p></body></html>", None))
        #self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Transects to EXCLUDE from Analysis</p></body></html>", None))
        self.ExcludeTransectHeader.setTitle(_translate("Dialog", "Transects to EXCLUDE from Analysis", None))
        
        self.OmitAll.setText(_translate("Dialog", "Include All Transects In Calculations", None))
        self.IncludeAll.setText(_translate("Dialog", "Exclude All Transects from Calculations", None))
        self.PreviousSite.setText(_translate("Dialog", "Previous", None))
        self.NextSite.setText(_translate("Dialog", "Next", None))
        self.QuitAnal.setText(_translate("Dialog", "Finished", None))
        
        self.HeadersKey.setText(_translate("ExcludeTransect", "Headers Key", None))
        self.TransectNumber_2.setText(_translate("ExcludeTransect", "Transect Number", None))



 




if __name__ == "__main__":
    import sys
    TransectNumber=[[1,2],[3,4]]
    TranChar=['A survey', 'over there','sometime',2013,6,12]
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = SCsite(Dialog,TransectNumber,TranChar)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

