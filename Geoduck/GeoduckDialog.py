# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GeoduckDialog.ui'
#
# Created: Wed Oct  2 09:21:37 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

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

class GeoduckDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(604, 522)
        font = QtGui.QFont()
        font.setPointSize(12)
        Dialog.setFont(font)
        self.AllSurveys = QtGui.QCheckBox(Dialog)
        self.AllSurveys.setGeometry(QtCore.QRect(20, 210, 141, 41))
        self.AllSurveys.setStyleSheet(_fromUtf8("font: 12pt \"MS Shell Dlg 2\";"))
        self.AllSurveys.setObjectName(_fromUtf8("AllSurveys"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 10, 241, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.NumberBootstrapLabel = QtGui.QLabel(Dialog)
        self.NumberBootstrapLabel.setGeometry(QtCore.QRect(430, 120, 131, 41))
        self.NumberBootstrapLabel.setWordWrap(True)
        self.NumberBootstrapLabel.setObjectName(_fromUtf8("NumberBootstrapLabel"))
        self.NumberBootstrap = QtGui.QPlainTextEdit(Dialog)
        self.NumberBootstrap.setGeometry(QtCore.QRect(320, 120, 101, 31))
        self.NumberBootstrap.setObjectName(_fromUtf8("NumberBootstrap"))
        self.RandomSeed = QtGui.QPlainTextEdit(Dialog)
        self.RandomSeed.setGeometry(QtCore.QRect(320, 170, 101, 31))
        self.RandomSeed.setObjectName(_fromUtf8("RandomSeed"))
        self.RandomSeedLabel = QtGui.QLabel(Dialog)
        self.RandomSeedLabel.setGeometry(QtCore.QRect(430, 170, 131, 31))
        self.RandomSeedLabel.setObjectName(_fromUtf8("RandomSeedLabel"))
        self.AvailSurveys = QtGui.QListWidget(Dialog)
        self.AvailSurveys.setGeometry(QtCore.QRect(21, 40, 251, 161))
        self.AvailSurveys.setObjectName(_fromUtf8("AvailSurveys"))
        self.DoCalcs = QtGui.QPushButton(Dialog)
        self.DoCalcs.setGeometry(QtCore.QRect(190, 380, 91, 41))
        self.DoCalcs.setObjectName(_fromUtf8("DoCalcs"))
        self.QuitBttn = QtGui.QPushButton(Dialog)
        self.QuitBttn.setGeometry(QtCore.QRect(320, 380, 91, 41))
        self.QuitBttn.setObjectName(_fromUtf8("QuitBttn"))
        self.MinDepthLabel = QtGui.QLabel(Dialog)
        self.MinDepthLabel.setGeometry(QtCore.QRect(300, 280, 131, 31))
        self.MinDepthLabel.setWordWrap(True)
        self.MinDepthLabel.setObjectName(_fromUtf8("MinDepthLabel"))
        self.MinDepth = QtGui.QPlainTextEdit(Dialog)
        self.MinDepth.setGeometry(QtCore.QRect(190, 280, 101, 31))
        self.MinDepth.setObjectName(_fromUtf8("MinDepth"))
        self.MaxDepth = QtGui.QPlainTextEdit(Dialog)
        self.MaxDepth.setGeometry(QtCore.QRect(190, 330, 101, 31))
        self.MaxDepth.setObjectName(_fromUtf8("MaxDepth"))
        self.MaxDepthLabel = QtGui.QLabel(Dialog)
        self.MaxDepthLabel.setGeometry(QtCore.QRect(300, 330, 131, 31))
        self.MaxDepthLabel.setWordWrap(True)
        self.MaxDepthLabel.setObjectName(_fromUtf8("MaxDepthLabel"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(330, 0, 241, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.RunComments = QtGui.QPlainTextEdit(Dialog)
        self.RunComments.setGeometry(QtCore.QRect(320, 40, 251, 51))
        self.RunComments.setObjectName(_fromUtf8("RunComments"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Geoduck Analysis Program", None))
        self.AllSurveys.setText(_translate("Dialog", "Do All Projects?", None))
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Available Projects</p></body></html>", None))
        self.NumberBootstrapLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Number of Bootstrap Repititions</span></p></body></html>", None))
        self.RandomSeedLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Random Seed</span></p></body></html>", None))
        self.DoCalcs.setText(_translate("Dialog", "Do\n"
"Calculations", None))
        self.QuitBttn.setText(_translate("Dialog", "Quit", None))
        self.MinDepthLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Minimum Depth (m)</span></p></body></html>", None))
        self.MaxDepthLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Maximum Depth (m)</span></p></body></html>", None))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Run Comments</p></body></html>", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

