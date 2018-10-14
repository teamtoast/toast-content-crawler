import os 

DIR="./Dialog Flow Example Project/intents/"

# deleting some intents that have an error sententce.
targets=[
'145127b6428c',
'14015d374076',
'1401cc8a40b3',
'1451bc4266be',
'1451b39a0148',
'105137cdd164',
'1401fec0f8e8',
'1051e6b4632a',
'145138afb780',
'1451bc4266be',
'1451e8f0d5cb',
'1051b5472e66',
'1001bb2b5200',
'1451153fae0e',
'1451bc0aa2a9',
'1001956e5832',
'105112bdd48a',
'1451bcdef726',
'1451ef55eba6',
'1051b3439dd6',
'1051bb288765',
'1001d0245578',
'14011ae6df96',
'1101cab5bc06',
'145103636150',
'140141837fb0',
'1401c7dde1b5',
'140192c0fdf1',
'1451400f135b'
]

for ROOT, DIRS, FILES in os.walk(DIR): 
  for F in FILES: 
    filename = "{}/{}".format(ROOT, F) 

    for i in range(0, len(targets)):
      if targets[i] in filename: 
        print("Deleting file \"{}\"".format(filename)) 
        os.remove(filename) 