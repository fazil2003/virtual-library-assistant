import pandas as pd
import numpy as np

df=pd.read_csv("books_with_scores.csv")
df.drop(['description','genre','image_link','book_rating','ratings_count','author','author_rating','year','edition','impressions','clicks','score'],axis=1,inplace=True)

df['title']=df["id"].astype(str) +"---"+ df["title"] 	#Concatenate id and name into single column

df_new=pd.DataFrame(df['title'])

with open('tatoeba.en-zh','w') as f:
    f.writelines('')

np.savetxt(r'tatoeba.en-zh', df_new.values, fmt='%s')  ### %s for string, %d for integer

print(df_new)
