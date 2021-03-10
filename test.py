from Entities.TeacherCodeEntry import TeacherCodeEntry
from Entities.connection import Connection

code = TeacherCodeEntry("123456789qweerty")
re = code.find()
print(re.__len__())
