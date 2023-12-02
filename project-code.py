import json
#to create graphs/histograms we use matplotlib.
import matplotlib.pyplot as plt
import numpy as np

#open the json file.
f = open('sample_small.json')
#read the data.
data=json.load(f)

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
plt.hist(countries_set,weights=countries_weights)
plt.ylabel('Repeatitions')
plt.xlabel('Countries')
plt.title("Countries Repeatition Histogram")
plt.show()

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


