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

            number = user.get("Телефон")
            doc ={"Телефон": str(number)}
            teachersNum = db.PhoneNumber
            teachersNum.insert_one(doc)

            login = user.get("Логин")
            doc_log ={"Логин": str(login)}
            usersLogin = db.Login
            usersLogin.insert_one(doc_log)

            res = Result(True, "")


        except Exception :
            res = Result(False, traceback.print_exc())

        return res

    @staticmethod
    def DeleteAllFromDatabase(city, filter, isTeacher):
        #Удалить все объекты, подходящие под фильтр   
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

            listUser = list(collect.find(filter))
            listTel = []
            listLog = []
            for user in listUser:
                listTel.append({"Телефон":str(user.get("Телефон"))})
                listLog.append({"Логин":str(user.get("Логин"))})
                
            telephone = db.PhoneNumber
            login = db.Login
            
            for i in listTel:
                telephone.delete_one(i)

            for j in listLog:
                login.delete_one(j)

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
                telUser = doc.get("Телефон")
                logUser = doc.get("Логин")
                telephone = db.PhoneNumber
                login = db.Login
                telephone.delete_one({"Телефон": str(telUser)})
                login.delete_one({"Логин": str(logUser)})
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

    @staticmethod
    def ChangeRecordInDatabase( city, filter, newRecord, isTeacher):
        # filter - полностью старая запись пользователя
        # newRecord - полностью новая запись пользователя
        
        try:
            client = MongoClient()
            db = client['UsersDB']

            if(isTeacher):
                nameCollect = city+'teacher'
                collect = db[nameCollect]               

            else:
                nameCollect = city+'students'
                collect = db[nameCollect]    

            if (collect.count_documents(filter)==1):
                doc = dict(collect.find_one(filter))             
                telUser = doc.get("Телефон")
                logUser = doc.get("Логин")
                telUserNew = newRecord.get("Телефон")
                logUserNew = newRecord.get("Логин")
                telephone = db.PhoneNumber
                login = db.Login
                telephone.update_one({"Телефон": str(telUser)},{'$set' : {"Телефон": str(telUserNew)}})
                login.update_one({"Логин": str(logUser)}, {'$set' :{"Логин": str(logUserNew)}})
                collect.update_one(filter,{'$set' :newRecord})
                res = Result(True, " ")
            else:
                res = Result(False, " ")        

            
        except Exception:
            res = Result(False, traceback.print_exc())

        return res

    @staticmethod
    def GetUserID(city, filter, isTeacher):
    
        try:
            client = MongoClient()
            db = client['UsersDB']
            res = Result(False, '')

            if(isTeacher):
                nameCollect = city+'teacher'
                collect = db[nameCollect]               

            else:
                nameCollect = city+'students'
                collect = db[nameCollect] 

            if(collect.count_documents(filter)==1):
                doc = dict(collect.find_one(filter))
                idUser = doc.get("id")
                res = Result(True, idUser)          
            

        except Exception:
            res = Result(False, traceback.print_exc())   

        return res.ErrorMessage  

    @staticmethod
    def CheckUserTelephone(user):
        #Если вернулся true - добавляем запись
        #
        try:
            client = MongoClient()
            db = client['UsersDB']
            res = Result(False, '')
            telephone = db.PhoneNumber
            telUser = user.get("Телефон")
            filter = {"Телефон": str(telUser)}
            #если мы добавляем новую запись => такого номера еще нет
            if(telephone.count_documents(filter)>=1):
                res.isGood = False
            else:
                res.isGood = True

        except Exception:
            res = Result(False, traceback.print_exc())

        return res.isGood

    @staticmethod
    def CheckUserLogin(user):
        #Если вернулся true - добавляем запись
        try:
            client = MongoClient()
            db = client['UsersDB']
            res = Result(False, '')
            login = db.Login
            logUser = user.get("Логин")
            filter = {"Логин": str(logUser)}
            #если мы добавляем новую запись => такого логина еще нет
            if(login.count_documents(filter)>=1):
                res.isGood = False
            else:
                res.isGood = True

        except Exception:
            res = Result(False, traceback.print_exc())

        return res.isGood

