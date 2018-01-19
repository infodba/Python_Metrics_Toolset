# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 10:31:08 2016

@author: DAKHMETO
TC 11 syslog parser to investigate 2T Login perfomance problem
"""
import glob
import re
import xlsxwriter
import datetime
from pytz import timezone
import pytz

#RFOLDER_PATH = "c:\\_WORK\\PBI\\July2017\\FNA_2T\\"
#RFOLDER_PATH = "c:\\_WORK\\2018_Metrics\\Houston_We_Have_A_Problem\\2T_Login_FNA_22Dec_Upward_Shift\\Dec_2017\\"
RFOLDER_PATH = "c:\\_WORK\\2018_Metrics\\Houston_We_Have_A_Problem\\2T_Login_FNA_22Dec_Upward_Shift\\Jan_09\\10AM\\temp\\4parser\\"
WFILE_PATH = RFOLDER_PATH

#RFOLDER_PATH = "c:\\_WORK\\PBI\\2T_Login_low_perf\\syslogs\\Login0216\\"
#WFILE_PATH = "c:\\_WORK\\PBI\\2T_Login_low_perf\\syslogs\\Login0216\\"

#RFOLDER_PATH = "c:\\_WORK\\PBI\\2T_Login_low_perf\\FCO\\FCO_Syslogs\\"
#WFILE_PATH = "c:\\_WORK\\PBI\\2T_Login_low_perf\\FCO\\FCO_Syslogs\\"



THRESHOLD_DBCON = datetime.timedelta(seconds=3)
THRESHOLD_SCHLD1 = datetime.timedelta(seconds=3)
THRESHOLD_TRNSV = datetime.timedelta(seconds=5)
THRESHOLD_TCHTH = datetime.timedelta(seconds=7)
THRESHOLD_LIBTCCORE = datetime.timedelta(seconds=10)
THRESHOLD_SCHLD2 = datetime.timedelta(seconds=10)
THRESHOLD_CCAS = datetime.timedelta(seconds=5)
THRESHOLD_CHKLIC = datetime.timedelta(seconds=8)
THRESHOLD_LIBSUB = datetime.timedelta(seconds=10)
THRESHOLD_STRT = datetime.timedelta(seconds=10)
THRESHOLD_IMANV = datetime.timedelta(seconds=10)

def time2ets (UTCeventdatetime):
    UTCeventdatetime=(pytz.utc).localize(UTCeventdatetime)
    print ("  func: in UTC= ",end="")
    print(UTCeventdatetime)
    #FNA US/Eastern
    ETSeventdatetime=UTCeventdatetime.astimezone(timezone('US/Eastern'))
    #FSA America/Bahia
    #ETSeventdatetime=UTCeventdatetime.astimezone(timezone('America/Bahia'))
    #FCO China/Beijing
    #ETSeventdatetime=UTCeventdatetime.astimezone(timezone('Asia/Shanghai'))
    #FOE Europe/Budapest
    #ETSeventdatetime=UTCeventdatetime.astimezone(timezone('Europe/Budapest'))
    #IND Asia/Calcutta
    #ETSeventdatetime=UTCeventdatetime.astimezone(timezone('Asia/Calcutta'))
    print ("  func: in ETS= ",end="")
    print(ETSeventdatetime)
    format="%Y-%m-%d %H:%M:%S"
    #change format after tz conversion
    strETSeventdatetime=ETSeventdatetime.strftime(format)
    #convert again to datetime object
    ETSeventdatetime=datetime.datetime.strptime(strETSeventdatetime, format)
    return ETSeventdatetime

def duration (datetimeafter, datetimebefore):
    datetimeafter=datetimeafter.replace(microsecond=0)
    datetimebefore=datetimebefore.replace(microsecond=0)
    duration = datetimeafter - datetimebefore
    print ("  func: duration= ",end="")
    print(duration)
    #strduration=str(duration)
    return duration

def check_duration(duration, treshhold):
    alarm=False
    if duration > treshhold:
        alarm=True
        print ("Long duration detected!!!")
    return alarm
    
print("START")
#print (os.listdir(RFOLDER_PATH))
print (RFOLDER_PATH + "*.syslog")
file_list = glob.glob(RFOLDER_PATH + "*.syslog")
file_list.reverse()
print (file_list)


# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook(WFILE_PATH + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(":","_") + '_results.xlsx')
worksheet = workbook.add_worksheet()
# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True, 'bg_color': 'silver'})
red = workbook.add_format({'bold': True, 'font_color': 'red', 'bg_color': 'yellow'})
link_format = workbook.add_format({'color': 'blue', 'underline': 1})

# Widen the column to make the text clearer.
worksheet.set_column('A:A', len('Syslog Creation Date  ')) 
# Write captions text.
worksheet.write('A1', 'Syslog Creation Date', bold)

# Widen the column to make the text clearer.
worksheet.set_column('B:B', len('Connection to DB   '))
# Write captions text.
worksheet.write('B1', 'Connection to DB', bold)

# Widen the column to make the text clearer.
worksheet.set_column('C:C', len('Con2DBduration '))
# Write captions text.
worksheet.write('C1', 'Con2DBduration', bold)

# Widen the column to make the text clearer.
worksheet.set_column('D:D', len('SchemaLoaded1     '))
# Write captions text.
worksheet.write('D1', 'SchemaLoaded1', bold)

# Widen the column to make the text clearer.
worksheet.set_column('E:E', len('SchLd1duration'))
# Write captions text.
worksheet.write('E1', 'SchLd1duration', bold)

# Widen the column to make the text clearer.
worksheet.set_column('F:F', len('Transient Volume     '))
# Write captions text.
worksheet.write('F1', 'Transient Volume', bold)

# Widen the column to make the text clearer.
worksheet.set_column('G:G', len('TrnsVolduration'))
# Write captions text.
worksheet.write('G1', 'TrnsVolduration', bold)

# Widen the column to make the text clearer.
worksheet.set_column('H:H', len('00001 - Service Request:'))
# Write captions text.
worksheet.write('H1', '00001 - Service Request:', bold)

# Widen the column to make the text clearer.
worksheet.set_column('I:I', len('DurBWNTrnsV&1stRequest'))
# Write captions text.
worksheet.write('I1', 'DurBWNTrnsV&1stRequest', bold)

# Widen the column to make the text clearer.
worksheet.set_column('J:J', len('libtcsoacore.dll     '))
# Write captions text.
worksheet.write('J1', 'libSessionVersion_register_callbacks', bold)

# Widen the column to make the text clearer.
worksheet.set_column('K:K', len('DurBWN1stRequest&libSessionVersion_register_callbacks'))
# Write captions text.
worksheet.write('K1', 'DurBWN1stRequest&libSessionVersion_register_callbacks', bold)

# Widen the column to make the text clearer.
worksheet.set_column('L:L', len('POM_login     '))
# Write captions text.
worksheet.write('L1', 'POM_login', bold)

# Widen the column to make the text clearer.
worksheet.set_column('M:M', len('CCAS=POM_login - libSessionVersion_register_callbacks'))
# Write captions text.
worksheet.write('M1', 'CCAS=POM_login-libSessionVersion_register_callbacks', bold)

# Widen the column to make the text clearer.
worksheet.set_column('N:N', len('check_license    '))
# Write captions text.
worksheet.write('N1', 'check_license', bold)

# Widen the column to make the text clearer.
worksheet.set_column('O:O', len('check_license-POM_login'))
# Write captions text.
worksheet.write('O1', 'check_license-POM_login', bold)

# Widen the column to make the text clearer.
worksheet.set_column('P:P', len('MultiFieldKeyAttrsMap    '))
# Write captions text.
worksheet.write('P1', 'MultiFieldKeyAttrsMap', bold)

# Widen the column to make the text clearer.
worksheet.set_column('Q:Q', len('b/n chklic and MultiFieldKeyAttrsMap'))
# Write captions text.
worksheet.write('Q1', 'b/n chklic and MultiFieldKeyAttrsMap', bold)

# Widen the column to make the text clearer.
worksheet.set_column('R:R', len('LOV-Master     '))
# Write captions text.
worksheet.write('R1', 'LOV-Master', bold)

# Widen the column to make the text clearer.
worksheet.set_column('S:S', len('DurBWNLOV-Master&MFK'))
#Write captions text.
worksheet.write('S1', 'DurBWNLOV-Master&MFK', bold)

# Widen the column to make the text clearer.
worksheet.set_column('T:T', len('Started.    '))
# Write captions text.
worksheet.write('T1', 'Started.', bold)

# Widen the column to make the text clearer.
worksheet.set_column('U:U', len('b/n LOV-Master and Started.'))
# Write captions text.
# Library is delay loaded
worksheet.write('U1', 'b/n LOV-Master andt Started.', bold)

# Widen the column to make the text clearer.
worksheet.set_column('V:V', len('ImanVolumeImpl::    '))
# Write captions text.
worksheet.write('V1', 'ImanVolumeImpl::', bold)

# Widen the column to make the text clearer.
worksheet.set_column('W:W', len('b/n Started. and ImanVolumeImpl'))
# Write captions text.
# Library is delay loaded
worksheet.write('W1', 'b/n Started. and ImanVolumeImpl', bold)

# Widen the column to make the text clearer.
worksheet.set_column('X:X', len('library libeint    '))
# Write captions text.
worksheet.write('X1', 'library libeint', bold)

# Widen the column to make the text clearer.
worksheet.set_column('Y:Y', len('Duration b/n ImanVolumeImpl and library_libeint'))
# Write captions text.
# Library is delay loaded
worksheet.write('Y1', 'Duration b/n ImanVolumeImpl and library_libeint', bold)

# Widen the column to make the text clearer.
worksheet.set_column('Z:Z', len('EndOfSession    '))
# Write captions text.
worksheet.write('Z1', 'EndOfSession', bold)

# Widen the column to make the text clearer.
worksheet.set_column('AA:AA', len('Duration b/n syslogcreation and endofsession'))
# Write captions text.
# Library is delay loaded
worksheet.write('AA1', 'Duration b/n syslogcreation and endofsession', bold)



worksheetnew = workbook.add_worksheet()
# Create a new Chart object.
chart = workbook.add_chart({'type': 'column'})


re1='.*?'	# Non-greedy match on filler
re2='((?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Tues|Thur|Thurs|Sun|Mon|Tue|Wed|Thu|Fri|Sat))'	# Day Of Week 1
re3='(\\s+)'	# White Space 1
re4='((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Sept|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?))'	# Month 1
re5='(\\s+)'	# White Space 2
re6='((?:(?:[0-2]?\\d{1})|(?:[3][01]{1})))(?![\\d])'	# Day 1
re7='(\\s+)'	# White Space 3
re8='((?:(?:[0-1][0-9])|(?:[2][0-3])|(?:[0-9])):(?:[0-5][0-9])(?::[0-5][0-9])?(?:\\s?(?:am|AM|pm|PM))?)'	# HourMinuteSec 1
re9='(\\s+)'	# White Space 4
re10='((?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3})))(?![\\d])'	# Year 1
rg0 = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9+re10,re.IGNORECASE|re.DOTALL)

rre1='.*?'	# Non-greedy match on filler
rre2='((?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3}))[-:\\/.](?:[0]?[1-9]|[1][012])[-:\\/.](?:(?:[0-2]?\\d{1})|(?:[3][01]{1})))(?![\\d])'	# YYYYMMDD 1
rre3='(.)'	# Any Single Character 1
rre4='((?:(?:[0-1][0-9])|(?:[2][0-3])|(?:[0-9])):(?:[0-5][0-9])(?::[0-5][0-9])?(?:\\s?(?:am|AM|pm|PM))?)'	# HourMinuteSec 1
rg = re.compile(rre1+rre2+rre3+rre4,re.IGNORECASE|re.DOTALL)

file_counter = 0

gap = 1
for file in file_list:
    file_counter +=1
    line_counter = 0
    gap +=14
    found_flag = 0
    print (str(file_counter) +" "+ file)
    chartdata = []
    with open (file, "r") as syslog:
        for line in syslog:
            line_counter +=1
            if (re.search('system log created', line)):
               m = rg0.search(line)
               if m:
                    dayofweek1=m.group(1)
                    ws1=m.group(2)
                    month1=m.group(3)
                    ws2=m.group(4)
                    day1=m.group(5)
                    ws3=m.group(6)
                    time1=m.group(7)
                    ws4=m.group(8)
                    year1=m.group(9)
                    content = dayofweek1+ws1+month1+ws2+day1+ws3+time1+ws4+year1
                    print (content)
                    format='%a %b %d %H:%M:%S %Y'
                    syscrdatetime=datetime.datetime.strptime(content, format)
                    print(syscrdatetime)
                    #change dateformat
                    format="%Y-%m-%d %H:%M:%S"
                    #syscrdatetime=syscrdatetime.strftime(format)
                    #syscrdatetime = time.strptime(content, '%a %b %d %H:%M:%S %Y')
                    syscrtime = syscrdatetime.time()
                    print ("ETS syslog creation: ",end="")
                    print(syscrdatetime)
                    #print (syscrtime)             
                    # Text with formatting.
                    cell = 'A'+ str(file_counter + 1)
                    #worksheet.write(cell, content+"  "+ file)                          
                    content = content+"  "+ file
                    worksheet.write_url(cell, file, link_format, content)
                    print(cell + " COMPLETED")                    
            if (re.search('Database Installation Identifier:', line)):
                m = rg.search(line)
                if m:
                    yyyymmdd1=m.group(1)
                    c1=m.group(2)
                    time1=m.group(3)
                    print(yyyymmdd1)
                    print(yyyymmdd1[0:4])
                    print(yyyymmdd1[5:7])
                    print(yyyymmdd1[8:10])
                    print(time1)
                    #content=yyyymmdd1[5:10]+"/"+yyyymmdd1[0:4]
                    content=yyyymmdd1[0:4]+"-"+yyyymmdd1[5:7]+"-"+yyyymmdd1[8:10]+" "+time1                 
                    format="%Y-%m-%d %H:%M:%S"
                    content=content.strip()
                    print('-=DEBUG=-')
                    print(content)
                    # UTC time from syslog
                    dbcondatetime=datetime.datetime.strptime(content, format)
                    print ("UTC db connect: ",end="")
                    print(dbcondatetime)
                    # Convert to ETS timezone based on syslog creation
                    dbcondatetime=time2ets(dbcondatetime)
                    print (dbcondatetime)
                    content=dbcondatetime.strftime(format)+"   line#: " + str(line_counter)
                    print(content)
                    # Text with formatting.
                    cell = 'B'+ str(file_counter + 1)
                    worksheet.write(cell, content)
                    content=str(duration(dbcondatetime,syscrdatetime))
                    # Text with formatting.
                    cell = 'C'+ str(file_counter + 1)
                    if check_duration(duration(dbcondatetime,syscrdatetime),THRESHOLD_DBCON):
                        worksheet.write(cell, content, red)
                    else: worksheet.write(cell, content)
                    chartdata.append(content)                          
                    print(cell + " COMPLETED")
            if (re.search('NoId - Schema Loaded.', line)):
                m = rg.search(line)
                if m:
                    yyyymmdd1=m.group(1)
                    c1=m.group(2)
                    time1=m.group(3)
                    #content=yyyymmdd1[5:10]+"/"+yyyymmdd1[0:4]
                    content=yyyymmdd1[0:4]+"-"+yyyymmdd1[5:7]+"-"+yyyymmdd1[8:10]+" "+time1                 
                    format="%Y-%m-%d %H:%M:%S"
                    content=content.strip()
                    print(content)
                    # UTC time from syslog
                    schl1datetime=datetime.datetime.strptime(content, format)
                    print ("UTC schema loaded1: ",end="")
                    print(schl1datetime)
                    # Convert to ETS timezone based on syslog creation
                    schl1datetime=time2ets(schl1datetime)
                    print (schl1datetime)
                    content=schl1datetime.strftime(format)+"   line#: " + str(line_counter)
                    print(content)
                    # Text with formatting.
                    cell = 'D'+ str(file_counter + 1)
                    worksheet.write(cell, content)
                    try:
                        content=str(duration(schl1datetime, dbcondatetime))
                        # Text with formatting.
                        cell = 'E'+ str(file_counter + 1)
                        if check_duration(duration(schl1datetime, dbcondatetime),THRESHOLD_SCHLD1):
                            worksheet.write(cell, content, red)
                        else: worksheet.write(cell, content)
                        chartdata.append(content)
                        print(cell + " COMPLETED")
                    except Exception:
                        pass
            if (re.search('The Transient Volume Root Directory at', line)):
                m = rg.search(line)
                if m:
                    yyyymmdd1=m.group(1)
                    c1=m.group(2)
                    time1=m.group(3)
                    #content=yyyymmdd1[5:10]+"/"+yyyymmdd1[0:4]
                    content=yyyymmdd1[0:4]+"-"+yyyymmdd1[5:7]+"-"+yyyymmdd1[8:10]+" "+time1                 
                    format="%Y-%m-%d %H:%M:%S"
                    content=content.strip()
                    print(content)
                    # UTC time from syslog
                    trnsvoldatetime=datetime.datetime.strptime(content, format)
                    print ("UTC Transient Vol: ",end="")
                    print(trnsvoldatetime)
                    # Convert to ETS timezone based on syslog creation
                    trnsvoldatetime=time2ets(trnsvoldatetime)
                    print (trnsvoldatetime)
                    content=trnsvoldatetime.strftime(format) +"   line#: " + str(line_counter)
                    print(content)
                    # Text with formatting.
                    cell = 'F'+ str(file_counter + 1)
                    worksheet.write(cell, content)
                    content=str(duration(trnsvoldatetime,schl1datetime))
                    # Text with formatting.
                    cell = 'G'+ str(file_counter + 1)
                    if check_duration(duration(trnsvoldatetime,schl1datetime),THRESHOLD_TRNSV):
                        worksheet.write(cell, content, red)
                    else: worksheet.write(cell, content)                      
                    print(cell + " COMPLETED")
            if (re.search('00001 - Service Request:', line)): # 00001 - Service Request:  Core-2011-06-Session:login
                m = rg.search(line)
                if m:
                    yyyymmdd1=m.group(1)
                    c1=m.group(2)
                    time1=m.group(3)
                    #content=yyyymmdd1[5:10]+"/"+yyyymmdd1[0:4]
                    content=yyyymmdd1[0:4]+"-"+yyyymmdd1[5:7]+"-"+yyyymmdd1[8:10]+" "+time1                 
                    format="%Y-%m-%d %H:%M:%S"
                    content=content.strip()
                    print(content)
                    # UTC time from syslog
                    hthmondatetime=datetime.datetime.strptime(content, format)
                    print ("UTC 00001 - Service Request: ",end="")
                    print(hthmondatetime)
                    # Convert to ETS timezone based on syslog creation
                    hthmondatetime=time2ets(hthmondatetime)
                    print (hthmondatetime)
                    content=hthmondatetime.strftime(format) +"   line#: " + str(line_counter)
                    print(content)
                    # Text with formatting.
                    cell = 'H'+ str(file_counter + 1)
                    worksheet.write(cell, content)
                    content=str(duration(hthmondatetime,trnsvoldatetime))
                    # Text with formatting.
                    cell = 'I'+ str(file_counter + 1)
                    if check_duration(duration(hthmondatetime,trnsvoldatetime),THRESHOLD_TCHTH):
                        worksheet.write(cell, content, red)
                    else: worksheet.write(cell, content)                          
                    print(cell + " COMPLETED")                    
            if (re.search('libSessionVersion_register_callbacks', line)): #to estimate CCAS time
                m = rg.search(line)
                if m:
                    yyyymmdd1=m.group(1)
                    c1=m.group(2)
                    time1=m.group(3)
                    #content=yyyymmdd1[5:10]+"/"+yyyymmdd1[0:4]
                    content=yyyymmdd1[0:4]+"-"+yyyymmdd1[5:7]+"-"+yyyymmdd1[8:10]+" "+time1                 
                    format="%Y-%m-%d %H:%M:%S"
                    content=content.strip()
                    print(content)
                    # UTC time from syslog
                    libtcsoacoredatetime=datetime.datetime.strptime(content, format)
                    print ("UTC error about libSessionVersion_register_callbacks: ",end="")
                    print(libtcsoacoredatetime)
                    # Convert to ETS timezone based on syslog creation
                    libtcsoacoredatetime=time2ets(libtcsoacoredatetime)
                    print (libtcsoacoredatetime)
                    content=libtcsoacoredatetime.strftime(format) + "   line#: " + str(line_counter)
                    print(content)
                    # Text with formatting.
                    cell = 'J'+ str(file_counter + 1)
                    worksheet.write(cell, content)
                    try:
                        content=str(duration(libtcsoacoredatetime,hthmondatetime))
                        # Text with formatting.
                        cell = 'K'+ str(file_counter + 1)
                        if check_duration(duration(libtcsoacoredatetime,hthmondatetime),THRESHOLD_LIBTCCORE):
                            worksheet.write(cell, content, red)
                        else: worksheet.write(cell, content)                           
                        print(cell + " COMPLETED")
                    except Exception:
                        pass                  
            if (re.search('POM_login:', line)):
                m = rg.search(line)
                if m:
                    yyyymmdd1=m.group(1)
                    c1=m.group(2)
                    time1=m.group(3)
                    #content=yyyymmdd1[5:10]+"/"+yyyymmdd1[0:4]
                    content=yyyymmdd1[0:4]+"-"+yyyymmdd1[5:7]+"-"+yyyymmdd1[8:10]+" "+time1                 
                    format="%Y-%m-%d %H:%M:%S"
                    content=content.strip()
                    print(content)
                    # UTC time from syslog
                    pomlgndatetime=datetime.datetime.strptime(content, format)
                    print ("UTC POM_login: ",end="")
                    print(pomlgndatetime)
                    # Convert to ETS timezone based on syslog creation
                    pomlgndatetime=time2ets(pomlgndatetime)
                    print (pomlgndatetime)
                    content=pomlgndatetime.strftime(format) +"   line#: " + str(line_counter)
                    print(content)
                    # Text with formatting.
                    cell = 'L'+ str(file_counter + 1)
                    worksheet.write(cell, content)
                    try:
                        content=str(duration(pomlgndatetime,libtcsoacoredatetime))
                        # Text with formatting.
                        cell = 'M'+ str(file_counter + 1)
                        if check_duration(duration(pomlgndatetime,libtcsoacoredatetime),THRESHOLD_CCAS):
                            worksheet.write(cell, content, red)
                        else: worksheet.write(cell, content)
                        chartdata.append(content)                                               
                        print(cell + " COMPLETED")
                    except Exception:
                        pass
            if (re.search('library libdocmgt', line)): #to estimate license check
                m = rg.search(line)
                if m:
                    yyyymmdd1=m.group(1)
                    c1=m.group(2)
                    time1=m.group(3)
                    #content=yyyymmdd1[5:10]+"/"+yyyymmdd1[0:4]
                    content=yyyymmdd1[0:4]+"-"+yyyymmdd1[5:7]+"-"+yyyymmdd1[8:10]+" "+time1                 
                    format="%Y-%m-%d %H:%M:%S"
                    content=content.strip()
                    print(content)
                    # UTC time from syslog
                    chklicdatetime=datetime.datetime.strptime(content, format)
                    print ("UTC check_license, library libdocmgt is first event after lic info: ",end="")
                    print(chklicdatetime)
                    # Convert to ETS timezone based on syslog creation
                    chklicdatetime=time2ets(chklicdatetime)
                    print (chklicdatetime)
                    content=chklicdatetime.strftime(format) +"   line#: " + str(line_counter)
                    print(content)
                    # Text with formatting.
                    cell = 'N'+ str(file_counter + 1)
                    worksheet.write(cell, content)
                    content=str(duration(chklicdatetime,pomlgndatetime))
                    # Text with formatting.
                    cell = 'O'+ str(file_counter + 1)
                    if check_duration(duration(chklicdatetime,pomlgndatetime),THRESHOLD_CHKLIC):
                        worksheet.write(cell, content, red)
                    else: worksheet.write(cell, content)                          
                    print(cell + " COMPLETED")                    
            if (re.search('MultiFieldKeyAttrsMap', line)):
                m = rg.search(line)
                if m:
                    yyyymmdd1=m.group(1)
                    c1=m.group(2)
                    time1=m.group(3)
                    #content=yyyymmdd1[5:10]+"/"+yyyymmdd1[0:4]
                    content=yyyymmdd1[0:4]+"-"+yyyymmdd1[5:7]+"-"+yyyymmdd1[8:10]+" "+time1                 
                    format="%Y-%m-%d %H:%M:%S"
                    content=content.strip()
                    print(content)
                    # UTC time from syslog
                    libsubdatetime=datetime.datetime.strptime(content, format)
                    print ("UTC MultiFieldKeyAttrsMap: ",end="")
                    print(libsubdatetime)
                    # Convert to ETS timezone based on syslog creation
                    libsubdatetime=time2ets(libsubdatetime)
                    print (libsubdatetime)
                    content=libsubdatetime.strftime(format) +"   line#: " + str(line_counter)
                    print(content)
                    # Text with formatting.
                    cell = 'P'+ str(file_counter + 1)
                    worksheet.write(cell, content)
                    try:
                        content=str(duration(libsubdatetime,chklicdatetime))
                        # Text with formatting.
                        cell = 'Q'+ str(file_counter + 1)
                        if check_duration(duration(libsubdatetime,chklicdatetime),THRESHOLD_LIBSUB):
                            worksheet.write(cell, content, red)
                        else: worksheet.write(cell, content)                          
                        print(cell + " COMPLETED")
                    except Exception:
                        pass
            if (re.search('LOV-Master', line)):
                m = rg.search(line)
                if m:
                    yyyymmdd1=m.group(1)
                    c1=m.group(2)
                    time1=m.group(3)
                    #content=yyyymmdd1[5:10]+"/"+yyyymmdd1[0:4]
                    content=yyyymmdd1[0:4]+"-"+yyyymmdd1[5:7]+"-"+yyyymmdd1[8:10]+" "+time1                 
                    format="%Y-%m-%d %H:%M:%S"
                    content=content.strip()
                    print(content)
                    # UTC time from syslog
                    schl2datetime=datetime.datetime.strptime(content, format)
                    print ("UTC LOV-Master: ",end="")
                    print(schl2datetime)
                    # Convert to ETS timezone based on syslog creation
                    schl2datetime=time2ets(schl2datetime)
                    print (schl2datetime)
                    content=schl2datetime.strftime(format) +"   line#: " + str(line_counter)
                    print(content)
                    # Text with formatting.
                    cell = 'R'+ str(file_counter + 1)
                    worksheet.write(cell, content)
                    try:
                        content=str(duration(schl2datetime,libsubdatetime))
                        # Text with formatting.
                        cell = 'S'+ str(file_counter + 1)
                        if check_duration(duration(schl2datetime,libsubdatetime),THRESHOLD_SCHLD2):
                            worksheet.write(cell, content, red)
                        else: worksheet.write(cell, content)
                        #chartdata.append(content)                           
                        print(cell + " COMPLETED")
                    except Exception:
                        pass
            if (re.search('Started. - Teamcenter.CoreModelGeneral', line)):
                m = rg.search(line)
                if m:
                    yyyymmdd1=m.group(1)
                    c1=m.group(2)
                    time1=m.group(3)
                    #content=yyyymmdd1[5:10]+"/"+yyyymmdd1[0:4]
                    content=yyyymmdd1[0:4]+"-"+yyyymmdd1[5:7]+"-"+yyyymmdd1[8:10]+" "+time1                 
                    format="%Y-%m-%d %H:%M:%S"
                    content=content.strip()
                    print(content)
                    # UTC time from syslog
                    starteddatetime=datetime.datetime.strptime(content, format)
                    print ("UTC Started.: ",end="")
                    print(starteddatetime)
                    # Convert to ETS timezone based on syslog creation
                    starteddatetime=time2ets(starteddatetime)
                    print (starteddatetime)
                    content=starteddatetime.strftime(format) +"   line#: " + str(line_counter)
                    print(content)
                    # Text with formatting.
                    cell = 'T'+ str(file_counter + 1)
                    worksheet.write(cell, content)
                    try:
                        content=str(duration(starteddatetime,schl2datetime))
                        # Text with formatting.
                        cell = 'U'+ str(file_counter + 1)
                        worksheet.write(cell, content)                          
                        print(cell + " COMPLETED")
                    except Exception:
                        pass
            if (re.search('ImanVolumeImpl::', line)):
                if found_flag==0:
                    m = rg.search(line)
                    if m:
                        #To catch only first occurrence
                        found_flag=1
                        yyyymmdd1=m.group(1)
                        c1=m.group(2)
                        time1=m.group(3)
                        #content=yyyymmdd1[5:10]+"/"+yyyymmdd1[0:4]
                        content=yyyymmdd1[0:4]+"-"+yyyymmdd1[5:7]+"-"+yyyymmdd1[8:10]+" "+time1                 
                        format="%Y-%m-%d %H:%M:%S"
                        content=content.strip()
                        print(content)
                        # UTC time from syslog
                        imanvoldatetime=datetime.datetime.strptime(content, format)
                        print ("UTC ImanVolumeImpl: ",end="")
                        print(imanvoldatetime)
                        # Convert to ETS timezone based on syslog creation
                        imanvoldatetime=time2ets(imanvoldatetime)
                        print (imanvoldatetime)
                        content=imanvoldatetime.strftime(format) +"   line#: " + str(line_counter)
                        print(content)
                        # Text with formatting.
                        cell = 'V'+ str(file_counter + 1)
                        worksheet.write(cell, content)
                        content=str(duration(imanvoldatetime,starteddatetime))
                        # Text with formatting.
                        cell = 'W'+ str(file_counter + 1)
                        if check_duration(duration(imanvoldatetime,starteddatetime),THRESHOLD_IMANV):
                            worksheet.write(cell, content, red)
                        else: worksheet.write(cell, content)                          
                        print(cell + " COMPLETED")
            if (re.search('library libeint is delay loaded', line)):
               print(line) 
               m = rg.search(line)                    
               if m:
                    yyyymmdd1=m.group(1)
                    c1=m.group(2)
                    time1=m.group(3)
                    #content=yyyymmdd1[5:10]+"/"+yyyymmdd1[0:4]
                    content=yyyymmdd1[0:4]+"-"+yyyymmdd1[5:7]+"-"+yyyymmdd1[8:10]+" "+time1                 
                    format="%Y-%m-%d %H:%M:%S"
                    content=content.strip()
                    print(content)
                    # UTC time from syslog
                    libeintdatetime=datetime.datetime.strptime(content, format)
                    print ("UTC Started.: ",end="")
                    print(libeintdatetime)
                    # Convert to ETS timezone based on syslog creation
                    libeintdatetime=time2ets(libeintdatetime)
                    print (libeintdatetime)
                    content=libeintdatetime.strftime(format) +"   line#: " + str(line_counter)
                    print(content)
                    # Text with formatting.
                    cell = 'X'+ str(file_counter + 1)
                    worksheet.write(cell, content)
                    try:
                        content=str(duration(libeintdatetime,imanvoldatetime))
                        # Text with formatting.
                        cell = 'Y'+ str(file_counter + 1)
                        worksheet.write(cell, content)                          
                        print(cell + " COMPLETED")
                    except Exception:
                        pass            
            if (re.search('@@@', line)):#TC End of Session
               print(line) 
               m = rg0.search(line)                    
               if m:
                    dayofweek1=m.group(1)
                    ws1=m.group(2)
                    month1=m.group(3)
                    ws2=m.group(4)
                    day1=m.group(5)
                    ws3=m.group(6)
                    time1=m.group(7)
                    ws4=m.group(8)
                    year1=m.group(9)
                    content = dayofweek1+ws1+month1+ws2+day1+ws3+time1+ws4+year1
                    print (content)
                    format='%a %b %d %H:%M:%S %Y'
                    endofsessiontime=datetime.datetime.strptime(content, format)
                    print(endofsessiontime)
                    #change dateformat
                    format="%Y-%m-%d %H:%M:%S"
                    print ("ETS syslog creation: ",end="")
                    print(endofsessiontime)
                    # Text with formatting.
                    cell = 'Z'+ str(file_counter + 1)
                    worksheet.write(cell, content)
                    content=str(duration(endofsessiontime,syscrdatetime))
                    # Text with formatting.
                    cell = 'AA'+ str(file_counter + 1)
                    worksheet.write(cell, content)                          
                    print(cell + " COMPLETED")
 
                        
    #chart.add_series({'values': '=Sheet1!$B$2'})
    # Insert the chart into the worksheet.
    #place = 'A' + str(gap) 
    #worksheetnew.insert_chart(place, chart)               
                 

workbook.close()            
print("THIS IS THE END")
              
        
'''def time2ets (syscrdatetime,eventdatetime):
    delta = eventdatetime - syscrdatetime
    datetime.timedelta(0, 8, 562000)
    divmod(delta.days * 86400 + delta.seconds, 60)
    eventdatetime = eventdatetime - delta
    print ("func: UTC-ETS= ",end="")
    print (delta)
    print ("func: in ETS= ",end="")
    print(eventdatetime),
    return eventdatetime'''


# Write some numbers, with row/column notation.
#worksheet.write(2, 0, 123)
#worksheet.write(3, 0, 123.456)
# Insert an image.
#worksheet.insert_image('B5', 'logo.png')

