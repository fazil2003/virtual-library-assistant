searchQuery="what is ethical hacking"


import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    

import re

with open("file.txt", "rb") as f:
    text = str(f.readlines())


val=150000
a_string = text[val:]
sliced = a_string[:-val]

text=sliced
#print(sliced)

#res = bytes(text, 'utf-8') 

with open("new_file.txt","w") as f:
	f.writelines(text)


text_str = ""
for i in text:
    text_str = str(text)

line = text_str
line = re.sub(r'\n', '', line)
line = re.sub(r'\\n', '', line)
line = re.sub(r'\\x', '', line)
line = line.replace(",", "")
line = re.sub("b'", '', line)
line = re.sub("'", '', line)
text_str = line

text = text_str.split(".")

list_elem = []

for i in text:
    with open("file_new.txt", "a") as f:
        #f.writelines(i + "\n\n\n")
        f.writelines(i+"\n")
        
#################################
# FILE 4
################################# 

import pandas as pd
import joblib

from cdqa.utils.converters import df2squad
from cdqa.utils.download import download_model
from cdqa.reader.bertqa_sklearn import BertProcessor, BertQA

download_model(model='bert-squad_1.1', dir='./models')

with open("file_new.txt", "r") as f:
    text = str(f.readlines())
    
    
paragraph = text
query = searchQuery

# Create dataframe and convert it to squad-like json
df = pd.DataFrame({'title': 'Melbourne Convention', 'paragraphs': [[paragraph]]})
json_data = df2squad(df=df, squad_version='v1.1')

# Add question to json
json_data['data'][0]['paragraphs'][0]['qas'].append({"id": 0, "question": query})

# Preprocess json
processor = BertProcessor(do_lower_case=True, is_training=False)
examples, features = processor.fit_transform(X=json_data['data'])

# Load model and predict
qa_model = joblib.load("./models/bert_qa.joblib")

answer = qa_model.predict(X=(examples, features))
print(answer[0])

