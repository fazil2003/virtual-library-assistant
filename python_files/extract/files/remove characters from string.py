with open("test.txt", "rb") as f:
    a_string = str(f.readlines())
# a_string = "abcde"

a_string = a_string[4000:]
sliced = a_string[:-4000]

with open("test1.txt","w") as f:
	f.writelines(sliced)
#print(sliced)
