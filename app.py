import os, hashlib
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    make_response,
    Markup,
)
from WorkWithDB import WorkWithDB, Result

app = Flask(__name__)


@app.route("/", methods=["post", "get"])
def login():
    token = request.cookies.get('token')
    if token != None:
        return redirect("/profile")
    if request.method == "POST":
        login = request.form.get("email")
        password = request.form.get("psw")
        user = WorkWithDB.FoundUserInDatabase(login, password)
        if user == None:
            return render_template("errorRegistration.html", errorMessage="Ошибка входа!")
        resp = make_response(redirect("/profile"))
        resp.set_cookie('token', user['Токен'], max_age=60*60*24*365*2)
        return resp
    return render_template("login.html")
    
@app.route("/newstudent", methods=["post", "get"])
def new_student():
    if request.method == "POST":
        city = request.form.get("cities")
        user = {"Город": city}
        user.update({"Фамилия": request.form.get("LastName")})
        user.update({"Имя": request.form.get("FirstName")})
        birthday = request.form.get("date")
        birthdayInfo = birthday.split("-")
        birthday = birthdayInfo[2] + "." + birthdayInfo[1] + "." + birthdayInfo[0]
        user.update({"День_рождения": birthday})
        user.update({"Класс": request.form.get("class")})
        workform = []
        if request.form.get("option1") == "a1":
            workform.append("Еду к преподавателю")
        if request.form.get("option2") == "a2":
            workform.append("Преподаватель ко мне")
        if request.form.get("option3") == "a3":
            workform.append("Дистанционно")
        if len(workform) == 0:
            return render_template(
                "errorRegistration.html", errorMessage="Необходимо выбрать хоть 1 вариант формата занятий!"
            )
        user.update({"Формат_занятий": workform})
        if request.form.get("sex") == None:
            return render_template(
                "errorRegistration.html", errorMessage="Необходимо выбрать пол!"
            )
        user.update({"Пол": request.form.get("sex")})
        user.update({"Телефон": request.form.get("phone")})
        user.update({"Логин": request.form.get("login")})
        user.update({"Пароль": request.form.get("psw")})
        lessons = []
        if request.form.get("math") == "b1":
            lessons.append("Математика")
        if request.form.get("rus") == "b2":
            lessons.append("Русский язык")
        if request.form.get("phys") == "b3":
            lessons.append("Физика")
        if request.form.get("inf") == "b4":
            lessons.append("Информатика")
        if request.form.get("chemistry") == "b5":
            lessons.append("Химия")
        if request.form.get("bio") == "b6":
            lessons.append("Биология")
        if request.form.get("history") == "b7":
            lessons.append("История")
        if request.form.get("social") == "b8":
            lessons.append("Обществознание")
        if request.form.get("literature") == "b9":
            lessons.append("Литература")
        if request.form.get("geo") == "b10":
            lessons.append("География")
        if request.form.get("economy") == "b11":
            lessons.append("Экономика")
        if request.form.get("eng") == "b12":
            lessons.append("Английский язык")
        if request.form.get("dutch") == "b13":
            lessons.append("Немецкий язык")
        if len(lessons) == 0:
            return render_template(
                "errorRegistration.html", errorMessage="Необходимо выбрать хотя бы 1 изучаемый предмет!"
            )
        user.update({"Изучаемые_предметы": lessons})
        res = WorkWithDB.AddToDatabase(city, False, user)
        if res.isGood == False:
            return render_template(
                "errorRegistration.html", errorMessage=res.getErrorMessage()
            )
        resp = make_response(redirect("/"))
        resp.set_cookie('token', res.getErrorMessage(), max_age=60*60*24*365*2)
        return resp
    return render_template("newstudent.html")


@app.route("/newteacher", methods=["post", "get"])
def new_teacher():
    if request.method == "POST":
        city = request.form.get("cities")
        user = {"Город": city}
        user.update({"Фамилия": request.form.get("LastName")})
        user.update({"Имя": request.form.get("FirstName")})
        birthday = request.form.get("date")
        birthdayInfo = birthday.split("-")
        birthday = birthdayInfo[2] + "." + birthdayInfo[1] + "." + birthdayInfo[0]
        user.update({"День_рождения": birthday})
        workform = []
        if request.form.get("option1") == "a1":
            workform.append("Еду к ученику")
        if request.form.get("option2") == "a2":
            workform.append("Ученик ко мне")
        if request.form.get("option3") == "a3":
            workform.append("Дистанционно")
        if len(workform) == 0:
            return render_template(
                "errorRegistration.html", errorMessage="Необходимо выбрать хотя бы 1 вариант формата занятий!"
            )
        user.update({"Формат_занятий": workform})
        user.update({"Образование": request.form.get("education")})
        user.update({"Стаж_преподавания_в_годах": request.form.get("experience")})
        if request.form.get("sex") == None:
            return render_template(
                "errorRegistration.html", errorMessage="Необходимо выбрать пол!"
            )
        user.update({"Пол": request.form.get("sex")})
        user.update({"Телефон": request.form.get("phone")})
        user.update({"Логин": request.form.get("login")})
        user.update({"Пароль": request.form.get("psw")})
        lessons = []
        if request.form.get("math") == "b1":
            lessons.append("Математика")
        if request.form.get("rus") == "b2":
            lessons.append("Русский язык")
        if request.form.get("phys") == "b3":
            lessons.append("Физика")
        if request.form.get("inf") == "b4":
            lessons.append("Информатика")
        if request.form.get("chemistry") == "b5":
            lessons.append("Химия")
        if request.form.get("bio") == "b6":
            lessons.append("Биология")
        if request.form.get("history") == "b7":
            lessons.append("История")
        if request.form.get("social") == "b8":
            lessons.append("Обществознание")
        if request.form.get("literature") == "b9":
            lessons.append("Литература")
        if request.form.get("geo") == "b10":
            lessons.append("География")
        if request.form.get("economy") == "b11":
            lessons.append("Экономика")
        if request.form.get("eng") == "b12":
            lessons.append("Английский язык")
        if request.form.get("dutch") == "b13":
            lessons.append("Немецкий язык")
        if len(lessons) == 0:
            return render_template(
                "errorRegistration.html", errorMessage="Необходимо выбрать хотя бы один преподаваемый предмет!"
            )
        user.update({"Преподаваемые_предметы": lessons})
        user.update({"Ставка_в_час": request.form.get("rate")})
        typesOfLessons = []
        if request.form.get("single") == "c1":
            typesOfLessons.append("Разовые")
        if request.form.get("group") == "c2":
            typesOfLessons.append("Групповые")
        if request.form.get("home") == "c3":
            typesOfLessons.append("Помощь с домашкой")
        if request.form.get("usual") == "c4":
            typesOfLessons.append("Обычные")
        if len(typesOfLessons) == 0:
            return render_template(
                "errorRegistration.html", errorMessage="Необходимо выбрать хотя бы один вариант вида занятий!"
            )
        user.update({"Вид_занятий": typesOfLessons})
        res = WorkWithDB.AddToDatabase(city, True, user)
        if res.isGood == False:
            return render_template(
                "errorRegistration.html", errorMessage=res.getErrorMessage()
            )
        resp = make_response(redirect("/"))
        resp.set_cookie('token', res.getErrorMessage(), max_age=60*60*24*365*2)
        return resp
    return render_template("newteacher.html")


@app.route("/favicon.ico")
def fav():
    return redirect(url_for("static", filename="favicon.ico"), code=302)

@app.route("/images/<name>")
def image(name):
    return redirect(url_for("static", filename="ProfilesImages/"+name), code=302)

@app.route("/profile")
def profile():
    photo = "https://avatars.mds.yandex.net/get-pdb/216365/cafc6922-7989-4b22-b23d-36a495ce95a0/s1200"
    user = WorkWithDB.FoundUserInDatabaseForToken(request.cookies.get('token'))
    if user == None:
        resp = make_response(redirect("/"))
        resp.set_cookie('token', '', expires = 0)
        return resp
    #photo = "/static/ProfilesImages/1.png"
    if user['Роль'] == 'Репетитор':
        lessons = ''
        for les in user['Преподаваемые_предметы']:
            lessons += '<br>' + les
        htmlLessons = Markup(lessons)
        return render_template("tutorprofile.html", LastName = user['Фамилия'], FirstName = user['Имя'], BirthDay = user['День_рождения'], Education = user['Образование'], Experions = user['Стаж_преподавания_в_годах'], Phone = user['Телефон'], About = user['О_себе'], Lessons = htmlLessons, Photo = photo)
    else:
        lessons = ''
        for les in user['Изучаемые_предметы']:
            lessons += '<br>' + les
        htmlLessons = Markup(lessons)
        return render_template("profile.html", LastName = user['Фамилия'], FirstName = user['Имя'], BirthDay = user['День_рождения'], SchoolClass = user['Класс'], Phone = user['Телефон'], About = user['О_себе'], Lessons = htmlLessons, Photo = photo)

@app.route("/edit", methods=["post", "get"])
def edit():
    user = WorkWithDB.FoundUserInDatabaseForToken(request.cookies.get('token'))
    photo = "https://avatars.mds.yandex.net/get-pdb/216365/cafc6922-7989-4b22-b23d-36a495ce95a0/s1200"
    #photo = "/static/ProfilesImages/1.png"
    if request.method == "POST" and user['Роль'] == 'Репетитор':
        user['Фамилия'] = request.form.get("LastName")
        user['Имя'] = request.form.get("FirstName")
        birthday = request.form.get("date")
        birthdayInfo = birthday.split("-")
        user['День_рождения'] = birthdayInfo[2] + "." + birthdayInfo[1] + "." + birthdayInfo[0]
        user['Образование'] = request.form.get("education")
        user['Стаж_преподавания_в_годах'] = request.form.get("experience")
        lessons = []
        if request.form.get("math") == "b1":
            lessons.append("Математика")
        if request.form.get("rus") == "b2":
            lessons.append("Русский язык")
        if request.form.get("phys") == "b3":
            lessons.append("Физика")
        if request.form.get("inf") == "b4":
            lessons.append("Информатика")
        if request.form.get("chemistry") == "b5":
            lessons.append("Химия")
        if request.form.get("bio") == "b6":
            lessons.append("Биология")
        if request.form.get("history") == "b7":
            lessons.append("История")
        if request.form.get("social") == "b8":
            lessons.append("Обществознание")
        if request.form.get("literature") == "b9":
            lessons.append("Литература")
        if request.form.get("geo") == "b10":
            lessons.append("География")
        if request.form.get("economy") == "b11":
            lessons.append("Экономика")
        if request.form.get("eng") == "b12":
            lessons.append("Английский язык")
        if request.form.get("dutch") == "b13":
            lessons.append("Немецкий язык")
        if len(lessons) == 0:
            return render_template(
                "errorRegistration.html", errorMessage="Необходимо выбрать хотя бы один преподаваемый предмет!"
            )
        user['Преподаваемые_предметы'] = lessons
        user['Телефон'] = request.form.get("phone")
        user['О_себе'] = request.form.get("about")
        res = WorkWithDB.ChangeRecordInDatabase(user['Токен'], user)
        if res.isGood == False:
            return render_template("errorRegistration.html", errorMessage = res.getErrorMessage())
        return redirect("/profile")
    if request.method == "POST" and user['Роль'] == 'Ученик':
        user['Фамилия'] = request.form.get("LastName")
        user['Имя'] = request.form.get("FirstName")
        birthday = request.form.get("date")
        birthdayInfo = birthday.split("-")
        user['День_рождения'] = birthdayInfo[2] + "." + birthdayInfo[1] + "." + birthdayInfo[0]
        user['Класс'] = request.form.get("class")
        lessons = []
        if request.form.get("math") == "b1":
            lessons.append("Математика")
        if request.form.get("rus") == "b2":
            lessons.append("Русский язык")
        if request.form.get("phys") == "b3":
            lessons.append("Физика")
        if request.form.get("inf") == "b4":
            lessons.append("Информатика")
        if request.form.get("chemistry") == "b5":
            lessons.append("Химия")
        if request.form.get("bio") == "b6":
            lessons.append("Биология")
        if request.form.get("history") == "b7":
            lessons.append("История")
        if request.form.get("social") == "b8":
            lessons.append("Обществознание")
        if request.form.get("literature") == "b9":
            lessons.append("Литература")
        if request.form.get("geo") == "b10":
            lessons.append("География")
        if request.form.get("economy") == "b11":
            lessons.append("Экономика")
        if request.form.get("eng") == "b12":
            lessons.append("Английский язык")
        if request.form.get("dutch") == "b13":
            lessons.append("Немецкий язык")
        if len(lessons) == 0:
            return render_template(
                "errorRegistration.html", errorMessage="Необходимо выбрать хотя бы один изучаемый предмет!"
            )
        user['Изучаемые_предметы'] = lessons
        user['Телефон'] = request.form.get("phone")
        user['О_себе'] = request.form.get("about")
        res = WorkWithDB.ChangeRecordInDatabase(user['Токен'], user)
        if res.isGood == False:
            return render_template("errorRegistration.html", errorMessage = res.getErrorMessage())
        return redirect("/profile")

    if user == None:
        resp = make_response(redirect("/"))
        resp.set_cookie('token', '', expires = 0)
        return resp
    if user['Роль'] == 'Репетитор':
        studCHECK = ""
        aspirCHECK = ""
        teacherCHECK = ""
        prepodCHECK = ""
        if user['Образование'] == "Студент":
            studCHECK = "selected"
        if user['Образование'] == "Аспирант":
            aspirCHECK = "selected"
        if user['Образование'] == "Учитель":
            teacherCHECK = "selected"
        if user['Образование'] == "Преподаватель":
            prepodCHECK = "selected"
        LessChecks = ["" for i in range(13)]
        LessChecks[0] = "checked" if 'Математика' in user['Преподаваемые_предметы'] else ""
        LessChecks[1] = "checked" if 'Русский язык' in user['Преподаваемые_предметы'] else ""
        LessChecks[2] = "checked" if 'Физика' in user['Преподаваемые_предметы'] else ""
        LessChecks[3] = "checked" if 'Информатика' in user['Преподаваемые_предметы'] else ""
        LessChecks[4] = "checked" if 'Химия' in user['Преподаваемые_предметы'] else ""
        LessChecks[5] = "checked" if 'Биология' in user['Преподаваемые_предметы'] else ""
        LessChecks[6] = "checked" if 'История' in user['Преподаваемые_предметы'] else ""
        LessChecks[7] = "checked" if 'Обществознание' in user['Преподаваемые_предметы'] else ""
        LessChecks[8] = "checked" if 'Литература' in user['Преподаваемые_предметы'] else ""
        LessChecks[9] = "checked" if 'География' in user['Преподаваемые_предметы'] else ""
        LessChecks[10] = "checked" if 'Экономика' in user['Преподаваемые_предметы'] else ""
        LessChecks[11] = "checked" if 'Английский язык' in user['Преподаваемые_предметы'] else ""
        LessChecks[12] = "checked" if 'Немецкий язык' in user['Преподаваемые_предметы'] else ""
        birth = user['День_рождения'].split('.')
        birthInTemplate = birth[2] + "-" + birth[1] + "-" + birth[0]
        return render_template("edittutorprofile.html", LastName = user['Фамилия'], FirstName = user['Имя'], BirthDay = birthInTemplate, CHECK1 = studCHECK, CHECK2 = aspirCHECK, CHECK3 = teacherCHECK, CHECK4 = prepodCHECK, Exp = user['Стаж_преподавания_в_годах'], LESS1 = LessChecks[0], LESS2 = LessChecks[1], LESS3 = LessChecks[2], LESS4 = LessChecks[3], LESS5 = LessChecks[4], LESS6 = LessChecks[5], LESS7 = LessChecks[6], LESS8 = LessChecks[7], LESS9 = LessChecks[8], LESS10 = LessChecks[9], LESS11 = LessChecks[10], LESS12 = LessChecks[11], LESS13 = LessChecks[12], Phone = user['Телефон'], About = user['О_себе'], Photo = photo)
    else:
        birth = user['День_рождения'].split('.')
        birthInTemplate = birth[2] + "-" + birth[1] + "-" + birth[0]
        ClassChecks = ["" for i in range(11)]
        ClassChecks[0] = "selected" if user['Класс'] == "1" else ""
        ClassChecks[1] = "selected" if user['Класс'] == "2" else ""
        ClassChecks[2] = "selected" if user['Класс'] == "3" else ""
        ClassChecks[3] = "selected" if user['Класс'] == "4" else ""
        ClassChecks[4] = "selected" if user['Класс'] == "5" else ""
        ClassChecks[5] = "selected" if user['Класс'] == "6" else ""
        ClassChecks[6] = "selected" if user['Класс'] == "7" else ""
        ClassChecks[7] = "selected" if user['Класс'] == "8" else ""
        ClassChecks[8] = "selected" if user['Класс'] == "9" else ""
        ClassChecks[9] = "selected" if user['Класс'] == "10" else ""
        ClassChecks[10] = "selected" if user['Класс'] == "11" else ""
        LessChecks = ["" for i in range(13)]
        LessChecks[0] = "checked" if 'Математика' in user['Изучаемые_предметы'] else ""
        LessChecks[1] = "checked" if 'Русский язык' in user['Изучаемые_предметы'] else ""
        LessChecks[2] = "checked" if 'Физика' in user['Изучаемые_предметы'] else ""
        LessChecks[3] = "checked" if 'Информатика' in user['Изучаемые_предметы'] else ""
        LessChecks[4] = "checked" if 'Химия' in user['Изучаемые_предметы'] else ""
        LessChecks[5] = "checked" if 'Биология' in user['Изучаемые_предметы'] else ""
        LessChecks[6] = "checked" if 'История' in user['Изучаемые_предметы'] else ""
        LessChecks[7] = "checked" if 'Обществознание' in user['Изучаемые_предметы'] else ""
        LessChecks[8] = "checked" if 'Литература' in user['Изучаемые_предметы'] else ""
        LessChecks[9] = "checked" if 'География' in user['Изучаемые_предметы'] else ""
        LessChecks[10] = "checked" if 'Экономика' in user['Изучаемые_предметы'] else ""
        LessChecks[11] = "checked" if 'Английский язык' in user['Изучаемые_предметы'] else ""
        LessChecks[12] = "checked" if 'Немецкий язык' in user['Изучаемые_предметы'] else ""
        return render_template("editStudentProfile.html", LastName = user['Фамилия'], FirstName = user['Имя'], BirthDay = birthInTemplate, CHECK1 = ClassChecks[0], CHECK2 = ClassChecks[1], CHECK3 = ClassChecks[2], CHECK4 = ClassChecks[3], CHECK5 = ClassChecks[4], CHECK6 = ClassChecks[5], CHECK7 = ClassChecks[6], CHECK8 = ClassChecks[7], CHECK9 = ClassChecks[8], CHECK10 = ClassChecks[9], CHECK11 = ClassChecks[10], LESS1 = LessChecks[0], LESS2 = LessChecks[1], LESS3 = LessChecks[2], LESS4 = LessChecks[3], LESS5 = LessChecks[4], LESS6 = LessChecks[5], LESS7 = LessChecks[6], LESS8 = LessChecks[7], LESS9 = LessChecks[8], LESS10 = LessChecks[9], LESS11 = LessChecks[10], LESS12 = LessChecks[11], LESS13 = LessChecks[12], Phone = user['Телефон'], About = user['О_себе'], Photo = photo)

if __name__ == "__main__":
    app.run()
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=8080)
