from numpy import ndarray
from scipy.stats import beta,nbinom

from datetime import datetime

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from SFdate import SFplot

def RandSFCorr(NumShow, SF=None, sfp=None,date=None,CalcNumDuck=True,Randomize=True):
    '''RandSFCorr(NumShow, SF=None, sfp=None,date=None,CalcNumDuck=True)
    Make a random-correction to the number of shows in order to get the number of geoducks.
    *SF is the show-factor.  zero to one.  It takes precedent over show-factor plot.
    *sfp is an instance of SFplot.  It represents a show-factor plot or a list of show-factor plots.
    *date is only relevent if SF is undefined.
    *CalcNumDuck indicates that the number of geoducks in the show-factor plot(s) needs to be re-calculated
    '''
    if SF==1: return(NumShow)

    if (SF==None) and (sfp==None):#ignore show-factor effect if there is no indication of value to use.
        return(NumShow)
    
    if isinstance(SF,(list,ndarray)): return(list(map(lambda sf: RandSFCorr(NumShow, SF=sf, ,CalcNumDuck=CalcNumDuck,Randomize=Randomize)  ,SF)))


    if not(SF==None):#A single deterministic value for show-factor
        if not(Randomize):#deterministic
            return(float(NumShow)/SF)

        #Probabilistic
        result=NumShow+nbinom.rvs(NumShow,SF)
        return(result)


    #Get the show-factor from a set of show-factor data
    sf=sfp.RandSF(date=date,CalcNumDuck=CalcNumDuck)
    result=RandSFCorr(NumShow, SF=sf, CalcNumDuck=CalcNumDuck,Randomize=Randomize)
    return(result)
    
if __name__ == "__main__":
    from ADOSFdate import ADOmultiSFplot
    from ADO import adoBaseClass as OpenDB

    databasepath='H:\AnalysisPrograms2013\PyFunctions\Geoduck\SampleAIP\Geoduck_Bio.mdb'
    NumShow=95
    ODB=OpenDB(databasepath)
    SurveyName="Boatswain Bank"
    SurveyYear=2001
    SFPlotNum=[1,2]

    
    sfp=ADOmultiSFplot( ODB,SurveyName,SurveyYear,SFPlotNum=None)
    print('\n  RandSFCorr(NumShow,SF=1.  ) ',RandSFCorr(NumShow,SF=1.))
    print('\n  RandSFCorr(NumShow,SF=0.95) ',RandSFCorr(NumShow,SF=0.95))
    print(  '  RandSFCorr(NumShow,SF=0.95) ',RandSFCorr(NumShow,SF=0.95))
    print(  '  RandSFCorr(NumShow,SF=0.95) ',RandSFCorr(NumShow,SF=0.95))
    print(  '  RandSFCorr(NumShow,SF=0.95) ',RandSFCorr(NumShow,SF=0.95))
    print(  '  RandSFCorr(NumShow,SF=0.95) ',RandSFCorr(NumShow,SF=0.95))
    print(  '  RandSFCorr(NumShow,SF=0.95) ',RandSFCorr(NumShow,SF=0.95))
    print(  '  RandSFCorr(NumShow,SF=0.95) ',RandSFCorr(NumShow,SF=0.95))
    print(  '  RandSFCorr(NumShow,SF=0.95) ',RandSFCorr(NumShow,SF=0.95))
    print(  '  RandSFCorr(NumShow,SF=0.95) ',RandSFCorr(NumShow,SF=0.95))
    print(  '  RandSFCorr(NumShow,SF=0.95) ',RandSFCorr(NumShow,SF=0.95))

    print('\n sfp.EstSF() \n',  sfp.EstSF() )
    print( ' RandSFCorr(NumShow,sfp=sfp) \n ', RandSFCorr(NumShow,sfp=sfp) )

    

