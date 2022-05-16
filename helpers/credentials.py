class Credentials:
    def __init__(self, server):
        self.cursor = server

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