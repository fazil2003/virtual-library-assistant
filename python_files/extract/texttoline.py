filename="60.txt"

with open(filename,"rb") as f:
	line=str(f.readlines())


import re

line=re.sub(r'\n', '', line)
line=re.sub(r'\\n', '', line)
line=re.sub(r'\\x', '', line)
line=line.replace(",","")
line=re.sub("b'", '', line)
line=re.sub("'", '', line)



filename="new/"+filename


line=bytes(line, 'utf-8') 
with open(filename,"wb") as f:
	f.write(line)
