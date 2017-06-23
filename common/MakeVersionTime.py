'''Generate a python-script named VersionTime.py
VersionTime.py contains a single function called VersionTime.
The output of VersionTime is simply the time at which this library was executed.

This library will probably be executed as part of the process that creates an
executeable (setup.bat).  The result of VersionTime will be the time at which
the executeable was created.'''


from datetime import datetime

CurTime=datetime.now()
nowyear=CurTime.year    
nowmonth=CurTime.month    
nowday=CurTime.day    
nowhour=CurTime.hour    
nowminute=CurTime.minute
nowsecond=CurTime.second
nowmicrosecond=CurTime.microsecond

txtfunc ='\nfrom datetime import datetime '
txtfunc+='\ndef VersionTime(): '
txtfunc+='\n  result=datetime( '
txtfunc+='  '+str(nowyear) +' , '
txtfunc+='  '+str(nowmonth) +' , '
txtfunc+='  '+str(nowday) +' , '
txtfunc+='  '+str(nowhour) +' , '
txtfunc+='  '+str(nowminute) +' , '
txtfunc+='  '+str(nowsecond) +' , '
txtfunc+='  '+str(nowmicrosecond) +' )\n '

txtfunc+='\n  return(result)'


outfile=open('VersionTime.py','w')
outfile.write(txtfunc)
outfile.close()




    
    
    