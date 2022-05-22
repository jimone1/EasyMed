from helpers.credentials import *
from helpers.drugs import *
from helpers.resources import *
from flask import Flask
from flask import request

app = Flask(__name__)

credentials = Credentials()
drugs = Drugs()
resources = Resources()

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        pwd = request.json['password']
        if credentials.checkUserName(username):
            return "Username doesn't exists."
        if not credentials.checkPassword(username, pwd):
            return "Wrong password."
        return "Success!"

@app.route("/signup", methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.json['username']
        pwd = request.json['password']
        if not credentials.checkUserName(username):
            return "Username already exists."
        
        credentials.registerUser(username, pwd)
        return "Success!"

@app.route("/getDrugList", methods=['POST'])
def getDrugList():
    if request.method == 'POST':
        username = request.json['username']
        if drugs.checkUserName(username):
            return {"druglist": []}
        return {"druglist": drugs.getDrugList(username)}

@app.route("/addDrug", methods=['POST'])
def addDrug():
    if request.method == 'POST':
        username = request.json['username']
        drug_name = request.json['drug_name']
        drug_image_url = request.json['drug_image_url']
        drug_upc_code = request.json['drug_upc_code']
        drug_desc = request.json['drug_desc']

        if drugs.ifUpcCodeExist(username, drug_upc_code):
            return "User already has this drug."
        
        drugs.addDrug(username, drug_name, drug_image_url, drug_upc_code, drug_desc)
        return "Success!"

@app.route("/removeDrug", methods=['POST'])
def removeDrug():
    if request.method == 'POST':
        username = request.json['username']
        drug_upc_code = request.json['drug_upc_code']

        if not drugs.ifUpcCodeExist(username, drug_upc_code):
            return "User doesn't have this drug."
        
        drugs.removeDrug(username, drug_upc_code)
        return "Success!"

@app.route("/getResources", methods=['GET'])
def getResources():
    if request.method == 'GET':
        return resources.getResources()

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=10000)