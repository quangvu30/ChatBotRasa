import logging
import re
from bson.objectid import ObjectId
from typing import Any, Text
from services.analysis_faulty import AnalysisFaulty
from services.analysis_question import AnalysisQuestion


from channels.facebook import Facebook
from Entities.MessageNotRespondEntry import MessageNotRespondEntry
from Entities.TeacherEntry import TeacherEntry
from Entities.TeacherCodeEntry import TeacherCodeEntry
from Entities.KhoaEntry import KhoaEntry

logger = logging.getLogger(__name__)

class AnalysisService:
    message: str

    facultyId: str

    faultyList=[]

    question_id: str

    def __init__(self, message: str):
        self.message = message

    def setQuestionId(self, question_id: str):
        self.question_id = question_id

    @staticmethod
    def checkIfIsQuestion(text: str) -> bool:
        #token text to words array
        words = AnalysisQuestion.tokenize(text)

        get_question_file = AnalysisQuestion.get_question_file(words)

        confidence = AnalysisQuestion.compute_confidence(get_question_file)

        return confidence > 0

    def analysisFaculty(self) -> Any:
        words = AnalysisFaulty.tokenize(self.message)
        map_with_faultys = AnalysisFaulty.map_with_faulty_file(words)
        map_with_faultys_confidences = {}
        max_confidences = 0
        faultys = []

        for item, value in map_with_faultys.items():
            map_with_faultys_confidences[item] =  AnalysisFaulty.compute_confidence(value)

        logger.debug("map_with_faultys_confidences")
        logger.debug(map_with_faultys_confidences)

        for attr, value in map_with_faultys_confidences.items():
            if value > 0:
                print("max_confidences", max_confidences, value)
                if max_confidences == value:
                    print("max_confidences ==")
                    faultys.append(attr.upper())
                else:
                    if max_confidences < value:
                        print("max_confidences")
                        max_confidences = value
                        faultys = [attr.upper()]

        self.faultyList = faultys

        if len(faultys) == 0:
            return False
        return True


    def RegisterTeacher(self,sender_id: str) -> str:
        teacher = TeacherEntry()
        if teacher.find_one('teacher_id', sender_id).__len__() == 0:
            code = self.message.split(':')[1].strip()
            #Kiem tra code co trong bang TeacherCode khong
            teacher_code = TeacherCodeEntry()
            if teacher_code.find_one('teacher_code', code).__len__() == 1:
                self.insert_info(sender_id, code)
                # Yeu cau cap nhat thong tin giao vien
                return 'B???n h??y nh???p theo format: name : [your_name], birday : [yyyy-mm-dd]'
            else:
                return 'M?? code kh??ng t???n t???i !!!'
        else:
            return 'T??i kho???n ???? ????ng k??!!!'

    def UpdateInforTeacher(self,sender_id : str) -> str:
        teacher = TeacherEntry()
        if teacher.find_one('teacher_id', sender_id).__len__() == 1:
            name = re.findall("name :.+,", self.message)[0].split(':')[1].strip(' ,')
            birday = re.findall("birday :.+", self.message)[0].split(':')[1].strip()

            # Update th??ng tin gi??o vi??n
            self.update_info_teacher(sender_id, name, birday)
            return 'B???n ???? c???p nh???t th??ng tin th??nh c??ng'
        else:
            return 'Tr?????c ti??n b???n ph???i ????ng k?? gi??o vi??n !!!'

    def TeacherReply(self, sender_id: str):
        teacher = TeacherEntry()
        if teacher.find_one('teacher_id', sender_id).__len__() == 1:
            # L??u c??u tr??? l???i xu???ng csdl
            content = self.message.split(':')
            idQuestion = content[1].strip()
            idHocSinh = content[2].strip()
            anwser = content[3].strip()
            self.update_message_not_respond(idQuestion, anwser)

            # G???i c??u tr??? l???i cho sinh vi??n
            Facebook("").send_text(idHocSinh, anwser)    
        else:
            return 'Tr?????c ti??n b???n ph???i ????ng k?? gi??o vi??n !!!'

    def insert_info(self, id : str, code : str):
        teacher_code = TeacherCodeEntry()
        MaKhoa = teacher_code.find_one('teacher_code', code)[0][1]

        teacher = TeacherEntry()
        teacher.insert([(id, code, '', '', MaKhoa)])

    def update_info_teacher(self, id: str, name: str, birday: str):
        teacher = TeacherEntry()
        teacher.update(['teacher_name', 'teacher_birday'], [name, birday], 'teacher_id', id)

    def update_message_not_respond(self, idQuestion: str, utter : str):
        mess = MessageNotRespondEntry()
        mess.update(['content'], [utter], 'question_id', idQuestion)

    