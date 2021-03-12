import json
import os

def check_file(fname):
    if not os.path.exists(fname):
        with open(fname,'w') as f:
            json.dump(dict(),f)


class Contact:
    def __init__(self, fname):
        check_file(fname)
        self.fname = fname
        with open(fname) as f:
            self.data = json.load(f)

    def add(self,username,eng_name,wx_id,email):
        if username in self.data:
            print("Username already exists")
            return
        cur = {}
        cur['eng_name'] = eng_name
        cur['wx_id'] = wx_id
        cur['email'] = email
        self.data[username] = cur
        self.save()

    def delete_all(self):
        self.data = {}

    def delete(self,username):
        if username in self.data:
            del self.data[username]
        self.save()

    def pnt_all(self):
        for username in self.data:
            self.pnt_one(username)

    def pnt_one(self,username):
        print("-"*10)
        print(f"中文名:{username}")
        cur_data = self.data[username]
        print(f"英文名:{cur_data['eng_name']}")
        print(f"微信号:{cur_data['wx_id']}")
        print(f"email:{cur_data['email']}")
        print("-"*10)
        print()

    def find(self,username):
        if username in self.data:
            self.pnt_one(username)
        else:
            print("Not found!")

    def change(self,username,field,value):
        if username not in self.data:
            print("Username not found!")
            return
        self.data[username][field] = value

    def save(self):
        with open(self.fname,'w') as f:
            json.dump(self.data,f)

class CLI:
    def __init__(self,fname):
        self.contact = Contact(fname)
        self.funcMap = {
            "ADD":self.contact.add,
            "DEL":self.contact.delete,
            "FIND":self.contact.find,
            "CHANGE":self.contact.change,
            "PRINTALL":self.contact.pnt_all,
            "DELALL":self.contact.delete_all
        }
    def run(self):
        while True:
            inp = input(">>>").split()
            typ,param = inp[0],inp[1:]
            if typ=="BYE":
                print("bye")
                break
            elif not(typ in self.funcMap):
                print("command not found")
                break
            self.funcMap[typ](*param)

cli = CLI("cont.json")
cli.run()