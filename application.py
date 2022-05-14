from helpers.credentials import *
from flask import Flask
from flask import request

app = Flask(__name__)
credentials = Credentials()

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

