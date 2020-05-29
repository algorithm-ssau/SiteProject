import pymongo, hashlib
from pymongo import MongoClient
import traceback
import time, requests

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

    ''''установка в отдельную соллекцию'''
    @staticmethod
    def getNewID():
        try:
            newID = 0
            client = MongoClient()
            db = client['UsersDB']
            collect = db['ID']
            
            if collect.estimated_document_count()==0:
                collect.insert_one({'ID':0})
                newID=0
            else:
                newID = int(collect.find().sort('ID', -1)[0].get('ID'))+1
                collect.update_one({'ID':int(newID-1)},{'$set' : {'ID': newID}})

        except:
            print("упс")

        return newID

    @staticmethod
    def getNewToken(user, isTeacher):
        try:
            count = 0
            while True:
                tokenSTR = str(user['Логин']) + str(user['Пароль']) + str(user['ID']) + str(user['День_рождения']) + str(count)
                hash_object = hashlib.sha512(tokenSTR.encode())
                hex_dig = hash_object.hexdigest()
                client = MongoClient()
                db = client['UsersDB']
                collect = db['Tokens']
                findRes = collect.find_one({'Токен': hex_dig})
                if findRes != None:
                    count += 1
                    continue
                TokenInfo = {}
                TokenInfo['Токен'] = hex_dig
                TokenInfo['Город'] = user['Город']
                if isTeacher:
                    TokenInfo['Роль'] = 'Репетитор'
                else:
                    TokenInfo['Роль'] = 'Ученик'
                TokenInfo['ID'] = user['ID']
                collect.insert_one(TokenInfo)
                return hex_dig
        except:
            print("упс")

        return None


    @staticmethod
    def AddToDatabase(city, isTeacher, user):
        res = Result(True, "",[])

        try:
            
            client = MongoClient()
            db = client['UsersDB']

            resCheckTelephone = WorkWithDB.CheckUserTelephone(user)
            resCheckLogin = WorkWithDB.CheckUserLogin(user)

            if(resCheckTelephone.isGood and resCheckLogin.isGood):

                user['ID'] = int(WorkWithDB.getNewID())
                nameCollect = ''

                user['Токен'] = WorkWithDB.getNewToken(user, isTeacher)
                user['О_себе'] = ''

                passwordReal = user['Пароль']
                hash_object = hashlib.sha512(passwordReal.encode())
                user['Пароль'] = hash_object.hexdigest()

                if isTeacher:
                    user['Роль'] = 'Репетитор'
                    nameCollect = city+'teachers'
                    collect = db[nameCollect]
                    collect.insert_one(user)
                else:
                    user['Роль'] = 'Ученик'
                    nameCollect = city+'students'
                    collect = db[nameCollect]
                    collect.insert_one(user)                

                number = user.get("Телефон")
                doc ={"Телефон": str(number)}
                teachersNum = db.PhoneNumber
                teachersNum.insert_one(doc) 

                login = user.get("Логин")
                doc_log ={"Логин": str(login), "Коллекция": str(nameCollect)}
                usersLogin = db.Login
                usersLogin.insert_one(doc_log)            
            else:
                res.setIsGoodVariable(False)            

            if(res.isGood==False):
                if(resCheckLogin.isGood == False and resCheckTelephone.isGood == False):
                    res.setErrorMessage("Пользователь с таким логином и номером телефона уже существует.")
                if(resCheckLogin.isGood == True and resCheckTelephone.isGood == False):
                    res.setErrorMessage("Пользователь с таким номером телефона уже существует.")
                if(resCheckLogin.isGood == False and resCheckTelephone.isGood == True):
                    res.setErrorMessage("Пользователь с таким логином уже существует.")
            else:
                res.setIsGoodVariable(True)
                res.setErrorMessage(user['Токен'])


        except Exception :
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка: неправильно заполнены поля.")

        return res

    
    @staticmethod
    def FoundUserInDatabase(login, password):
        try:
            client = MongoClient()
            db = client['UsersDB']
            usersLogin = db.Login

            hash_object = hashlib.sha512(password.encode())
            password = hash_object.hexdigest()

            doc = {'Логин': str(login)}
            filter = {'Логин': str(login), 'Пароль': str(password)}

            if(usersLogin.count_documents(doc)==1):
                docUser = dict(usersLogin.find_one(doc))
                nameCollect = docUser.get('Коллекция')                
               
                collect = db[nameCollect] 
                if(collect.count_documents(filter))==1:
                    return dict(collect.find_one(filter))
                else:
                    return None

            else:
                return None           

        except Exception:
            return None

        return None

    @staticmethod
    def FoundUserInDatabaseForToken(token):
        try:
            if token == '' or token == None:
                return None
            client = MongoClient()
            db = client['UsersDB']
            collectToken = db['Tokens']
            tokenInfo = collectToken.find_one({'Токен': token})
            nameCollect = tokenInfo['Город']
            if tokenInfo['Роль'] == 'Репетитор':
                nameCollect += 'teachers'
            else:
                nameCollect += 'students'
            collect = db[nameCollect]
            return collect.find_one({'ID': tokenInfo['ID']})        

        except Exception:
            return None


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

            cursorUser = None

            if(isTeacher):
                nameCollect = city+'students'
                collect = db[nameCollect]               
                cursorUser = collect.find(filter, {"_id": 0, "Пароль": 0, "Токен": 0, "Логин": 0, "Роль": 0}) 
                
            else:
                nameCollect = city+'teachers'
                collect = db[nameCollect]
                cursorUser = collect.find(filter, {"_id": 0, "Пароль": 0, "Токен": 0, "Логин": 0, "Роль": 0})        

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
    def ChangeRecordInDatabase(token, newRecord):
        res = Result(False, "",[])

        try:
            if token == '' or token == None:
                res.setIsGoodVariable(False)
                res.setErrorMessage("Токен пуст. Обратитесь к разработчикам!")
                return res
            client = MongoClient()
            db = client['UsersDB']
            collectToken = db['Tokens']
            tokenInfo = collectToken.find_one({'Токен': token})
            nameCollect = tokenInfo['Город']
            if tokenInfo['Роль'] == 'Репетитор':
                nameCollect += 'teachers'
            else:
                nameCollect += 'students'
            collect = db[nameCollect]
            user = collect.find_one({'ID': tokenInfo['ID']})

            if user['Телефон'] != newRecord['Телефон']:
                resCheckTelephone = WorkWithDB.CheckUserTelephone(newRecord)
                if resCheckTelephone.isGood == False:
                    res.setIsGoodVariable(False)
                    res.setErrorMessage("Новый номер телефона уже занят!")
                    return res
          
            telUser = user.get("Телефон")
            logUser = user.get("Логин")
            telUserNew = newRecord.get("Телефон")
            logUserNew = newRecord.get("Логин")
            telephone = db.PhoneNumber
            login = db.Login
            telephone.update_one({"Телефон": str(telUser)},{'$set' : {"Телефон": str(telUserNew)}})
            login.update_one({"Логин": str(logUser)}, {'$set' :{"Логин": str(logUserNew)}})
            collect.update_one(user,{'$set' :newRecord})
            res.setIsGoodVariable(True)
            res.setErrorMessage("Успешно")      

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
                idUser = doc.get("ID")
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

    @staticmethod
    def createNewDialog(IDuser1, IDuser2):
        res = Result(False," ",[])
        try:
            listID = [IDuser1, IDuser2]
            listID.sort()
            client = MongoClient()
            db = client['UsersDB']
            nameCollect = str(listID[0])+'and'+str(listID[1])
            db.create_collection(nameCollect)

        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")
        return res


    @staticmethod
    def sendMessege(IDuserFrom, IDuserTo, message, sity):
        res = Result(False," ",[])
        try:
            data = time.ctime(int(requests.get("https://time100.ru/api").text))
            client = MongoClient()
            db = client['UsersDB']
            listID = [IDuserFrom, IDuserTo]
            listID.sort()
            nameCollect = str(listID[0])+'and'+str(listID[1])

            try:
                userColl = db[str(sity+'teachers')]
                nameFrom = ''

                if(userColl.find_one({'ID': IDuserFrom})):
                    doc = dict(userColl.find_one({'ID': IDuserFrom}))
                    nameFrom = doc.get('Имя')
                else:
                    userColl = db[str(sity+'students')]
                    doc = dict(userColl.find_one({'ID': IDuserFrom}))
                    nameFrom = doc.get('Имя')

                collect = db[nameCollect]
                collect.insert_one({'Сообщение':message, 'От':nameFrom, 'Дата и время':data})

                res.setIsGoodVariable(True)
                res.setErrorMessage("Операция выполнена успешно.")

            except:
                WorkWithDB.createNewDialog(IDuserFrom, IDuserTo)
                userColl = db[str(sity+'teachers')]
                nameFrom = ''

                if(userColl.find_one({'ID': IDuserFrom})):
                    doc = dict(userColl.find_one({'ID': IDuserFrom}))
                    nameFrom = doc.get('Имя')
                else:
                    userColl = db[str(sity+'students')]
                    doc = dict(userColl.find_one({'ID': IDuserFrom}))
                    nameFrom = doc.get('Имя')

                collect = db[nameCollect]
                collect.insert_one({'Сообщение':message, 'От':nameFrom, 'Дата и время':data})

                res.setIsGoodVariable(True)
                res.setErrorMessage("Операция выполнена успешно.")

        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")

        return res

    @staticmethod
    def getMessage(count, IDuser1, IDuser2):
        listMes = []
        res = Result(False," ",[])
        try:
            client = MongoClient()
            db = client['UsersDB']

            listID = [IDuser1, IDuser2]
            listID.sort()
            nameCollect = str(listID[0])+'and'+str(listID[1])
            collect = db[nameCollect]

            tmp = collect.find().sort('_id' , -1).limit(int(count))
            for message in tmp:
                listMes.append(dict(message))

            res.setIsGoodVariable(True)
            res.setErrorMessage("Операция выполнена успешно.")
            res.setList(listMes)    

        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")

        return res

    @staticmethod
    def createBot():
        res = Result(False," ",[])
        try:
            client = MongoClient()
            db = client['UsersDB']
            db.create_collection('bot')
            res.setIsGoodVariable(True)
            res.setErrorMessage("Операция выполнена успешно.")
        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")
        return res

        
    @staticmethod
    def checkBot(idUser):
        res =Result(False,"",[])
        try:
            client = MongoClient()
            db = client['UsersDB']

            filter = {'ID': idUser}
            try:
                collect = db['bot']
                if(collect.count_documents(filter)==1):#такая запись уже есть
                    res.setIsGoodVariable(True)
                    res.setErrorMessage('Операция выполнена успешно')
                else:
                    collect.insert_one({'ID':idUser,'Состояние': 'start'})
                    res.setIsGoodVariable(True)
                    res.setErrorMessage('Операция выполнена успешно')

            except:
                WorkWithDB.createBot()
                collect = db['bot']
                collect.insert_one({'ID':idUser,'Состояние': 'start'})
                res.setIsGoodVariable(True)
                res.setErrorMessage("Операция выполнена успешно.")

        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")
            
        return res

    @staticmethod
    def getState(idUser):
        res = Result(False," ",[])
        try:
            client = MongoClient()
            db = client['UsersDB']
            collect = db['bot']

            filter = {'ID': idUser}
            doc = dict(collect.find_one(filter))   
            lastState = doc.get('Состояние')
            res.setErrorMessage(str(lastState))
            res.setIsGoodVariable(True)  
        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage('Ошибка выполнения операции.')
        return res.ErrorMessage


    @staticmethod
    def stateBot(idUser, state):
        res = Result(False," ",[])
        try:
            client = MongoClient()
            db = client['UsersDB']

            filter = {'ID': idUser}
            collect = db['bot']

            doc = dict(collect.find_one(filter))
            lastState = doc.get('Состояние')
            collect.update_one({'ID':idUser, 'Состояние': str(lastState)}, {'$set' :{'ID':idUser,'Состояние': str(state)}})

            res.setIsGoodVariable(True)
            res.setErrorMessage("Операция выполнена успешно.")
            

        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")

        return res

    @staticmethod
    def getNewIDforNote():
        try:
            newID = 0
            client = MongoClient()
            db = client['UsersDB']

            try:
                collect = db['IDNote']
            except:
                db.create_collection('IDNote')
                collect = db['IDNote']

            if collect.estimated_document_count()==0:
                collect.insert_one({'ID':0})
                newID=0
            else:
                newID = int(collect.find().sort('ID', -1)[0].get('ID'))+1
                collect.update_one({'ID':int(newID-1)},{'$set' : {'ID': newID}})

        except:
            message = 'Ошибка'

        return newID

    @staticmethod
    def NewNode(user):
        res = Result(False," ",[])
        try:
            client = MongoClient()
            db = client['UsersDB']

            try:
                collect = db['Notes']
            except:
                db.create_collection('Notes')
                collect = db['Notes']

            user['idNote'] = int(WorkWithDB.getNewIDforNote())
            collect.insert_one(user)

            res.setErrorMessage("Операция выполнена успешно")
            res.setIsGoodVariable(True)

        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")

        return res

    @staticmethod
    def UpdateNode(newNote):
        res = Result(False, '', [])
        try:
            client = MongoClient()
            db = client['UsersDB']
            collect = db['Notes']

            idNote =int(newNote['idNote'])

            doc = dict(collect.find_one({'idNote': idNote}))
            collect.update_one(doc, {'$set': newNote})

            res.setErrorMessage("Операция выполнена успешно")
            res.setIsGoodVariable(True)

        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")

        return res

    @staticmethod
    def DeleteNote(doc):
        res = Result(False, '', [])
        try:
            client = MongoClient()
            db = client['UsersDB']
            collect = db['Notes']

            collect.delete_one(doc)

            res.setErrorMessage("Операция выполнена успешно")
            res.setIsGoodVariable(True)

        except Exception:
            res.setIsGoodVariable(False)
            res.setErrorMessage("Ошибка выполнения операции.")
        
        return res

    @staticmethod
    def FoundUserInDatabaseForID(idUser):
        try:
            client = MongoClient()
            db = client['UsersDB']
            collect = db['Tokens']

            doc = dict(collect.find_one({'ID': int(idUser)}))

            if doc == None:
                return None

            city = doc['Город']
            role = doc['Роль']
            nameCollect = ''

            if(role == 'Ученик'):
                nameCollect = city+'students'
            else:
                nameCollect = city+'teachers'
                       
            collect = db[nameCollect]
            user = collect.find_one({'ID': int(idUser)})    

        except Exception:
            return None
        
        return user