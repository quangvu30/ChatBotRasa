from Entities.TeacherEntry import TeacherEntry


field_name = ['teacher_name', 'teacher_birday']
field_value = ['quang vu', '2000-11-30']

teacher = TeacherEntry()
print(tuple(teacher.find_one('teacher_id', '2086508114793671')))
# set_value = ""
# leng = field_name.__len__()
# for i in range(0, leng):
#     if i < leng - 1:
#         set_value += "{} = '{}',".format(field_name[i], field_value[i])
#     else:
#         set_value += "{} = '{}'".format(field_name[i], field_value[i])


# print(set_value)