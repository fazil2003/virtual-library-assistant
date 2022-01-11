##############################################
#   REMOVE FIRST AND LAST SOME SENTENCES     #
##############################################


with open("test.txt", "rb") as f:
    a_string = str(f.readlines())
# a_string = "abcde"

a_string = a_string[4000:]
sliced = a_string[:-4000]

with open("test1.txt","w") as f:
	f.writelines(sliced)


##############################################
#               SUMMARIZER                   #
##############################################

"""
# importing libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import re

# Input text - to summarize
with open("test1.txt", "rb") as f:
    text = str(f.readlines())

# Tokenizing the text
stopWords = set(stopwords.words("english"))
words = word_tokenize(text)

# Creating a frequency table to keep the
# score of each word
# print("tokenize:",words)
freqTable = dict()
for word in words:
    word = word.lower()
    if word in stopWords:
        continue
    if word in freqTable:
        freqTable[word] += 1
    else:
        freqTable[word] = 1

# Creating a dictionary to keep the score
# of each sentence
sentences = sent_tokenize(text)
sentenceValue = dict()

# print("Sentences: ",sentences)
for sentence in sentences:
    for word, freq in freqTable.items():
        if word in sentence.lower():
            if sentence in sentenceValue:
                sentenceValue[sentence] += freq
            else:
                sentenceValue[sentence] = freq

sumValues = 0
for sentence in sentenceValue:
    sumValues += sentenceValue[sentence]

# Average value of a sentence from the original text

average = int(sumValues / len(sentenceValue))

# Storing sentences into our summary.
summary = ''

# print("Sentences: ",sentences)
# print("Val",sentenceValue)
for sentence in sentences:
    if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
        summary += " " + sentence

summary = summary.replace("[b'[0c", "")

with open("test2.txt","w") as f:
	f.writelines(summary)

"""

##############################################
#             RAKE - KEYWORDS                #
##############################################


# RAKE
import RAKE
import operator
import re

# Reka setup with stopword directory
stop_dir = "SmartStoplist.txt"
rake_object = RAKE.Rake(stop_dir)

# Sample text to test RAKE
with open("test1.txt", "rb") as f:
    text = str(f.readlines())

text = text.replace(" xc ", "")
text = text.replace(" xa ", "")
text = text.replace(" xb ", "")
text = text.replace(" xd ", "")
text = text.replace(" xe ", "")
# Extract keywords


letters_only = re.sub("[^a-zA-Z]",  # Search for all non-letters
                      " ",  # Replace all non-letters with spaces
                      str(text))

keywords = rake_object.run(letters_only)
count = 0
print(":::::KEYWORDS:::::")

words = dict()
for i, j in keywords:
    # print(i,j)

    k = i.split(" ")
    # print("K:", k)
    for l in k:
        if (l != ""):
            if l in words.keys():
                words[l] = words[l] + 1
            else:
                words[l] = 1

    count += 1
    
list_avoid = ["xa", "xb", "xc", "xd", "xe"]
for i, j in words.items():
    if (j > 50):
        if (i not in list_avoid):
            print(i)

print("\n\nSUB KEYWORDS:")
for i, j in words.items():
    if (j > 30 and j<50):
        if (i not in list_avoid):
            print(i)
            
            
