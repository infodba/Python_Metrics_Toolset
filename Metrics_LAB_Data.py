import glob
import  re
import datetime
from plotly import tools
#from plotly import graph_objs as go
#import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot as py

RFOLDER_PATH = 'c:\\_WORK\\2018_Metrics\\4T_latencies\\FNA2FNA_LAB\\'
FILE_EXTENSION = "*.log"

def findresults(record, activity):
    results_dict = {}
    global key
    global value
    rg_activity = re.compile('.*?' + '('+ activity +')', re.IGNORECASE | re.DOTALL)
    rg_results = re.compile('.*?' + '([+-]?\\d*\\.\\d+)(?![-+0-9\\.])',
                             re.IGNORECASE | re.DOTALL)  # to find the last float
    re1 = '((?:2|1)\\d{3}(?:-|\\/)(?:(?:0[1-9])|(?:1[0-2]))(?:-|\\/)(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))(?:T|\\s)(?:(?:[0-1][0-9])|(?:2[0-3])):(?:[0-5][0-9]):(?:[0-5][0-9]))'  # Time Stamp 1
    rg_timestamp = re.compile(re1, re.IGNORECASE | re.DOTALL)
    print(record)
    m = rg_activity.search(record)  # Find Activity name
    if m:
        activity_name = m.group(1)
        print(activity_name)
        m = rg_timestamp.search(record) # Find StartDateTime
        if m:
            timestamp = m.group(1)
            #call_dict.update({str(rqstnum): extracted_timestamp.replace(',','.') +'_'+extracted_name})
            key = timestamp
            print(key)
            m = rg_results.search(record) # Find Duration value
            if m:
                duration = m.group(1)
                value = float(duration)
                print(value)
                results_dict.update({key:value})
            else:
                print("Empty value for Duration! Will put zero seconds")
                value = 0.00
                results_dict.update({key:value})

    print(results_dict)
    return results_dict

print('START')
file_list = glob.glob(RFOLDER_PATH + FILE_EXTENSION)
#file_list.reverse()
#print(file_list)
file_counter = 0
login_dict = {}
openfolder_dict = {}
remotesearch_dict = {}
login_x = []
login_y = []
openfolder_x = []
openfolder_y = []
remotesearch_x = []
remotesearch_y = []


for file in file_list:
    print(file)
    file_counter +=1
    line_counter = 0

    with open(file, "r") as log:
        for line in log:
            line_counter += 1
            login_dict.update(findresults(line,'Login'))
            openfolder_dict.update(findresults(line,'OpenFolder'))
            remotesearch_dict.update(findresults(line,'RemoteSearch'))
            '''login_x.append(findxdata(line,'Login'))
            login_y.append(findydata(line,'Login'))
            openfolder_x.append(findxdata(line,'OpenFolder'))
            openfolder_y.append(findydata(line,'OpenFolder'))


print(login_x)
print(login_y)
print('OpenFolder')
print(openfolder_x)
print(openfolder_y)'''
print('Login')
print(login_dict)
print('OpenFolder')
print(openfolder_dict)

for key in sorted(login_dict):
    #print(key + ' |Value=| ' + (login_dict[key]))
    login_x.append(key)
    login_y.append(login_dict[key])
for key in sorted(openfolder_dict):
    #print(key + ' |Value=| ' + (login_dict[key]))
    openfolder_x.append(key)
    openfolder_y.append(openfolder_dict[key])
for key in sorted(remotesearch_dict):
    #print(key + ' |Value=| ' + (login_dict[key]))
    remotesearch_x.append(key)
    remotesearch_y.append(remotesearch_dict[key])

#trace1 = go.Scatter(x=[1, 2, 3], y=[4, 5, 6])
trace1 = go.Scatter(x=login_x, y=login_y)
trace2 = go.Scatter(x=openfolder_x, y=openfolder_y)
trace3 = go.Scatter(x=remotesearch_x, y=remotesearch_y)
trace4 = go.Scatter(x=[4000, 5000, 6000], y=[7000, 8000, 9000])

fig = tools.make_subplots(rows=2, cols=3, subplot_titles=('Login', 'OpenFolder',
                                                          'RemoteSearch', 'FreezeWorkflow'))

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)
fig.append_trace(trace3, 1, 3)
fig.append_trace(trace4, 2, 1)

fig['layout'].update(height=600, width=1900, title='4T Metrics Results')

py(fig, filename='make-subplots-multiple-with-titles.html')