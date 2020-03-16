import pymongo
from pymongo import MongoClient
import traceback

class Result():
    '''статические атрибуты'''
    isGood = False
    ErrorMessage = "green"    

    def __init__(self, isGood, ErrorMessage):
        self.isGood = bool(isGood)
        self.ErrorMessage = ErrorMessage
        
    @staticmethod
    def getErrorMessage(): return Result.ErrorMessage 

    @staticmethod
    def setIsGoodVariable(isGood):
        Result.isGood = isGood

    @staticmethod
    def setErrorMessage(ErrorMessage):
        Result.ErrorMessage = ErrorMessage

class WorkWithDB():
    ''''Класс результата операции. Сюда заносить isGood = true, если всё хорошо
    и обе переменные, если есть косяки и операция не получилась'''
    @staticmethod
    def AddToDatabase(city, isTeacher, user):
        res = Result(True, ' ')

        try:
            
            client = MongoClient()
            db = client['UsersDB']

            if isTeacher:
                nameCollect = city+'teachers'
                collect = db[nameCollect]
                collect.insert_one(user)

            else:
                nameCollect = city+'students'
                collect = db[nameCollect]
                collect.insert_one(user)

            number = user.get("Telephone")
            doc ={"Telephone": str(number)}
            teachersNum = db.PhoneNumber
            teachersNum.insert_one(doc)

            login = user.get("Login")
            doc_log ={"Login": str(login)}
            usersLogin = db.Login
            usersLogin.insert_one(doc_log)

            res = Result(True, "")


        except Exception :
            res = Result(False, traceback.print_exc())

        return res
    @staticmethod
    def DeleteOneFromDatabase(city, filter, isTeacher):
        '''Удалить все объекты, подходящие под фильтр'''   
        res = Result(True, ' ')
        try:
            client = MongoClient()
            db = client['UsersDB']

            if(isTeacher):
                nameCollect = city+'teachers'
                collect = db[nameCollect]
            else:
                nameCollect = city+'students'
                collect = db[nameCollect]  

            collect.delete_many(filter)
            res = Result(True, "")
        except Exception:
            res = Result(False, traceback.print_exc())

        return res  


            
test = WorkWithDB()
user = {"name":"Daniil", "Telephone":"89201122088", "Login":"Test2"}
'''WorkWithDB.AddToDatabase("SAMARA", True, user)'''

filter = {"name":"Daniil"}
WorkWithDB.DeleteOneFromDatabase("SAMARA", filter, True)

'''filter = {"name": "Polya"}
test.DeleteOneFromDatabase("SAMARA", filter, True)'''