class Resources:
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

    def getResources(self):
        resources = {}
        resources["DDI"] = self.getOneResource("DDI")
        resources["DFI"] = self.getOneResource("DFI")
        return resources
    
    def getOneResource(self, type):
        self.cursor.execute(
            f"SELECT * FROM Resources WHERE Type='{type}'"
        )
        res = []
        for name, source, type_ in self.cursor.fetchall():
            res.append({
                "name": name,
                "source": source, 
                "type": type_
            })
        return res
