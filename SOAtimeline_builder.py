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

for args in sys.argv:
    print(args)


####################################CONTANTS#########################################################################
#RFOLDER_PATH = "c:\\_WORK\PBI\RevisionRule\\FOA\\2017_08_17_01_55_53\\"
#RFOLDER_PATH = 'c:\\_WORK\\PBI\\LocalSearch\\IND_4T\\Sep\\GPRABHUD_TcRAC_20170912190009\\'
#RFOLDER_PATH = sys.argv[2]
#RFOLDER_PATH = 'c:\\_WORK\\PBI\\LocalSearch\\FNA\\2T\\'
RFOLDER_PATH = '.\\'
FILE_EXTENSION = "*.txt"
WFILE_PATH = RFOLDER_PATH
STARTNUM = sys.argv[1] #use format "00000" 5 digits
ENDNUM = sys.argv[2]

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
    print('datetimeafter=',end="")
    print(datetimeafter)
    print('datetimebefore=',end="")
    print(datetimebefore)
    print ("  func: duration= ",end="")
    print(duration)
    #strduration=str(duration)
    return duration

####################################EXCEL############################################################################
# Create an new Excel file and add a worksheet.
'''workbook = xlsxwriter.Workbook(WFILE_PATH + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(":","_") + '_SOAtimeliner_results.xlsx')
worksheet = workbook.add_worksheet()
# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True, 'bg_color': 'silver'})
red = workbook.add_format({'bold': True, 'font_color': 'red', 'bg_color': 'yellow'})
link_format = workbook.add_format({'color': 'blue', 'underline': 1})

# Widen the column to make the text clearer.
worksheet.set_column('A:A', len('ComLog Creation Date  '))
# Write captions text.
worksheet.write('A1', 'ComLog Creation Date', bold)

# Widen the column to make the text clearer.
worksheet.set_column('B:B', len('Link to Timeline    '))
# Write captions text.
worksheet.write('B1', 'Link to Timeline', bold) '''
####################################EXCEL############################################################################

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
re444='('+STARTNUM+')'
rgrequestnum = re.compile(re1+re222+re333+re444,re.IGNORECASE|re.DOTALL)
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

for file in file_list:
    file_counter +=1
    line_counter = 0
    with open(file, "r") as syslog:
        for line in syslog:
            line_counter += 1
            #print(line_counter)
            if line_counter ==1:
                print(line)
                m = rgtimestamp.search(line)
                if m:
                    content = m.group(1)+m.group(2)+m.group(3)
                    print("STRING format: "+content)
                    format = "%Y-%m-%d %H:%M:%S,%f"
                    timestamp = datetime.datetime.strptime(content, format)
                    print(timestamp.time())
                    # Text with formatting.
                    cell = 'A' + str(file_counter + 1)
                    content = content + "  " + file
                    #worksheet.write_url(cell, file, link_format, content)
                    #print(cell + " COMPLETED")
            m = rgdebug.search(line)
            if m:
                debug_messages_list.append(line)

    deduplicated_list = remove_duplicates(debug_messages_list)
    print(deduplicated_list)
    for element in deduplicated_list:
        #print(indexval)
        #print(debug_messages_list[indexval])
        rqstnum = int(STARTNUM.lstrip('0'))
        while rqstnum <= int(ENDNUM.lstrip('0')):
            #print(rqstnum)
            str_rqstnum = str(rqstnum).zfill(5)
            #print(str_rqstnum)
            search_call1 = re.compile('.*?' + re2 + re3 + re4 + '.*?' + '(c3pmonit)' + '(\\.)' + '(' + str_rqstnum + ')' +'(\\:)' + '.*?' + '(\w+)$',
                                      re.IGNORECASE | re.DOTALL)
            search_call2 = re.compile('.*?' + re2 + re3 + re4 + '.*?' + '(c3pmonit)' + '(\\.)' + '(' + str_rqstnum + ')' +'(\\:)' + '.*?' + '(\w+)' +'(\s)'+ '(\\))$',
                                      re.IGNORECASE | re.DOTALL)
            search_reply = re.compile('.*?' + re2 + re3 + re4 + '.*?' + '(c3pmonit)' + '(\\.)' + '(' + str_rqstnum + ')' +'($)',
                                      re.IGNORECASE | re.DOTALL)
            m1 = search_call1.search(element)
            m2 = search_call2.search(element)
            m3 = search_reply.search(element)

            if m1:
                #print("!!!RESULT!!!" + deduplicated_list[indexval])
                extracted_timestamp = m1.group(1)+m1.group(2)+m1.group(3)
                #print(extracted_timestamp)
                extracted_number = m1.group(6)
                #print(extracted_number)
                extracted_name = m1.group(8)

                #format = "%Y-%m-%d %H:%M:%S,%f"
                #timestamp = (datetime.datetime.strptime(extracted_timestamp, format)).time()
                #print(timestamp.time())
                call_list.append(element)
                #call_dict[str(rqstnum)]=extracted_timestamp + '_' + extracted_name
                call_dict.update({str(rqstnum): extracted_timestamp.replace(',','.') +'_'+extracted_name})

            if m2:
                #print("!!!RESULT!!!" + deduplicated_list[indexval])
                extracted_timestamp = m2.group(1)+m2.group(2)+m2.group(3)
                #print(extracted_timestamp)
                extracted_number = m2.group(6)
                #print(extracted_number)
                extracted_name = m2.group(8)

                #format = "%Y-%m-%d %H:%M:%S,%f"
                #timestamp = (datetime.datetime.strptime(extracted_timestamp, format)).time()
                #print(timestamp.time())
                call_list.append(element)
                #call_dict[str(rqstnum)] = extracted_timestamp + '_' + extracted_name
                call_dict.update({str(rqstnum): extracted_timestamp.replace(',','.') +'_'+extracted_name})

            if m3:
                #print("!!!RESULT!!!" + deduplicated_list[indexval])
                extracted_timestamp = m3.group(1)+m3.group(2)+m3.group(3)
                #print(extracted_timestamp)
                extracted_number = m3.group(6)
                #print(extracted_number)

                #format = "%Y-%m-%d %H:%M:%S,%f"
                #timestamp = datetime.datetime.strptime(extracted_timestamp, format)
                #print(timestamp.time())

                reply_list.append(element)
                #reply_dict[str(rqstnum)] = extracted_timestamp
                reply_dict.update({str(rqstnum): extracted_timestamp.replace(',','.')})

            rqstnum += 1

print('-= FOUNDED RESULTS: =-')
for items in call_list:
    print("CALL_LIST-> "+items)
for items in reply_list:
    print("REPLY_LIST-> "+items)
#for key, value in sorted(call_dict.items()):
#    print("{} : {}".format(key, value))

#call_dict = sorted(call_dict.items())
print("CALL DICT :")
print(call_dict)
#reply_dict = sorted(reply_dict.items())

print("REPLY DICT :")
#print(sorted(reply_dict.__iter__()))

colors = []
# fill gantt_data
isfirst = True
last_key = ''
for key in sorted(call_dict):
    if key in reply_dict:
        print(key + ' |name| '+ (call_dict[key])[24:] +' |call| '+ (call_dict[key])[:22] + ' |reply| '+ reply_dict[key])
        r = lambda: random.randint(0, 255)
        #print('#%02X%02X%02X' % (r(), r(), r()))
        colors.append('#%02X%02X%02X' % (r(), r(), r()))
        #convert str2time to calculate call&reply duration
        format = "%Y-%m-%d %H:%M:%S.%f"
        calltime = datetime.datetime.strptime((call_dict[key])[:22], format)
        replytime = datetime.datetime.strptime(reply_dict[key], format)
        strduration = str(duration(replytime, calltime))
        #
        gantt_data.append(dict(Task=key.zfill(5), Start=(call_dict[key])[:22], Finish=reply_dict[key], Resource=key.zfill(5) +' ' +(call_dict[key])[24:]+', '+strduration) )
        if isfirst:
            start_time = calltime
        isfirst = False

print(gantt_data)
print(colors)
try:
    print(start_time)
    print(replytime)
    totaltime = duration(replytime, start_time)
    print(totaltime)
    fig = ff.create_gantt(gantt_data, colors=colors, index_col='Resource', reverse_colors=True, width=1900, height=1024,
                          title='SOA Timeline for Metrics Use Case, ' + str(
                              len(gantt_data)) + ' call&reply' + '; TotalTime ' + str(totaltime),
                          bar_width=0.8, showgrid_x=True, showgrid_y=True, show_colorbar=True)

    plot(fig, filename=RFOLDER_PATH + 'Gantt-timeline.html')
except Exception:
    pass
#print ("pairs dict:")
#pairs_dict = {key:reply_dict[key] for key in call_dict if key in reply_dict}
#print(pairs_dict)
####################################LOOP#############################################################################

####################################HTML#############################################################################

'''df = [
    dict(Task='setSessionGroupMember', Start='2017-08-01 01:36:22.853', Finish='2017-08-01 01:36:23.914', Resource='setSessionGroupMember'),
    dict(Task='getPreferences1', Start='2017-08-01 01:36:23.930', Finish='2017-08-01 01:36:24.288', Resource='getPreferences1'),
    #dict(Task='getPreferences2', Start='2017-08-01 14:40:00.092', Finish='2017-08-01 14:40:03.321', Resource='getPreferences2'),
    dict(Task='getQueries1', Start='2017-08-01 01:36:24.320', Finish='2017-08-01 01:36:24.444', Resource='getQueries1'),
    #dict(Task='getQueries2', Start='2017-08-01 14:40:03.336', Finish='2017-08-01 14:40:04.148', Resource='getQueries2'),
    dict(Task='getAvailableTypesWithDisplayNames', Start='2017-08-01 01:36:24.460', Finish='2017-08-01 01:36:24.507', Resource='getAvailableTypesWithDisplayNames'),
    dict(Task='getDatasetTypeInfo', Start='2017-08-01 01:36:24.522', Finish='2017-08-01 01:36:27.143', Resource='getDatasetTypeInfo'),
    dict(Task='getQueries2', Start='2017-08-01 01:36:27.159', Finish='2017-08-01 01:36:27.284', Resource='getQueries2'),
    #dict(Task='findProjects', Start='2017-08-01 14:40:05.957', Finish='2017-08-01 14:40:06.098', Resource='findProjects'),
    dict(Task='askDefaultRole1', Start='2017-08-01 01:36:27.299', Finish='2017-08-01 01:36:27.299', Resource='askDefaultRole1'),
    dict(Task='askDefaultRole2', Start='2017-08-01 01:36:27.299', Finish='2017-08-01 01:36:27.315', Resource='askDefaultRole2'),
    dict(Task='checkPrivileges', Start='2017-08-01 01:36:27.799', Finish='2017-08-01 01:36:27.799', Resource='checkPrivileges')]

df = [dict(Task="Job A", Start='2009-01-01', Finish='2009-02-01', Resource='Apple'),
      dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Resource='Grape'),
      dict(Task="Job C", Start='2009-04-20', Finish='2009-09-30', Resource='Banana')]

colors = []
for item in df:
    r = lambda: random.randint(0,255)
    print('#%02X%02X%02X' % (r(),r(),r()))
    colors.append('#%02X%02X%02X' % (r(),r(),r()))
print(colors)
#colors = ['#7a0504', (0.2, 0.7, 0.3), 'rgb(210, 60, 180)']
fig = ff.create_gantt(df, colors=colors, index_col='Resource', reverse_colors=True, show_colorbar=True)'''


####################################HTML#############################################################################

#workbook.close()
print("THIS IS THE END")