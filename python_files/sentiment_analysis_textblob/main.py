from textblob import TextBlob
import nltk


def sentiment_analysis_function(text):
    nltk.download("punkt")

    text=text

    # Create a TextBlob object
    obj=TextBlob(text)

    sentiment=obj.sentiment.polarity
    print(sentiment)

    if sentiment==0:
        result="Neutral"  #Neutral
    elif sentiment>0:
        result="Positive"  #Positive
    else:
        result="Negative"  #Negative

    return result,sentiment