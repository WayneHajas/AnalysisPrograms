'''Formerly called RemoveQuotes.
This routine converts a value to a character-string that can be used as part of an insert-query
to put the value into a .mdb file.

For character strings:Any single quotes (apostrophes) must be changed to two single quotes.  
                        Double quotes must also be converted to two double quotes.
                        
Time and date values have formatting issues.  A time-value has an implicit date that is generally doesen't appear
in ACCESS by a trick of formatting. These implicit dates seem to be between 1899 and 1903.  If the date is 
before 1950, I will try to coerce the value to appear as date-only.

20150529 'nan gets conveted to 'NULL'

'''

from numpy import array,ndarray

import datetime
import copy

def PrepForMDB(xstr):
    
    #xstr is an array
    if isinstance(xstr,(list,ndarray)):
        result=list(map(lambda t:PrepForMDB(t)  ,xstr))
        return(result)
        
    #xstr is a dictionary
    if isinstance(xstr,dict):
        result=copy.deepcopy(xstr)
        for t in list(xstr.keys()):
            result[t]=PrepForMDB(xstr[t])
        return(result)
    
    if xstr==None:
        return("NULL")
    
    #xstr is a date or time
    if isinstance(xstr,datetime.datetime ):
        result='#'  #Access needs this to indicate a time-value
        if isinstance(xstr,datetime.date):        
          if xstr.year>1950:
            result+=str(xstr.year)+'-'+str(xstr.month)+'-'+str(xstr.day)+' '
        
        result+=str(xstr.hour)+':'+str(xstr.minute)+':'+str(xstr.second)
        result+='#'  #So accesss knows this is time-value
        return(result)

    #xstr is a boolean    
    if isinstance(xstr,bool):
        if (xstr):
            return('-1')#true in access
        return('0')#false in access
    
    #Make sure we are dealing with character strings
    ystr=str(xstr)
    
    #Undefined values can end up as 'nan' and still remain numeric
    if ystr=='nan':
        return("NULL")
        
    
    ystr=ystr.replace('"','""')#A pair of double-quotes will appear as single double-quote in the .mdb file
    ystr=ystr.replace("'","''")#A pair of single-quotes will appear as single single-quote in the .mdb file
    ystr="'"+ystr+"'"
    return(ystr)
    
   

if __name__ == "__main__":    
    
        
    import datetime
    
    xstr=['abcd'+"'"+'efgh'+ '"'+'ijk',datetime.date(2015,4,27),datetime.time(13,22,35)]
   
    
    print(xstr)
    print(PrepForMDB(xstr))
    
    ystr={'a':'abcd'+"'"+'efgh'+ '"'+'ijk', 'b':datetime.date(2015,4,27), 'c':datetime.time(13,22,35),'nan':'nan'}
    print(ystr)
    print(PrepForMDB(ystr))
    

    