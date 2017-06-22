#Class to represent a 'class' of transects that will be used to represent an entity.  Typically, all the transects in a site.


from ADO import adoBaseClass as OpenDB
from numpy.random import choice
from transect import transect
from SumAbundance import SumAbundance,CalcDensity,CalcAvgWeight
from BCA import BCA
import pdb


class transectclass:
    def __init__(self,ODB,key,AlloSource,QueryFunc,SizeBound=None,MinDepth=-999,MaxDepth=999):
        '''transectclass(ODB,key,QueryFunc,SizeBound=None)
        ODB (open database) is an instance of the ADO class
        key is a list of values from the headers table
        AlloSource is an entity that generates allometric functions
        QueryFunc is library of function to create species-specific functions and data
        SizeBound is a list of upper bounds on the size-classes'''

        self.MinDepth,self.MaxDepth=MinDepth,MaxDepth
        try:
            self.transects=list(map(lambda k:transect(ODB,k,QueryFunc,SizeBound=SizeBound,MinDepth=self.MinDepth,MaxDepth=self.MaxDepth),key))
            self.transects=list(filter(lambda t:t.nquad>0,self.transects))
        except:
            print('\ntransectclass 25')
            print (key[:5])
            print('dir(QueryFunc)', dir(QueryFunc))
            print('type(QueryFunc)', type(QueryFunc))
            self.transects=list(map(lambda k:transect(ODB,k,QueryFunc,SizeBound=SizeBound,MinDepth=self.MinDepth,MaxDepth=self.MaxDepth),key))
        self.ntransect=len(self.transects)
        self.AlloSource=AlloSource
        self.AE=self.AlloSource.AvgWgtDetermAE()

    def GetSurveyedArea(self):
        result=sum(list(map(lambda t:t.GetQuadArea(),self.transects)))
        return(result)

    def GetSurveyedWidth(self):
        result=sum(list(map(lambda t:t.GetTranWidth(),self.transects)))
        return(result)

    def GetAbundance(self,AverageWeight=None,UseDeterm=False):
        if (AverageWeight==None):
            if UseDeterm:
                self.AE=self.AlloSource.AvgWgtDetermAE()
            else:
                self.AE=self.AlloSource.AvgWgtRndAE()
            AverageWeight=self.GetAvgWeight()
        byTran=list(map(lambda t:t.GetAbundance(AverageWeight=AverageWeight,UseDeterm=UseDeterm),self.transects))
        try:
            result=SumAbundance(byTran)
        except:
            print ('transectclass 48 byTran\n',byTran)
            result=SumAbundance(byTran)
        return(result)

    def GetAvgAbundance(self,AverageWeight=None,UseDeterm=False):
        Abundance=self.GetAbundance(AverageWeight=AverageWeight,UseDeterm=UseDeterm)
        SurveyedArea=self.GetSurveyedArea()
        SurveyedWidth=self.GetSurveyedWidth()
        result={}
        result['linear' ]=CalcDensity(Abundance,SurveyedWidth)
        result['spatial']=CalcDensity(Abundance,SurveyedArea)
        return(result)

    def GetAvgWeight(self):
        '''transectclass.GetAvgWeight()
         Provide average weight (by size-class) for all the animals in all the transects'''
        for t in self.transects:t.CalcAbundMeasured(self.AE)
        ByTransect=list(map(lambda t:t.MeasAbund,self.transects))
        try:
            Abund=SumAbundance(ByTransect)
        except:
            print ('transect class 69 ByTransect\n',ByTransect)
            Abund=SumAbundance(ByTransect)
        try:
            AverageWeight=CalcAvgWeight(Abund)
        except:
            print ('\ntransectclass 74,Abund\n',Abund)
            AverageWeight=CalcAvgWeight(Abund)
        return(AverageWeight)

    def RandomizeSizeProb(self,UseDeterm=False):
        for t in self.transects:t.RandomizeSizeProb(UseDeterm=UseDeterm)

    def DetermMeanAbund(self):
        self.RandomizeSizeProb(UseDeterm=True)
        self.AE=self.AlloSource.AvgWgtDetermAE()
        result=self.GetAvgAbundance(AverageWeight=self.GetAvgWeight(),UseDeterm=True)
        return(result)
            

    def RandAbund(self,nboot=None):
        if nboot!=None:
            return(list(map(lambda dummy:self.RandAbund(),range(nboot))))
        SampTran=SampleTransect(self)
        result=SampTran.GetAvgAbundance(AverageWeight=SampTran.GetAvgWeight())
        return(result)

    def GetJackAbund(self):
        self.RandomizeSizeProb(UseDeterm=True)
        result=[]
        for i in range(self.ntransect):
            CurJack=JackKnife(self,i)
            result+=[CurJack.MeanAbund]
        return(result)
    
    def GetQuantile(self,p,nboot=1000):
        determEst=self.DetermMeanAbund()
        probSample=self.RandAbund(nboot=nboot)
        JackSample=self.GetJackAbund()
        result=BCA(determEst,probSample,JackSample,p=p)
        return(result)
    def GetSizeLim(self):
        '''Size boundaries in a more tabular form'''
        try:
           SizeBound=self.transects[0].SizeBound
           nSizeBound=len(SizeBound)
        except:
           print('transectclass 114')
           print('self.transects[0].SizeBound',self.transects[0].SizeBound)
           import pdb
           pdb.set_trace()
           SizeBound=self.transects[0].SizeBound
           SizeBound=len(SizeBound)
           
           
        SizeLim=[[0,SizeBound[0]]]
        for j in range(1,nSizeBound):SizeLim+=[[1+ SizeBound[j-1] ,SizeBound[j]]]
        return(SizeLim)

    def GetPctCB(self,CB,nboot=1000):
        '''transectclass(CB,nboot=1000)
         0<CB<100 is a single value or a list

         Produce confidence bounds on mean-abundance'''
     
        if isinstance(CB,(int,float)):
            nCB=1
            if CB<=0:return(None)
            if CB>=100:return(None)
            p=[.5-CB/200.,.5+CB/200 ]
            CB=[CB]
        else:
            CB=list(filter(lambda x:(x>0) and (x<100),CB))
            nCB=len(CB)
            if nCB==0:return(None)
            CB.sort(reverse=True)
            p=[]
            for cb in CB:p+=[.5-cb/200.,.5+cb/200]
            p.sort()
        q=self.GetQuantile(p,nboot=nboot)

        #Now it's just a matter of resturcturing q into something that is easy to put into a table
        #SizeLimits that can be put in a table
        #pdb.set_trace()
        SizeLim=self.GetSizeLim()
       
        result=[]
        for i in range(nCB):
            CBresult={'CB':CB[i]}
            for SL in SizeLim:
                SizeResult={'SizeLimit':SL}
                kname='USL'+str(SL[1])

                CurLinear={}
                CurLinear['Pop'  ]=[q['linear'][kname]['Pop'  ][i], q['linear'][kname]['Pop'  ][-i-1]]
                CurLinear['Bmass']=[q['linear'][kname]['Bmass'][i], q['linear'][kname]['Bmass'][-i-1]]
                SizeResult['linear']=CurLinear
                
                CurSpatial={}
                if q['spatial']!=None:
                    CurSpatial['Pop'  ]=[q['spatial'][kname]['Pop'  ][i], q['spatial'][kname]['Pop'  ][-i-1]]
                    CurSpatial['Bmass']=[q['spatial'][kname]['Bmass'][i], q['spatial'][kname]['Bmass'][-i-1]]
                else:
                    CurSpatial['Pop'  ]=[None,None]
                    CurSpatial['Bmass']=[None,None]
                    
                SizeResult['spatial']=CurSpatial
                CBresult[kname]=SizeResult
            result+=[CBresult]
        return(result)
                
        

    def GetFormatEstVal(self):
        '''transectclass.GetFormatEstVal()        

         Produce formatted estimates of mean-abundance'''
     
        q=self.DetermMeanAbund()

        #Now it's just a matter of resturcturing q into something that is easy to put into a table
        #SizeLimits that can be put in a table
        #pdb.set_trace()
        SizeLim=self.GetSizeLim()
       
        result={}

        for SL in SizeLim:
            SizeResult={'SizeLimit':SL}
            kname='USL'+str(SL[1])

            CurLinear={}
            CurLinear['Pop'  ]=q['linear'][kname]['Pop'  ]
            CurLinear['Bmass']=q['linear'][kname]['Bmass']
            SizeResult['linear']=CurLinear
            
            CurSpatial={}
            if q['spatial']!=None:
                CurSpatial['Pop'  ]=q['spatial'][kname]['Pop'  ]
                CurSpatial['Bmass']=q['spatial'][kname]['Bmass']
            else:
                CurSpatial['Pop'  ]=None
                CurSpatial['Bmass']=None
            
            SizeResult['spatial']=CurSpatial
            result[kname]=SizeResult
        return(result)

class SampleTransect(transectclass):
    def __init__(self,tc,ntransect=None,replace=True):
        '''SampleTransect(tc,SampleSize=None,replace=True)
        tc is an instance of transectclass
        SampleSize is the number of transects in teh resample - will default to the same number as in tc
        replace indicates if sampling is done with replacement'''

        self.ntransect= ntransect
        if self.ntransect==None:self.ntransect=tc.ntransect
        self.transects=choice(tc.transects,size=self.ntransect,replace=replace)
        self.AlloSource=tc.AlloSource
        self.AE=self.AlloSource.AvgWgtRndAE()
        self.RandomizeSizeProb()

class JackKnife(transectclass):
    def __init__(self,tc,i):

        #Get a deep copy of the list of transects
        self.transects=list(map(lambda x:x,tc.transects))
        dummy=self.transects.pop(i)
        self.ntransect= len(self.transects)
        self.AlloSource=tc.AlloSource
        self.AE=self.AlloSource.AvgWgtRndAE()
        if self.ntransect==0:
            self.MeanAbund=None
        else:
            self.MeanAbund=self.GetAvgAbundance(UseDeterm=True)
     
                            
def GetStats(ODB,key,AlloSource,QueryFunc,SizeBound=None,MinDepth=-999,MaxDepth=999,nboot=1000,p=[.025,.975]):
     print('\ntransectclass 143')
     print('key',key)
     print('Creating Transect Class')
     
     TC=transectclass(ODB,key,AlloSource,QueryFunc,SizeBound=SizeBound,MinDepth=MinDepth,MaxDepth=MaxDepth)
     print('Doing Calculations')
     result=TC.GetQuantile(p,nboot=nboot)
     return(result)


if __name__ == "__main__":

    from numpy import inf
    import sys
    sys.path.append('D:\Coding\AnalysisPrograms2013\PyFunctions\RSU')

    import RSUQueryFunc as QueryFunc
    databasepath='d:\scratch\Tofino2010Site4.mdb'
    ODB=OpenDB(databasepath)
    SizeBound=[89]
    TransectNumber=[12322,12325,12328,12339,12352]
    def AE(L):return(1)
    def sum2(x,USL,PB,AvgWeight):
        result=0.
        for t in x:
             try:
                 result+=t.GetUnMeas.UnMeas.GetAbundance(AvgWeight)[USL][PB]
             except:
                 dummy=True
        return(result)


    AlloSource=QueryFunc.AlloEqn()
    p=[.025,.975]




    ByTransect=list(map(lambda tn: transect(ODB,tn,QueryFunc,SizeBound=SizeBound),TransectNumber))
    for bt in ByTransect:
        print (bt.key,\
               bt.nquad,
               ' ',\
               sum(list(map(lambda q:q.GetMeasAbundance(AE)['USL89' ]['Pop'  ],bt.quad))),\
               sum(list(map(lambda q:q.UnMeas.GetAbundance(AvgWeight=[1,1])['USL89' ]['Pop'  ],bt.quad))),\
               bt.GetAbundance(AE=AE, AverageWeight=[1,1],UseDeterm=True)[  'USL89' ]['Pop'  ],\
               ' ',\
               sum(list(map(lambda q:q.GetMeasAbundance(AE)['USLinf']['Pop'  ],bt.quad))),\
               sum(list(map(lambda q:q.UnMeas.GetAbundance(AvgWeight=[1,1])['USLinf']['Pop'  ],bt.quad))),\
               bt.GetAbundance(AE=AE, AverageWeight=[1,1],UseDeterm=True)[  'USLinf'  ]['Pop'  ],\

               ' ', \
               sum(list(map(lambda q:q.GetMeasAbundance(AE)['USL89' ]['Bmass'],bt.quad))),\
               sum(list(map(lambda q:q.UnMeas.GetAbundance(AvgWeight=[1,1])['USL89' ]['Bmass'],bt.quad))),\
               bt.GetAbundance(AE=AE, AverageWeight=[1,1],UseDeterm=True)[  'USL89' ]['Bmass'],\

               ' ',\
               sum(list(map(lambda q:q.GetMeasAbundance(AE)['USLinf']['Bmass'],bt.quad))),\
               sum(list(map(lambda q:q.UnMeas.GetAbundance(AvgWeight=[1,1])['USLinf']['Bmass'],bt.quad))),\
               bt.GetAbundance(AE=AE, AverageWeight=[1,1],UseDeterm=True)['USLinf' ]['Bmass']\
               ) 


    tc=transectclass(ODB,TransectNumber,AlloSource,QueryFunc,SizeBound=SizeBound)
    print  ('\ntc.DetermMeanAbund()',tc.DetermMeanAbund())
    print ('\ndone transect class')
