import numpy
import _pickle as pkl

from collections import OrderedDict
from nltk.corpus import stopwords

import glob
import os
import re

def extract_words(sentences):
    result = []
    stop = stopwords.words('english')
    trash_characters = '?.,!:;"$%^&*()#@+/0123456789<>=\\[]_~{}|`'
    #trans = string.maketrans(trash_characters, ' '*len(trash_characters))

    for text in sentences:
        text = re.sub(r'[^\x00-\x7F]+',' ', text)
        text = text.replace('<br />', ' ')
        text = text.replace('--', ' ').replace('\'s', '')
        #text = text.translate(trans)
        text=text.replace(trash_characters,' '*len(trash_characters))
        text = ' '.join([w for w in text.split() if w not in stop])

        words = []
        for word in text.split():
            word = word.lstrip('-\'\"').rstrip('-\'\"')
            if len(word)>2 :
                words.append(word.lower())
        text = ' '.join(words)
        result.append(text.strip())
    return result


def sentiment_analysis_function(searchText):

     
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn import metrics
    import six.moves.cPickle as pickle

    # Load All Reviews in train and test datasets
    f = open(r'/media/mohamedfazil/Projects/Final Year Project/library/python_files/sentiment_analysis/naive/train.pkl', 'rb')
    reviews = pickle.load(f)
    f.close()

    f = open(r'/media/mohamedfazil/Projects/Final Year Project/library/python_files/sentiment_analysis/naive/test.pkl', 'rb')
    test = pickle.load(f)
    f.close()


    # Generate counts from text using a vectorizer.  
    # There are other vectorizers available, and lots of options you can set.
    # This performs our step of computing word counts.
    vectorizer = CountVectorizer()
    train_features = vectorizer.fit_transform([r for r in reviews[0]])
    test_features = vectorizer.transform([r for r in test[0]])

    # Fit a naive bayes model to the training data.
    # This will train the model using the word counts we computer, 
    #       and the existing classifications in the training set.
    nb = MultinomialNB()
    nb.fit(train_features, [int(r) for r in reviews[1]])

    # Now we can use the model to predict classifications for our test features.
    predictions = nb.predict(test_features)

    # Compute the error.  
    print(metrics.classification_report(test[1], predictions))
    print("accuracy: {0}".format(metrics.accuracy_score(test[1], predictions)))


    result="neutral"
    sentences = []
    sentence=searchText
    if sentence == "exit":
        print("\033[93mexit program ...\033[0m\n")
    else:
        sentences.append(sentence)
        input_features = vectorizer.transform(extract_words(sentences))
        prediction = nb.predict(input_features)
        if prediction[0] == 1 :
            result="Positive"
        else:
            result="Negative"
    
    return result

