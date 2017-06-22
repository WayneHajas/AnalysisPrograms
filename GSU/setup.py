#
import sys
from cx_Freeze import setup, Executable

base = None
#if sys.platform == 'win32':
#    base = 'Win32GUI'
    
sys.path.append('d:\\Coding\\AnalysisPrograms2013\\PyFunctions\\GSU\\MakeInstall')
path='H:\cxfreeze\ado'


includes= []
packages=[	'ADO',
		'BCA',
		'CreateExe',
		'DataAllometric',
		'GetSurveys',
		'GSUQueryFunc',
		'InputOutputMDB',
		'InterpProd',
		'KeyValues',
		'MeasAnimals',
		'mquantiles',
		'MetaTransectClass',
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
    Executable('GSUAP.py', base=base)]




options = {
    'build_exe': {
        'includes':includes,
        'packages':packages
    }
}
setup(name='GSUAP',
      version='July 2013',
      description='Green Sea Urchin Analysis Program',
      options=options,
      executables=executables
      )
