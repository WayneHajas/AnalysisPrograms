'''Index of Field-types used in python/adodb

When I deconstruct a table, field-types are given as numbers.
When I build a table, field-types are given as text.
This library does the conversion.'''

from numpy import ndarray

numericCode=[  202, 130, 203, 203,  17,\
                 2,   3,   4,   5,  72,\
               131,   7,   6,   3,  11,\
               205, 203,  204]
textCode=   ['varchar','','','','BYTE',\
             'INT','Long','SINGLE','DOUBLE','',\
             '','TIME','','','',\
             '','','']
             
def GetTextCode(nc):
    if isinstance(nc,(list,ndarray)):
        result=list(map(lambda t:GetTextCode(t)  ,nc))
        return(result)
    try:
        i=numericCode.index(nc)
        result=textCode[i]
        return(result)
    except:
        return(None)
if __name__ == "__main__":
    nc=3
    print(GetTextCode(nc))
    print(GetTextCode([17,4,7]))
    