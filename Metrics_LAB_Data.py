import glob
import  re
from plotly import tools
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

def tracefactory(activity_dict):
    x_data = []
    y_data = []
    for key in sorted(activity_dict):
        # print(key + ' |Value=| ' + (login_dict[key]))
        x_data.append(key)
        y_data.append(activity_dict[key])
    trace = go.Scatter(x=x_data, y=y_data)
    return trace

def findaverage(activity_dict):
    if len(activity_dict) > 0:
        value = sum(activity_dict.values())/len(activity_dict)
        stringvalue = "{0:.2f}".format(value)

    return stringvalue

print('START')
file_list = glob.glob(RFOLDER_PATH + FILE_EXTENSION)
#file_list.reverse()
#print(file_list)
file_counter = 0
login_dict = {}
openfolder_dict = {}
remotesearch_dict = {}
freezeworkflow_dict = {}
tcrevise_dict = {}
freezeworkflowpublished_dict = {}
loadintvvis_dict = {}
createecn_dict = {}
wherereferenced_dict = {}
whereused_dict = {}
changegroup_dict = {}
localsearch_dict = {}
openinsm_dict = {}
revisionrule_dict = {}
loadincatia_dict = {}



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
            freezeworkflow_dict.update(findresults(line,'FreezeWorkflow'))
            tcrevise_dict.update(findresults(line,'TcRevise'))
            freezeworkflowpublished_dict.update(findresults(line,'FreezeWorkflowPublished'))
            loadintvvis_dict.update(findresults(line,'LoadInTCVis'))
            createecn_dict.update(findresults(line,'CreateECN'))
            wherereferenced_dict.update(findresults(line,'WhereReferenced'))
            whereused_dict.update(findresults(line,'WhereUsed'))
            changegroup_dict.update(findresults(line,'ChangeGroup'))
            localsearch_dict.update(findresults(line,'LocalSearch'))
            openinsm_dict.update(findresults(line,'OpenInSM'))
            revisionrule_dict.update(findresults(line,'RevisionRule'))
            loadincatia_dict.update(findresults(line,'LoadInCatia'))

fig = tools.make_subplots(rows=5, cols=3,
                          subplot_titles=('Login, Avg='+findaverage(login_dict)+' sec',
                                          'OpenFolder, Avg='+findaverage(openfolder_dict)+' sec',
                                          'RemoteSearch, Avg='+findaverage(remotesearch_dict)+' sec',
                                          'FreezeWorkflow, Avg='+findaverage(freezeworkflow_dict)+' sec',
                                          'TcRevise, Avg='+findaverage(tcrevise_dict)+' sec',
                                          'FreezeWorkflowPublished, Avg='+findaverage(freezeworkflowpublished_dict)+' sec',
                                          'LoadInTCVis, Avg='+findaverage(loadintvvis_dict)+' sec',
                                          'CreateECN, Avg='+findaverage(createecn_dict)+' sec',
                                          'WhereReferenced, Avg='+findaverage(wherereferenced_dict)+' sec',
                                          'WhereUsed, Avg='+findaverage(whereused_dict)+' sec',
                                          'ChangeGroup, Avg='+findaverage(changegroup_dict)+' sec',
                                          'LocalSearch, Avg='+findaverage(localsearch_dict)+' sec',
                                          'OpenInSM, Avg='+findaverage(openinsm_dict)+' sec',
                                          'RevisionRule, Avg='+findaverage(revisionrule_dict)+' sec',
                                          'LoadInCatia, Avg='+findaverage(loadincatia_dict)+' sec'))

fig.append_trace(tracefactory(login_dict), 1, 1)
fig.append_trace(tracefactory(openfolder_dict), 1, 2)
fig.append_trace(tracefactory(remotesearch_dict), 1, 3)
fig.append_trace(tracefactory(freezeworkflow_dict), 2, 1)
fig.append_trace(tracefactory(tcrevise_dict), 2, 2)
fig.append_trace(tracefactory(freezeworkflowpublished_dict), 2, 3)
fig.append_trace(tracefactory(loadintvvis_dict), 3, 1)
fig.append_trace(tracefactory(createecn_dict), 3, 2)
fig.append_trace(tracefactory(wherereferenced_dict), 3, 3)
fig.append_trace(tracefactory(whereused_dict), 4, 1)
fig.append_trace(tracefactory(changegroup_dict), 4, 2)
fig.append_trace(tracefactory(localsearch_dict), 4, 3)
fig.append_trace(tracefactory(openinsm_dict), 5, 1)
fig.append_trace(tracefactory(revisionrule_dict), 5, 2)
fig.append_trace(tracefactory(loadincatia_dict), 5, 3)

fig['layout'].update(height=1024, width=1900, title='4T FNA2FNA LAB PC Metrics Results')

py(fig, filename='FNA_lab_metrics_results.html')