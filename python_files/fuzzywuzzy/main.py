def fuzzywuzzy_search(searchQuery):

    import pandas as pd
    from fuzzywuzzy import fuzz


    df=pd.read_csv("/media/mohamedfazil/Projects/Final Year Project/library/python_files/fuzzywuzzy/books_with_scores.csv")

    ##### SORTED AND REVERSED LIST FUNCTION #####
    def sort_for_fuzzywuzzy_search(sub_li): 
        return(sorted(sub_li, key = lambda x: x[13], reverse=True))

    ##### SORTED AND REVERSED THE DICTIONARY INTO LIST #####
    query=searchQuery

    appended_list=[]

    for ind in df.index: 
        content = df['title'][ind].lower()+' '+df['description'][ind].lower()+' '+df['genre'][ind].lower()+' '+df['author'][ind].lower()
        score=fuzz.token_set_ratio(query,content)

        #value = [ book_id_list[i] , title_list[i] , description_list[i] , genre_list[i] , image_link_list[i] , book_rating_list[i] , ratings_count_list[i] , author_list[i], author_rating_list[i] , year_list[i] , edition_list[i] , impressions_list[i] , clicks_list[i] , score_list[i] ]
        value = [ df['id'][ind] , df['title'][ind] , df['description'][ind] , df['genre'][ind] , df['image_link'][ind] , df['book_rating'][ind] , df['ratings_count'][ind] , df['author'][ind] , df['author_rating'][ind] , df['year'][ind] , df['edition'][ind] , df['impressions'][ind] , df['clicks'][ind] , score ]
        #value=[df['title'][ind], score, df['id'][ind]]

        appended_list.append(value)
    appended_list=sort_for_fuzzywuzzy_search(appended_list)

    new_appended_list=[]
    count=0
    for i in appended_list:
        new_appended_list.append(i)
        if(count==10):
            break
        count=count+1


    return new_appended_list

    # for i in appended_list:
    #     print(i[0]," - ",i[1]," - ",i[2])