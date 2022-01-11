def spell_check(text):

    from textblob import TextBlob 

    text=text.split(" ")
    result=""
    for i in text:
        b = TextBlob(i) 
        result=result+str(b.correct())+" "

    return result