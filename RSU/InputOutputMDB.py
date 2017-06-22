
import sys
from PyQt4 import QtGui
from PyQt4.QtCore import *

import os
from win32com.client.gencache import EnsureDispatch as Dispatch
from ADO import adoBaseClass as OpenDB
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from GetSurveys import AllSurveys
from NewMDB import NewMDB
import pdb


class dataODB:
    def __init__(self,prompt="Select !!input!! database file",DefaultDirec="T:\\", FileExt="Access Files (*.mdb *.accdb)"):

        app = QtGui.QApplication(sys.argv)
        self.w = QtGui.QWidget()
        self.MDBfile = QtGui.QFileDialog.getOpenFileNamesAndFilter(self.w, prompt,DefaultDirec,FileExt)[0][0]
        self.ODB=OpenDB(self.MDBfile)
        del self.w,app

class resultODB:
    def __init__(self,prompt="Select **output** database file",DefaultDirec="c:\\", FileExt="Access Files (*.mdb *.accdb)"):

        app = QtGui.QApplication(sys.argv)
        self.w = QtGui.QWidget()
        self.MDBfile = QtGui.QFileDialog.getSaveFileName(self.w, prompt,DefaultDirec,FileExt)
        self.ODB=NewMDB(self.MDBfile)
        del self.w,app


        

if __name__ == "__main__":
    inMDB=dataODB(prompt="Select input database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")
    outMDB=resultODB(prompt="Select output database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")

    print ('inMDB',inMDB.MDBfile)
    print ('outMDB',outMDB.MDBfile)
