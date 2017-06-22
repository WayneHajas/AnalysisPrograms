# -*- coding: utf-8 -*-
"""
Created on Wed May 29 13:04:37 2013

@author: hajasw
"""

import os
os.chdir('H:\\AnalysisPrograms2013\\PyFunctions\\RSU')
from distutils.core import setup
import py2exe
setup(console=['RSUAP.exe'])