def fuzzywuzzy_search(searchQuery):

    import pandas as pd
    from fuzzywuzzy import fuzz


    df=pd.read_csv("/media/mohamedfazil/Projects/Final Year Project/library/python_files/images.csv")

    ##### SORTED AND REVERSED LIST FUNCTION #####
    def sort_for_fuzzywuzzy_search(sub_li): 
        return(sorted(sub_li, key = lambda x: x[2], reverse=True))

    ##### SORTED AND REVERSED THE DICTIONARY INTO LIST #####
    query=searchQuery

    appended_list=[]

    for ind in df.index: 
        content = df['keywords'][ind].lower()
        score=fuzz.token_set_ratio(query,content)

        value = [ df['id'][ind] , df['image'][ind] , score ]

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