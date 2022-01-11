# searchQuery="what is ethical hacking"


import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    

import re


import pandas as pd
import joblib

from cdqa.utils.converters import df2squad
from cdqa.utils.download import download_model
from cdqa.reader.bertqa_sklearn import BertProcessor, BertQA

download_model(model='bert-squad_1.1', dir='./models')

def func(searchQuery):

    with open("/media/mohamedfazil/Projects/Final Year Project/library/python_files/book_bot/test.txt", "r") as f:
        text = str(f.readlines())

    line=text
    line=re.sub(r'\n', '', line)
    line=re.sub(r'\\n', '', line)
    line=re.sub(r'\\x', '', line)
    line=re.sub(r'\\', '', line)
    line=line.replace(",","")
    line=re.sub("b'", '', line)
    line=re.sub("'", '', line)
    text=line

    with open("/media/mohamedfazil/Projects/Final Year Project/library/python_files/book_bot/test_new.txt","w") as f:
        f.writelines(text)

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
    # print(answer[0])

    return answer[0]



def func1(searchQuery):

    with open("/media/mohamedfazil/Projects/Final Year Project/library/python_files/book_bot/test1.txt", "r") as f:
        text = str(f.readlines())

    line=text
    line=re.sub(r'\n', '', line)
    line=re.sub(r'\\n', '', line)
    line=re.sub(r'\\x', '', line)
    line=re.sub(r'\\', '', line)
    line=line.replace(",","")
    line=re.sub("b'", '', line)
    line=re.sub("'", '', line)
    text=line

    with open("/media/mohamedfazil/Projects/Final Year Project/library/python_files/book_bot/test_new1.txt","w") as f:
        f.writelines(text)

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
    # print(answer[0])

    return answer[0]




def func2(searchQuery):

    with open("/media/mohamedfazil/Projects/Final Year Project/library/python_files/book_bot/test2.txt", "r") as f:
        text = str(f.readlines())

    line=text
    line=re.sub(r'\n', '', line)
    line=re.sub(r'\\n', '', line)
    line=re.sub(r'\\x', '', line)
    line=re.sub(r'\\', '', line)
    line=line.replace(",","")
    line=re.sub("b'", '', line)
    line=re.sub("'", '', line)
    text=line

    with open("/media/mohamedfazil/Projects/Final Year Project/library/python_files/book_bot/test_new2.txt","w") as f:
        f.writelines(text)

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
    # print(answer[0])

    return answer[0]

