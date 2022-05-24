from helpers.credentials import *
from helpers.drugs import *
from helpers.resources import *
from flask import Flask
from flask import request

app = Flask(__name__)

credentials = Credentials()
drugs = Drugs()
resources = Resources()

# 1. Credentials API.
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

# 2. Drugs API
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

# 3. Resources API.
@app.route("/getResources", methods=['GET'])
def getResources():
    if request.method == 'GET':
        return resources.getResources()

# 4. DDI/DFI API.
@app.route("/getDDI", methods=['POST'])
def getDDI():
    if request.method == 'POST':
        username = request.json['username']
        curr_drug = request.json['curr_drug']
        drug_desc = request.json['drug_desc']
        
        other_drugs = []

        # TODO: Consider check upc code instead of drug_name.
        for drug_info in drugs.getDrugList(username):
            if drug_info["drug_name"] == curr_drug:
                continue
            other_drugs.append({
                "drug_name": drug_info["drug_name"],
                "drug_desc": drug_info["drug_desc"]
            })

        request_json = {
            "current_drug": {
                "drug_title": curr_drug,
                "drug_desc": drug_desc
            },
            "other_drugs": other_drugs
        }

        return request_json

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=10000)