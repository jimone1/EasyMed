class Drugs:
    def __init__(self):
        self.cursor = self.connect()

    def connect(self):
        import pyodbc
        server = 'tcp:ucsdserver.database.windows.net' 
        database = 'ucsd' 
        username = 'odl_user_616221' 
        password = 'xzno31GKZ*5t'
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER='+server+';DATABASE='+database+';'
            'UID='+username+';'
            'PWD='+ password, autocommit=True)
        return cnxn.cursor()

    def checkUserName(self, username):
        self.cursor.execute(
            "SELECT COUNT(1) " +
            "FROM Drugs " +
            f"WHERE UserName='{username}'")
        res_list = self.cursor.fetchall() # Should expect 1 row.
        return res_list[0][0] == 0

    # Assume username already exists in database.
    def getDrugList(self, username, drug_title=False):
        self.cursor.execute(
            "SELECT * " +
            "FROM Drugs " +
            f"WHERE UserName='{username}'")
        res_list = self.cursor.fetchall() # Should expect 1 row.
        drugs = []
        for drug in res_list:
            _, drug_name, drug_image_url, drug_upc_code, drug_desc = drug
            drugs.append(
                {
                    "upc_code": drug_upc_code,
                    "drug_title" if drug_title else "drug_name": drug_name,
                    "drug_image_url": drug_image_url,
                    "drug_desc": drug_desc
                }
            )
        return drugs

    def ifUpcCodeExist(self, username, drug_upc_code):
        self.cursor.execute(
            "SELECT COUNT(1) " +
            "FROM Drugs " +
            f"WHERE UserName='{username}' and " +
            f"DrugUpcCode='{drug_upc_code}'")
        res_list = self.cursor.fetchall() # Should expect 1 row.
        return res_list[0][0] == 1

    def addDrug(self, username, drug_name, drug_image_url, drug_upc_code, drug_desc):
        command = "INSERT INTO Drugs (UserName, DrugName, DrugImageUrl, DrugUpcCode, DrugDesc) " + \
        f"VALUES ('{username}', '{drug_name}', '{drug_image_url}', '{drug_upc_code}', '{drug_desc}')"

        self.cursor.execute(command)
        self.cursor.commit()
    
    def removeDrug(self, username, drug_upc_code):
        self.cursor.execute(
            "DELETE FROM Drugs " +
            f"WHERE UserName='{username}' and DrugUpcCode='{drug_upc_code}'")
        self.cursor.commit()
    
    def prepareRequestML(self, username, curr_drug, drug_desc):
        other_drugs = []

        for drug_info in self.getDrugList(username):
            if drug_info["drug_name"] == curr_drug:
                continue
            other_drugs.append({
                "drug_title": drug_info["drug_name"],
                "drug_desc": drug_info["drug_desc"]
            })

        request_json = {
            "current_drug": {
                "drug_title": curr_drug,
                "drug_desc": drug_desc
            },
            "other_drug": other_drugs
        }

        return request_json