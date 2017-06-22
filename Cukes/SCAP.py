#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see http://talk.maemo.org/showthread.php?t=51578
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication
from InputOutputMDB import dataODB,resultODB
from SCmain import SCmain
import pdb

if __name__ == "__main__":
    import sys
    ODB=dataODB(prompt="Select input database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")
    OUTmdb=resultODB(prompt="Select output database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")

    app = QApplication(sys.argv)
    ui = SCmain(ODB,OUTmdb)
    #pdb.set_trace()
    ui.show()
    sys.exit(app.exec_())
