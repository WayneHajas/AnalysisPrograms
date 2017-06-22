#
import sys
from cx_Freeze import setup, Executable

base = None
#if sys.platform == 'win32':
#    base = 'Win32GUI'
    
sys.path.append('d:\\Coding\\AnalysisPrograms2013\\PyFunctions\\Cukes\\MakeInstall')


includes= []
packages=[	'ADO',
		'BCA',
		'californicusQueryFunc',
		'CukeQueryFunc',
		'CukeTransect',
		'CukeTransectclass',
		'GetSurveys',
		'InputOutputMDB',
		'InterpProd',
		'KeyValues',
		'MainWin',
		'MetaTransectClass',
		'miniataQueryFunc',
		'NewMDB',
		'pallidaQueryFunc',
		'quadrat',
		'ReasonOmit',
		'RejectDialog',
		'SCAP',
		'SCmain',
		'SiteDialog',
		'SiteInfo',
		'SumAbundance',
		'transect',
		'transectclass',
		'wchNorm',
		'win32verstamp',
		'win32timezone','zipimport','scipy.stats','scipy.stats.mstats','scipy.special','scipy.special._ufuncs',\
		'numpy','zipimport'] 
executables = [\
    Executable('SCAP.py', base=base)]




options = {
    'build_exe': {
        'includes':includes,
        'packages':packages
    }
}
setup(name='SCAP',
      version='September 2013',
      description='Sea Cucumber Analysis Program',
      options=options,
      executables=executables
      )
