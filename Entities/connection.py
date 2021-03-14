import pyodbc 

class Connection:
    connectionString = """Driver={SQL Server Native Client 11.0};
                        Server=DESKTOP-2AR95A5;
                        Database=ChatBot;
                        Trusted_Connection=yes;"""
    cnxn = None
    cursor = None
    tableName : str

    def __init__(self, tableName: str) -> None:
        #self.connectionString = connectionString
        self.tableName = tableName
        self.cnxn = pyodbc.connect(self.connectionString)
        self.cursor = self.cnxn.cursor()

    def close(self) -> None:
        self.cursor.close()

    def QUERY(self, query: str): 
        return self.cursor.execute(query)

    def find_one(self, condition_name: str, condition_value: str):
        query = "select * from {} where {}='{}'".format(self.tableName, condition_name, condition_value)
        return tuple(self.cursor.execute(query))

    def insert(self, list_data: list):
        for data in list_data:
            query = "INSERT INTO {} VALUES {};".format(self.tableName, data)
            print(query)
            self.cursor.execute(query)
            self.cnxn.commit()
        return "Done insert!"

    def update(self, field_name: list, field_value: list, condition_name: str, condition_value: str):
        set_value = ""
        leng = field_name.__len__()
        for i in range(0, leng):
            if i < leng - 1:
                set_value += "{} = '{}',".format(field_name[i], field_value[i])
            else:
                set_value += "{} = '{}'".format(field_name[i], field_value[i])
        
        query = "update {} set {} where {} = '{}';".format(self.tableName, set_value, condition_name, condition_value)
        print(query)
        self.cursor.execute(query)
        self.cnxn.commit()
        return "Done update!"

    def __del__(self) -> None:
        self.close()
        print("__del__")
