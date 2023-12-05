import json
import matplotlib.pyplot as plt
import numpy as np
import os


def json_format(path):
    import linecache as l
    # Input file path
    input_file_path = 'sample_tiny.json'

    # Output directory
    output_directory = 'output_files/'

    # Create the output directory if it doesn't exist

    os.makedirs(output_directory, exist_ok=True)

    # Initialize variables
    line_count = 1
    output_file = open(f'output_file.json', 'w')
    # Read input file and write to different files
    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()
        output_file.write('{"logs":[\n')
        l = ''
        for i,line in enumerate(lines):
            l = line 
            if i != len(lines)-1:
                if '}' in line: 
                    output_file.write(l.replace('}',"},"))
            else:
                output_file.write(l.replace('}',"}\n]}"))
            line_count += 1
    output_file.close()
    return output_file

#using the function to convert data to correct format.
json_format('sample_tiny.json')
file = open('output_file.json')
data = json.load(file)

#get the list of countries.
countries = []
for log in data['logs']:
    countries.append(log['visitor_country'])

#to realise how many unique countries are there we convert the list to a set to remove repeatition.
countries_set = set(countries)

#get number of countries.
#for giving the number of each country to it we need a dictionary.
#first element of this dictionary is the name of country and the second one is the number of repeatitions.
countries_dict = {}
for item in countries_set:
    countries_dict[item]=countries.count(item)

#to create histograms we need to export the values from dictionary and give them to hist().
countries_weights=[]
for item in countries_set:
    countries_weights.append(countries.count(item))
#plt.hist(countries_set,weights=countries_weights)
#plt.ylabel('Repeatitions')
#plt.xlabel('Countries')
#plt.title("Countries Repeatition Histogram")
#plt.show()

#get the browsers and identify the most popular ones.
browsers=[]
for log in data['logs']:
    browsers.append(log['visitor_useragent'])
#change the whole line to the browser name only. apparently all the browser names are followed by a '/' character.
#let's slice our strings!
for item in browsers:
    item = str(item)
    point = item.find('/')
    #slice the string to the '/' index.
    slice = item[:point:]
    browsers = list(map(lambda x: x.replace(item,slice),browsers))

#create a histogram for the browsers.
browsers_set = set(browsers)
browsers_dict = {}
for item in browsers_set:
    browsers_dict[item] = browsers.count(item)
browsers_histogram = []
for item in browsers_dict:
    browsers_histogram.append(browsers_dict[item])
#set the histogram
browsers_weights = []
for item in browsers_set:
    browsers_weights.append(browsers.count(item))
#plt.hist(browsers_set,weights=browsers_weights)
#plt.ylabel('Repeatitions')
#plt.xlabel('Browsers')
#plt.title("Browsers Repeatition Histogram")
#plt.show()

#readers time spent.
#first I will add the users in a set.
users_set = []
for log in data['logs']:
    users_set.append(log['visitor_uuid'])
users_set=set(users_set)
#now that we have list of users we have to calculate reading time spent for each user.
#need a dictionary to specify time spent for each user.
timeSpent_dict={}
for user in users_set:
    #create a 'time_spent' variable to store the sum of time spent.
    time_spent=0
    for log in data['logs']:
        #check for user event type and uuid to sum up the reading time.
        if(log['visitor_uuid']==user) and log['event_type']=="pagereadtime":
            time_spent+=log['event_readtime']
    #if user has spent time on reading.
    if time_spent!=0:
        timeSpent_dict[user]=time_spent
#now that we have the dictionary, let's find the top 10 readers!
top_readers=[]
i = 0
for t in timeSpent_dict:
    #making sure max number won't pass 10
    if i<10:
        #finding max value's key
        maximum = max(timeSpent_dict)
        #add it to our list
        top_readers.append(max)
        #change the value to -1 to prevent selecting this key for next iterations
        timeSpent_dict[maximum]=-1
        i+=1
    else:
        #if it passed we just break.
        break

#'Also likes' functionality.
#for this functionality we need readers of that document.
#return all the users that have read the document.
def also_likes_doc(doc_uuid):
    readers=[]
    for log in data['logs']:
        if log['env_doc_id']==doc_uuid:
            readers.append(log['visitor_uuid'])
    #remove the repeatitions.
    set(readers)
    return readers
#return the whole documents that have been read by user.
def also_likes_user(user_uuid):
    docs = []
    for log in data['logs']:
        if log['visitor_uuid']==user_uuid:
            docs.append(log['evn_doc_id'])
    set(docs)
    return docs
#now the 'also likes' function
def also_likes(doc_uuid,user_uuid):
    #TODO - need the also likes function 5-C completed.
    print("TODO - need the also likes function 5-C completed.")
    
