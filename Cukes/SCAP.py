#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see http://talk.maemo.org/showthread.php?t=51578
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication
from InputOutputMDB import dataODB,resultODB
from SCmain import SCmain

if __name__ == "__main__":
    import sys
    ODB=dataODB(prompt="Select input database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")
    OUTmdb=resultODB(prompt="Select output database file",DefaultDirec="d:\\scratch\\", FileExt="Access Files (*.mdb *.accdb)")

    app = QApplication(sys.argv)
    ui = SCmain(ODB,OUTmdb)
    ui.show()
    sys.exit(app.exec_())
