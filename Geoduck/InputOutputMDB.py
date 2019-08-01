
'''
20190731
    Updated from PyQt4 to PyQt5
    No intended change to functionality
    '''
import sys
from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import QApplication, QLabel,QWidget,QFileDialog
getOpenFileNames=QFileDialog.getOpenFileNames
getSaveFileName=QFileDialog.getSaveFileName

import os
from win32com.client.gencache import EnsureDispatch as Dispatch
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from ADO import adoBaseClass as OpenDB
from GetSurveys import AllSurveys
from NewMDB import NewMDB


class dataODB:
    def __init__(self,prompt="Select !!input!! database file",DefaultDirec="T:\\", FileExt="Access Files (*.mdb *.accdb)"):

        app = QApplication(sys.argv)
        self.w = QWidget()
        self.MDBfile = getOpenFileNames(self.w, prompt,DefaultDirec,FileExt)[0][0]
        self.ODB=OpenDB(self.MDBfile)
        del self.w,app

class resultODB:
    def __init__(self,prompt="Select **output** database file",DefaultDirec="c:\\", FileExt="Access Files (*.mdb *.accdb)"):

        app = QApplication(sys.argv)
        self.w = QWidget()
        self.MDBfile = QFileDialog.getSaveFileName(self.w, prompt,DefaultDirec,FileExt)[0]
        self.ODB=NewMDB(self.MDBfile)
        del self.w,app


        

if __name__ == "__main__":
    inMDB=dataODB(prompt="Select input database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")
    outMDB=resultODB(prompt="Select output database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")

    print ('inMDB',inMDB.MDBfile)
    print ('outMDB',outMDB.MDBfile)
