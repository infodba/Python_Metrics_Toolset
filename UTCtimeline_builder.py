import sys
import glob
import re
import xlsxwriter
import datetime
from plotly.offline import plot
import random
import plotly.graph_objs as go
import plotly.plotly as py
from plotly.tools import FigureFactory as ff
from pytz import timezone
import pytz

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("SyslogLatencyReport.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

sys.stdout = Logger()

for args in sys.argv:
    print(args)


####################################CONTANTS#########################################################################
RFOLDER_PATH = '.\\'
FILE_EXTENSION = "*.syslg"
WFILE_PATH = RFOLDER_PATH
STARTNUM = "00000"#sys.argv[1] #use format "00000" 5 digits
ENDNUM = "00000"#sys.argv[2]

####################################CONTANTS#########################################################################
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

def duration (datetimeafter, datetimebefore):
    #datetimeafter=datetimeafter.replace(microsecond=0)
    #datetimebefore=datetimebefore.replace(microsecond=0)
    datetimeafter=datetimeafter
    datetimebefore=datetimebefore
    duration = datetimeafter - datetimebefore
    #print('datetimeafter=',end="")
    #print(datetimeafter)
    #print('datetimebefore=',end="")
    #print(datetimebefore)
    #print ("  func: duration= ",end="")
    #print(duration)
    #strduration=str(duration)
    return duration

####################################REGEX############################################################################
re1='.*?'	# Non-greedy match on filler
re2='((?:2|1)\\d{3}(?:-|\\/)(?:(?:0[1-9])|(?:1[0-2]))(?:-|\\/)(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))(?:T|\\s)(?:(?:[0-1][0-9])|(?:2[0-3])):(?:[0-5][0-9]):(?:[0-5][0-9]))'	# Time Stamp 1
re3='(.)'	# Any Single Character 1
re4='(\\d+)'	# Any Digits

rgtimestamp = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)

re22='(DEBUG)'
rgdebug = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)

re222='(c3pmonit)'	# Alphanum 1
re333='(\\.)'
# re444='('+STARTNUM+')'
re444='('')'
rgrequestnum = re.compile(re1+re222+re333+re444,re.IGNORECASE|re.DOTALL)

rre1='.*?'	# Non-greedy match on filler
rre2='((?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3}))[-:\\/.](?:[0]?[1-9]|[1][012])[-:\\/.](?:(?:[0-2]?\\d{1})|(?:[3][01]{1})))(?![\\d])'	# YYYYMMDD 1
rre3='(.)'	# Any Single Character 1
rre4='((?:(?:[0-1][0-9])|(?:[2][0-3])|(?:[0-9])):(?:[0-5][0-9])(?::[0-5][0-9])?(?:\\s?(?:am|AM|pm|PM))?)'	# HourMinuteSec 1
rg = re.compile(rre1+rre2+rre3+rre4+re3+re4,re.IGNORECASE|re.DOTALL)
####################################REGEX############################################################################

####################################LOOP#############################################################################
print('START')
#print(re1+re222+re333+re444)
#print(RFOLDER_PATH + "*.log")
file_list = glob.glob(RFOLDER_PATH + FILE_EXTENSION)
file_list.reverse()
print(file_list)
file_counter = 0
debug_messages_list = []
call_list = []
reply_list = []
activity_list = []
gantt_data = []
call_dict = {}
reply_dict = {}
colors = []


for file in file_list:
    print(file)
    file_counter +=1
    line_counter = 0
    timestamp = ""
    currentline = ""
    currentlinenumber = 0
    with open(file, "r") as syslog:
        for line in syslog:
            line_counter += 1
            # print(line_counter)
            if line_counter >=0:
                #print(line)
                m = rg.search(line)
                if m:
                    content = m.group(1)+' '+m.group(3)+m.group(4)+m.group(5)
                    content=content.strip()
                    #print("STRING format: "+content)
                    # format = "%Y/%m/%d-%H:%M:%S,%f"
                    format="%Y/%m/%d %H:%M:%S.%f"
                    try:
                        previouslinenumber = currentlinenumber
                        currentlinenumber = line_counter
                        previousline = currentline
                        currentline = line
                        oldtimestamp = timestamp
                        timestamp = datetime.datetime.strptime(content, format)
                        #print(oldtimestamp)
                        #print(timestamp)
                        timediff = str(duration(timestamp, oldtimestamp))
                        #print(timediff)
                        if timediff >="0:00:00.5":
                            print('!!!!!LATENCY '+str(timediff)+' DETECTED!!!! between Line# '+str(previouslinenumber)+ ' and Line# '+str(currentlinenumber))
                            print('Line# '+str(previouslinenumber)+': '+previousline)
                            #print(timediff)
                            print('Line# '+str(currentlinenumber)+': '+currentline)
                            gantt_data.append(
                                dict(Task='B/n Line# '+str(previouslinenumber).zfill(5)+' and Line# '+str(currentlinenumber).zfill(5), Start=oldtimestamp, Finish=timestamp,
                                     Resource='B/n Line# '+str(previouslinenumber).zfill(5)+' and Line# '+str(currentlinenumber).zfill(5) + ', ' + timediff))
                            # print(gantt_data)
                            r = lambda: random.randint(0, 255)
                            # print('#%02X%02X%02X' % (r(), r(), r()))
                            colors.append('#%02X%02X%02X' % (r(), r(), r()))
                    except Exception:
                        pass
####################################LOOP#############################################################################

####################################HTML#############################################################################
    try:
        fig = ff.create_gantt(gantt_data, colors=colors, index_col='Resource', reverse_colors=True, width=1900,
                               height=1024,
                               title='Syslog Timeline for ' + str(len(gantt_data)) + ' latencies more than 0.5 sec. ',
                               bar_width=0.8, showgrid_x=True, showgrid_y=True, show_colorbar=True)

        plot(fig, filename=RFOLDER_PATH + 'SyslogDelaysChart.html')
    except Exception:
        pass
####################################HTML#############################################################################
print("THIS IS THE END")