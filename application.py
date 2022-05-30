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
            return {"code": 1, "msg": "Username doesn't exists."}
        if not credentials.checkPassword(username, pwd):
            return {"code": 1, "msg": "Wrong password."}
        return {"code": 0, "msg": "Success!"}

@app.route("/signup", methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.json['username']
        pwd = request.json['password']
        if not credentials.checkUserName(username):
            return {"code": 1, "msg": "Username already exists."}
        
        credentials.registerUser(username, pwd)
        return {"code": 0, "msg": "Success!"}

@app.route("/updateProfile", methods=['POST'])
def updateProfile():
    if request.method == 'POST':
        old_username = request.json['old_username']
        new_username = request.json['new_username']
        new_password = request.json['new_password']
        if credentials.checkUserName(username):
            return {"code": 1, "msg": "Username doesn't exists."}
        
        credentials.updateProfile(old_username, new_username, new_password)
        return {"code": 0, "msg": "Success!"}

# 2. Drugs API
@app.route("/getDrugList", methods=['POST'])
def getDrugList():
    if request.method == 'POST':
        username = request.json['username']
        if drugs.checkUserName(username):
            return {"code": 1, "msg": "Username doesn't exists.", "druglist": []}
        return {"code": 0, "msg": "Success!", "druglist": drugs.getDrugList(username)}

@app.route("/addDrug", methods=['POST'])
def addDrug():
    if request.method == 'POST':
        username = request.json['username']
        drug_name = request.json['drug_name']
        drug_image_url = request.json['drug_image_url']
        drug_upc_code = request.json['drug_upc_code']
        drug_desc = request.json['drug_desc']

        if drugs.ifUpcCodeExist(username, drug_upc_code):
            return {"code": 1, "msg": "User already has this drug."}
        
        drugs.addDrug(username, drug_name, drug_image_url, drug_upc_code, drug_desc)
        return {"code": 0, "msg": "Success!"}

@app.route("/removeDrug", methods=['POST'])
def removeDrug():
    if request.method == 'POST':
        username = request.json['username']
        drug_upc_code = request.json['drug_upc_code']

        if not drugs.ifUpcCodeExist(username, drug_upc_code):
            return {"code": 1, "msg": "User doesn't have this drug."}
        
        drugs.removeDrug(username, drug_upc_code)
        return {"code": 0, "msg": "Success!"}

# 3. Resources API.
@app.route("/getResources", methods=['GET'])
def getResources():
    if request.method == 'GET':
        return {"code": 0, "msg": "Success!", "resources": resources.getResources()}

# 4. DDI/DFI API.
@app.route("/getDDI", methods=['POST'])
def getDDI():
    if request.method == 'POST':
        username = request.json['username']
        curr_drug = request.json['curr_drug']
        drug_desc = request.json['drug_desc']
        
        request_json = drugs.prepareRequestML(username, curr_drug, drug_desc)
        
        # TODO: Send request json and get response to request_json.
        return request_json

@app.route("/getDrugDetail", methods=['POST'])
def getDrugDetail():
    if request.method == 'POST':
        username = request.json['username']
        curr_drug = request.json['curr_drug']
        drug_desc = request.json['drug_desc']
        
        if credentials.checkUserName(username):
            return {
                "code": 1,
                "msg": "Failed: Username doesn't exists."
            }

        request_json = drugs.prepareRequestML(username, curr_drug, drug_desc)

        res = {
            "code": 0,
            "msg": "success",
            "drug_detail":{
                "drug_list_empty": len(drugs.getDrugList(username)) == 0,
                "is_in_list": drugs.ifUpcCodeExist(username, drug_upc_code),
                "drug_interactions": [], #TODO: Get drug interactions.
                "food_interactions": []  #TODO: Get food interactions.
            }
        }

        return res

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=10000)