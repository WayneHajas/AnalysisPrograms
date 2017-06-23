#Class to represent a transect
from numpy import inf
from ADO import adoBaseClass as OpenDB
from quadrat import quadrat
from InterpProd import InterpProb,WCHinterp
from SumAbundance import SumAbundance,CalcAvgWeight
import pdb

class transect:
    '''
    transect(ODB,key)
    ODB (open database) is an instance of the ADO class
    key is the key-value from the headers table
'''
    def __init__(self,ODB,key,QueryFunc,SizeBound=None,MinDepth=-999,MaxDepth=999):
        #pdb.set_trace()
        self.key=key
        self.ODB=ODB
        self.MinDepth,self.MaxDepth=MinDepth,MaxDepth
        self.QueryFunc=QueryFunc
        self.SizeBound=SizeBound
        if self.SizeBound==None:self.SizeBound=[inf]
        if self.SizeBound==inf:self.SizeBound=[inf]
        if isinstance(self.SizeBound,(float,int)):self.SizeBound=[self.SizeBound,inf]
        if (len(self.SizeBound)==1) and (self.SizeBound[0]!=inf):self.SizeBound.append(inf)
        self.SizeBound.sort()
        self.MeasAbund=None
        query=self.QueryFunc.QnumDepthCount(self.key)
        try:
            ODB.execute(query)
        except:
            print('\ntransect line 30')
            print('query\n',query)
        c=self.ODB.GetVariable('CountTotal')#Number of counted animals#Quadrat Number
        q=self.ODB.GetVariable('QuadNum')#Quadrat Number
        d=self.ODB.GetVariable('Depth')#Depth
        if len(q)==0:
            self.quad=[]
            self.nquad=0
            self.IndexWithMeas=[]
            self.self.IndexWithCount=[]
            return

        try:
            AllQ=list(range(q[0],1+q[-1]))
        except:
            print('transect 36 key,type(q),q\n',key,type(q),q)
        
        self.IndexWithCount=list(map(lambda q2:q2-q[0],q))
        
        AllC=WCHinterp(q,c,AllQ)
        AllD=WCHinterp(q,d,AllQ)
        try:
            self.quad=list(map(lambda a1,a2,a3:quadrat(a1,a2,NumCount=a3,SizeBound=self.SizeBound),AllQ,AllD,AllC))
        except:
            print ('transect line 38, key,SizeBound',key,'\n',SizeBound)
            self.quad=list(map(lambda a1,a2,a3:quadrat(a1,a2,NumCount=a3,SizeBound=self.SizeBound),AllQ,AllD,AllC))
            
        self.nquad=len(self.quad)
        nInDepthRange=len(list(filter(lambda r:(r>=self.MinDepth) and (r<=self.MaxDepth),d)))
        self.FracInDepthRange=float(nInDepthRange)/float(len(d))
        self.SetIndexWithMeas()
        for Qnum in self.IndexWithMeas:
            try:
              CurQuad=self.quad[Qnum]
            except:
                pdb.set_trace()
                CurQuad=self.quad[Qnum]
            query=self.QueryFunc.MeasInQuad(self.key,CurQuad.QuadNum)
            self.ODB.execute(query)
            SizeMeas=self.ODB.GetVariable('AnimalLength')
            CurQuad.AddSizeMeas(SizeMeas)
        self.CalcAbundMeasured(None)
        self.RandomizeSizeProb(UseDeterm=True)
        

    def SetIndexWithMeas(self):
       query=self.QueryFunc.QuadWithMeas(self.key)
       if query==None:
           self.IndexWithMeas=([])
           return
       self.ODB.execute(query)
       QuadNum=self.ODB.GetVariable('QuadNum')
       try:
          self.IndexWithMeas=[]
          if len(QuadNum)>0:
             self.IndexWithMeas=list(map(lambda x: x-self.quad[0].QuadNum,QuadNum))
       except:
          print('transect 73')
          import pdb
          #pdb.set_trace()
          self.IndexWithMeas=[]
          if len(QuadNum)>0:
             self.IndexWithMeas=list(map(lambda x: x-self.quad[0].QuadNum,QuadNum))
       
    def CalcAbundMeasured(self,AE):
        '''transect.AbundMeasured(AE)
        AE(size) is the allometric equation relating animal-length to weight'''
        #pdb.set_trace()

        #A temporary list of quadrats
        TempQuad=list(map(lambda q:self.quad[q],self.IndexWithMeas))
        #pdb.set_trace()

        if len(TempQuad)==0:
            self.MeasAbund={}
            for USL in self.SizeBound:
                kname='USL'+str(USL)
                self.MeasAbund[kname]={'Pop':0,'Bmass':0.}
            return
        TempQuad=list(filter(lambda q: (q.Depth>=self.MinDepth) and (q.Depth<=self.MaxDepth)   ,TempQuad))
        if len(TempQuad)==0:
            self.MeasAbund={}
            for USL in self.SizeBound:
                kname='USL'+str(USL)
                self.MeasAbund[kname]={'Pop':0,'Bmass':0.}
            return
        #pdb.set_trace()
        ByQuad=list(map(lambda q:q.Meas.GetAbundance(AE),TempQuad))
        #pdb.set_trace()
        self.MeasAbund=SumAbundance(ByQuad)
        return

    def CalcAvgWeight(self,AE=None,ReCalcAbundMeasured=False):
        if self.IndexWithMeas==[]:
            result={}
            for USL in self.SizeBound:
                kname='USL'+str(USL)
                result[kname]=None
            return(result)  
        
        if ReCalcAbundMeasured:self.CalcAbundMeasured(AE)
        result=CalcAvgWeight(self.MeasAbund)
        return(result)            
    
    def RandomizeSizeProb(self,UseDeterm=False):
        #There is only a single size-class
        if self.SizeBound==[inf]:
            for q in self.quad:q.UnMeas.SetSizeProb([1.0])
            return
        AllQNum=list(map(lambda q:q.QuadNum,self.quad))
        if len(self.IndexWithMeas)>0:            
            qmeas=[]
            ProbMeas=[]
            for q in self.IndexWithMeas:
                CurQuad=self.quad[q]
                qmeas.append(CurQuad.QuadNum)
                ProbMeas.append(CurQuad.Meas.ResampSizeProb(UseDeterm=UseDeterm))
            try:
                 AllProb=InterpProb(qmeas,ProbMeas,AllQNum)
            except:
                print ('\ntransect 137,UseDeterm',UseDeterm)
                print ('self.key',self.key)
                print ('CurQuad.QuadNum',CurQuad.QuadNum)
                print ('qmeas\n',qmeas)
                print ('ProbMeas\n',ProbMeas)
                print ('AllQNum\n',AllQNum)
                for q in self.IndexWithMeas:
                    CurQuad=self.quad[q]
                    print('\nself.key,q,CurQuad.QuadNum,CurQuad.Meas.Nanimal',self.key,q,CurQuad.QuadNum,CurQuad.Meas.Nanimal)
                    print('CurQuad.Meas.SizeMeas',CurQuad.Meas.SizeMeas)
                    print('CurQuad.Meas.SizeFreq',CurQuad.Meas.SizeFreq)
                    print('self.QueryFunc.MeasInQuad(self.key,CurQuad.QuadNum)',self.QueryFunc.MeasInQuad(self.key,CurQuad.QuadNum))
                    
                AllProb=InterpProb(qmeas,ProbMeas,AllQNum)
        else:
            #Without any pertinent information, assume all size-classes are equally probable
            AllProb=list(map( lambda t: list(map(lambda s: 1./len(self.SizeBound)  ,self.SizeBound))   ,AllQNum))            

        for i in range(len(self.quad)):
            CurQuad=self.quad[i]
            CurQuad.UnMeas.SetSizeProb(AllProb[i])
            
        return        

    def CalcAbundUnMeasured(self,AvgWeight,UseDeterm=False):
        '''transect.CalcAbundUnMeasured(AvgWeight)'''
        TempQuad=list(filter(lambda q:  (q.UnMeas.nAnimals>0) and \
                                         (q.Depth>=self.MinDepth) and \
                                         (q.Depth<=self.MaxDepth),self.quad))
        
        #pdb.set_trace()
        if len(TempQuad)==0:
            self.UnMeasAbund={}
            for USL in self.SizeBound:
                kname='USL'+str(USL)
                self.UnMeasAbund[kname]={'Pop':0,'Bmass':0.}
            return
        try:
           ByQuad=list(map(lambda q:q.UnMeas.GetAbundance(AvgWeight=AvgWeight,UseDeterm=UseDeterm),TempQuad))
           #pdb.set_trace()
           self.UnMeasAbund=SumAbundance(ByQuad)
        except:
           print('\ntransect line 171')
           print('AvgWeight',AvgWeight)
           print('self.key',self.key)
           for q in TempQuad:
           	print (q.QuadNum)
           	print('          ',q.UnMeas.GetAbundance(AvgWeight=AvgWeight,UseDeterm=UseDeterm))
           ByQuad=list(map(lambda q:q.UnMeas.GetAbundance(AvgWeight=AvgWeight,UseDeterm=UseDeterm),TempQuad))
           print('ByQuad',ByQuad)
           dummy=1/0
       
        
    def GetAbundance(self,AE=None,AverageWeight=None,UseDeterm=False):
        #pdb.set_trace()
        self.RandomizeSizeProb(UseDeterm=UseDeterm)
        #Measured Animals
        if (AE!=None):self.CalcAbundMeasured(AE)

        #Unmeasured anaimals
        self.RandomizeSizeProb(UseDeterm=UseDeterm)
        try:
            self.CalcAbundUnMeasured(AverageWeight,UseDeterm=UseDeterm)
        except:
            print('\ntransect 193 self.key,AverageWeight,UseDeterm\n',\
            self.key,AverageWeight,UseDeterm)
            self.CalcAbundUnMeasured(AverageWeight,UseDeterm=UseDeterm)
        
        try:
            result=SumAbundance([self.UnMeasAbund,self.MeasAbund])
        except:
            print ('\ntransect 196 ',self.key)
            print('self.UnMeasAbund\n',self.UnMeasAbund)
            print('self.MeasAbund\n',self.MeasAbund)
            result=SumAbundance([self.UnMeasAbund,self.MeasAbund])
        return(result)
    
    def GetTranWidth(self):return(self.QueryFunc.TranWidth)
    def GetQuadArea(self):
        result=self.GetNumQuad()*self.QueryFunc.QuadArea
        return(result)
    def GetTranLength(self):
        result=self.GetQuadArea()/self.GetTranWidth()
        return(result)
    def GetNumQuad(self):
        TempQuad=list(filter(lambda q: (q.Depth>=self.MinDepth) and (q.Depth<=self.MaxDepth)   ,self.quad))
        result=len(TempQuad)
        return(result)
      
    def GetNumSurveyedQuadInDepthRange(self):
         TempQuad=list(map(lambda i:self.quad[i] , self.IndexWithCount ))
         TempQuad=list(filter(lambda q: (q.Depth>=self.MinDepth) and (q.Depth<=self.MaxDepth)   ,TempQuad))
         return(len(TempQuad))
  

if __name__ == "__main__":
    databasepath='D:\StrippedBioDataBases\RedUrchin_Bio.mdb'
    ODB=OpenDB(databasepath)
    AvgWeight=[10,20]
    import sys
    sys.path.append('D:\Coding\AnalysisPrograms2013\Fossil\working\RSU')
    import RSUQueryFunc
    key=13089
    tran1=transect(ODB,key,RSUQueryFunc,SizeBound=[89])
    tran1.CalcAbundUnMeasured(AvgWeight,UseDeterm=False)
    print('done transect')

