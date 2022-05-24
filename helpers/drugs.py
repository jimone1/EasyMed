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
    def getDrugList(self, username):
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
                    "drug_name": drug_name,
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
        self.cursor.execute(
            "INSERT INTO Drugs (UserName, DrugName, DrugImageUrl, DrugUpcCode, DrugDesc) " +
            f"VALUES ('{username}', '{drug_name}', '{drug_image_url}', '{drug_upc_code}', '{drug_desc}')")
        self.cursor.commit()
    
    def removeDrug(self, username, drug_upc_code):
        self.cursor.execute(
            "DELETE FROM Drugs " +
            f"WHERE UserName='{username}' and DrugUpcCode='{drug_upc_code}'")
        self.cursor.commit()