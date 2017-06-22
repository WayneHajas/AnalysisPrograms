from numpy import ndarray,array
from numpy.random import choice
from mquantiles import mquantiles
#from InterpProd import WCHinterp
from wchNorm import InvNorm
from BCA import Naive_CB
import pdb

def LevelFromList(x,n=None,newq=None,nlevel=31):
    x2=sorted(x)
    oldn=len(x2)
    #oldq=list(map(lambda i: (i+.5)/float(oldn),   range(oldn)))
    useq=newq
    if useq==None:useq=list(map(lambda i: (i+.5)/float(   nlevel),   range(   nlevel)))
    newLev=mquantiles(x2,useq)
    return(newLev)

def LevelFromStErr(x,n=None,newq=None,nlevel=31):
    EstVal=x[0]
    SteVal=x[1]
    useq=newq
    if useq==None:useq=list(map(lambda i: (i+.5)/float(   nlevel),   range(   nlevel)))
    result=InvNorm(useq)
    result=list(map(lambda x: x*SteVal,result))
    result=list(map(lambda x: x+EstVal,result))
    return(result)
    
def LevelFromDict(x,nlevel=31,newq=None):
    useq=newq
    if useq==None:useq=list(map(lambda i: (i+.5)/float(   nlevel),   range(   nlevel)))
    if isinstance(x,(list,ndarray)):
        result=list(map(lambda y: LevelFromDict(y,newq=useq)  ,x))
        return(result)    
    result={'SampPopDensity':LevelFromList(x['SampPopDensity'],newq=useq),\
            'CL':LevelFromStErr(x['CL'],newq=useq),\
            'MW':LevelFromStErr(x['MW'],newq=useq)}
        
    return(result)

def RotateList(x,nplace):
    nval=len(x)
    if (nplace%nval)==0:return(x)
    nv=(nplace%nval)

    for i in range(nv):
        dummy=x.pop()
        x.insert(0,dummy)
    return(x)



def BuildSequence(levels,index,randomize=True):
    if index<0:return(None)
    x=levels
    nlevel=len(x)
    if index>(-1+nlevel):return(None)
    if randomize:x=choice(x,replace=False,size=len(x))

    result=list(map(lambda i: x[(i+index*(1+int(i/nlevel)))%nlevel   ]   ,range(nlevel*nlevel)))
    return(result)

def BuildSeqForDict(x,InitIndex, newq=None,randomize=True,nlevel=31):
    useq=newq
    if useq==None:useq=list(map(lambda i: (i+.5)/float(   nlevel),   range(   nlevel)))
    levels=LevelFromDict(x,newq=useq)
    result=[\
        BuildSequence(levels['SampPopDensity'],InitIndex+0,randomize=True),\
        BuildSequence(levels['CL'            ],InitIndex+1,randomize=True),\
        BuildSequence(levels['MW'            ],InitIndex+2,randomize=True)]
    return(result)

def CalcOverallStats(SiteVal, newq=None,randomize=True,CB=[99,95,90,75,50],nlevel=31):
    useq=newq
    if useq==None:useq=list(map(lambda i: (i+.5)/float(   nlevel),   range(   nlevel)))
    nsite=len(SiteVal)

    ParamVal=list(map(lambda x,i:BuildSeqForDict(x,3*i, newq=newq,randomize=randomize),SiteVal,range(nsite)))
    PopDens=list(map(lambda x:x[0],ParamVal))
    CoastLe=list(map(lambda x:x[1],ParamVal))
    MeanWgt=list(map(lambda x:x[2],ParamVal))

    iiter=list(range(len(ParamVal[0][0])))

    TotalCL=list(map(lambda i:sum(list(map(lambda c:  c[i],CoastLe)))                           ,iiter))
    TotaPop=list(map(lambda i:sum(list(map(lambda p,c:p[i]*c[i],PopDens,CoastLe)))              ,iiter))
    TotaBma=list(map(lambda i:sum(list(map(lambda p,c,w:p[i]*c[i]*w[i],PopDens,CoastLe,MeanWgt))) ,iiter))


    PopDens=list(map(lambda p,c:p/c, TotaPop,TotalCL))
    BmaDens=list(map(lambda b,c:b/c, TotaBma,TotalCL))

    PopDensCB=Naive_CB(PopDens,CB=CB)
    BmaDensCB=Naive_CB(BmaDens,CB=CB)
    TotaPopCB=Naive_CB(TotaPop,CB=CB)
    TotaBmaCB=Naive_CB(TotaBma,CB=CB)
    result={'PopDensCB':PopDensCB,'BmaDensCB':BmaDensCB,'TotaPopCB':TotaPopCB,'TotaBmaCB':TotaBmaCB}
    return(result)
    
                   
    


if __name__ == "__main__":
        
    from numpy import corrcoef,sqrt
    from numpy.random import seed
    import matplotlib.pyplot as plt
    from scipy.stats import norm,lognorm

    import matplotlib.pyplot as plt
    
    seed(756)
    CB=[99]
    nrep=50
    CL=[10000,100]
    MW=[266,26.6]


    nlevel=200
    newq=list(map(lambda i: (i+.5)/float(   nlevel),   range(   nlevel)))
    SampPopDensity=list(map(lambda x: lognorm.isf(x,1),newq))
    asDict={'SampPopDensity':SampPopDensity,'CL':CL,'MW':MW}
    SiteVal=5*[asDict]
    test200=list(map(lambda i:CalcOverallStats(SiteVal, newq=newq,randomize=True,CB=CB,nlevel=nlevel)['PopDensCB'],range(nrep)))
    L200=list(map(lambda x:x[0],test200))
    U200=list(map(lambda x:x[1],test200))

    print( lognorm.isf(.5/50.,1),  lognorm.isf(1.-.5/50.,1))
    print( lognorm.isf(.5/100.,1),  lognorm.isf(1.-.5/100.,1))
    print( lognorm.isf(.5/200.,1),  lognorm.isf(1.-.5/200.,1))
    
    print('\nCalcOverallStats(SiteVal, newq=newq,randomize=True,CB=CB,nlevel=nlevel)\n',CalcOverallStats(SiteVal, newq=newq,randomize=True,CB=CB,nlevel=nlevel))


    nlevel=100
    newq=list(map(lambda i: (i+.5)/float(   nlevel),   range(   nlevel)))
    SampPopDensity=list(map(lambda x: lognorm.isf(x,1),newq))
    asDict={'SampPopDensity':SampPopDensity,'CL':CL,'MW':MW}
    SiteVal=5*[asDict]
    test100=list(map(lambda i:CalcOverallStats(SiteVal, newq=newq,randomize=True,CB=CB,nlevel=nlevel)['PopDensCB'],range(nrep)))
    L100=list(map(lambda x:x[0],test100))
    U100=list(map(lambda x:x[1],test100))



    nlevel=50
    newq=list(map(lambda i: (i+.5)/float(   nlevel),   range(   nlevel)))
    SampPopDensity=list(map(lambda x: lognorm.isf(x,1),newq))
    asDict={'SampPopDensity':SampPopDensity,'CL':CL,'MW':MW}
    SiteVal=5*[asDict]
    test50=list(map(lambda i:CalcOverallStats(SiteVal, newq=newq,randomize=True,CB=CB,nlevel=nlevel)['PopDensCB'],range(nrep)))
    L50 =list(map(lambda x:x[0],test50 ))
    U50 =list(map(lambda x:x[1],test50 ))

    

    bins=list(map(lambda i:80+5*i,range(13)))
    plt.hist(L50 ,alpha=0.25,fc='r')#,bins=bins)
    plt.hist(L100,alpha=0.50,fc='b')#,bins=bins)
    plt.hist(L200,alpha=0.75,fc='g')#,bins=bins)
    plt.hist(U50 ,alpha=0.25,fc='r')
    plt.hist(U100,alpha=0.50,fc='b')
    plt.hist(U200,alpha=0.75,fc='g')
    plt.show()
   
    
    
    
    
