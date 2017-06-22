#
import sys
from cx_Freeze import setup, Executable

base = None
#if sys.platform == 'win32':
#    base = 'Win32GUI'
    
sys.path.append('H:\\AnalysisPrograms2013\\PyFunctions\\Geoduck\\MakeInstall')


includes= []
packages=[	'win32verstamp',    
		'ADOSFdate',
		'ADOWeightVal',
		'GAP',
		'GDtransect',
		'GDuckTransectclass',
		'GeoduckDialog',
		'GeoduckMain',
		'geoduckQueryFunc',
		'GetSurveys',
		'InputOutputMDB',
		'MetaTransectClass',
		'NegBinom_Beta',
		'NewMDB',
		'SFdate',
		'SiteSize',
		'WeightVal',
		'ADO',
		'BCA',
		'GDQueryFunc',
		'InterpProd',
		'KeyValues',
		'MeasAnimals',
		'mquantiles',
		'ParamLevelCombo',
		'win32verstamp',
		'win32timezone','zipimport','scipy.stats','scipy.stats.mstats','scipy.special','scipy.special._ufuncs', \
		'SumAbundance','numpy','zipimport'] 
executables = [\
    Executable('GAP.py', base=base)]



options = {
    'build_exe': {
        'includes':includes,
        'packages':packages
    }
}
setup(name='GAP',
      version='November 2013',
      description='Geoduck Analysis Program',
      options=options,
      executables=executables
      )
