import pymongo
from pymongo import MongoClient
import traceback

class Result():        

        def __init__(self, isGood, ErrorMessage):
            self.isGood = bool(isGood)
            self.ErrorMessage = ErrorMessage
        
        def getErrorMessage(self): return self.ErrorMessage 

        def setIsGoodVariable(self, isGood):
            self.isGood = isGood

        def setErrorMessage(self, ErrorMessage):
            self.ErrorMessage = ErrorMessage

class WorkWithDB():
    ''''Класс результата операции. Сюда заносить isGood = true, если всё хорошо
    и обе переменные, если есть косяки и операция не получилась'''
    
    def AddToDatabase(self, city, isTeacher, user):
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

    def DeleteOneFromDatabase(self, city, filter, isTeacher):
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

        return res;    


            
test = WorkWithDB()
user = {"name":"Irina", "Telephone":"89200000000", "Login":"NtreceLogin"}
test.AddToDatabase("SAMARA", False, user)

filter = {"name": "Polya"}
test.DeleteOneFromDatabase("SAMARA", filter, True)