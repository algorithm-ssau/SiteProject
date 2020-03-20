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
                listTel.append({"Telephone":str(user.get("Telephone"))})
                listLog.append({"Login":str(user.get("Login"))})
                
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
                telUser = doc.get("Telephone")
                logUser = doc.get("Login")
                telUserNew = newRecord.get("Telephone")
                logUserNew = newRecord.get("Login")
                telephone = db.PhoneNumber
                login = db.Login
                telephone.update_one({"Telephone": str(telUser)},{'$set' : {"Telephone": str(telUserNew)}})
                login.update_one({"Login": str(logUser)}, {'$set' :{"Login": str(logUserNew)}})
                collect.update_one(filter,{'$set' :newRecord})
                res = Result(True, " ")
            else:
                res = Result(False, " ")        

            
        except Exception:
            res = Result(False, traceback.print_exc())

        return res
        

            
#test = WorkWithDB()
user = {"name":"Polya", "Telephone":"89277538800", "Login":"Test1301","Password":"test13" }
user1 = {"name":"Polya", "Telephone":"89277538800", "Login":"Test13","Password":"test13"}
#WorkWithDB.AddToDatabase("SAMARA", False, user)
print(WorkWithDB.ChangeRecordInDatabase("SAMARA", user, user1, False))


#filter = {"name" :"Vladimir"}
#
##WorkWithDB.DeleteOneFromDatabase("SAMARA", filter, False)

filter = {"name": "Basya"} #89277538800  Test6
#WorkWithDB.DeleteAllFromDatabase("SAMARA", filter, True)
#WorkWithDB.DeleteOneFromDatabase("SAMARA", filter, False)

#print(WorkWithDB.GetRecordOnFilter("SAMARA", filter, False))



#"Alina"Telephone"89799077711"
#Login"Test9"