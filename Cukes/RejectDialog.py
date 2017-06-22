# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RejectReason.ui'
#
# Created: Thu Aug 15 13:45:45 2013
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

class RejectDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(367, 287)
        Dialog.setAutoFillBackground(False)
        self.TransectHeading = QtGui.QLabel(Dialog)
        self.TransectHeading.setGeometry(QtCore.QRect(70, 20, 261, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.TransectHeading.setFont(font)
        self.TransectHeading.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.TransectHeading.setAlignment(QtCore.Qt.AlignCenter)
        self.TransectHeading.setObjectName(_fromUtf8("GiveCount"))
       #self.GroupReasons = QtGui.QGroupBox(Dialog)
       #self.GroupReasons.setGeometry(QtCore.QRect(49, 60, 271, 161))
       #self.GroupReasons.setObjectName(_fromUtf8("GroupReasons"))
        self.Finished = QtGui.QPushButton(Dialog)
        self.Finished.setGeometry(QtCore.QRect(140, 250, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Finished.setFont(font)
        self.Finished.setObjectName(_fromUtf8("Finished"))
        self.splitter = QtGui.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(60, 71, 256, 151))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.UserReason = QtGui.QPlainTextEdit(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.UserReason.setFont(font)
        self.UserReason.setObjectName(_fromUtf8("UserReason"))
        self.NoAnimals = QtGui.QPushButton(self.splitter)
        self.NoAnimals.setObjectName(_fromUtf8("NoAnimals"))
        self.NotHarvestable = QtGui.QPushButton(self.splitter)
        self.NotHarvestable.setObjectName(_fromUtf8("NotHarvestable"))
        self.PoorQuality = QtGui.QPushButton(self.splitter)
        self.PoorQuality.setObjectName(_fromUtf8("PoorQuality"))
        self.SeparateAnalysis = QtGui.QPushButton(self.splitter)
        self.SeparateAnalysis.setObjectName(_fromUtf8("SeparateAnalysis"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Reason to omit transect from calculations", None))
        self.TransectHeading.setText(_translate("Dialog", "Transect Number", None))
       #self.GroupReasons.setTitle(_translate("Dialog", "Reason", None))
        self.Finished.setText(_translate("Dialog", "Done", None))
        self.NoAnimals.setText(_translate("Dialog", "No animals", None))
        self.NotHarvestable.setText(_translate("Dialog", "Animals are not harvestable", None))
        self.PoorQuality.setText(_translate("Dialog", "Poor quality animals", None))
        self.SeparateAnalysis.setText(_translate("Dialog", "To be analyzed separately", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

