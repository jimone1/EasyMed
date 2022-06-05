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

    def getAllTypes(self):
        self.cursor.execute("SELECT DISTINCT(Type) FROM Resources")
        return [type_[0].capitalize() for type_ in self.cursor.fetchall()]

    def getResources(self):
        import random
        all_resources = self.getOneResource("article") + \
                        self.getOneResource("video") + \
                        self.getOneResource("news") + \
                        self.getOneResource("facts")
                
        res = []
        for resource in all_resources:
            res.append({
                "name": resource["name"],
                "source": resource["source"],
                "type": resource["type"],
                "image_url": resource["image_url"],
                "desc": resource["desc"],
                "is_new": (random.randint(0, 1) == 0),
                "is_video": resource["type"] == "Video"
            })
        return res
    
    def getOneResource(self, type):
        self.cursor.execute(
            f"SELECT * FROM Resources WHERE Type='{type}'"
        )
        res = []
        for name, source, type_, image_url, desc in self.cursor.fetchall():
            res.append({
                "name": name,
                "source": source, 
                "type": type_.capitalize(),
                "desc": ("" if not desc else desc),
                "image_url": ("" if not image_url else image_url)
            })
        return res