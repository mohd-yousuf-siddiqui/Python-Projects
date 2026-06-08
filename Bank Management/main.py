# Bank Account
# Deposit Money
# Withdraw Money
# Details
# Update Details
# Delete Account


import json
import random
import string
from pathlib import Path


class Bank:
    database = Path(__file__).parent / "data.json"
    data = []
    
    try:
        
        with open(database) as fs:
            data = json.loads(fs.read())
    except Exception as err:
        print(f"an exception occured as {err}")
    
    
    @staticmethod
    def __update():
        with open(Bank.database,'w') as fs:
            fs.write(json.dumps(Bank.data))
    
    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=1)
        spchar = random.choices("!@#$%^&*", k=1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)
    
    
    def createaccount(self):
        info = {
            "name": input("Enter your name:- "),
            "age": int(input("Enter your age:- ")),
            "email": input("Enter your email:- "),
            "pin": int(input("Enter your 4 number pin:- ")),
            "accountNo.": Bank.__accountgenerate(),
            "balance": 0
        }
        if info['age'] < 18 or len(str(info['pin'])) != 4:
            print("Sorry you cannot create your account")
        else:
            print("Account has been created successfully")
            for i in info:
                print(f"{i} : {info[i]}")
            print("please note down your account number")
            
            Bank.data.append(info)
            
            Bank.__update()
            
            
    def depositmoney(self):
        accnumber = input("Please enter your account no.:- ")
        pin = int(input("Please enter your pin:- "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]
        
        if userdata == False:
            print("Sorry no data found")
            
        else:
            amount = int(input("Enter amount to deposit:- "))
            if amount > 10000 and amount <0:
                print("Sorry the amount is too much you can deposit below 10000 and above 0")
                
            else:
                userdata[0]['balance'] += amount
                
                Bank.__update()
                print("Amount deposited successfully")
    
    
    
    def withdrawmoney(self):
        accnumber = input("Please enter your account no.:- ")
        pin = int(input("Please enter your pin:- "))

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]
        
        if userdata == False:
            print("Sorry no data found")
            
        else:
            amount = int(input("Enter amount to withdraw:- "))
            if amount > userdata[0]['balance'] and amount < 0:
                print("transaction failed enter correct amount")
                
            else:
                userdata[0]['balance'] -= amount
                
                Bank.__update()
                print("Transaction Completed Successfully")
                
                
    def showdetails(self):
        accnumber = input("Please enter your account no.:- ")
        pin = int(input("Please enter your pin:- "))
        
        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]
        print("\nYour account details are: \n\n")
        
        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")
            
            
    def updatedetails(self):
        accnumber = input("Please enter your account no.:- ")
        pin = int(input("Please enter your pin:- "))
        
        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]
        
        if userdata == False:
            print("Sorry no data found")
            
        else:
            print("you cannot change the age, account number and balance")
            
            print("Fill the details for change or leave it empty if no change")
            
            newdata = {
                "name": input("Enter new name:- "),
                "email": input("Enter new email:- "),
                "pin": int(input("Enter new pin:- "))
            }
            
            if newdata["name"] == "":
                newdata["name"] = userdata[0]['name']
            
            if newdata["email"] == "":
                newdata["email"] = userdata[0]['email']
            
            if newdata["pin"] == "":
                newdata["pin"] = userdata[0]['pin']
        
            newdata['age'] = userdata[0]['age']
            newdata['accountNo.'] = userdata[0]['accountNo.']
            newdata['balance'] = userdata[0]['balance']
            
            if type(newdata['pin']) == str:
                newdata['pin'] = int(newdata['pin'])
        

            for i in newdata:
                if newdata[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i] = newdata[i]
                    
            Bank.__update()
            print("Details updated successfully")
            
    
    def delete(self):
        accnumber = input("Please enter your account no.:- ")
        pin = int(input("Please enter your pin:- "))
        
        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]
        
        if userdata == False:
            print("Sorry no data found")
            
        else:
            check = input("Press Y if you want to delete account or press N:- ")
            
            if check == 'y' or 'Y':
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("Account Deleted successfully")
                
                Bank.__update()

            else:
                print("Bypassed")
                
        

user = Bank()

print("press 1 for creating an account")
print("press 2 for Depositing the money in the bank")
print("press 3 for withdrawing the money")
print("press 4 for details")
print("press 5 for updating the details")
print("press 6 for deleting your account")

check = int(input("Tell your response:- "))

if check == 1:
    user.createaccount()
    
if check == 2:
    user.depositmoney()

if check == 3:
    user.withdrawmoney()
    
if check == 4:
    user.showdetails()
    
if check == 5:
    user.updatedetails()

if check == 6:
    user.delete()
