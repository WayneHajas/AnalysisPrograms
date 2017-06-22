#
import sys
from cx_Freeze import setup, Executable

base = None
#if sys.platform == 'win32':
#    base = 'Win32GUI'
    
sys.path.append('d:\\Coding\\AnalysisPrograms2013\\PyFunctions\\RSU\\MakeInstall')


includes= []
packages=[	'ADO',
		'BCA',
		'GetSurveys',
		'RSUQueryFunc',
		'InputOutputMDB',
		'InterpProd',
		'KeyValues',
		'MeasAnimals',
		'MetaTransectClass',
		'mquantiles',
		'NewMDB',
		'quadrat',
		'SumAbundance',
		'transect',
		'transectclass',
		'UnMeasAnimals',\
		'win32verstamp',\
		'win32timezone','zipimport','scipy.stats','scipy.stats.mstats','scipy.special','scipy.special._ufuncs',\
		'numpy','zipimport'] 
executables = [\
    Executable('RSUAP.py', base=base)]




options = {
    'build_exe': {
        'includes':includes,
        'packages':packages
    }
}
setup(name='RSUAP',
      version='June 2014',
      description='Red Sea Urchin Analysis Program',
      options=options,
      executables=executables
      )
