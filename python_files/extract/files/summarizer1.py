# importing libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import re

# Input text - to summarize
with open("test1.txt", "rb") as f:
    text = str(f.readlines())
# text = """ """

# text = re.sub("[^a-zA-Z ]",  # Search for all non-letters
#               "",  # Replace all non-letters with spaces
#               str(text))
# print(text)

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

#print(summary)
