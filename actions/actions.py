# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import re
import time
import logging
from typing import Any, Text, Dict, List
from bson.objectid import ObjectId

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted

from channels.facebook import Facebook
from services.analysisService import AnalysisService
from Entities.TeacherEntry import TeacherEntry
logger = logging.getLogger(__name__)

class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        try:
            logger.debug("-------------------------Action action_default_fallback--------------")
            logger.debug(tracker.sender_id)
            # lấy câu hỏi mới nhất của sinh viên
            message = tracker.latest_message['text']
            service = AnalysisService(message)

            # Kiem tra user dang ky giao vien
            if re.findall("\Acode", message):
                dispatcher.utter_message(service.RegisterTeacher(tracker.sender_id))
                return []
            # Kiem tra user cap nhat thong tin 
            if re.findall("\Aname .+birday :", message):
                dispatcher.utter_message(service.UpdateInforTeacher(tracker.sender_id))
                return []

            # Kiểm tra user có muốn trả lời câu hỏi của sinh viên không 
            if re.findall("\Areply", message):
                dispatcher.utter_message(service.TeacherReply(tracker.sender_id))
                return []

            # Neu khong phai 
            # Thi chuyen cau hoi cho giao vien

            # Nếu là user bình thường sẽ chuyển câu hỏi cho giáo viên còn không thì dừng
            teacher = TeacherEntry()
            if teacher.find_one('teacher_id', tracker.sender_id).__len__() == 0:
                # Xác định câu hỏi thuộc khoa nào
                #analysisService = AnalysisService(message)
                #facultyId = analysisService.analysisFaculty()
                facultyId = "CNTT"

                # tim id giao vien trong bang giao vien
                teacher_id = teacher.find_id_by_faculty(facultyId)

                # Gửi câu hỏi cho giáo viên của khoa đó
                for id in teacher_id:
                    idteacher = tuple(id)[0]
                    logger.debug("id giáo vien : " + idteacher)
                    fb = Facebook("EAALDNVOTxYEBAIQTOhRKl7ZA7EM7mTz4k2UFMSHomhZAZBp7uL5NIQmyUhjwKtKcC1pM0KacxpQsiJ8ASQIDZC7XQZAyy9p9rCxZAUBkXZA8JaCnqRzFzFbbCGu8mRl5XCAF3pU91cwuECZBfwhYwGVXPBi3xJzWqDgY37inltG3xwZDZD")
                    text =  "{} : {} : {}".format([id cau hoi] , tracker.sender_id, message)
                    await fb.send_text(idteacher, text)

                    dispatcher.utter_message('Tôi đã chuyển câu hỏi này cho giáo viên. Tôi sẽ phản hồi khi có thông tin cho bạn !')
            else:
                dispatcher.utter_message(text="Xin lỗi nhưng câu hỏi của không có trong dữ liệu. Tôi sẽ phản hồi nó khi có thông tin về câu hỏi của bạn")
        except Exception as e:
            logger.debug(e)
            dispatcher.utter_message(text="Xin lỗi nhưng câu hỏi của không có trong dữ liệu. Tôi sẽ phản hồi nó khi có thông tin về câu hỏi của bạn")
            pass

        logger.debug("Done analysis")
        
        # Revert user message which led to fallback.
        return []


class ActionRegisterTeacher(Action):
    def name(self) -> Text:
        return "action_register_teacher"
    
    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            logger.debug("-------------------------Action action_register_teacher--------------")
            logger.debug(tracker.sender_id)
            
            client = MessengerClient("EAALDNVOTxYEBAIQTOhRKl7ZA7EM7mTz4k2UFMSHomhZAZBp7uL5NIQmyUhjwKtKcC1pM0KacxpQsiJ8ASQIDZC7XQZAyy9p9rCxZAUBkXZA8JaCnqRzFzFbbCGu8mRl5XCAF3pU91cwuECZBfwhYwGVXPBi3xJzWqDgY37inltG3xwZDZD")
            bot = MessengerBot(client)
            await bot.send_text_message("2086508114793671", "heloo ban nho")
            if tracker.latest_action_name == 'utter_register_teacher':
                message = tracker.latest_message['text']
                code = message.split(':')[1]
                logger.debug(message)
                dispatcher.utter_message("Mã code của bạn là " + code)
                # search teacher code trong database
                isExist =  TeacherCodeEntry(code)
                if isExist.find().__len__() == 1:
                    dispatcher.utter_message(text="Bạn đã đăng ký thành công!!!")
                else:
                    dispatcher.utter_message(text="Mã code không đúng!!")
        except Exception as e:
            logger.debug(e)
            dispatcher.utter_message(text="Xin lỗi nhưng câu hỏi của không có trong dữ liệu. Tôi sẽ phản hồi nó khi có thông tin về câu hỏi của bạn")
            pass

        logger.debug("Done analysis")
        return []


# class FormGetInfor(FormAction):

#     def name(self) -> Text:
#         return "form_get_infor"

#     @staticmethod
    
#     def required_slots(tracker: Tracker) -> List[Text]:
#         return ["name", "address"]

#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         return {
#             "name": [self.from_entity(entity="name", intent=["inform"] ), self.from_text()],
#             "address": [self.from_entity(entity="address", intent=["inform"] ), self.from_text()],
#         }
        
#     def submit(
#                 self,
#                 dispatcher: CollectingDispatcher,
#                 tracker: Tracker,
#                 domain: Dict[Text, Any],
#             ) -> List[Dict]:

#         user = [x["metadata"] for x in tracker.events if x["event"] == "user"][-1]
#         user_id = f["sender_id"]
#         user_name = tracker.get_slot('name')
#         user_address = tracker.get_slot('address')
#         Customer.create(user_id=user_id, name=name, address=address)


