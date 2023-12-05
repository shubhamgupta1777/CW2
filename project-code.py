import json
import matplotlib.pyplot as plt
import numpy as np
import os


#-------------------------------------------Read File-------------------------------------------#
def json_format(path):
    import linecache as l
    # Input file path
    input_file_path = 'sample_small.json'

    # Output directory
    output_directory = 'output_files/'

    # Create the output directory if it doesn't exist

    os.makedirs(output_directory, exist_ok=True)

    # Initialize variables
    line_count = 1
    output_file = open(f'output_file.json', 'w')
    # Read input file and write to different files
    with open(input_file_path, 'r') as input_file:
        #clear the output file first.
        output_file.truncate()
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

#-------------------------------------------Read File Ends-------------------------------------------#


#-------------------------------------------Get Countries and Show Histogram-------------------------------------------#
def get_countries(data):
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
    countries_weights = []
    #to create histograms we need to export the values from dictionary and give them to hist().
    for item in countries_set:
        countries_weights.append(countries.count(item))
    data = [countries,countries_set,countries_weights]
    return data
        
def show_countries_hist(countries,countries_set,countries_weights):
    #plt.hist(countries_set,weights=countries_weights)
    #plt.ylabel('Repeatitions')
    #plt.xlabel('Countries')
    #plt.title("Countries Repeatition Histogram")
    #plt.show()
    print()



#-------------------------------------------Get Countries and Show Histogram-------------------------------------------#


#-------------------------------------------Get Browsers and Show Histogram-------------------------------------------#

def get_browsers():
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
    browsers_weights = []
    #set the histogram
    for item in browsers_set:
        browsers_weights.append(browsers.count(item))
    data = [browsers,browsers_set,browsers_weights]
    return data

def show_browsers_hist(browsers,browsers_set,browsers_weights):
    #plt.hist(browsers_set,weights=browsers_weights)
    #plt.ylabel('Repeatitions')
    #plt.xlabel('Browsers')
    #plt.title("Browsers Repeatition Histogram")
    #plt.show()
    print()


#-------------------------------------------Get Browsers and Show Histogram Ends-------------------------------------------#


#-------------------------------------------Get Users Time Spent-------------------------------------------#

def user_timeSpent():
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
    for _ in range(10):
        #finding max value's key
        maximum = max(timeSpent_dict)
        #add it to our list
        top_readers.append(max)
        #change the value to -1 to prevent selecting this key for next iterations
        timeSpent_dict[maximum]=-1
    return top_readers

#-------------------------------------------Get Users Time Spent Ends-------------------------------------------#


#-------------------------------------------Also Likes-------------------------------------------#

#'Also likes' functionality.
#for this functionality we need readers of that document.
#return all the users that have read the document.
def also_likes_doc(doc_uuid):
    readers=[]
    for log in data['logs']:
        if ("subject_doc_id" in log) and (str(log['subject_doc_id'])==doc_uuid):
            readers.append(log['visitor_uuid'])
    #remove the repeatitions.
    readers = set(readers)
    return readers
#return the whole documents that have been read by user.
def also_likes_user(user_uuid):
    docs = []
    for log in data['logs']:
        if "subject_doc_id" in log and (str(log['visitor_uuid'])==user_uuid):
            docs.append(log['subject_doc_id'])
    return docs
#now the 'also likes' function
def also_likes(doc_uuid,user_uuid):
    people = also_likes_doc(doc_uuid)
    docs = []
    for person in people:
        user_docs = also_likes_user(person)
        for item in user_docs:
            if item!=doc_uuid:
                docs.append(item)        
    repetitons = {}
    for item in docs:
        repetitons[item]=docs.count(item)

    
    top_ten=[]
    for _ in range(10):
        maximum = max(repetitons)
        top_ten.append(maximum)
        repetitons.pop(maximum)
    return top_ten

#-------------------------------------------Also Likes Ends-------------------------------------------#

#using the function to convert data to correct format.
json_format('sample_small.json')
file = open('output_file.json')
data = json.load(file)

data = get_countries(data)
show_countries_hist(data[0],data[1],data[2])