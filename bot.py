from random import randint

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

messageBot.Welcome(5)
messageBot.MainMenu(2)