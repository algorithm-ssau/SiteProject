import pymongo
from pymongo import MongoClient
import traceback

class Result():
    
    isGood = False
    ErrorMessage = " " 
    listRes = []   

    def __init__(self, isGood, ErrorMessage, listRes):
        self.isGood = bool(isGood)
        self.ErrorMessage = ErrorMessage
        self.listRes = listRes    
    
    def getErrorMessage(self): return self.ErrorMessage 
    
    def setIsGoodVariable(self, isGood):
        self.isGood = isGood

    def setErrorMessage(self, ErrorMessage):
        self.ErrorMessage = ErrorMessage

    def setList(self, listRes):
        self.listRes = listRes

class WorkWithDB():
    ''''Класс результата операции. Сюда заносить isGood = true, если всё хорошо
    и обе переменные, если есть косяки и операция не получилась'''
    @staticmethod
    def AddToDatabase(city, isTeacher, user):
        res = Result(True, "",[])

        try:
            
            client = MongoClient()
            db = client['UsersDB']            

            if(WorkWithDB.CheckUserTelephone(user).isGood and WorkWithDB.CheckUserLogin(user).isGood):

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
            else:
                res.setIsGoodVariable(False)            

            if(res.isGood==False):
                res.setErrorMessage("Пользователь с таким логином/номером телефона уже существует.")
            else:
                res.setIsGoodVariable(True)
                res.setErrorMessage("Регистрация выполнена!")


        except Exception :
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка: неправильно заполнены поля.")

        return res

    @staticmethod
    def DeleteAllFromDatabase(city, filter, isTeacher):
        #Удалить все объекты, подходящие под фильтр   
        res = Result(False, ' ',[])
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
            res.setIsGoodVariable(True)
            res.setErrorMessage("Удаление выполнено")
        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")

        return res

    @staticmethod
    def DeleteOneFromDatabase(city, filter, isTeacher):
        res = Result(False, ' ',[])
        
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
                res.setIsGoodVariable(False)
                res.setErrorMessage("Много записей, подходящих под фильтер!")
            else:
                doc = dict(collect.find_one(filter))             
                telUser = doc.get("Телефон")
                logUser = doc.get("Логин")
                telephone = db.PhoneNumber
                login = db.Login
                telephone.delete_one({"Телефон": str(telUser)})
                login.delete_one({"Логин": str(logUser)})
                collect.delete_one(filter)
                res.setIsGoodVariable(True)
                res.setErrorMessage("Удаление выполнено успешно!")
                

        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")

        return res

    @staticmethod
    def GetRecordOnFilter(city, filter, isTeacher):
     #если запрос делает ученик, то искать будем в учителях
        listUser = [] 
        res = Result(False," ",[])
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

            res.setIsGoodVariable(True)
            res.setErrorMessage("Операция выполнена успешно.")
            res.setList(listUser)
        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")
        
        return res

    @staticmethod
    def ChangeRecordInDatabase( city, filter, newRecord, isTeacher):
        # filter - полностью старая запись пользователя
        # newRecord - полностью новая запись пользователя
        res = Result(False, "",[])
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
                res.setIsGoodVariable(True)
                res.setErrorMessage("Успешно")
            else:
                res.setIsGoodVariable(False)
                res.setErrorMessage("Много записей добходит под фильтер.")        

            
        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")

        return res

    @staticmethod
    def GetUserID(city, filter, isTeacher):
        res = Result(False, "",[])
        try:
            client = MongoClient()
            db = client['UsersDB']

            if(isTeacher):
                nameCollect = city+'teacher'
                collect = db[nameCollect]               

            else:
                nameCollect = city+'students'
                collect = db[nameCollect] 

            if(collect.count_documents(filter)==1):
                doc = dict(collect.find_one(filter))
                idUser = doc.get("id")
                res.setIsGoodVariable(True)
                res.setErrorMessage(idUser)  

        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции")   

        return res

    @staticmethod
    def CheckUserTelephone(user):
        #Если вернулся true - добавляем запись
        #
        res = Result(False,"",[])
        try:
            client = MongoClient()
            db = client['UsersDB']
            telephone = db.PhoneNumber
            telUser = user.get("Телефон")
            filter = {"Телефон": str(telUser)}
            #если мы добавляем новую запись => такого номера еще нет
            if(telephone.count_documents(filter)>=1):
                res.setIsGoodVariable(False)
            else:
                res.setIsGoodVariable(True)

        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")

        return res

    @staticmethod
    def CheckUserLogin(user):
        #Если вернулся true - добавляем запись
        res = Result(False,"",[])
        try:
            client = MongoClient()
            db = client['UsersDB']
            login = db.Login
            logUser = user.get("Логин")
            filter = {"Логин": str(logUser)}
            #если мы добавляем новую запись => такого логина еще нет
            if(login.count_documents(filter)>=1):
                res.setErrorMessage(False)
            else:
                res.setIsGoodVariable(True)

        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции")

        return res