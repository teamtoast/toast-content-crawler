import os 

FIND_DIR="./error messages.txt"
ERROR_DIR="./Dialog Flow Example Project/intents/"

def find_all(string,substring):
    length = len(substring)
    c=0
    indexes = []
    while c < len(string):
        if string[c:c+length] == substring:
            indexes.append(c)
        c=c+1
    return indexes

f = open(FIND_DIR, "r")
s = f.read()
all_errors = find_all(s, "intents/")

for ROOT, DIRS, FILES in os.walk(ERROR_DIR): 
  for F in FILES: 
    filename = "{}/{}".format(ROOT, F) 

    for i in range(0, len(all_errors)):
      index = all_errors[i]
      if s[index+8:index + 20] in filename: 
        print("Deleting file \"{}\"".format(filename)) 
        os.remove(filename)