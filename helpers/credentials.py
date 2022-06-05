class Credentials:
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

    def updateUserProfile(self, old_username, new_username, new_password):
        self.cursor.execute(
            "UPDATE Credentials " +
            f"SET UserName='{new_username}', PassWord='{new_password}' " +
            f"WHERE UserName='{old_username}'")
        self.cursor.commit()

    def checkUserName(self, username):
        self.cursor.execute(
            "SELECT COUNT(1) " +
            "FROM Credentials " +
            f"WHERE UserName='{username}'")
        res_list = self.cursor.fetchall() # Should expect 1 row.
        if len(res_list) != 1:
            print("Error: There are multiple user name in the databse!")
        if res_list[0][0] == 0:
            return True # User name can be used.
        return False # User name cannot be used.

    # Assume username already exists in database.
    def checkPassword(self, username, password):
        self.cursor.execute(
            "SELECT COUNT(1) " +
            "FROM Credentials " +
            f"WHERE UserName='{username}' " +
            f"AND Password='{password}'")
        res_list = self.cursor.fetchall() # Should expect 1 row.
        if res_list[0][0] == 1:
            return True # Password matched.
        return False # Wrong password.
    
    def registerUser(self, username, password):
        self.cursor.execute(
            "INSERT INTO Credentials (UserName, Password) " +
            f"VALUES ('{username}', '{password}')")
        self.cursor.commit()
