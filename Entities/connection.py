import pyodbc 

class Connection:
    connectionString = """Driver={SQL Server Native Client 11.0};
                        Server=DESKTOP-2AR95A5;
                        Database=ChatBot;
                        Trusted_Connection=yes;"""
    cnxn = None
    cursor = None

    def __init__(self) -> None:
        #self.connectionString = connectionString
        self.cnxn = pyodbc.connect(self.connectionString)
        self.cursor = self.cnxn.cursor()

    def close(self) -> None:
        self.cursor.close()

    def QUERY(self, query: str):  
        return  self.cursor.execute(query)

    def __del__(self) -> None:
        self.close()
        print("__del__")
