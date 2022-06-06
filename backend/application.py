from helpers.credentials import *
from helpers.drugs import *
from helpers.resources import *
from helpers.utils import *
from helpers.interactions import *
from flask import Flask
from flask import request
from deepddi.main import *
from helpers.report import *

app = Flask(__name__)

credentials = Credentials()
drugs = Drugs()
resources = Resources()
interaction = Interaction()
report = Report()

# 1. Credentials API.
@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.json['username'].replace("'", "''")
        pwd = request.json['password'].replace("'", "''")
        if credentials.checkUserName(username):
            return {"code": 1, "msg": "Username doesn't exists."}
        if not credentials.checkPassword(username, pwd):
            return {"code": 1, "msg": "Wrong password."}
        return {"code": 0, "msg": "Success!"}

@app.route("/signup", methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.json['username'].replace("'", "''")
        pwd = request.json['password'].replace("'", "''")
        if not credentials.checkUserName(username):
            return {"code": 1, "msg": "Username already exists."}
        
        credentials.registerUser(username, pwd)
        return {"code": 0, "msg": "Success!"}

@app.route("/updateProfile", methods=['POST'])
def updateProfile():
    if request.method == 'POST':
        old_username = request.json['old_username'].replace("'", "''")
        new_username = request.json['new_username'].replace("'", "''")
        new_password = request.json['new_password'].replace("'", "''")
        if credentials.checkUserName(old_username):
            return {"code": 1, "msg": "Username doesn't exists."}
        
        credentials.updateUserProfile(old_username, new_username, new_password)
        return {"code": 0, "msg": "Success!"}

# 2. Drugs API
@app.route("/getDrugList", methods=['POST'])
def getDrugList():
    if request.method == 'POST':
        username = request.json['username'].replace("'", "''")
        
        return {
            "code": 0,
            "msg": "Success!",
            "druglist": interaction.updateDrugList(username, drugs.getDrugList(username))
        }

@app.route("/addDrug", methods=['POST'])
def addDrug():
    if request.method == 'POST':
        username = request.json['username'].replace("'", "''")
        drug_name = request.json['drug_name'].replace("'", "''")
        drug_image_url = request.json['drug_image_url']
        drug_upc_code = request.json['drug_upc_code']
        drug_desc = request.json['drug_desc'].replace("'", "''")
        interaction_pairs = request.json['interaction_pairs']

        if drugs.ifUpcCodeExist(username, drug_upc_code):
            return {
                "code": 1,
                "msg": "User already has this drug."
            }
        
        drugs.addDrug(username, drug_name, drug_image_url, drug_upc_code, drug_desc)
        if interaction_pairs and len(interaction_pairs[1]) != 0:
            interaction.addInteractions(username, interaction_pairs)
        return {
            "code": 0,
            "msg": "Success!"
        }

@app.route("/removeDrug", methods=['POST'])
def removeDrug():
    if request.method == 'POST':
        username = request.json['username'].replace("'", "''")
        drug_upc_code = request.json['drug_upc_code']
        curr_drug = request.json['curr_drug'].replace("'", "''")

        if not drugs.ifUpcCodeExist(username, drug_upc_code):
            return {
                "code": 1,
                "msg": "User doesn't have this drug."
            }
        
        drugs.removeDrug(username, drug_upc_code)
        interaction.deleteInteractions(username, curr_drug)
        return {
            "code": 0,
            "msg": "Success!"
        }

# 3. Resources API.
@app.route("/getResources", methods=['GET'])
def getResources():
    if request.method == 'GET':
        return {
            "code": 0,
            "msg": "Success!",
            "tags": resources.getAllTypes(),
            "resources": resources.getResources()
        }

# 4. DDI/DFI API.
@app.route("/getDFI", methods=['POST'])
def getDFI():
    if request.method == 'POST':
        username = request.json['username'].replace("'", "''")
        food_list = request.json['food_list']
        
        if credentials.checkUserName(username):
            return {
                "code": 1,
                "msg": "Failed: Username doesn't exists."
            }

        request_json = {
            "drug_list": drugs.getDrugList(username, drug_title=True),
            'food_list': food_list
        }

        return {
            "code": 0,
            "msg": "Success!",
            "interactions": makeUnique(food_list, run(request_json, "DFI"))
        }

# 4. Get Drug Detail.
@app.route("/getDrugDetail", methods=['POST'])
def getDrugDetail():
    if request.method == 'POST':
        username = request.json['username'].replace("'", "''")
        curr_drug = request.json['curr_drug']
        drug_desc = request.json['drug_desc'].replace("'", "''")
        drug_upc_code = request.json['upc_code']

        if credentials.checkUserName(username):
            return {
                "code": 1,
                "msg": "Failed: Username doesn't exists."
            }

        ddi_data = drugs.prepareRequestML(username, curr_drug, drug_desc)
        try:
            ddi_result = run(ddi_data, "DDI")
        except:
            return {
                "code": 0,
                "msg": "Success!",
                "drug_list_empty": len(drugs.getDrugList(username)) == 0,
                "is_in_list": drugs.ifUpcCodeExist(username, drug_upc_code),
                "cur_drug_side_effect": [],
                "drug_interactions": []
            }

        updateDDIResult(ddi_result)

        res = {
            "code": 0,
            "msg": "Success!",
            "drug_list_empty": len(drugs.getDrugList(username)) == 0,
            "is_in_list": drugs.ifUpcCodeExist(username, drug_upc_code),
            "cur_drug_side_effect": ddi_result["cur_drug_side_effect"],
            "drug_interactions": ddi_result["drug_interactions"],
            "interaction_pairs": [[curr_drug], interaction.transformDrugInteractions(ddi_result["drug_interactions"])]
        }

        return res

# 5. Send Feedbacks
@app.route("/sendFeedback", methods=['POST'])
def sendFeedback():
    if request.method == 'POST':
        username = request.json['username'].replace("'", "''")
        email = request.json['email'].replace("'", "''")
        title = request.json['title'].replace("'", "''")
        content = request.json['content'].replace("'", "''")
        
        report.sendFeedbacks(username, email, title, content)

        return {
            "code": 0,
            "msg": "Success!"
        }

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=10000)
    