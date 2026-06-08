from pathlib import Path

def readfileandfolder():
    path = Path('')
    items = list(path.rglob('*'))
    for i, items in enumerate(items):
        print(f"{i+1}  : {items}")

def createfile():
    try:
        readfileandfolder()
        name = input("Please tell your file name:- ")
        p = Path(name)
        if not p.exists() and p.is_file():
            with open(p,"w") as fs:
                data = input("What you want to write in this file:- ")
                fs.write(data)

            print(F"File Created Successfully")
        
        else:
            print("thiis file already exist")
            
    except Exception as err:
        print(f"An error occured as {err}")
        

def readfile():
    try:
        readfileandfolder()
        name = input("Which file you want to read:-")
        p = Path(name)
        if p.exists() and p.is_file():
            with open(p,'r') as fs:
                data = fs.read()
                print(data)
                
            print("Readed successfully")
        else:
            print("the file does not exist")
    except Exception as err:
        print(f"An error occured as {err}")
        
    

print("Press 1 for creating a file")
print("Press 2 for reading a file")
print("Press 3 for updating a file")
print("Press 4 for deletion a file")

check = int(input("Please tell your response:- "))

if check == 1:
    createfile()
    
if check == 2:
    readfile()
    
# if check == 3:
#     updatefile()