def search_using_pytorch(searchQuery):

    ##### IMPORT THE NECESSARY LIBRARIES #####
    from tqdm import tqdm
    import numpy as np
    import nmslib
    import torch
    from transformers import DistilBertTokenizer, DistilBertModel, DistilBertForSequenceClassification
    from transformers import BertTokenizer, BertModel

    #tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    #model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')

    #tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-uncased')
    #model = BertModel.from_pretrained('bert-base-multilingual-uncased')

    tokenizer = BertTokenizer.from_pretrained('/media/mohamedfazil/Projects/College/FinalYear/SearchEngine/bert-base-multilingual-uncased/')
    model = BertModel.from_pretrained('/media/mohamedfazil/Projects/College/FinalYear/SearchEngine/bert-base-multilingual-uncased/')

    def vectorize(text):
        input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0)
        return model(input_ids)[1].squeeze().detach().numpy()

    sentences = []
    with open('/media/mohamedfazil/Projects/Final Year Project/library/python_files/search_engine/tatoeba.en-zh') as fin:
        for line in fin:
            if line.strip():
                #en, zh = line.strip().split('\t')
                en=line.strip()
                sentences.append(en)
                #sentences.append(zh)

    sentences = list(set(sentences)) # Unique list.

    # Converts sentences to arrays of floats.
    vectorized_sents = [vectorize(s) for s in tqdm(sentences)]

    # Concatenate the arrays.
    data = np.vstack(vectorized_sents)

    # Create the index
    index = nmslib.init(method='hnsw', space='cosinesimil')
    # Add data to index.
    index.addDataPointBatch(data)
    # The actual indexing.
    index.createIndex({'post': 2}, print_progress=True)

    # When using the index.

    # Convert single string to array of floats.
    query = vectorize(searchQuery)

    ids, distances = index.knnQuery(query, k=10) # k=10 means top-10 results

    list_results=[]
    # Results.
    for i in ids:
        list_results.append(sentences[i])

    new_results=[]
    for i in list_results:
        book_id=str(i.split("---")[0])
        new_results.append(book_id)

    #return list_results
    return new_results
