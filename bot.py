from random import randint
from WorkWithDB import WorkWithDB

def BotGraf(IDuser, text):

    WorkWithDB.checkBot(IDuser)
    state = str(WorkWithDB.getState(IDuser))

    if state == 'start':
        welcomeList = ['Привет, друг!','И снова здрвствуй!','Давно не виделись!','Доброго времени суток!','Привет. Как жизнь?','Приветствую!']
        message = str(welcomeList[randint(0, len(welcomeList)-1)])+' Меня зовут Тимофей, для друзей Тимоха и я могу тебе помочь в некоторых вопросах.\nВ каком предмете тебе нужна помощь?\n1.Литература и русский язык\n2.Математика\n0.Хочу написать разработчикам'
        
        state = 'stateA1'
        WorkWithDB.stateBot(IDuser, state)
    elif state == 'stateA1':
        if text == '0':
            message = 'Лови! https://vk.com/spolik3 , https://vk.com/yt_clame , https://vk.com/naek__ek \nОни будут рады пообщаться с тобой!\nДля возвращения в меню напиши : Меню'
            
        elif text == '1':
            message = 'О, знаю я пару полезных сайтиков:\nБесплатная литература: https://aldebaran.ru/genre/klassika/russkaya_klassika/\nБанк аргументов: https://4ege.ru/russkiy/56021-bank-argumentov.html\nВсе правила русского языка: https://best-language.ru/\nДля возвращения в меню напиши : Меню'
            
        elif text == '2':
            message = 'Хорошо, сйечас посмотрим. Вот геометрия: https://www.webmath.ru/poleznoe/formules_19_0.php \nА вот математика:\nДля возвращения в меню напиши : Меню'#ПОЛИК НЕ ЗАБУДЬ ПРО МАТЕМАТИКУ
            
        elif text == 'Меню':
            state ='start'
            WorkWithDB.stateBot(IDuser, state)
            message = BotGraf(IDuser,'')


        else:
            message = 'Не понимаю :(\nДавай еще раз.'
            
        
    return message