import json
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


data = []
main = None
window = None
flag = 0

#--------------------------------------------- Get Countries and Show Histogram ---------------------------------------------#

def get_countries():
    global data
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
    result = [countries,countries_set,countries_weights]
    show_countries_hist(result[0],result[1],result[2])
        
def show_countries_hist(countries,countries_set,countries_weights):
    plt.hist(countries_set,weights=countries_weights)
    plt.ylabel('Repeatitions')
    plt.xlabel('Countries')
    plt.title("Countries Repeatition Histogram")
    plt.show()
    

#--------------------------------------------- Get Countries and Show Histogram ---------------------------------------------#

#------------------------------------------- Get Browsers and Show Histogram Ends -------------------------------------------#

def get_browsers():
    global data
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
    result = [browsers,browsers_set,browsers_weights]
    show_browsers_hist(result[0],result[1],result[2])

def show_browsers_hist(browsers,browsers_set,browsers_weights):
    plt.hist(browsers_set,weights=browsers_weights)
    plt.ylabel('Repeatitions')
    plt.xlabel('Browsers')
    plt.title("Browsers Repeatition Histogram")
    plt.show()


#------------------------------------------- Get Browsers and Show Histogram Ends -------------------------------------------#

#-------------------------------------------Get Users Time Spent-------------------------------------------#

def user_timeSpent():
    global data
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
        maximum = max(timeSpent_dict)
        top_readers.append(maximum)
        timeSpent_dict.pop(maximum)
    top_readers=set(top_readers)
    print_data(top_readers,'Top 10 Readers','Readers ID')

#-------------------------------------------Get Users Time Spent Ends-------------------------------------------#


#-------------------------------------------Also Likes-------------------------------------------#

#'Also likes' functionality.
#for this functionality we need readers of that document.
#return all the users that have read the document.
def also_likes_doc(doc_uuid):
    global data
    readers=[]
    for log in data['logs']:
        if ("subject_doc_id" in log) and (str(log['subject_doc_id'])==doc_uuid):
            readers.append(log['visitor_uuid'])
    #remove the repeatitions.
    readers = set(readers)
    return readers
#return the whole documents that have been read by user.
def also_likes_user(user_uuid):
    global data
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

    print_data(top_ten, 'Also Likes','Document ID')


#-------------------------------------------Also Likes Ends-------------------------------------------#

#----------------------------------------------------------- GUI -----------------------------------------------------------#
# function for printing data
def print_data(data, t, c):

    root = Tk()
    root.title(t)

    
    table = ttk.Treeview(root)
    table["columns"] = ("Column 1",)
    table["show"] = "headings"

    # Add column
    table.heading("Column 1", text=c)
    table.column("Column 1", width=200,)

    # Insert data into the tree
    for item in data:
        table.insert("", "end", values=(item,))

    table.pack(side="left", fill="both", expand=True) 

def getResults(doc_id, vis_id):
    if doc_id == '' or vis_id == '':
        pass
    else:
        also_likes(doc_id, vis_id)

def setup_window(window, t, w, h):
      # this function setup the given window with given attributes like height, width and title 
      window.title(t)
      window.resizable(width=False,height=False)
      width=  w
      height= h
      window.geometry("%dx%d" % (width, height))
      screen_width = window.winfo_screenwidth()
      screen_height = window.winfo_screenheight()

      # sets the window to display middle of the screen
      x_cordinate = int((screen_width/2) - (width/2))
      y_cordinate = int((screen_height/2) - (height/2))
      window.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate))

def open_file():
    # checking if analyzer is already analyzing a file
    if flag == 1:
          # Yes: warning is shown
          messagebox.showwarning('Warning', 'A file is already open in Data Analyzer!!!')
    else:
          # No: open file and call analyzer
          file_path = filedialog.askopenfilename(initialdir="output_files", title="Select A File", filetypes=(("json files", "*.json"),("all files", "*.*")))
          if file_path:
            print(file_path)
            initiate_Analyzer(file_path)

def exit():
      global window
      window.quit()

def initiate_Analyzer(file_path):
      # fetching data before analyzer is called
      global data
      load_data(file_path)
      # calling analyzer
      run_Analyzer()
      
def run_Analyzer():
      # Data Analyzer is run here
      global main, flag
      analyzer = Tk()
      setup_window(analyzer, 'Data Analyzer',500,200)
      main = analyzer
      flag = 1
      analyzer.protocol("WM_DELETE_WINDOW", exit_analyzer)
      top_frame = Frame(analyzer)
      top_frame.grid(row=0)
      bottom_frame = Frame(analyzer)
      bottom_frame.grid(row=1)

      # View by Countries
      country_button = Button(top_frame, text="View by Countries", command=get_countries)
      # View by Browsers
      browser_button = Button(top_frame, text="View by Browsers", command=get_browsers)
      # View Top 10 Readers
      reader_button = Button(top_frame, text="Top 10 Readers", command=user_timeSpent)
      
      country_button.grid(row=0, column=0, padx=10, pady=10)
      browser_button.grid(row=0, column=1, padx=10, pady=10)
      reader_button.grid(row=0, column=2, padx=10, pady=10)

      doc = Label(bottom_frame, text='Document_ID')
      doc.grid(row=0, column=0)
      doc_id = Entry(bottom_frame)
      doc_id.grid(row=0, column=1)
      
      
      vis = Label(bottom_frame, text='Visitor_ID')
      vis.grid(row=1,column=0)
      vis_id = Entry(bottom_frame)
      vis_id.grid(row=1, column=1)

      # View Top 10 documents of Also Likes functionality
      also_like_btn = Button(bottom_frame, text='Also Likes', command=lambda: getResults(doc_id.get(), vis_id.get()))
      also_like_btn.grid(row=2, column=1)
      analyzer.mainloop()


def exit_analyzer():
     # performing on closing operations after exiting the analyzer
     global flag, main, window
     flag = 0
     main.destroy()
     main = window

def load_data(file_path):
      # loading json data in global data variable
      global data
      with open(file_path, 'r') as input_file:
            data = json.load(input_file)
      input_file.close()

# main window
window = Tk()
main = window

setup_window(window,'Data Analysis Application', 700, 500)
window.protocol("WM_DELETE_WINDOW", exit)
top = Frame(window, height=400, width=700)
top.grid(row=0)
bg_img = Image.open('bg.webp').resize((700,400))
img = ImageTk.PhotoImage(bg_img)
label = Label(top, image = img)
label.pack()
bottom = Frame(window, height=100, width=700)
bottom.grid(row=1)

title = Label(bottom, text='Data Analysis Application', font = ('Helvetica', 20, 'bold'))
title.place(x=100,y=40)

# fetch json file 
file_btn = Button(bottom,text='Open File', command=open_file)
file_btn.place(x=500,y=40)
# exit
exit_btn = Button(bottom, text='Exit', command=exit)
exit_btn.place(x=600,y=40)


window.mainloop()

#----------------------------------------------------------- GUI -----------------------------------------------------------#