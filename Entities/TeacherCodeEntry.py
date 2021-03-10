from Entities.connection import Connection

class TeacherCodeEntry():
    teacher_code: str
    MaKhoa: str

    def __init__(self, teacher_code: str):
        self.teacher_code = teacher_code

    def find(self):
        con = Connection()
        res = tuple(con.QUERY("select * from TeacherCode where teacher_code='"+ self.teacher_code +"'"))
        return res

