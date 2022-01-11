from test import *

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

value=input("Search: ")
result=search_using_pytorch(value)

for i in result:
    print(i)
