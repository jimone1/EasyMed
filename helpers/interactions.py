class Interaction:
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

    def transformDrugInteractions(self, interaction_datas):
        return [interaction_data["other_drug_name"] for interaction_data in interaction_datas]

    def ifInteractionPairExist(self, username, drug_a, drug_b):
        self.cursor.execute(
            "SELECT COUNT(1) " +
            "FROM Interactions " +
            f"WHERE UserName='{username}' and DrugName='{drug_a}' and OtherDrugName='{drug_b}'")
        res_list = self.cursor.fetchall() # Should expect 1 row.
        return res_list[0][0] != 0

    def insertInteractionPair(self, username, drug_a, drug_b):
        command = "INSERT INTO Interactions (UserName, DrugName, OtherDrugName) " + \
        f"VALUES ('{username}', '{drug_a}', '{drug_b}')"
        self.cursor.execute(command)
        self.cursor.commit()
    
    def getNumberOfInteractions(self, username, drug):
        command = "SELECT COUNT(1) " + "FROM Interactions " + f"WHERE UserName='{username}' and (DrugName='{drug}' or OtherDrugName='{drug}')"
        self.cursor.execute(command)
        res_list = self.cursor.fetchall() # Should expect 1 row.
        return res_list[0][0]

    def addInteractions(self, username, interaction_data):
        # 1. Transform
        curr_drug, other_drugs = interaction_data
        curr_drug = curr_drug[0].replace("'", "''")
        for other_drug in other_drugs:
            if self.ifInteractionPairExist(username, curr_drug, other_drug): continue
            self.insertInteractionPair(username, curr_drug, other_drug.replace("'", "''"))
    
    def deleteInteractions(self, username, curr_drug):
        self.cursor.execute(
            "DELETE FROM Interactions " +
            f"WHERE UserName='{username}' and (DrugName='{curr_drug}' or OtherDrugName='{curr_drug}')")
        self.cursor.commit()

    def updateDrugList(self, username, drug_list):
        for drug_detail in drug_list:
            drug_detail["num_of_interactions"] = self.getNumberOfInteractions(
                username, drug_detail["drug_name"].replace("'", "''"))
        return drug_list