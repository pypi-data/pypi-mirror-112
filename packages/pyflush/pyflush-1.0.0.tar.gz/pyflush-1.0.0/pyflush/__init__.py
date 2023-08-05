import random
import os

def info():
    return "This library was designed and developed by Mr.Ravin Kumar. Project_URL: github.com/mr-ravin/pyflush. For more details about the developer, please do visit the URL: mr-ravin.github.io"

def randomchar():
    random_index=random.randint(32,126)
    return chr(random_index)

def flushfile(file_name):
    cnt=0
    file_size=os.path.getsize(file_name)
    wlink=open(file_name,"w")
    while cnt<file_size:
      wlink.write(randomchar())
      cnt=cnt+1
    wlink.close()

def flushdir(dir_name):
    for root, dirs, files in os.walk(dir_name):
      for fname in files:
        file_name=root+os.sep+fname
        flushfile(file_name)
