from Entities.connection import Connection

class MessageNotRespondEntry(Connection):
    tableName = 'MessageNotRespond'

    def __init__(self):
        super().__init__(self.tableName)