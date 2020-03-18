import pymongo
from pymongo import MongoClient
import traceback

class Result():
    
    isGood = False
    ErrorMessage = " "    

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
    def DeleteAllFromDatabase(city, filter, isTeacher):
        '''Удалить все объекты, подходящие под фильтр'''   
        res = Result(False, ' ')
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

    @staticmethod
    def DeleteOneFromDatabase(city, filter, isTeacher):
        res = Result(False, ' ')
        
        try:
            client = MongoClient()
            db = client['UsersDB']

            if(isTeacher):
                nameCollect = city+'teachers'
                collect = db[nameCollect]
            else:
                nameCollect = city+'students'
                collect = db[nameCollect] 

            if(collect.count_documents(filter)>1):
                res = Result(False, ' ')
            else:
                doc = dict(collect.find_one(filter))             
                telUser = doc.get("Telephone")
                logUser = doc.get("Login")
                telephone = db.PhoneNumber
                login = db.Login
                telephone.delete_one({"Telephone": str(telUser)})
                login.delete_one({"Login": str(logUser)})
                collect.delete_one(filter)
                res = Result(True, ' ')
                

        except Exception:
            res = Result(False, traceback.print_exc())

        return res

    @staticmethod
    def GetRecordOnFilter(city, filter, isTeacher):
     #если запрос делает ученик, то искать будем в учителях
        listUser = [] 
        try:
            client = MongoClient()
            db = client['UsersDB']

            if(isTeacher):
                nameCollect = city+'students'
                collect = db[nameCollect]               

            else:
                nameCollect = city+'teachers'
                collect = db[nameCollect]            

            cursorUser = collect.find(filter)
            for user in cursorUser:
                listUser.append(dict(user))        

            res = Result(True, ' ')
        except Exception:
            res = Result(False, traceback.print_exc())
        
        return listUser

            
#test = WorkWithDB()
user = {"name":"Vladimir", "Telephone":"89277534488", "Login":"Test12","Password":"test12" }
WorkWithDB.AddToDatabase("SAMARA", True, user)


#filter = {"name" :"Vladimir"}
#WorkWithDB.DeleteAllFromDatabase("SAMARA", filter, False)
##WorkWithDB.DeleteOneFromDatabase("SAMARA", filter, False)

filter = {"name": "Vladimir"} #8979908888  Test6
#WorkWithDB.DeleteOneFromDatabase("SAMARA", filter, False)

print(WorkWithDB.GetRecordOnFilter("SAMARA", filter, False))



