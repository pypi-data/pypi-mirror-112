import requests
import json

api_url = "https://i2db-server.iexi416.repl.co/api/v1"


class Database:
    def __init__(self,user,token):
        self.user = user
        self.token = token


    @property
    def ping(self):
        return requests.get("https://i2db-server.iexi416.repl.co").text

    @property
    def get(self):
        return json.loads(requests.post(f"{api_url}/get/",data={"name":self.name,"path":self.path},headers={"Authorization":self.token}).text)

    @property
    def listdb(self):
        return requests.post(f"{api_url}/list-db",data={"name":self.name},headers={"Authorization":self.token}).text

    def commit(self,data):
        data = json.dumps(data)
        requests.post(f"{api_url}/dump",data={"name":self.name,"data":data,"path":self.path},headers={"Token":self.token})
        print(f"Done")

class User:
    def __init__(self):
        pass

    def token(self,name,password):
        return requests.post(f"{api_url}/sign-in/",data={"name":name,"password":password}).text

    def register(self,name,password):
        requests.post(f"{api_url}/sign-up",data={"name":name,"password":password}).text
        print(f"Done user created")

    def cDB(self,name,token,path):
        requests.post(f"{api_url}/create-db/",data={"name":name,"path":path},headers={"Authorization":token}).text
        print('Done db created')

    def rDB(self,name,token,path):
        requests.post(f"{api_url}/remove-db/",data={"name":name,"path":path},headers={"Authorization":token}).text
        print('Done db removed')