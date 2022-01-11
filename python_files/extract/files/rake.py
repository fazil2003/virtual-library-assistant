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
# print ("keywords: ", keywords)
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
    # if (count > 200000):
    #     break

# print(words)

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
