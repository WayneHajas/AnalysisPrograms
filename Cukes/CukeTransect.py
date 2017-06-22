from copy import deepcopy
from datetime import datetime
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from transect import transect

class CukeTransect(transect):
    def __init__(self,ODB,key,QueryFunc,SizeBound=None,MinDepth=-999,MaxDepth=999):
        super().__init__(ODB,key,QueryFunc,SizeBound=SizeBound,MinDepth=MinDepth,MaxDepth=MaxDepth) 
        self.GetAuxData()

    def GetAuxData(self):
        query ="SELECT Headers.Transect, "
        query+="DateSerial( Headers.Year,Headers.Month,Headers.Day) as SurveyDate,"
        query+="Headers.TimeStart, Headers.Comments "
        query+="FROM Headers "
        query+="WHERE (((Headers.Key)="
        query+=str(self.key)
        query+="));"

        try:
            ODB.execute(query)
        except:
            print('\ntransect line 21')
            print('query\n',query)

        self.AuxData={}
        self.AuxData['TransectNumber']=self.ODB.GetVariable('Transect')[0]
        self.AuxData['SurveyDate']=self.ODB.GetVariable('SurveyDate')[0]
        self.AuxData['Comments']=self.ODB.GetVariable('Comments')[0]

        #construct a practical representation of the time of the survey
        DateSurvey=self.ODB.GetVariable('SurveyDate')[0]
        TimeSurvey=self.ODB.GetVariable('TimeStart')[0]
        self.AuxData['time']=\
                    datetime(DateSurvey.year,DateSurvey.month,DateSurvey.day,\
                             TimeSurvey.hour,TimeSurvey.minute)
        self.AuxData['OmitTransect']=None
        self.AuxData['OmitTransectReason']=''

    def SetOmit(self, OmitTransect=None,OmitTransectReason=''):
        self.AuxData['OmitTransect']=OmitTransect
        self.AuxData['OmitTransectReason']=OmitTransectReason

    def GetDepth(self):
        QuadInDepth=list(filter(lambda q: (q.Depth >=self.MinDepth)&(q.Depth <=self.MaxDepth),self.quad))
        print('\nGetDepth ', self.MinDepth, self.MaxDepth)
        for q in QuadInDepth:
            print (q.QuadNum,q.Depth,q.NumCount)

        Depth=list(map(lambda q:q.Depth,QuadInDepth))
        return(Depth)

    def GetMinDepth(self):
        Depth=self.GetDepth()
        return(min(Depth))

    def GetMaxDepth(self):
        Depth=self.GetDepth()
        return(max(Depth))
                       
        

    def MakeTransectRec(self,TranCharKey=None,AvgWeight=None,OmitTransect=None,OmitTransectReason=''):
        '''Collect all the data to go into a record of Results_Transect
         in the output.'''
        result=deepcopy(self.AuxData)
        result['TranCharKey']=TranCharKey
        result['HeaderKey']=self.key
        result['MinDepth']=self.GetMinDepth()
        result['MaxDepth']=self.GetMaxDepth()

        QuadInDepth=list(filter(lambda q: (q.Depth >=self.MinDepth)&(q.Depth <=self.MaxDepth),self.quad))
        QuadLen= float(self.QueryFunc.QuadArea/self.QueryFunc.TranWidth)
        result['TranLength']=float(len(QuadInDepth))*QuadLen
        result['NumQuadrats']=len(QuadInDepth)

        result['NumAnimals']=self.GetAbundance(UseDeterm=True)['USLinf']['Pop']
        result['Density']=float(result['NumAnimals'])/float(self.QueryFunc.TranWidth)
        result['Biomass']=None
        if AvgWeight!=None: result['Biomass']=float(result['NumAnimals'])*AvgWeight
        result['OmitTransect']=OmitTransect
        result['OmitTransectReason']=OmitTransectReason
        return(result)

                                   
        
        
 
if __name__ == "__main__":
       
    databasepath='H:\scratch\SeaCuke_Bio_97_NoLink.mdb'
    from ADO import adoBaseClass as OpenDB

    ODB=OpenDB(databasepath)
    import sys
    sys.path.append('D:\Coding\AnalysisPrograms2013\PyFunctions\Cukes')
    import californicusQueryFunc as QueryFunc
    
    key=11076
    tran1=CukeTransect(ODB,key,QueryFunc,SizeBound=None,MinDepth=.5,MaxDepth=6)
    print('\nAllQuad')
    for q in tran1.quad:
        print (q.QuadNum,q.Depth,q.NumCount)
    
    print(     tran1.MakeTransectRec())  
