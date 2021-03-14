from Entities.connection import Connection

class KhoaEntry(Connection):
    tableName = 'Khoa'

    def __init__(self):
        super().__init__(self.tableName)