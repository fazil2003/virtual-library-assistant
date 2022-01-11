from django.shortcuts import render,redirect
from django.http import HttpResponse

import pandas as pd

import base64

# Create your views here.
def home(request):

    ##### GET USERNAME FROM ID #####
    if 'id' not in request.session:
        return redirect('/login')
    else:
        df=pd.read_csv("/media/mohamedfazil/Projects/Final Year Project/library/python_files/users.csv")
        df=df.query('id == '+str(request.session['id'])+'') 
        if((df['name'].count())>0):
            username=df['name'].item()
    ################################

    df=pd.read_csv('python_files/books_with_scores.csv')

    sample_df = df.sample(n=16).index

    books_as_string=""

    for i in sample_df:


        # MOSTLY TAKEN LIST
        location_sales="/media/mohamedfazil/Projects/Final Year Project/library/python_files/users_clicks.csv"
        df_mt=pd.read_csv(location_sales)
        most_taken_by=""
        df_mt = df_mt[(df_mt['book_id']==df['id'][i])]
        if not df_mt.empty:
            most_taken_by=df_mt['department'].value_counts().idxmax()
        else:
            most_taken_by=""


        books_as_string+="""
        <a href="http://127.0.0.1:8000/details/?id={0}">

        <div class='content'>
            <div class='top'>
                <img src="{1}" />
            </div>
            <div class='middle'>
                <div class='title'>{2}</div>
                <p class='description'>
                    <span class='author'><i class='fa fa-user-o'> </i> {3}</span><br>
                    {4}
                </p>
            </div>
            <div class='bottom'>
                    <b><i class='fa fa-star'> </i> {5:.2f} % - <span>{6}</span></b>
            </div>
        </div>

        </a>
        """.format( df['id'][i], df['image_link'][i], df['title'][i], df['author'][i], df['description'][i], df['score'][i], most_taken_by )

    return render(request,"home.html",{'username':username,'books_as_string':books_as_string})

def login_guest(request):
    request.session['id']=1
    return redirect("/")

def login(request):
    #del request.session['id']
    return render(request,"login.html",{'error':''})

def login_authentication(request):
    rollno=request.POST['rollno']
    password=request.POST['password']

    rollno=rollno.lower()

    df=pd.read_csv("/media/mohamedfazil/Projects/Final Year Project/library/python_files/users.csv")
    df=df.query('rollno == "'+rollno+'" and password =="'+password+'"') 


    if((df['id'].count())>0):
        #if(rollno=="18DX14" and password=="04jun03"):
        #return home(request)
        #return redirect(home)
        request.session['id']=df['id'].item()
        return redirect("/")
    else:
        return render(request,"login.html",{'error':'Roll No and Password are not valid.'})

def logout(request):
    del request.session['id']
    return redirect('/login')

def profile(request):
    ##### GET USERNAME FROM ID #####
    if 'id' not in request.session:
        return redirect('/login')
    else:
        df=pd.read_csv("/media/mohamedfazil/Projects/Final Year Project/library/python_files/users.csv")
        df=df.query('id == '+str(request.session['id'])+'') 
        if((df['name'].count())>0):
            username=df['name'].item()
            rollno=df['rollno'].item().upper()
    ################################
    
    return render(request,"profile.html",{'username':username,'rollno':rollno})

def search(request):
    df=pd.read_csv('python_files/books_with_scores.csv')
    li=df['title']
    return render(request,"search.html",{'li':li})

def results(request):

    searchQuery_sales=request.GET['searchQuery']
    location_sales="/media/mohamedfazil/Projects/Final Year Project/library/admin_files/sales.csv"
    import datetime
    now = datetime.datetime.now()
    year=now.year
    month=now.month
    day=now.day
    # df_sales=pd.read_csv(location_sales)
    searchQuery_list=searchQuery_sales.split(" ")
    for i in searchQuery_list:
        with open(location_sales,"a") as f:
            text_to_write="1,1,"+str(year)+","+str(month)+","+str(day)+","+str(i)+"\n"
            f.write(text_to_write)



        

    ##### IMPORT FOR PYTORCH SEARCH #####
    from python_files.search_engine.main import search_using_pytorch

    searchQuery=request.GET['searchQuery']

    ##### SPELL CHECKER #####
    from python_files.spellchecker.spell_checker_using_textblob import spell_check
    spell_check_result=spell_check(searchQuery)
    if(spell_check_result.strip()==searchQuery.strip()):
        spell_check_result=""
        
    #########################

    check_for_errors=''.join(e for e in searchQuery if e.isalnum())
    if(check_for_errors==""):
        return render(request,"error_page.html")

    searchQuery=searchQuery.replace("(","")
    searchQuery=searchQuery.replace(")","")

    df=pd.read_csv('python_files/books_with_scores.csv')
    df['content']=df['title'].str.lower()+' '+df['description'].str.lower()+' '+df['genre'].str.lower()+' '+df['author'].str.lower()
    searchQuery_lower=searchQuery.lower()
    filters=df['content'].str.contains(searchQuery_lower,na=False)
    list_of_columns=['id','title','description','genre','image_link','book_rating','ratings_count','author','author_rating','year','edition','impressions','clicks','score']
    #results=df.loc[filters,['id','title','content','score','genre']]
    results=df.loc[filters,list_of_columns]

    results=results.sort_values(by='score')




    

    ##########################################################
    #                     NORMAL SEARCH                      #
    ##########################################################



    results_book_id_list = []
    results_title_list = []
    results_description_list = []
    results_genre_list = []
    results_image_link_list = []
    results_book_rating_list = []
    results_ratings_count_list = []
    results_author_list = []
    results_author_rating_list = []
    results_year_list = []
    results_edition_list = []
    results_impressions_list = []
    results_clicks_list = []
    results_score_list = []
    results_algorithm_type=[]


    ##### CONVERT LARGE DICTIONARY TO SET OF DICTIONARIES #####
    results_dict=results.to_dict()

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
    impressions = results_dict['impressions']
    clicks = results_dict['clicks']
    score = results_dict['score']


    ##### CONVERT LARGE DICTIONARY TO SET OF DICTIONARIES #####
    # results_dict=results.to_dict()
    # book_id=results_dict['id']
    # name=results_dict['title']
    # content=results_dict['content']
    # score=results_dict['score']
    # genre=results_dict['genre']


    ##### SORTED AND REVERSED LIST FUNCTION #####
    def sort_for_normal_search(sub_li): 
        return(sorted(sub_li, key = lambda x: x[13], reverse=True)) # 13 indicates the index position of score


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
    impressions_list = list(impressions.values())
    clicks_list = list(clicks.values())
    score_list = list(score.values())

    ##### SORTED AND REVERSED THE DICTIONARY INTO LIST #####
    # score_list=list(score.values())
    # book_id_list=list(book_id.values())

    appended_list=[]
    for i in range(len(score_list)):
        value = [ book_id_list[i] , title_list[i] , description_list[i] , genre_list[i] , image_link_list[i] , book_rating_list[i] , ratings_count_list[i] , author_list[i], author_rating_list[i] , year_list[i] , edition_list[i] , impressions_list[i] , clicks_list[i] , score_list[i] ]
        appended_list.append(value)
    appended_list=sort_for_normal_search(appended_list)

    # appended_list=[]
    # for i in range(len(score_list)):
    #     value=[book_id_list[i],score_list[i]]
    #     appended_list.append(value)
    # appended_list=Sort(appended_list)
    # print(appended_list)


    ##### MAKE RESULT SET #####
    for i in appended_list:
        ### HERE i[0] indicates the index 0, Which is book_id, Based on book_id we get other attributes
        results_book_id_list.append(book_id[i[0]-1])
        results_title_list.append(title[i[0]-1])
        results_description_list.append(description[i[0]-1])
        results_genre_list.append(genre[i[0]-1])
        results_image_link_list.append(image_link[i[0]-1])
        results_book_rating_list.append(book_rating[i[0]-1])
        results_ratings_count_list.append(ratings_count[i[0]-1])
        results_author_list.append(author[i[0]-1])
        results_author_rating_list.append(author_rating[i[0]-1])
        results_year_list.append(year[i[0]-1])
        results_edition_list.append(edition[i[0]-1])
        results_impressions_list.append(impressions[i[0]-1])
        results_clicks_list.append(clicks[i[0]-1])
        results_score_list.append((score[i[0]-1])*100)

        results_algorithm_type.append("Normal")



    ##########################################################
    #                  FUZZYWUZZZY SEARCH                    #
    ##########################################################

    ##### IMPORT FOR FUZZYWUZZY SEARCH #####
    from python_files.fuzzywuzzy.main import fuzzywuzzy_search


    results_fuzzy=fuzzywuzzy_search(searchQuery)

    for i in results_fuzzy:
        if(i[0] not in results_book_id_list):
            results_book_id_list.append(i[0])
            results_title_list.append(i[1])
            results_description_list.append(i[2])
            results_genre_list.append(i[3])
            results_image_link_list.append(i[4])
            results_book_rating_list.append(i[5])
            results_ratings_count_list.append(i[6])
            results_author_list.append(i[7])
            results_author_rating_list.append(i[8])
            results_year_list.append(i[9])
            results_edition_list.append(i[10])
            results_impressions_list.append(i[11])
            results_clicks_list.append(i[12])
            results_score_list.append(i[13])
            results_algorithm_type.append("NLP")

    #########################################################





    books_as_string = ""

    for i in range(0,10,1):


        # MOSTLY TAKEN LIST
        location_sales="/media/mohamedfazil/Projects/Final Year Project/library/python_files/users_clicks.csv"
        df_mt=pd.read_csv(location_sales)
        most_taken_by=""
        df_mt = df_mt[(df_mt['book_id']==results_book_id_list[i])]
        if not df_mt.empty:
            most_taken_by=df_mt['department'].value_counts().idxmax()
        else:
            most_taken_by=" - "


        books_as_string+="""
        <a href="http://127.0.0.1:8000/details/?id={0}">
        
        <div class='content'>

            <div class='top-content'>
                <div class='top'>
                    <img src="{1}" />
                </div>
                
                <div class='middle'>
                    <div class='title'>{2}</div>
                    <p class='description'>
                        <span class='author'>{3}</span><br>
                        {4}
                    </p>
                    <br>
                    <p class='score'>Score : <b>{5:.2f}</b> | Genre : <b>{6}</b> | {7} </p>
                </div>
            </div>
                
            <div class='bottom-content'>
                <span>Mostly taken by <b>{8}</b> department</span>
            </div>     

        </div>   

        </a> 
        """.format(results_book_id_list[i],results_image_link_list[i],results_title_list[i],results_author_list[i],results_description_list[i],results_score_list[i],results_genre_list[i],results_algorithm_type[i],most_taken_by)


    ##### ADD TO IMPRESSIONS
    searchQuery_sales=request.GET['searchQuery']
    location_sales="/media/mohamedfazil/Projects/Final Year Project/library/admin_files/impressions.csv"
    import datetime
    now = datetime.datetime.now()
    year=now.year
    month=now.month
    day=now.day
    searchQuery_list=searchQuery_sales.split(" ")
    for j in range(0,10,1):
        for i in searchQuery_list:
            with open(location_sales,"a") as f:
                text_to_write="1,"+str(results_book_id_list[j])+","+str(year)+","+str(month)+","+str(day)+","+str(i)+"\n"
                f.write(text_to_write)

    ### ADD TO IMPRESSIONS

    

    return render(request,"results.html",{'searchQuery':searchQuery,'books_as_string':books_as_string,'spell_check_result':spell_check_result})


def details(request):

    import datetime

    book_id_get=int(request.GET['id'])

    ##### GET USERNAME FROM ID #####
    if 'id' not in request.session:
        return redirect('/login')
    else:
        ##### ADD TO CSV
        user_id=request.session['id']


        df=pd.read_csv("/media/mohamedfazil/Projects/Final Year Project/library/python_files/users.csv")
        df=df.query('id == '+str(request.session['id'])+'') 
        if((df['department'].count())>0):
            department=df['department'].item()


        location_sales="/media/mohamedfazil/Projects/Final Year Project/library/python_files/users_clicks.csv"
        
        now = datetime.datetime.now()
        year=now.year
        month=now.month
        day=now.day
        with open(location_sales,"a") as f:
            text_to_write=str(user_id)+","+str(department)+","+str(book_id_get)+","+str(year)+","+str(month)+","+str(day)+"\n"
            f.write(text_to_write)


        
        # df = df[(df['book_id']==book_id_get) & (df['user_id']==user_id)]
        # most_taken_by=df[''].value_counts().idxmax()


        # MOSTLY TAKEN LIST
        location_sales="/media/mohamedfazil/Projects/Final Year Project/library/python_files/users_clicks.csv"
        df=pd.read_csv(location_sales)
        most_taken_by=""
        df = df[(df['book_id']==book_id_get)]
        most_taken_by=df['department'].value_counts().idxmax()

        ### ADD TO CSV
    ################################


    ##### ADD TO IMPRESSIONS
    location_sales="/media/mohamedfazil/Projects/Final Year Project/library/admin_files/clicks.csv"

    now = datetime.datetime.now()
    year=now.year
    month=now.month
    day=now.day
    with open(location_sales,"a") as f:
        text_to_write="1,"+str(book_id_get)+","+str(year)+","+str(month)+","+str(day)+"\n"
        f.write(text_to_write)
    ### ADD TO IMPRESSIONS


    ##### SENTIMENTS
    location_comments = "/media/mohamedfazil/Projects/Final Year Project/library/python_files/comments.csv"
    df_comments = pd.read_csv(location_comments)
    df_comments = df_comments[df_comments['book_id'] == book_id_get]

    df_positive = df_comments
    df_negative = df_comments

    df_positive = df_positive[df_positive['result']=="Positive"]
    df_negative = df_negative[df_negative['result']=="Negative"]

    positive_values = len(df_positive.axes[0])
    negative_values = len(df_negative .axes[0])
    total_values = positive_values+negative_values
    if(total_values!=0):
        positive_values=(positive_values/total_values)*100
        negative_values=(negative_values/total_values)*100
        sentiment_values="Positive: "+str(positive_values)+", Negative: "+str(negative_values)+""
        positive_negative_bar="<div class='positive_negative_bar'><div class='positive' style='width:"+str(int(positive_values))+"%'></div><div class='negative' style='width:"+str(int(negative_values))+"%'></div></div>"
    else:
        sentiment_values="Positive: 0, Negative: 0"
        positive_negative_bar="<div class='positive_negative_bar'><span>No Reviews Yet.</span></div>"
    # df.apply(pd.Series.value_counts)
    ### SENTIMENTS


    df=pd.read_csv('python_files/books_with_scores.csv')
    results=df.loc[df['id'] == book_id_get]
    
    ##### CONVERT LARGE DICTIONARY TO SET OF DICTIONARIES #####
    results_dict=results.to_dict()

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
    impressions = results_dict['impressions']
    clicks = results_dict['clicks']
    score = results_dict['score']
    availability = results_dict['availability'] 

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
    impressions_list = list(impressions.values())
    clicks_list = list(clicks.values())
    score_list = list(score.values())
    availability_list = list(availability.values())

    score_in_two_decimals=score_list[0]*100
    score_in_two_decimals=round(score_in_two_decimals,2)




    ##### COMMENTS #####
    df_comments=pd.read_csv("python_files/comments.csv")
    df_comments=df_comments.loc[df_comments['book_id'] == book_id_get]
    ##### CONVERT LARGE DICTIONARY TO SET OF DICTIONARIES #####
    df_comments=df_comments.to_dict()

    comment_sentiment = df_comments['comment']
    result_sentiment = df_comments['result']

    comment_sentiment = list(comment_sentiment.values())
    result_sentiment = list(result_sentiment.values())

    comments_text=""
    for i in range(len(comment_sentiment)):
        if(result_sentiment[i]=="Positive"):
            sent="<span style='color:green'>Positive</span>"
        elif(result_sentiment[i]=="Negative"):
            sent="<span style='color:red'>Negative</span>"
        else:
            sent="<span style='color:dodgerblue'>Neutral</span>"

        comments_text+="<div class='comments_div'><b>"+comment_sentiment[i]+"</b><br>"+sent+"</div>"







    ##### RECOMMENDATIONS #####
    from python_files.word2vec.main import recommendations

    # results_list=recommendations("The Road Ahead")
    
    results_list1=recommendations(title_list[0])

    df1=pd.read_csv('python_files/books_with_scores.csv')
    results1=df1.loc[df1['id'].isin(results_list1)]

    ##### CONVERT LARGE DICTIONARY TO SET OF DICTIONARIES #####
    results_dict1=results1.to_dict()

    ##### CREATE LIST FOR EACH ATTRIBUTES #####
    book_id1 = results_dict1['id']
    title1 = results_dict1['title']
    description1 = results_dict1['description']
    genre1 = results_dict1['genre']
    image_link1 = results_dict1['image_link']
    book_rating1 = results_dict1['book_rating']
    ratings_count1 = results_dict1['ratings_count']
    author1 = results_dict1['author']
    author_rating1 = results_dict1['author_rating']
    year1 = results_dict1['year']
    edition1 = results_dict1['edition']
    impressions1 = results_dict1['impressions']
    clicks1 = results_dict1['clicks']
    score1 = results_dict1['score']

    ##### SORTED AND REVERSED THE DICTIONARY INTO LIST #####
    book_id_list1 = list(book_id1.values())
    title_list1 = list(title1.values())
    description_list1 = list(description1.values())
    genre_list1 = list(genre1.values())
    image_link_list1 = list(image_link1.values())
    book_rating_list1 = list(book_rating1.values())
    ratings_count_list1 = list(ratings_count1.values())
    author_list1 = list(author1.values())
    author_rating_list1 = list(author_rating1.values())
    year_list1 = list(year1.values())
    edition_list1 = list(edition1.values())
    impressions_list1 = list(impressions1.values())
    clicks_list1 = list(clicks1.values())
    score_list1 = list(score1.values())

    books_as_string=""

    for i in range(len(book_id_list1)):

        if(availability_list[0]=="Yes"):
            availability=1
        else:
            availability=0

        books_as_string+="""
        <a href="http://127.0.0.1:8000/details/?id={0}">
        
        <div class='recommendations-content'>
            <div class='top-content'>
                <div class='top'>
                    <img src="{1}" />
                </div>
                
                <div class='middle'>
                    <div class='title'>{2}</div>
                    <p class='description'>
                        <span class='author'>{3}</span><br>
                        {4}
                    </p>
                    <br>
                    <p class='score'><!--Score : <b>{5:.2f}</b> | -->Genre : <b>{6}</b></p>
                </div>
            </div>
                
            <div class='bottom-content'>
                <span>Mostly taken by <b>___</b></span>
            </div>
                
        </div>   

        </a> 
        """.format( book_id_list1[i], image_link_list1[i], title_list1[i], author_list1[i], description_list1[i], score_list1[i], genre_list1[i] )

    recommendations_list=books_as_string
    ##########

    return render(request,"details.html",{'title':title_list[0], 'description':description_list[0] , 'genre':genre_list[0], 'image_link':image_link_list[0] , 'author':author_list[0], 'score':score_in_two_decimals, 'availability':availability, 'book_id_get':book_id_get, 'comments_text':comments_text,'recommendations_list':recommendations_list,'sentiment_values':sentiment_values,'positive_negative_bar':positive_negative_bar,'most_taken_by':most_taken_by})


def inform_me(request):
    mail=request.POST['mymail']
    book_id=request.GET['id']

    text=book_id+","+mail
    
    with open('python_files/inform_me.csv','a') as f:
        f.writelines("\n")
        f.writelines(text)

    # df=pd.read_csv('python_files/inform_me.csv')

    # df1 = pd.DataFrame({"book_id":[mail], 
    #                 "user_mail":[book_id]}) 

    # df.append(df1, ignore_index = True) 

    # df.to_csv('python_files/inform_me.csv')

    link='/details/?id='+str(book_id)

    return redirect(link)

def recommendations(request):

    from python_files.word2vec.main import recommendations

    results_list=recommendations("The Road Ahead")

    df=pd.read_csv('python_files/books_with_scores.csv')
    results=df.loc[df['id'].isin(results_list)]

    ##### CONVERT LARGE DICTIONARY TO SET OF DICTIONARIES #####
    results_dict=results.to_dict()

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
    impressions = results_dict['impressions']
    clicks = results_dict['clicks']
    score = results_dict['score']

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
    impressions_list = list(impressions.values())
    clicks_list = list(clicks.values())
    score_list = list(score.values())

    books_as_string=""

    for i in range(len(book_id_list)):

        books_as_string+="""
        <div class='content'>
            <div class='top-content'>
                <div class='top'>
                    <img src="{0}" />
                </div>
                
                <div class='middle'>
                    <div class='title'>{1}</div>
                    <p class='description'>
                        <span class='author'>{2}</span><br>
                        {3}
                    </p>
                    <br>
                    <p class='score'>Score : <b>{4:.2f}</b> | Genre : <b>{5}</b></p>
                </div>
            </div>
                
            <div class='bottom-content'>
                <span>Mostly taken by <b>___</b></span>
            </div>
                
        </div>    
        """.format( image_link_list[i], title_list[i], author_list[i], description_list[i], score_list[i], genre_list[i] )

    results_list=books_as_string

    return render(request,"recommendations.html",{'results_list':results_list})

def autocomplete_text(request):
    from python_files.autocomplete_text.main import function
    text=request.POST['searchVal']
    result=function(text)
    return render(request,"autocomplete_text.html",{'result':result})

def sentiment_analysis(request):
    return render(request,"sentiment_analysis.html")

def validate_sentiment_analysis(request):
    # from python_files.sentiment_analysis.naive.naive import sentiment_analysis_function
    # text=request.POST['text']
    # result=sentiment_analysis_function(text)

    from python_files.sentiment_analysis_textblob.main import sentiment_analysis_function
    text = request.POST['text']
    result,sentiment = sentiment_analysis_function(text)

    user_id = str(request.session['id'])
    book_id = str(request.GET['book_id'])

    df = pd.read_csv('python_files/comments.csv')
    results = df[(df.book_id == int(book_id)) & (df.user_id == int(user_id))]
    if(len(results.index)>0):
        print("You cant commment multiple times")
    else:
        text_into_file=book_id+","+user_id+","+str(text)+","+str(result)+","+str(sentiment)
        with open('python_files/comments.csv','a') as f:
            f.writelines("\n")
            f.writelines(text_into_file)
        # return render(request,"validate_sentiment_analysis.html",{'result':result,'sentiment':sentiment})
    link='/details/?id='+str(book_id)
    return redirect(link)
    

def chatbot(request):
    return render(request,"chatbot.html")
    

def chatbot_response(request):
    from python_files.chatbot.chatbot import myChatbot
    text=request.GET['text']
    response=myChatbot(text)
    bot_response="<p class='message bot_message'><span>Bot:</span><br>"+response+"</p>"
    return HttpResponse(bot_response)

def assignment_helper(request):
    return render(request,"assignment_helper.html")

def assignment_helper_response(request):
    from python_files.assignment_helper.helper import helper_bot
    text=request.GET['text']
    response=helper_bot(text)
    bot_response="<p class='message bot_message'><span>Bot:</span><br>"+response+"</p>"
    return HttpResponse(bot_response)

def book_bot(request):
    book_id = request.GET['id']
    return render(request,"book_bot.html",{'book_id':book_id})
    

def book_bot_response(request):
    from python_files.book_bot.helper import func, func1, func2
    text=request.GET['text']

    book_id = int(request.GET['book_id'])

    if(book_id == 494):
        response=func(text)

    elif(book_id == 527):
        response=func1(text)

    elif(book_id == 631):
        response=func2(text)

    else:
        response=func(text)


    bot_response="<p class='message bot_message'><span>Bot:</span><br>"+response+"</p>"
    return HttpResponse(bot_response)



def image_search(request):
    return render(request,"image_search.html")


def results_image(request):
    searchQuery=request.GET['searchQuery']

    ##### SPELL CHECKER #####
    from python_files.spellchecker.spell_checker_using_textblob import spell_check
    spell_check_result=spell_check(searchQuery)
    if(spell_check_result.strip()==searchQuery.strip()):
        spell_check_result=""
        
    #########################

    check_for_errors=''.join(e for e in searchQuery if e.isalnum())
    if(check_for_errors==""):
        return render(request,"error_page.html")

    searchQuery=searchQuery.replace("(","")
    searchQuery=searchQuery.replace(")","")

    ##### IMPORT FOR FUZZYWUZZY SEARCH #####
    from python_files.fuzzywuzzy.image import fuzzywuzzy_search


    results_fuzzy=fuzzywuzzy_search(searchQuery)

    results_image_id_list=[]
    results_image_list=[]

    for i in results_fuzzy:
        results_image_id_list.append(i[0])
        results_image_list.append(i[1])
    #########################################################


    books_as_string = ""

    for i in range(0,10,1):

        with open(r"/media/mohamedfazil/Projects/Final Year Project/library/python_files/flask_image_search/static/img/"+results_image_list[i], "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string=encoded_string.decode('utf-8')

        books_as_string+="""
        <div class='content'>

            <div class='top-content'>
                <div class='top'>
                    <img src="data:image/png;base64, {0}" />
                </div>
                
                <div class='middle'>
                    <div class='title'>{1}</div>
                </div>
            </div>
        </div>   
        

        </a> 
        """.format(encoded_string,results_image_id_list[i])

    return render(request,"results_image.html",{'searchQuery':searchQuery,'books_as_string':books_as_string,'spell_check_result':spell_check_result})




def availability(request):
    return render(request,"availability.html")



def availability_enter(request):

    from python_files.email.mail import send_mail

    book_id_get=int(request.POST['book_id'])

    df=pd.read_csv('python_files/inform_me.csv')
    results=df.loc[df['book_id'] == book_id_get]
    
    ##### CONVERT LARGE DICTIONARY TO SET OF DICTIONARIES #####
    results_dict=results.to_dict()

    ##### CREATE LIST FOR EACH ATTRIBUTES #####
    user_mail = results_dict['user_mail']


    ##### SORTED AND REVERSED THE DICTIONARY INTO LIST #####
    user_mail = list(user_mail.values())   

    for i in range(len(user_mail)):
        send_mail(user_mail[i],book_id_get)

    return redirect("/availability/")


def clicks_history(request):

    ##### GET USERNAME FROM ID #####
    if 'id' not in request.session:
        return redirect('/login')
    else:
        df=pd.read_csv("/media/mohamedfazil/Projects/Final Year Project/library/python_files/users.csv")
        df=df.query('id == '+str(request.session['id'])+'') 
        user_id=request.session['id']
        if((df['name'].count())>0):
            username=df['name'].item()
    ################################

    # MOSTLY TAKEN LIST
    location_sales="/media/mohamedfazil/Projects/Final Year Project/library/python_files/users_clicks.csv"
    df=pd.read_csv(location_sales)
    df = df.iloc[::-1]
    most_taken_by=""
    df = df[(df['user_id']==user_id)]


    ##### CONVERT LARGE DICTIONARY TO SET OF DICTIONARIES #####
    results_dict=df.to_dict()

    ##### CREATE LIST FOR EACH ATTRIBUTES #####
    book_id = results_dict['book_id']
    year = results_dict['year']
    month = results_dict['month']
    date = results_dict['date']

    book_id_list = list(book_id.values())
    title_list = list(year.values())
    description_list = list(month.values())
    genre_list = list(date.values())

    book_as_string=""
    for i in range(len(book_id_list)):
        book_as_string+="""
        <div class='content1'>
        <b>ID: {0}</b><br>
        DATE: {1}-{2}-{3}
        <br><br><a href='/details/?id={4}'><button>View</button></a>
        </div>
        """.format(book_id_list[i],title_list[i],description_list[i],genre_list[i],book_id_list[i])

    return render(request,"clicks_history.html",{'book_as_string':book_as_string})



    