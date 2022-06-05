class Report:
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
    
    def sendFeedbacks(self, username, email, title, content):
        self.cursor.execute(
            "INSERT INTO Feedbacks (UserName, Email, Title, Content) " +
            f"VALUES ('{username}', '{email}', '{title}', '{content}')")
        self.cursor.commit()
