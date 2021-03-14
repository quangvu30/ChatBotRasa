from Entities.connection import Connection

class TeacherEntry(Connection):
    tableName = 'Teacher'

    def __init__(self):
        super().__init__(self.tableName)

    def find_id_by_faculty(self, faculty: str):
        query = "select teacher_id from {} where teacher_faculty='{}'".format(self.tableName, faculty)
        return super().QUERY(query)