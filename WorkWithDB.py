import pymongo
class WorkWithDB:
    ''''Класс результата операции. Сюда заносить isGood = true, если всё хорошо
    и обе переменные, если есть косяки и операция не получилась'''
    class Result:
        isGood
        ErrorMessage

        def __init__(self, isGood, ErrorMessage):
            self.isGood = isGood
            self.ErrorMessage = ErrorMessage

        @staticmethod
        def isGood(): return isGood

        @staticmethod
        def getErrorMessage(): return ErrorMessage

        @staticmethod
        def setIsGoodVariable(isGood):
            self.isGood = isGood

        @staticmethod
        def setErrorMessage(ErrorMessage):
            self.ErrorMessage = ErrorMessage


    @staticmethod
    def AddToDatabase(city, isTeacher, user):
        res = Result(True, 'non')

        try:
            from pymongo import MongoClient
            client = MongoClient()
            db = client['UsersDB']

            if isTeacher:
                nameCollect = city+'teachers'
                collection = db.[nameCollect]
                db.collection.insert_one(usre)
    

    
    