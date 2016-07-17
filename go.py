#%matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
import requests

from operator import itemgetter
from pandas.io.json import json_normalize
from scipy import special, optimize

# form a request
# openFDA API key: TTwz56GNTpZnsL4il0pLIwz7F43QObZOQEssWlSU

def get_drug_adverse_event_data(drugname):
    
    request_string='https://api.fda.gov/drug/event.json?api_key=TTwz56GNTpZnsL4il0pLIwz7F43QObZOQEssWlSU&search=patient.drug.medicinalproduct:'+drugname+'&count=patient.reaction.reactionmeddrapt.exact'
    
    json_df = requests.get(request_string).json()
    
    json_list = json_df['results']
    
    print drugname
    for x in range(0, min(15, len(json_list))):
    	entry = json_list[x]
    	print 'term: ' + str(entry['term']) + " count " + str(entry['count'])
	
    # return the results
    return json_df['results']
    
def get_event_count(event_list, event):
    try:
        index=map(itemgetter('term'), event_list).index(event)
        return event_list[index].get('count')
    except ValueError:
        return 0

drugname1='tylenol'
drugname2='ibuprofen'

druglist1=get_drug_adverse_event_data(drugname1)
druglist2=get_drug_adverse_event_data(drugname2)

event1='NAUSEA'
event2='ANXIETY'

tylenol_list=[get_event_count(druglist1, event1), get_event_count(druglist1, event2)]
ibuprofen_list=[get_event_count(druglist2, event1), get_event_count(druglist2, event2)]

print "tylenol list: Nausea, Anxiety" 
print tylenol_list
print "ibuprofen list: Nausea, Anxiety"
print ibuprofen_list

color1='blue'
color2='green'

ind=np.asarray([1,2])
width = 0.35 
fig, ax = plt.subplots()

rects1 = plt.bar(ind, tylenol_list, width, color=color1)
rects2 = plt.bar(ind+width, ibuprofen_list, width, color=color2)

ax.set_ylabel('event counts')
ax.set_title('event counts by drug')

ax.set_xticks(ind+width)
ax.set_xticklabels( (event1, event2) )

ax.legend( (rects1[0], rects2[0]), (drugname1, drugname2) )

# plt.show()
plt.savefig('fdaOpen_incubator_fig_01.png')

events=['FLUSHING', 'DYSPNOEA', 'FATIGUE', 'NAUSEA', 'PAIN', 'DIZZINESS', 'ASTHENIA', 'MYOCARDIAL INFARCTION', 'DIARRHOEA', 'PRURITUS', 'HEADACHE', 'CHEST PAIN', 'DRUG INEFFECTIVE', 'VOMITING']

#DYSPNOEA, DIZZINESS, FATIGUE, ASTHENIA, MYOCARDIAL INFARCTION, DIARRHOEA, PRURITUS, HEADACHE, CHEST PAIN, DRUG INEFFECTIVE, VOMITING, PAIN, FALL

count1=[]
count2=[]

for event in events:
    count1.append(get_event_count(druglist1, event))
    count2.append(get_event_count(druglist2, event))
    
ind=np.arange(len(count1))
                  
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(25,25))

axes[0].barh(ind, count1, color=color1)
axes[0].set_yticks(ind+.3)
axes[0].set_yticklabels(events, fontsize=20)
axes[0].set_title(drugname1, fontsize=30)

axes[1].barh(ind, count2, color=color2)
axes[1].set_yticks(ind+.3)
axes[1].set_yticklabels(events, fontsize=20)
axes[1].set_title(drugname2, fontsize=30)

plt.suptitle('Event counts for drugs', fontsize=30)

# plt.show()
plt.savefig('fdaOpen_incubator_fig_02.png')


# Discarded code

  