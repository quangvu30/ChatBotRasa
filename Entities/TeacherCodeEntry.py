from Entities.connection import Connection

class TeacherCodeEntry(Connection):
    tableName = 'TeacherCode'
    
    def __init__(self):
        super().__init__(self.tableName)
