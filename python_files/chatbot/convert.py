with open("1.txt","r") as f:
	text=f.readlines()

for i in text:
	text_str=str(text)

text=text_str.split(".")

list_elem=[]
for i in text:
	with open("file.txt","a") as f:
		f.writelines(i+"\n")
