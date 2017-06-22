from numpy import ndarray
#import pdb

def SumAbundance(a):
    '''SumAbundance(a)
    a is a list of abundance structures
      each row in a corresponds to a size class
      first column corresponds to the number of animals
      second column is the corresponding biomass.
         if the biomass is undefined then the second column has None-values

    Assuming that each element in a is compatible'''
    if all(map(lambda y:y==None,a)):return(None)
    a=list(filter(lambda b:b!=None,a))
    if isinstance(a[0],dict):
        dk=a[0].keys()
        result={}
        for t in dk:
            suba=list(map(lambda a:a[t],a))
            result[t]=SumAbundance(suba)
        return(result)
    if isinstance(a[0],(list,ndarray)):
        result=[]
        for t in range(len(a[0])):
            try:
                suba=list(map(lambda b:b[t],a))
            except:
                print('\nSumAbundance 26,len(a[0]),a,t\n',len(a[0]),a,t)
                print(list(map(lambda b:len(b),a)))
                suba=list(map(lambda b:b[t],a))                
            try:
                result+=[SumAbundance(suba)]
            except:
                print ('SumAbundance 31,suba\n',suba)
        return(result)
    #a must be a list of single values
    if any(map(lambda y:y==None,a)):return(None)
    return(sum(a))
            
   

def CalcAvgWeight(a):
    '''CalcAvgWeight(a)
    a is sum structure built upon two-value (pop and bmass) lists
    Navigate the structure until the simple lists result'''
    #pdb.set_trace()
    if isinstance(a,dict):
        if sorted(list(a.keys()))==sorted(['Pop', 'Bmass']):
            if a['Pop']==0:return(0.) #It's precautionary     
            try:
                result=a['Bmass']/float(a['Pop'])
            except:
                result=None
            return(result)
            
        try:
            result={}
            for t in list(a.keys()):
                result[t]=CalcAvgWeight(a[t])
            return(result)
        except:
            print('\nSumAbundance 52 a\n')
            print('a\n',a)
            return(None)

    if isinstance(a,(list,ndarray)):
        result=map(lambda x: CalcAvgWeight(x) ,a)
        return(result)
    #Shouldn't get to this point in the routine
    print('SumAbundance 65,a\n',a)
    return(None)
           
        
    
def CalcDensity(a,size):
    '''CalcDensity(a,size)
    a is an abundance structure
    size is the size of sample - likely square-metres of shoreline'''

    if isinstance(size,(list,ndarray)):
        result=list(map(lambda suba,subsize:CalcDensity(suba,subsize),a,size))
        return(result)

    if a==None: return(None)
    if size==None: return(None)
    if size==0: return(None)


    if isinstance(a,dict):
        dk=a.keys()
        result={}
        for t in dk:
            result[t]=CalcDensity(a[t],size)
        return(result)
    if isinstance(a,(list,ndarray)):
        result=list(map(lambda suba:CalcDensity(suba,size),a))
        return(result)
    #a must be a single values
    try:
        result=float(a)/float(size)
    except:
        print ('SumAbundance 105, a,size\n',a,size)
        result=float(a)/float(size)
    return(result)
            
if __name__ == "__main__":
    b=[[1,None],[2,2],[3,3]]
    c=[[5,5],[5,5],[4,4]]
    d=[[5,5],[5,5],[4,4]]
    a=[b,c,d]
    SA=SumAbundance(a)
    print ('\n',SA)

    dens=CalcDensity(SA,2.)
    print ('\n',dens)
    

    
