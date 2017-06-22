from numpy.random import uniform,seed
from numpy import interp




def InterpProb(oldx, oldprob,newx):
    '''InterpProb(oldx, oldprob,newx)
    oldx is a list of values where the class probabilities are known
    oldprob is a list of lists.  for each element of old x, there is a list of class-probabilities

    It is assumed the old probabilities have been normalized.
    It is assumed there is some consistent order in the order of the classes
    It is assumed the old data has been sorted with respect to x-values'''
    if (oldx==[]):return(list(map(lambda t:1.0,newx)))
    nold=len(oldx)
    nnew=len(newx)

    #Get rid of any None's in the old-values
    GoodInt=list(filter(lambda i: (oldx[i]!=None) and (oldprob[i]!=None),range(nold)))
    oldx2=list(map(lambda j:oldx[j],GoodInt))
    oldprob2=list(map(lambda j:oldprob[j],GoodInt))
    nold=len(oldprob2)

    if nold==1:
        result=list(map(lambda t:oldprob[0],range(nnew)))
        return(result)
    nclass=len(oldprob2[0])

    #rotate the old probabilities
    trOldProb=list(map(lambda t: list(map(lambda s:s[t],oldprob2  ))      ,range(nclass)))

    #Apply interpolation to probability of each class
    trNewProb=list(map(lambda t: interp(newx,oldx2,trOldProb[t])     ,range(nclass)))

    #Do the transformation back to by-x data
    NewProb=list(map(lambda q:list(map(lambda c:c[q]   ,trNewProb))       ,range(nnew)))

    for q in range(nnew):
        if newx[q]<oldx2[0 ]:NewProb[q]=oldprob2[0 ]
        if newx[q]>oldx2[-1]:NewProb[q]=oldprob2[-1]
               
    return(NewProb)

def WCHinterp(oldx,oldy,newx):
    result=interp(newx,oldx,oldy)
    return (result)


if __name__ == "__main__":
    from numpy.random import uniform,seed
    nold=3
    oldx=list(range(4,8))
    nold=len(oldx)
    nclass=5

    def MakeProb(n):
        y=uniform(size=n)
        sumy=sum(y)
        result=list(map(lambda x:x/sumy,y))
        return (result)

    oldy=list(map(lambda x:MakeProb(nclass),oldx))

    newx=list(map(lambda i: 3.5+i*.5  ,range(10)))
    newy=InterpProb(oldx, oldy,newx)
    
    print ('\n')
    for i in range(len(newx)):print (newx[i],newy[i],sum(newy[i]))
    print ('\n')
    for i in range(len(oldx)):print (oldx[i],oldy[i],sum(oldy[i]))

    oldx=list(range(3,7))
    oldy=list(range(4,8))
    newx=list(range(0,10))

    for t in WCHinterp(oldx,oldy,newx):print (t)
              
              
