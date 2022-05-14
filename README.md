# microsoft_ai_hack_backend

### How to start the backend server?
1. ssh in Microsoft Azure VM.
2. `$ cd ~/microsoft_ai_hack_backend`
3. `$ export FLASK_APP=application`
4. `$ flask run --port=10000` Notice: We will run our server on port 10000

### API
The IP Address for our Microsoft Azure Virtual Machine is http://20.231.217.74:10000.
#### 1. Login
- POST Only
- API access: `http://20.231.217.74:10000/login`
- Json Data: `{username: xxx, password: zzz}`
- Returns:
    1. Username doesn't exists.
    2. Wrong password.
    3. Success!
#### 2. Sign Up
- POST Only
- API access: `http://20.231.217.74:10000/signup`
- Json Data: `{username: xxx, password: zzz}`
- Returns:
    1. Username already exists.
    2. Success!