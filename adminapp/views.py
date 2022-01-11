from django.shortcuts import render, redirect

import os
import pandas as pd
import matplotlib.pyplot as plt
import io
import urllib
import base64
import random
from collections import Counter
import datetime


# Create your views here.

def login(request):
    #del request.session['id']
    return render(request,"admin/login.html",{'error':''})

def login_authentication(request):
    rollno=request.POST['rollno']
    password=request.POST['password']

    if(rollno=="123456" and password=="123456"):
        #if(rollno=="18DX14" and password=="04jun03"):
        #return home(request)
        #return redirect(home)
        return redirect("/admin/")
    else:
        return render(request,"admin/login.html",{'error':'User ID and Password are not valid.'})

def home(request):
    return render(request,"admin/home.html")


def add_book(request):
    return render(request,"admin/add_book.html")

def update_book(request):
    book_id=int(request.POST['book_id'])

    df = pd.read_csv("/media/mohamedfazil/Projects/Final Year Project/library/python_files/books_with_scores.csv")

    df=df.loc[df['id'] == book_id]
    ##### CONVERT LARGE DICTIONARY TO SET OF DICTIONARIES #####
    df=df.to_dict()

    results_dict=df

    ##### CREATE LIST FOR EACH ATTRIBUTES #####
    book_id = results_dict['id']
    title = results_dict['title']
    description = results_dict['description']
    genre = results_dict['genre']
    image_link = results_dict['image_link']
    book_rating = results_dict['book_rating']
    ratings_count = results_dict['ratings_count']
    author = results_dict['author']
    author_rating = results_dict['author_rating']
    year = results_dict['year']
    edition = results_dict['edition']

    ##### SORTED AND REVERSED THE DICTIONARY INTO LIST #####
    book_id_list = list(book_id.values())
    title_list = list(title.values())
    description_list = list(description.values())
    genre_list = list(genre.values())
    image_link_list = list(image_link.values())
    book_rating_list = list(book_rating.values())
    ratings_count_list = list(ratings_count.values())
    author_list = list(author.values())
    author_rating_list = list(author_rating.values())
    year_list = list(year.values())
    edition_list = list(edition.values())

    return render(request,"admin/update_book.html",{"title":title_list[0],'description':description_list[0],'genre':genre_list[0],\
        'image_link':image_link_list[0],'book_rating':book_rating_list[0],'ratings_count':ratings_count_list[0],\
            'author':author_list[0],'author_rating':author_rating_list[0],'year':year_list[0],'edition':edition_list[0]})

def delete_book(request):
    return render(request,"admin/delete_book.html")




def showimage_bar(request):

    #####
    # BAR PLOT #
    #####

    # GET DATE TIME    
    now = datetime.datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second

    # if request.method == 'POST' and 'year' in request.POST:

    select_day=""
    select_month=""
    select_year=""

    if request.method == 'POST' and 'year' in request.POST:
        if(request.POST['year']!="0"):
            year=int(request.POST['year'])
            select_year=str(year)
        else:
            year=now.year
    else:
        year=now.year

    if request.method == 'POST' and 'month' in request.POST:
        if(request.POST['month']!="0"):
            month = int(request.POST['month'])
            months=['January','February','March','April','May','June','July','August','September','October','November','December']
            select_month = "<option value='"+str(month)+"'>"+months[month-1]+"</option>"
        else:
            month = None
    else:
        month = None


    if request.method == 'POST' and 'day' in request.POST:
        if(request.POST['day']!="0"):
            day = int(request.POST['day'])
            select_day = "<option value='"+str(day)+"'>"+str(day)+"</option>"
        else:
            day = None
    else:
        day = None


    # / GET DATE TIME

    
    df = pd.read_csv("admin_files/sales.csv")

    if(year!=None):
        if(month!=None):
            if(day!=None):
                df = df[(df['year'] == year) & (df['month'] == month ) & (df['day'] == day)]
            else:
                df = df[(df['year'] == year) & (df['month'] == month )]
        else:
            df = df[df['year'] == year]
    else:
        year=now.year



    """ 
    keywords = df['keywords'].unique()

    df = df[df["year"]==year]

    total_length=dict()

    for i in keywords:
        new_df=df[df['keywords']==i]
        total_length[i] = len(new_df)
    """

    # COUNTER 
    data = Counter(list(df['keywords']))
    data = data.most_common(10)

    # APPEND THE VALUES FROM COUNTER
    val1,val2=[],[]
    for i,j in data:
        val1.append(i)
        val2.append(j)


    colors=[]
    # RANDOM COLOR GENERATION
    for _ in range(10):
        r = random.random()
        b = random.random() 
        g = random.random()
        color = (r, g, b)
        colors.append(color)
    
    # COLOR OF PLOT
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0)


    plt.xlabel("KEYWORDS")
    plt.ylabel("CLICKS")
    plt.bar(val1, val2, color=colors)
    plt.legend()

    page="../showimage_bar/"


    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'admin/show_plots.html',{'data':uri,'page':page,'select_year':select_year,'select_month':select_month,'select_day':select_day})



def showimage_plot(request):

    #####
    # PLOT PLOT #
    #####

        # GET DATE TIME    
    now = datetime.datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second

    # if request.method == 'POST' and 'year' in request.POST:

    select_day=""
    select_month=""
    select_year=""

    if request.method == 'POST' and 'year' in request.POST:
        if(request.POST['year']!="0"):
            year=int(request.POST['year'])
            select_year=str(year)
        else:
            year=now.year
    else:
        year=now.year

    if request.method == 'POST' and 'month' in request.POST:
        if(request.POST['month']!="0"):
            month = int(request.POST['month'])
            months=['January','February','March','April','May','June','July','August','September','October','November','December']
            select_month = "<option value='"+str(month)+"'>"+months[month-1]+"</option>"
        else:
            month = None
    else:
        month = None


    if request.method == 'POST' and 'day' in request.POST:
        if(request.POST['day']!="0"):
            day = int(request.POST['day'])
            select_day = "<option value='"+str(day)+"'>"+str(day)+"</option>"
        else:
            day = None
    else:
        day = None


    # / GET DATE TIME

    
    df = pd.read_csv("admin_files/sales.csv")

    if(year!=None):
        if(month!=None):
            if(day!=None):
                df = df[(df['year'] == year) & (df['month'] == month ) & (df['day'] == day)]
            else:
                df = df[(df['year'] == year) & (df['month'] == month )]
        else:
            df = df[df['year'] == year]
    else:
        year=now.year







    # COUNTER 
    data = Counter(list(df['keywords']))
    data = data.most_common(10)

    # APPEND THE VALUES FROM COUNTER
    val1,val2=[],[]
    for i,j in data:
        val1.append(i)
        val2.append(j)

    # COLOR OF PLOT
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0)


    plt.xlabel("KEYWORDS")
    plt.ylabel("CLICKS")
    plt.plot(val1, val2 ,linestyle='--', marker='o', color='b')
    plt.legend()

    page="../showimage_plot/"


    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'admin/show_plots.html',{'data':uri,'page':page,'select_year':select_year,'select_month':select_month,'select_day':select_day})




def showimage_pie(request):

    #####
    # PIE PLOT #
    #####



        # GET DATE TIME    
    now = datetime.datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second

    # if request.method == 'POST' and 'year' in request.POST:

    select_day=""
    select_month=""
    select_year=""

    if request.method == 'POST' and 'year' in request.POST:
        if(request.POST['year']!="0"):
            year=int(request.POST['year'])
            select_year=str(year)
        else:
            year=now.year
    else:
        year=now.year

    if request.method == 'POST' and 'month' in request.POST:
        if(request.POST['month']!="0"):
            month = int(request.POST['month'])
            months=['January','February','March','April','May','June','July','August','September','October','November','December']
            select_month = "<option value='"+str(month)+"'>"+months[month-1]+"</option>"
        else:
            month = None
    else:
        month = None


    if request.method == 'POST' and 'day' in request.POST:
        if(request.POST['day']!="0"):
            day = int(request.POST['day'])
            select_day = "<option value='"+str(day)+"'>"+str(day)+"</option>"
        else:
            day = None
    else:
        day = None


    # / GET DATE TIME

    
    df = pd.read_csv("admin_files/sales.csv")

    if(year!=None):
        if(month!=None):
            if(day!=None):
                df = df[(df['year'] == year) & (df['month'] == month ) & (df['day'] == day)]
            else:
                df = df[(df['year'] == year) & (df['month'] == month )]
        else:
            df = df[df['year'] == year]
    else:
        year=now.year



    # COUNTER 
    data = Counter(list(df['keywords']))
    data = data.most_common(10)

    # APPEND THE VALUES FROM COUNTER
    val1,val2=[],[]
    for i,j in data:
        val1.append(i)
        val2.append(j)


    colors=[]
    # RANDOM COLOR GENERATION
    for _ in range(len(val1)):
        r = random.random()
        b = random.random() 
        g = random.random()
        color = (r, g, b)
        colors.append(color)

    myexplode=[0.05]
    for _ in range(len(val1)-1):
        myexplode.append(0)

    # COLOR OF PLOT
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0)

    if(len(val1)>0):
        plt.pie(val2, labels=val1,autopct='%1.1f%%', explode=myexplode, shadow=True)
    else:
        plt.pie(val2, labels=val1)


    plt.legend()

    page="../showimage_pie/"
        

    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'admin/show_plots.html',{'data':uri,'page':page,'select_year':select_year,'select_month':select_month,'select_day':select_day})



def showimage_scatter(request):

    #####
    # PIE PLOT #
    #####



        # GET DATE TIME    
    now = datetime.datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second

    # if request.method == 'POST' and 'year' in request.POST:

    select_day=""
    select_month=""
    select_year=""

    if request.method == 'POST' and 'year' in request.POST:
        if(request.POST['year']!="0"):
            year=int(request.POST['year'])
            select_year=str(year)
        else:
            year=now.year
    else:
        year=now.year

    if request.method == 'POST' and 'month' in request.POST:
        if(request.POST['month']!="0"):
            month = int(request.POST['month'])
            months=['January','February','March','April','May','June','July','August','September','October','November','December']
            select_month = "<option value='"+str(month)+"'>"+months[month-1]+"</option>"
        else:
            month = None
    else:
        month = None


    if request.method == 'POST' and 'day' in request.POST:
        if(request.POST['day']!="0"):
            day = int(request.POST['day'])
            select_day = "<option value='"+str(day)+"'>"+str(day)+"</option>"
        else:
            day = None
    else:
        day = None


    # / GET DATE TIME

    
    df = pd.read_csv("admin_files/sales.csv")

    if(year!=None):
        if(month!=None):
            if(day!=None):
                df = df[(df['year'] == year) & (df['month'] == month ) & (df['day'] == day)]
            else:
                df = df[(df['year'] == year) & (df['month'] == month )]
        else:
            df = df[df['year'] == year]
    else:
        year=now.year



    # COUNTER 
    data = Counter(list(df['keywords']))
    data = data.most_common(10)

    # APPEND THE VALUES FROM COUNTER
    val1,val2=[],[]
    for i,j in data:
        val1.append(i)
        val2.append(j)


    colors=[]
    # RANDOM COLOR GENERATION
    for _ in range(len(val1)):
        r = random.random()
        b = random.random() 
        g = random.random()
        color = (r, g, b)
        colors.append(color)

    myexplode=[0.05]
    for _ in range(len(val1)-1):
        myexplode.append(0)

    # COLOR OF PLOT
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0)

    plt.scatter(val1, val2)


    plt.legend()

    page="../showimage_scatter/"
        

    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'admin/show_plots.html',{'data':uri,'page':page,'select_year':select_year,'select_month':select_month,'select_day':select_day})








##################
##################
##################
##################
##################
##################
# FOR IMPRESSIONS
##################
##################
##################
##################
##################
##################
##################

impressions_csv="admin_files/impressions.csv"

def showimage_bar_impressions(request):

    #####
    # BAR PLOT #
    #####

    # GET DATE TIME    
    now = datetime.datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second

    # if request.method == 'POST' and 'year' in request.POST:

    select_day=""
    select_month=""
    select_year=""

    if request.method == 'POST' and 'year' in request.POST:
        if(request.POST['year']!="0"):
            year=int(request.POST['year'])
            select_year=str(year)
        else:
            year=now.year
    else:
        year=now.year

    if request.method == 'POST' and 'month' in request.POST:
        if(request.POST['month']!="0"):
            month = int(request.POST['month'])
            months=['January','February','March','April','May','June','July','August','September','October','November','December']
            select_month = "<option value='"+str(month)+"'>"+months[month-1]+"</option>"
        else:
            month = None
    else:
        month = None


    if request.method == 'POST' and 'day' in request.POST:
        if(request.POST['day']!="0"):
            day = int(request.POST['day'])
            select_day = "<option value='"+str(day)+"'>"+str(day)+"</option>"
        else:
            day = None
    else:
        day = None


    # / GET DATE TIME

    
    df = pd.read_csv(impressions_csv)

    if(year!=None):
        if(month!=None):
            if(day!=None):
                df = df[(df['year'] == year) & (df['month'] == month ) & (df['day'] == day)]
            else:
                df = df[(df['year'] == year) & (df['month'] == month )]
        else:
            df = df[df['year'] == year]
    else:
        year=now.year



    """ 
    keywords = df['keywords'].unique()

    df = df[df["year"]==year]

    total_length=dict()

    for i in keywords:
        new_df=df[df['keywords']==i]
        total_length[i] = len(new_df)
    """

    # COUNTER 
    data = Counter(list(df['book_id']))
    data = data.most_common(10)

    # APPEND THE VALUES FROM COUNTER
    val1,val2=[],[]
    for i,j in data:
        val1.append(i)
        val2.append(j)


    colors=[]
    # RANDOM COLOR GENERATION
    for _ in range(10):
        r = random.random()
        b = random.random() 
        g = random.random()
        color = (r, g, b)
        colors.append(color)
    
    # COLOR OF PLOT
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0)


    plt.xlabel("BOOK ID")
    plt.ylabel("CLICKS")
    plt.bar(val1, val2, color=colors)
    plt.legend()

    page="../showimage_bar_impressions/"


    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'admin/show_plots_impressions.html',{'data':uri,'page':page,'select_year':select_year,'select_month':select_month,'select_day':select_day})



def showimage_plot_impressions(request):

    #####
    # PLOT PLOT #
    #####

        # GET DATE TIME    
    now = datetime.datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second

    # if request.method == 'POST' and 'year' in request.POST:

    select_day=""
    select_month=""
    select_year=""

    if request.method == 'POST' and 'year' in request.POST:
        if(request.POST['year']!="0"):
            year=int(request.POST['year'])
            select_year=str(year)
        else:
            year=now.year
    else:
        year=now.year

    if request.method == 'POST' and 'month' in request.POST:
        if(request.POST['month']!="0"):
            month = int(request.POST['month'])
            months=['January','February','March','April','May','June','July','August','September','October','November','December']
            select_month = "<option value='"+str(month)+"'>"+months[month-1]+"</option>"
        else:
            month = None
    else:
        month = None


    if request.method == 'POST' and 'day' in request.POST:
        if(request.POST['day']!="0"):
            day = int(request.POST['day'])
            select_day = "<option value='"+str(day)+"'>"+str(day)+"</option>"
        else:
            day = None
    else:
        day = None


    # / GET DATE TIME

    
    df = pd.read_csv(impressions_csv)

    if(year!=None):
        if(month!=None):
            if(day!=None):
                df = df[(df['year'] == year) & (df['month'] == month ) & (df['day'] == day)]
            else:
                df = df[(df['year'] == year) & (df['month'] == month )]
        else:
            df = df[df['year'] == year]
    else:
        year=now.year







    # COUNTER 
    data = Counter(list(df['book_id']))
    data = data.most_common(10)

    # APPEND THE VALUES FROM COUNTER
    val1,val2=[],[]
    for i,j in data:
        val1.append(i)
        val2.append(j)

    # COLOR OF PLOT
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0)


    plt.xlabel("BOOK ID")
    plt.ylabel("CLICKS")
    plt.plot(val1, val2 ,linestyle='--', marker='o', color='b')
    plt.legend()

    page="../showimage_plot_impressions/"


    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'admin/show_plots_impressions.html',{'data':uri,'page':page,'select_year':select_year,'select_month':select_month,'select_day':select_day})




def showimage_pie_impressions(request):

    #####
    # PIE PLOT #
    #####



        # GET DATE TIME    
    now = datetime.datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second

    # if request.method == 'POST' and 'year' in request.POST:

    select_day=""
    select_month=""
    select_year=""

    if request.method == 'POST' and 'year' in request.POST:
        if(request.POST['year']!="0"):
            year=int(request.POST['year'])
            select_year=str(year)
        else:
            year=now.year
    else:
        year=now.year

    if request.method == 'POST' and 'month' in request.POST:
        if(request.POST['month']!="0"):
            month = int(request.POST['month'])
            months=['January','February','March','April','May','June','July','August','September','October','November','December']
            select_month = "<option value='"+str(month)+"'>"+months[month-1]+"</option>"
        else:
            month = None
    else:
        month = None


    if request.method == 'POST' and 'day' in request.POST:
        if(request.POST['day']!="0"):
            day = int(request.POST['day'])
            select_day = "<option value='"+str(day)+"'>"+str(day)+"</option>"
        else:
            day = None
    else:
        day = None


    # / GET DATE TIME

    
    df = pd.read_csv(impressions_csv)

    if(year!=None):
        if(month!=None):
            if(day!=None):
                df = df[(df['year'] == year) & (df['month'] == month ) & (df['day'] == day)]
            else:
                df = df[(df['year'] == year) & (df['month'] == month )]
        else:
            df = df[df['year'] == year]
    else:
        year=now.year



    # COUNTER 
    data = Counter(list(df['book_id']))
    data = data.most_common(10)

    # APPEND THE VALUES FROM COUNTER
    val1,val2=[],[]
    for i,j in data:
        val1.append(i)
        val2.append(j)


    colors=[]
    # RANDOM COLOR GENERATION
    for _ in range(len(val1)):
        r = random.random()
        b = random.random() 
        g = random.random()
        color = (r, g, b)
        colors.append(color)

    myexplode=[0.05]
    for _ in range(len(val1)-1):
        myexplode.append(0)

    # COLOR OF PLOT
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0)

    if(len(val1)>0):
        plt.pie(val2, labels=val1,autopct='%1.1f%%', explode=myexplode, shadow=True)
    else:
        plt.pie(val2, labels=val1)


    plt.legend()

    page="../showimage_pie_impressions/"
        

    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'admin/show_plots_impressions.html',{'data':uri,'page':page,'select_year':select_year,'select_month':select_month,'select_day':select_day})



def showimage_scatter_impressions(request):

    #####
    # PIE PLOT #
    #####



        # GET DATE TIME    
    now = datetime.datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second

    # if request.method == 'POST' and 'year' in request.POST:

    select_day=""
    select_month=""
    select_year=""

    if request.method == 'POST' and 'year' in request.POST:
        if(request.POST['year']!="0"):
            year=int(request.POST['year'])
            select_year=str(year)
        else:
            year=now.year
    else:
        year=now.year

    if request.method == 'POST' and 'month' in request.POST:
        if(request.POST['month']!="0"):
            month = int(request.POST['month'])
            months=['January','February','March','April','May','June','July','August','September','October','November','December']
            select_month = "<option value='"+str(month)+"'>"+months[month-1]+"</option>"
        else:
            month = None
    else:
        month = None


    if request.method == 'POST' and 'day' in request.POST:
        if(request.POST['day']!="0"):
            day = int(request.POST['day'])
            select_day = "<option value='"+str(day)+"'>"+str(day)+"</option>"
        else:
            day = None
    else:
        day = None


    # / GET DATE TIME

    
    df = pd.read_csv(impressions_csv)

    if(year!=None):
        if(month!=None):
            if(day!=None):
                df = df[(df['year'] == year) & (df['month'] == month ) & (df['day'] == day)]
            else:
                df = df[(df['year'] == year) & (df['month'] == month )]
        else:
            df = df[df['year'] == year]
    else:
        year=now.year



    # COUNTER 
    data = Counter(list(df['book_id']))
    data = data.most_common(10)

    # APPEND THE VALUES FROM COUNTER
    val1,val2=[],[]
    for i,j in data:
        val1.append(i)
        val2.append(j)


    colors=[]
    # RANDOM COLOR GENERATION
    for _ in range(len(val1)):
        r = random.random()
        b = random.random() 
        g = random.random()
        color = (r, g, b)
        colors.append(color)

    myexplode=[0.05]
    for _ in range(len(val1)-1):
        myexplode.append(0)

    # COLOR OF PLOT
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0)

    plt.scatter(val1, val2)


    plt.legend()

    page="../showimage_scatter_impressions/"
        

    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'admin/show_plots_impressions.html',{'data':uri,'page':page,'select_year':select_year,'select_month':select_month,'select_day':select_day})









##################
##################
##################
##################
##################
##################
# FOR CLICKS
##################
##################
##################
##################
##################
##################
##################

clicks_csv="admin_files/clicks.csv"

def showimage_bar_clicks(request):

    #####
    # BAR PLOT #
    #####

    # GET DATE TIME    
    now = datetime.datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second

    # if request.method == 'POST' and 'year' in request.POST:

    select_day=""
    select_month=""
    select_year=""

    if request.method == 'POST' and 'year' in request.POST:
        if(request.POST['year']!="0"):
            year=int(request.POST['year'])
            select_year=str(year)
        else:
            year=now.year
    else:
        year=now.year

    if request.method == 'POST' and 'month' in request.POST:
        if(request.POST['month']!="0"):
            month = int(request.POST['month'])
            months=['January','February','March','April','May','June','July','August','September','October','November','December']
            select_month = "<option value='"+str(month)+"'>"+months[month-1]+"</option>"
        else:
            month = None
    else:
        month = None


    if request.method == 'POST' and 'day' in request.POST:
        if(request.POST['day']!="0"):
            day = int(request.POST['day'])
            select_day = "<option value='"+str(day)+"'>"+str(day)+"</option>"
        else:
            day = None
    else:
        day = None


    # / GET DATE TIME

    
    df = pd.read_csv(clicks_csv)

    if(year!=None):
        if(month!=None):
            if(day!=None):
                df = df[(df['year'] == year) & (df['month'] == month ) & (df['day'] == day)]
            else:
                df = df[(df['year'] == year) & (df['month'] == month )]
        else:
            df = df[df['year'] == year]
    else:
        year=now.year



    """ 
    keywords = df['keywords'].unique()

    df = df[df["year"]==year]

    total_length=dict()

    for i in keywords:
        new_df=df[df['keywords']==i]
        total_length[i] = len(new_df)
    """

    # COUNTER 
    data = Counter(list(df['book_id']))
    data = data.most_common(10)

    # APPEND THE VALUES FROM COUNTER
    val1,val2=[],[]
    for i,j in data:
        val1.append(i)
        val2.append(j)


    colors=[]
    # RANDOM COLOR GENERATION
    for _ in range(10):
        r = random.random()
        b = random.random() 
        g = random.random()
        color = (r, g, b)
        colors.append(color)
    
    # COLOR OF PLOT
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0)


    plt.xlabel("BOOK ID")
    plt.ylabel("CLICKS")
    plt.bar(val1, val2, color=colors)
    plt.legend()

    page="../showimage_bar_clicks/"


    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'admin/show_plots_clicks.html',{'data':uri,'page':page,'select_year':select_year,'select_month':select_month,'select_day':select_day})



def showimage_plot_clicks(request):

    #####
    # PLOT PLOT #
    #####

        # GET DATE TIME    
    now = datetime.datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second

    # if request.method == 'POST' and 'year' in request.POST:

    select_day=""
    select_month=""
    select_year=""

    if request.method == 'POST' and 'year' in request.POST:
        if(request.POST['year']!="0"):
            year=int(request.POST['year'])
            select_year=str(year)
        else:
            year=now.year
    else:
        year=now.year

    if request.method == 'POST' and 'month' in request.POST:
        if(request.POST['month']!="0"):
            month = int(request.POST['month'])
            months=['January','February','March','April','May','June','July','August','September','October','November','December']
            select_month = "<option value='"+str(month)+"'>"+months[month-1]+"</option>"
        else:
            month = None
    else:
        month = None


    if request.method == 'POST' and 'day' in request.POST:
        if(request.POST['day']!="0"):
            day = int(request.POST['day'])
            select_day = "<option value='"+str(day)+"'>"+str(day)+"</option>"
        else:
            day = None
    else:
        day = None


    # / GET DATE TIME

    
    df = pd.read_csv(clicks_csv)

    if(year!=None):
        if(month!=None):
            if(day!=None):
                df = df[(df['year'] == year) & (df['month'] == month ) & (df['day'] == day)]
            else:
                df = df[(df['year'] == year) & (df['month'] == month )]
        else:
            df = df[df['year'] == year]
    else:
        year=now.year







    # COUNTER 
    data = Counter(list(df['book_id']))
    data = data.most_common(10)

    # APPEND THE VALUES FROM COUNTER
    val1,val2=[],[]
    for i,j in data:
        val1.append(i)
        val2.append(j)

    # COLOR OF PLOT
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0)


    plt.xlabel("BOOK ID")
    plt.ylabel("CLICKS")
    plt.plot(val1, val2 ,linestyle='--', marker='o', color='b')
    plt.legend()

    page="../showimage_plot_clicks/"


    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'admin/show_plots_clicks.html',{'data':uri,'page':page,'select_year':select_year,'select_month':select_month,'select_day':select_day})




def showimage_pie_clicks(request):

    #####
    # PIE PLOT #
    #####



        # GET DATE TIME    
    now = datetime.datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second

    # if request.method == 'POST' and 'year' in request.POST:

    select_day=""
    select_month=""
    select_year=""

    if request.method == 'POST' and 'year' in request.POST:
        if(request.POST['year']!="0"):
            year=int(request.POST['year'])
            select_year=str(year)
        else:
            year=now.year
    else:
        year=now.year

    if request.method == 'POST' and 'month' in request.POST:
        if(request.POST['month']!="0"):
            month = int(request.POST['month'])
            months=['January','February','March','April','May','June','July','August','September','October','November','December']
            select_month = "<option value='"+str(month)+"'>"+months[month-1]+"</option>"
        else:
            month = None
    else:
        month = None


    if request.method == 'POST' and 'day' in request.POST:
        if(request.POST['day']!="0"):
            day = int(request.POST['day'])
            select_day = "<option value='"+str(day)+"'>"+str(day)+"</option>"
        else:
            day = None
    else:
        day = None


    # / GET DATE TIME

    
    df = pd.read_csv(clicks_csv)

    if(year!=None):
        if(month!=None):
            if(day!=None):
                df = df[(df['year'] == year) & (df['month'] == month ) & (df['day'] == day)]
            else:
                df = df[(df['year'] == year) & (df['month'] == month )]
        else:
            df = df[df['year'] == year]
    else:
        year=now.year



    # COUNTER 
    data = Counter(list(df['book_id']))
    data = data.most_common(10)

    # APPEND THE VALUES FROM COUNTER
    val1,val2=[],[]
    for i,j in data:
        val1.append(i)
        val2.append(j)


    colors=[]
    # RANDOM COLOR GENERATION
    for _ in range(len(val1)):
        r = random.random()
        b = random.random() 
        g = random.random()
        color = (r, g, b)
        colors.append(color)

    myexplode=[0.05]
    for _ in range(len(val1)-1):
        myexplode.append(0)

    # COLOR OF PLOT
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0)

    if(len(val1)>0):
        plt.pie(val2, labels=val1,autopct='%1.1f%%', explode=myexplode, shadow=True)
    else:
        plt.pie(val2, labels=val1)


    plt.legend()

    page="../showimage_pie_clicks/"
        

    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'admin/show_plots_clicks.html',{'data':uri,'page':page,'select_year':select_year,'select_month':select_month,'select_day':select_day})



def showimage_scatter_clicks(request):

    #####
    # PIE PLOT #
    #####



        # GET DATE TIME    
    now = datetime.datetime.now()
    # now.year, now.month, now.day, now.hour, now.minute, now.second

    # if request.method == 'POST' and 'year' in request.POST:

    select_day=""
    select_month=""
    select_year=""

    if request.method == 'POST' and 'year' in request.POST:
        if(request.POST['year']!="0"):
            year=int(request.POST['year'])
            select_year=str(year)
        else:
            year=now.year
    else:
        year=now.year

    if request.method == 'POST' and 'month' in request.POST:
        if(request.POST['month']!="0"):
            month = int(request.POST['month'])
            months=['January','February','March','April','May','June','July','August','September','October','November','December']
            select_month = "<option value='"+str(month)+"'>"+months[month-1]+"</option>"
        else:
            month = None
    else:
        month = None


    if request.method == 'POST' and 'day' in request.POST:
        if(request.POST['day']!="0"):
            day = int(request.POST['day'])
            select_day = "<option value='"+str(day)+"'>"+str(day)+"</option>"
        else:
            day = None
    else:
        day = None


    # / GET DATE TIME

    
    df = pd.read_csv(clicks_csv)

    if(year!=None):
        if(month!=None):
            if(day!=None):
                df = df[(df['year'] == year) & (df['month'] == month ) & (df['day'] == day)]
            else:
                df = df[(df['year'] == year) & (df['month'] == month )]
        else:
            df = df[df['year'] == year]
    else:
        year=now.year



    # COUNTER 
    data = Counter(list(df['book_id']))
    data = data.most_common(10)

    # APPEND THE VALUES FROM COUNTER
    val1,val2=[],[]
    for i,j in data:
        val1.append(i)
        val2.append(j)


    colors=[]
    # RANDOM COLOR GENERATION
    for _ in range(len(val1)):
        r = random.random()
        b = random.random() 
        g = random.random()
        color = (r, g, b)
        colors.append(color)

    myexplode=[0.05]
    for _ in range(len(val1)-1):
        myexplode.append(0)

    # COLOR OF PLOT
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.0)

    plt.scatter(val1, val2)


    plt.legend()

    page="../showimage_scatter_clicks/"
        

    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'admin/show_plots_clicks.html',{'data':uri,'page':page,'select_year':select_year,'select_month':select_month,'select_day':select_day})
