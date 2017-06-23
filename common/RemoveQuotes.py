from numpy import array,ndarray
def RemoveQuotes(xstr,qchar=["'", '"'],ReplaceString=' '):
    
    #xstr is an array
    if isinstance(xstr,(list,ndarray)):
        result=list(map(lambda t:RemoveQuotes(t,qchar=qchar,ReplaceString=ReplaceString)  ,xstr))
        return(result)
    
    #Make sure we are dealing with character strings
    ystr=str(xstr)
    
    #A single charater to get rid of
    if isinstance(qchar,str):
        return(ystr.replace(qchar,ReplaceString))    
    for qc in qchar:
        ystr=ystr.replace(qc,ReplaceString)
    return(ystr)

if __name__ == "__main__":    
    
    xstr='abcd'+"'"+'efgh'+ '"'+'ijk'
    ystr='lmno'+"'"+'pqrs'+ '"'+'tuv'
    qchar=["'", '"']
    ReplaceString=' '
    
    print(xstr)
    print(RemoveQuotes(xstr,qchar=qchar,ReplaceString=ReplaceString))

    print(RemoveQuotes([xstr,2,None,ystr,['aa',2]],qchar=qchar         ,ReplaceString=ReplaceString))
    print(RemoveQuotes([xstr,2,None,ystr,['aa',2]],qchar=qchar+['None'],ReplaceString=ReplaceString))
    