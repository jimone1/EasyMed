# microsoft_ai_hack_backend

### How to start the backend server?
1. ssh in Microsoft Azure VM.
2. `$ cd ~/microsoft_ai_hack_backend`
3. `$ export FLASK_APP=application`
4. `$ python3 application.py` Notice: We will run our server on 10000 port
5. Ip address is 20.231.217.74.

### API
The IP Address for our Microsoft Azure Virtual Machine is http://ip_address:port.

### 1. Credentials
#### 1. Login
- POST Only
- API access: `http://ip_address:port/login`
- Json Data: `{username: xxx, password: zzz}`
- Returns:
    {
        "code": 1 -> Failed / 0 -> Success,
        "msg": "Username doesn't exists." | "Wrong password." | "Success!"
    }
#### 2. Sign Up
- POST Only
- API access: `http://ip_address:port/signup`
- Json Data: `{username: xxx, password: zzz}`
- Returns:
    {
        "code": 1 -> Failed / 0 -> Success,
        "msg": "Username already exists." | "Success!"
    }

### 2. Drugs
#### 1. Get Drug List
- POST Only
- API access: `http://ip_address:port/getDrugList`
- Json Data: `{username: xxx, password: zzz}`
- Returns:
    {
        "code": 1 -> Failed / 0 -> Success,
        "msg": "Username doesn't exists." | "Success!",
        "druglist": [
            [
                "upc_code_1",
                "drug_name_1",
                "drug_img_url_1"
            ], ...
        ]
    }
#### 2. Add Drug
- POST Only
- API access: `http://ip_address:port/addDrug`
- Json Data: {
                "username" : "xxxx",
                "drug_name": "yyyy",
                "drug_image_url": "zzzz",
                "drug_upc_code": "eeee",
                "drug_desc": "xxxx"
            }
- Returns:
    {
        "code": 1 -> Failed / 0 -> Success,
        "msg": "User already has this drug." | "Success!"
    }
#### 3. Remove Drug
- POST Only
- API access: `http://ip_address:port/removeDrug`
- Json Data: {
                "username" : "xxxx",
                "drug_upc_code": "eeee"
            }
- Returns:
    {
        "code": 1 -> Failed / 0 -> Success,
        "msg": "User doesn't have this drug." | "Success!"
    }

### 3. Resources
- GET Only
- API access: `http://ip_address:port/getResources`
- Returns:
{

    "code": 1 -> Failed / 0 -> Success,
    "msg": "Success!",
    "resources": {
        "facts": [
            {
                "name": xxx,
                "source": xxx,
                "type": xxx
            }, ...
        ],
        "news": [
            {
                "name": xxx,
                "source": xxx,
                "type": xxx
            }, ...
        ],
        "video": [
            {
                "name": xxx,
                "source": xxx,
                "type": xxx
            }, ...
        ],
        "article": [
            {
                "name": xxx,
                "source": xxx,
                "type": xxx
            }, ...
        ]
    }
}

### 4. DDI/DFI API
- POST Only
- API access: `http://ip_address:port/getDDI`
- JSON Data: {
                "username": "xxxx",
                "curr_drug": "xxxx",
                "drug_desc": "xxx"
            }
- Returns: DDI info from AI API.