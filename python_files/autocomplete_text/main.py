import csv
from fast_autocomplete import AutoComplete
from fast_autocomplete.misc import read_csv_gen

from fuzzywuzzy import fuzz
                

def function(text):
    path="/media/mohamedfazil/Projects/Final Year Project/library/python_files/autocomplete_text/books_with_scores.csv"
    csv_gen = read_csv_gen(path, csv_func=csv.DictReader)
    words = {}
    for line in csv_gen:
        make = line['title']
        model = line['author']
        if make != model:
            local_words = [model, '{} {}'.format(make, model)]
            while local_words:
                word = local_words.pop()
                if word not in words:
                    words[word] = {}
        if make not in words:
            words[make] = {}

    words_list=words

    word = text.lower()
    word = word.strip()
                
    autocomplete = AutoComplete(words=words_list)
    result=autocomplete.search(word=word, max_cost=25, size=25)  # mis-spelling

    result_new=[]
    for i in result:
        result_new.append(i[0].lower())

    result_real=[]
    for i in result_new:
        if i not in result_real:
            score=fuzz.token_set_ratio(word,i)
            if(score>50):
                result_real.append(i)

    return result_real
