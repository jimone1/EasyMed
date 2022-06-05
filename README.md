## Microsoft Azure AI Backend
A backend service to support our EasyMed application.

## Tech/framework used
<b>Built with</b>
- [PyFlask](https://flask.palletsprojects.com/en/2.1.x/)
- [Azure ML] (https://azure.microsoft.com/en-us/services/machine-learning/)
- [Azure Virtual Machine] (https://azure.microsoft.com/en-us/services/virtual-machines/)
- [Azure SQL Database] (https://azure.microsoft.com/en-us/products/azure-sql/database/)

## Features
- All the data collected from users will be stored securely on **Azure SQL database**.
- We've utilized **Azure Machine Learning** to test and optimize our machine learning models.
- Our backend service is deployed on **Azure Virtual Machine** as well as our trained ML model.
- We referenced the ML model from a PNAS paper about drug-drug and drug-food interaction. https://www.pnas.org/doi/10.1073/pnas.1803294115
- Many medical terms in side-effects and drug-drug interactions are hard to understand for our primary users. Thus, we've decided to utilize **Webster's Medical Dictionary API** to provide a better experience for our user to understand.

## How to start our backend server?
1. ssh in Microsoft Azure VM.
2. `$ cd ~/microsoft_ai_hack_backend`
3. `$ export FLASK_APP=application`
4. `$ python3 application.py` Notice: We will run our server on 10000 port
5. Ip address is 20.231.217.74.

## Credits/Contributors
<b>DDI/DFI Machine Learning Service</b>
- [Yifei Ning](https://www.linkedin.com/in/yifei-ning/), [Xiangchen Zhao](https://www.linkedin.com/in/xiangchen-zhao-b640b0221/)
- Paper reference: https://www.pnas.org/doi/10.1073/pnas.1803294115

<b>Backend Service</b>
- [Yiyao Wan](https://www.linkedin.com/in/yiyao-jim-wan/)

## License
MIT © [Yiyao Wan](https://github.com/jimone1)
