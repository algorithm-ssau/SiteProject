from random import randint
import WorkWithDB

def BotGraf(text, state):

    def stateA():
        Welcome()
        state = stateA1
    return

    def stateA1(text):
        if text==0:
            state = stateC

    

    menu = input()
    if menu==0:
        message = 'Лови! https://vk.com/spolik3 , https://vk.com/yt_clame , https://vk.com/naek__ek \nОни будут рады пообщаться с тобой!\nДля возвращения в меню напиши : Меню'
        tmp = input()
        if tmp == 'Меню':
            goto .A1

    elif menu==1: #Русский и Литра
        message = 'О, знаю я пару полезных сайтиков:\nБесплатная литература: https://aldebaran.ru/genre/klassika/russkaya_klassika/\nБанк аргументов: https://4ege.ru/russkiy/56021-bank-argumentov.html\nВсе правила русского языка: https://best-language.ru/\nДля возвращения в меню напиши : Меню'
        tmp = input()
        if tmp == 'Меню':
            goto .A1

    elif menu==2: #Математика
        message = 'Хорошо, сйечас посмотрим. Что тебе нужно: 0.Вся геометрия\n1.Все формулы'
        tmp = input()
        if tmp == 0:
            messege = 'Лови! https://www.webmath.ru/poleznoe/formules_19_0.php'
        elif tmp == 1:
            #вот туть нужно передать документ
            i=5
        else:
            message='Я не понимаю. Пока.'

    elif menu==3: #информатика. тут калькулятор будет
        messege = 'Могу по переводить тебе что-нибудь.'

    else:
        messege = 'я не понимаю. Пока'
        



def Welcome(IDuser):
        welcomeList = ['Привет, друг!','И снова здрвствуй!','Давно не виделись!','Доброго времени суток!','Привет. Как жизнь?','Приветствую!']
        welcomeMessage = str(welcomeList[randint(0, len(welcomeList)-1)])+' Меня зовут Тимофей, для друзей Тимоха и я могу тебе помочь в некоторых вопросах.\nВ каком предмете тебе нужна помощь?\n1.Литература и русский язык\n2.Математика\n0.Хочу написать разработчикам'
        print(welcomeMessage)

def MainMenu(menu):
        
    menuList = {
        1 : messageBot.literature,
        2 : messageBot.rus,
        3 : messageBot.math,
        0 : messageBot.creator
    }

    func = menuList.get(menu)
    func()


def creator():
    message = 'Лови! https://vk.com/spolik3 , https://vk.com/yt_clame , https://vk.com/naek__ek \nОни будут рады пообщаться с тобой!\nДля возвращения в меню напиши : Меню'
        
def Next(menu):
    nextPoint = {'Меню': messageBot.MainMenu, 'меню': messageBot.MainMenu }
    func = nextPoint.get(menu)
    func()

def literature():
    print('litrature')

def rus():
    print('rus')

def math():
    print('math')

class messageBot():
    @staticmethod
    def Welcome(IDuser):
        welcomeList = ['Привет, друг!','И снова здрвствуй!','Давно не виделись!','Доброго времени суток!','Привет. Как жизнь?','Приветствую!']
        welcomeMessage = str(welcomeList[randint(0, len(welcomeList)-1)])+' Меня зовут Тимофей, для друзей Тимоха и я могу тебе помочь в некоторых вопросах.\nВ каком предмете тебе нужна помощь?\n1.Литература\n2.Русский язык\n3.Математика\n0.Хочу написать разработчикам'
        print(welcomeMessage)

    @staticmethod
    def MainMenu(menu):
        
        menuList = {
            1 : messageBot.literature,
            2 : messageBot.rus,
            3 : messageBot.math,
            0 : messageBot.creator
        }

        func = menuList.get(menu)
        func()

    @staticmethod
    def creator():
        message = 'Лови! https://vk.com/spolik3 , https://vk.com/yt_clame , https://vk.com/naek__ek \nОни будут рады пообщаться с тобой!\nДля возвращения в меню напиши : Меню'
        
    @staticmethod
    def Next(menu):
        nextPoint = {'Меню': messageBot.MainMenu, 'меню': messageBot.MainMenu }
        func = nextPoint.get(menu)
        func()

    @staticmethod
    def literature():
        print('litrature')

    @staticmethod
    def rus():
        print('rus')

    @staticmethod
    def math():
        print('math')

