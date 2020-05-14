from random import randint
from WorkWithDB import WorkWithDB

def BotGraf(IDuser, text = None, state = 'start'):

    if state == 'start':
        welcomeList = ['Привет, друг!','И снова здрвствуй!','Давно не виделись!','Доброго времени суток!','Привет. Как жизнь?','Приветствую!']
        welcomeMessage = str(welcomeList[randint(0, len(welcomeList)-1)])+' Меня зовут Тимофей, для друзей Тимоха и я могу тебе помочь в некоторых вопросах.\nВ каком предмете тебе нужна помощь?\n1.Литература и русский язык\n2.Математика\n0.Хочу написать разработчикам'
        print(welcomeMessage)
        state = 'stateA1'
        WorkWithDB.stateBot(IDuser, state)
    elif state == 'stateA1':
        if text == 0:
            message = 'Лови! https://vk.com/spolik3 , https://vk.com/yt_clame , https://vk.com/naek__ek \nОни будут рады пообщаться с тобой!\nДля возвращения в меню напиши : Меню'
            print(message)
        elif text == 1:
            message = 'О, знаю я пару полезных сайтиков:\nБесплатная литература: https://aldebaran.ru/genre/klassika/russkaya_klassika/\nБанк аргументов: https://4ege.ru/russkiy/56021-bank-argumentov.html\nВсе правила русского языка: https://best-language.ru/\nДля возвращения в меню напиши : Меню'
            print(message)
        elif text == 2:
            message = 'Хорошо, сйечас посмотрим. Вот геометрия: https://www.webmath.ru/poleznoe/formules_19_0.php \nА вот математика'#тут как-то файл загрузить
            print(message)
        elif text == 'Меню':
            state ='start'
            WorkWithDB.stateBot(IDuser, state)

        else:
            message = 'Не понимаю :(\nДавай еще раз.'
            print(message)
        
    else:
        message = 'Я не понимаю. Попробуй еще раз'
        print(message)
            
BotGraf(1)
BotGraf(1,0,'stateA1')
BotGraf(1,'Меню','stateA1')
