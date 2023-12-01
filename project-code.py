import json

#open the json file.
f = open('sample_small.json')
#read the data.
data=json.load(f)
#now 'data' variable contains the json file. we access attributes of each log like this:
for log in data['logs']:
    print(log['visitor_country'])
#now countires of each visitor as being shown in console.