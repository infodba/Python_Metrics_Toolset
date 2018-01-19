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
    x_data = []
    y_data = []
    rg_activity = re.compile('.*?' + '('+ activity +')', re.IGNORECASE | re.DOTALL)
    rg_results = re.compile('.*?' + '([+-]?\\d*\\.\\d+)(?![-+0-9\\.])',
                             re.IGNORECASE | re.DOTALL)  # to find the last float
    re1 = '((?:2|1)\\d{3}(?:-|\\/)(?:(?:0[1-9])|(?:1[0-2]))(?:-|\\/)(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))(?:T|\\s)(?:(?:[0-1][0-9])|(?:2[0-3])):(?:[0-5][0-9]):(?:[0-5][0-9]))'  # Time Stamp 1
    rg_timestamp = re.compile(re1, re.IGNORECASE | re.DOTALL)
    print(record)
    m = rg_activity.search(record)  # Find Activity name
    if m:
        content = m.group(1)
        print(content)
        m = rg_timestamp.search(record) # Find StartDateTime
        if m:
            content = m.group(1)
            print(content)
            x_data.append(content) # Put value for X
            m = rg_results.search(record) # Find Duration value
            if m:
                content = m.group(1)
                login_y.append(float(content))
                y_data.append(float(content))
                print(float(content))
            else:
                print("Empty value for Duration! Will put zero seconds")
                y_data.append(0.00)

    return x_data, y_data

file_list = glob.glob(RFOLDER_PATH + FILE_EXTENSION)
#file_list.reverse()
print(file_list)
file_counter = 0
login_x = []
login_y = []
openfolder_x = []
openfolder_y = []
remotesearch_x = []
remotesearch_y = []


rg_login = re.compile('.*?' + '(Login)', re.IGNORECASE | re.DOTALL)
rg_openfolder = re.compile('.*?' + '(OpenFolder)', re.IGNORECASE | re.DOTALL)
rg_remotesearch = re.compile('.*?' + '(RemoteSearch)', re.IGNORECASE | re.DOTALL)
rg_duration = re.compile('.*?' + '([+-]?\\d*\\.\\d+)(?![-+0-9\\.])', re.IGNORECASE | re.DOTALL) # to find the last float
re1='((?:2|1)\\d{3}(?:-|\\/)(?:(?:0[1-9])|(?:1[0-2]))(?:-|\\/)(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))(?:T|\\s)(?:(?:[0-1][0-9])|(?:2[0-3])):(?:[0-5][0-9]):(?:[0-5][0-9]))'	# Time Stamp 1
rg_timestamp = re.compile(re1,re.IGNORECASE|re.DOTALL)


for file in file_list:
    print(file)
    file_counter +=1
    line_counter = 0

    with open(file, "r") as log:
        for line in log:
            line_counter += 1
            login_x, login_y = findresults(line,'Login')
            openfolder_x, openfolder_y = 
            '''if line_counter >=0:
                print(line)
                m = rg_duration.search(line)
                if m:
                    content = m.group(1)
                    login_y.append(float(content))
                    openfolder_y.append(float(content))
                    print(float(content))
                    m = rg_login.search(line) #Login Activity
                    if m:
                        content = m.group(1)
                        print(content)
                        m = rg_timestamp.search(line)
                        if m:
                            content = m.group(1)
                            print(content)
                            login_x.append(content)
                    m = rg_openfolder.search(line)
                    if m:
                        content = m.group(1)
                        print(content)
                        m = rg_timestamp.search(line)
                        if m:
                            content = m.group(1)
                            print(content)
                            openfolder_x.append(content)
                    m = rg_openfolder.search(line)
                    if m:
                        content = m.group(1)
                        print(content)
                        m = rg_timestamp.search(line)
                        if m:
                            content = m.group(1)
                            print(content)
                            openfolder_x.append(content)
                    m = rg_remotesearch.search(line)
                    if m:
                        content = m.group(1)
                        print(content)
                        m = rg_timestamp.search(line)
                        if m:
                            content = m.group(1)
                            print(content)
                            openfolder_x.append(content)
                else:
                    print("Empty value for Duration! Will skip it")'''
print(login_x)
print(login_y)

#trace1 = go.Scatter(x=[1, 2, 3], y=[4, 5, 6])
trace1 = go.Scatter(x=login_x, y=login_y)
trace2 = go.Scatter(x=openfolder_x, y=openfolder_y)
trace3 = go.Scatter(x=[300, 400, 500], y=[600, 700, 800])
trace4 = go.Scatter(x=[4000, 5000, 6000], y=[7000, 8000, 9000])

fig = tools.make_subplots(rows=2, cols=3, subplot_titles=('Login', 'OpenFolder',
                                                          'Plot 3', 'Plot 4'))

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)
fig.append_trace(trace3, 1, 3)
fig.append_trace(trace4, 2, 1)

fig['layout'].update(height=600, width=1900, title='4T Metrics Results')

py(fig, filename='make-subplots-multiple-with-titles.html')