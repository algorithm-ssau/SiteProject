import os, hashlib, json, codecs
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
from bot import BotGraf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/ProfilesImages/'

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route("/", methods=["post", "get"])
def login():
    token = request.cookies.get('token')
    if token != None:
        return redirect("/welcome")
    if request.method == "POST":
        login = request.form.get("email")
        password = request.form.get("psw")
        user = WorkWithDB.FoundUserInDatabase(login, password)
        if user == None:
            return render_template("errorRegistration.html", errorMessage="Ошибка входа!")
        resp = make_response(redirect("/welcome"))
        resp.set_cookie('token', user['Токен'], max_age=60*60*24*365*2)
        if user['Город'] == 'SAMARA':
            resp.set_cookie('citycode', '0', max_age=60*60*24*365*2)
        elif user['Город'] == 'MOSCOW':
            resp.set_cookie('citycode', '1', max_age=60*60*24*365*2)
        elif user['Город'] == 'KAZAN':
            resp.set_cookie('citycode', '2', max_age=60*60*24*365*2)
        elif user['Город'] == 'KRASNOYARSK':
            resp.set_cookie('citycode', '3', max_age=60*60*24*365*2)
        elif user['Город'] == 'SOCHI':
            resp.set_cookie('citycode', '4', max_age=60*60*24*365*2)
        elif user['Город'] == 'SARANSK':
            resp.set_cookie('citycode', '5', max_age=60*60*24*365*2)
        return resp
    return render_template("login.html")

@app.route("/welcome", methods=["post", "get"])
def welcome():
    token = request.cookies.get('token')
    if token != None:
        user = WorkWithDB.FoundUserInDatabaseForToken(request.cookies.get('token'))
        if user == None:
            resp = make_response(redirect("/"))
            resp.set_cookie('token', '', expires = 0)
            resp.set_cookie('citycode', '', expires = 0)
            return resp
        if user['Роль'] == 'Репетитор':
            return render_template("welcomeTutor.html")
        else:
            return render_template("welcomeStudent.html")
    else:
        resp = make_response(redirect("/"))
        resp.set_cookie('token', '', expires = 0)
        resp.set_cookie('citycode', '', expires = 0)
        return resp

    
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
        user.update({"Класс": int(request.form.get("class"))})
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
        user.update({"Фотография": "Стандарт"})
        res = WorkWithDB.AddToDatabase(city, False, user)
        if res.isGood == False:
            return render_template(
                "errorRegistration.html", errorMessage=res.getErrorMessage()
            )
        resp = make_response(redirect("/welcome"))
        resp.set_cookie('token', res.getErrorMessage(), max_age=60*60*24*365*2)
        if user['Город'] == 'SAMARA':
            resp.set_cookie('citycode', '0', max_age=60*60*24*365*2)
        elif user['Город'] == 'MOSCOW':
            resp.set_cookie('citycode', '1', max_age=60*60*24*365*2)
        elif user['Город'] == 'KAZAN':
            resp.set_cookie('citycode', '2', max_age=60*60*24*365*2)
        elif user['Город'] == 'KRASNOYARSK':
            resp.set_cookie('citycode', '3', max_age=60*60*24*365*2)
        elif user['Город'] == 'SOCHI':
            resp.set_cookie('citycode', '4', max_age=60*60*24*365*2)
        elif user['Город'] == 'SARANSK':
            resp.set_cookie('citycode', '5', max_age=60*60*24*365*2)
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
        user.update({"Стаж_преподавания_в_годах": int(request.form.get("experience"))})
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
        user.update({"Ставка_в_час": int(request.form.get("rate"))})
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
        user.update({"Фотография": "Стандарт"})
        res = WorkWithDB.AddToDatabase(city, True, user)
        if res.isGood == False:
            return render_template(
                "errorRegistration.html", errorMessage=res.getErrorMessage()
            )
        resp = make_response(redirect("/welcome"))
        resp.set_cookie('token', res.getErrorMessage(), max_age=60*60*24*365*2)
        if user['Город'] == 'SAMARA':
            resp.set_cookie('citycode', '0', max_age=60*60*24*365*2)
        elif user['Город'] == 'MOSCOW':
            resp.set_cookie('citycode', '1', max_age=60*60*24*365*2)
        elif user['Город'] == 'KAZAN':
            resp.set_cookie('citycode', '2', max_age=60*60*24*365*2)
        elif user['Город'] == 'KRASNOYARSK':
            resp.set_cookie('citycode', '3', max_age=60*60*24*365*2)
        elif user['Город'] == 'SOCHI':
            resp.set_cookie('citycode', '4', max_age=60*60*24*365*2)
        elif user['Город'] == 'SARANSK':
            resp.set_cookie('citycode', '5', max_age=60*60*24*365*2)
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
    photo = ""
    user = WorkWithDB.FoundUserInDatabaseForToken(request.cookies.get('token'))
    if user == None:
        resp = make_response(redirect("/"))
        resp.set_cookie('token', '', expires = 0)
        resp.set_cookie('citycode', '', expires = 0)
        return resp
    if user['Фотография'] == 'Стандарт':
        photo = "https://api.adorable.io/avatars/234/" + str(user['ID'])
    else:
        photo = "/images/" + str(user['ID']) + ".png"
    if user['Роль'] == 'Репетитор':
        lessons = ''
        for les in user['Преподаваемые_предметы']:
            lessons += '<br>' + les
        htmlLessons = Markup(lessons)
        formatLessons = ''
        for forLes in user['Формат_занятий']:
            formatLessons += '<br>' + forLes
        htmlFormatLessons = Markup(formatLessons)
        viewsLessons = ''
        for viewLes in user['Вид_занятий']:
            viewsLessons += '<br>' + viewLes
        htmlViewsLessons = Markup(viewsLessons)
        return render_template("tutorProfile.html", LastName = user['Фамилия'], FirstName = user['Имя'], BirthDay = user['День_рождения'], Education = user['Образование'], Experions = str(user['Стаж_преподавания_в_годах']), Phone = user['Телефон'], About = user['О_себе'], Lessons = htmlLessons, FormatLessons = htmlFormatLessons, ViewsLessons = htmlViewsLessons, Price = str(user['Ставка_в_час']), Photo = photo, Button = "Редактировать информацию", DoCode = "document.location.href = '/edit'")
    else:
        lessons = ''
        for les in user['Изучаемые_предметы']:
            lessons += '<br>' + les
        htmlLessons = Markup(lessons)
        formatLes = ''
        for Fles in user['Формат_занятий']:
            formatLes += '<br>' + Fles
        htmlFormat = Markup(formatLes)
        return render_template("studentProfile.html", LastName = user['Фамилия'], FirstName = user['Имя'], BirthDay = user['День_рождения'], SchoolClass = str(user['Класс']), Phone = user['Телефон'], About = user['О_себе'], Lessons = htmlLessons, Format = htmlFormat, Photo = photo, Button = "Редактировать информацию", DoCode = "document.location.href = '/edit'")

@app.route("/edit", methods=["post", "get"])
def edit():
    user = WorkWithDB.FoundUserInDatabaseForToken(request.cookies.get('token'))
    if user == None:
        resp = make_response(redirect("/"))
        resp.set_cookie('token', '', expires = 0)
        resp.set_cookie('citycode', '', expires = 0)
        return resp
    photo = ""
    if user['Фотография'] == 'Стандарт':
        photo = "https://api.adorable.io/avatars/234/" + str(user['ID'])
    else:
        photo = "/images/" + str(user['ID']) + ".png"
    if request.method == "POST" and user['Роль'] == 'Репетитор':
        variablePhoto = request.files['file']
        if variablePhoto.filename != '':
            filename = str(user['ID']) + '.png'
            variablePhoto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user['Фотография'] = "Загружена"
        user['Фамилия'] = request.form.get("LastName")
        user['Имя'] = request.form.get("FirstName")
        birthday = request.form.get("date")
        birthdayInfo = birthday.split("-")
        user['День_рождения'] = birthdayInfo[2] + "." + birthdayInfo[1] + "." + birthdayInfo[0]
        user['Образование'] = request.form.get("education")
        user['Стаж_преподавания_в_годах'] = int(request.form.get("experience"))
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
        formatsLes = []
        if request.form.get("option1") == "a1":
            formatsLes.append("Еду к ученику")
        if request.form.get("option2") == "a2":
            formatsLes.append("Ученик ко мне")
        if request.form.get("option3") == "a3":
            formatsLes.append("Дистанционно")
        if len(formatsLes) == 0:
            return render_template(
                "errorRegistration.html", errorMessage="Необходимо выбрать хотя бы один формат занятий!"
            )
        user['Формат_занятий'] = formatsLes
        viewsLes = []
        if request.form.get("single") == "c1":
            viewsLes.append("Разовые")
        if request.form.get("group") == "c2":
            viewsLes.append("Групповые")
        if request.form.get("home") == "c3":
            viewsLes.append("Помощь с домашкой")
        if request.form.get("usual") == "c4":
            viewsLes.append("Обычные")
        if len(viewsLes) == 0:
            return render_template(
                "errorRegistration.html", errorMessage="Необходимо выбрать хотя бы один вид занятий!"
            )
        user['Вид_занятий'] = viewsLes
        user['Ставка_в_час'] = int(request.form.get("rate"))
        psw = request.form.get("psw")
        if psw != '':
            hash_object = hashlib.sha512(psw.encode())
            user['Пароль'] = hash_object.hexdigest()
        user['Телефон'] = request.form.get("phone")
        user['О_себе'] = request.form.get("about")
        res = WorkWithDB.ChangeRecordInDatabase(user['Токен'], user)
        if res.isGood == False:
            return render_template("errorRegistration.html", errorMessage = res.getErrorMessage())
        return redirect("/profile")
    if request.method == "POST" and user['Роль'] == 'Ученик':
        variablePhoto = request.files['file']
        if variablePhoto.filename != '':
            filename = str(user['ID']) + '.png'
            variablePhoto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user['Фотография'] = "Загружена"
        user['Фамилия'] = request.form.get("LastName")
        user['Имя'] = request.form.get("FirstName")
        birthday = request.form.get("date")
        birthdayInfo = birthday.split("-")
        user['День_рождения'] = birthdayInfo[2] + "." + birthdayInfo[1] + "." + birthdayInfo[0]
        user['Класс'] = int(request.form.get("class"))
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
        formatLes = []
        if request.form.get("option1") == "a1":
            formatLes.append("Еду к преподавателю")
        if request.form.get("option2") == "a2":
            formatLes.append("Преподаватель ко мне")
        if request.form.get("option3") == "a3":
            formatLes.append("Дистанционно")
        if len(formatLes) == 0:
            return render_template(
                "errorRegistration.html", errorMessage="Необходимо выбрать хотя бы один вид формата занятий!"
            )
        user['Формат_занятий'] = formatLes
        user['Телефон'] = request.form.get("phone")
        user['О_себе'] = request.form.get("about")
        psw = request.form.get("psw")
        if psw != '':
            hash_object = hashlib.sha512(psw.encode())
            user['Пароль'] = hash_object.hexdigest()
        res = WorkWithDB.ChangeRecordInDatabase(user['Токен'], user)
        if res.isGood == False:
            return render_template("errorRegistration.html", errorMessage = res.getErrorMessage())
        return redirect("/profile")

    if user == None:
        resp = make_response(redirect("/"))
        resp.set_cookie('token', '', expires = 0)
        resp.set_cookie('citycode', '', expires = 0)
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
        FormatChecks = ["" for i in range(3)]
        FormatChecks[0] = "checked" if 'Еду к ученику' in user['Формат_занятий'] else ""
        FormatChecks[1] = "checked" if 'Ученик ко мне' in user['Формат_занятий'] else ""
        FormatChecks[2] = "checked" if 'Дистанционно' in user['Формат_занятий'] else ""
        ViewChecks = ["" for i in range(4)]
        ViewChecks[0] = "checked" if 'Разовые' in user['Вид_занятий'] else ""
        ViewChecks[1] = "checked" if 'Групповые' in user['Вид_занятий'] else ""
        ViewChecks[2] = "checked" if 'Помощь с домашкой' in user['Вид_занятий'] else ""
        ViewChecks[3] = "checked" if 'Обычные' in user['Вид_занятий'] else ""
        return render_template("editTutor.html", LastName = user['Фамилия'], FirstName = user['Имя'], BirthDay = birthInTemplate, CHECK1 = studCHECK, CHECK2 = aspirCHECK, CHECK3 = teacherCHECK, CHECK4 = prepodCHECK, Exp = str(user['Стаж_преподавания_в_годах']), LESS1 = LessChecks[0], LESS2 = LessChecks[1], LESS3 = LessChecks[2], LESS4 = LessChecks[3], LESS5 = LessChecks[4], LESS6 = LessChecks[5], LESS7 = LessChecks[6], LESS8 = LessChecks[7], LESS9 = LessChecks[8], LESS10 = LessChecks[9], LESS11 = LessChecks[10], LESS12 = LessChecks[11], LESS13 = LessChecks[12], FORM1 = FormatChecks[0], FORM2 = FormatChecks[1], FORM3 = FormatChecks[2], VIEW1 = ViewChecks[0], VIEW2 = ViewChecks[1], VIEW3 = ViewChecks[2], VIEW4 = ViewChecks[3], Price = str(user['Ставка_в_час']), Phone = user['Телефон'], About = user['О_себе'], Photo = photo)
    else:
        birth = user['День_рождения'].split('.')
        birthInTemplate = birth[2] + "-" + birth[1] + "-" + birth[0]
        ClassChecks = ["" for i in range(11)]
        ClassChecks[0] = "selected" if user['Класс'] == 1 else ""
        ClassChecks[1] = "selected" if user['Класс'] == 2 else ""
        ClassChecks[2] = "selected" if user['Класс'] == 3 else ""
        ClassChecks[3] = "selected" if user['Класс'] == 4 else ""
        ClassChecks[4] = "selected" if user['Класс'] == 5 else ""
        ClassChecks[5] = "selected" if user['Класс'] == 6 else ""
        ClassChecks[6] = "selected" if user['Класс'] == 7 else ""
        ClassChecks[7] = "selected" if user['Класс'] == 8 else ""
        ClassChecks[8] = "selected" if user['Класс'] == 9 else ""
        ClassChecks[9] = "selected" if user['Класс'] == 10 else ""
        ClassChecks[10] = "selected" if user['Класс'] == 11 else ""
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
        FormatChecks = ["" for i in range(3)]
        FormatChecks[0] = "checked" if 'Еду к преподавателю' in user['Формат_занятий'] else ""
        FormatChecks[1] = "checked" if 'Преподаватель ко мне' in user['Формат_занятий'] else ""
        FormatChecks[2] = "checked" if 'Дистанционно' in user['Формат_занятий'] else ""
        return render_template("editStudent.html", LastName = user['Фамилия'], FirstName = user['Имя'], BirthDay = birthInTemplate, CHECK1 = ClassChecks[0], CHECK2 = ClassChecks[1], CHECK3 = ClassChecks[2], CHECK4 = ClassChecks[3], CHECK5 = ClassChecks[4], CHECK6 = ClassChecks[5], CHECK7 = ClassChecks[6], CHECK8 = ClassChecks[7], CHECK9 = ClassChecks[8], CHECK10 = ClassChecks[9], CHECK11 = ClassChecks[10], LESS1 = LessChecks[0], LESS2 = LessChecks[1], LESS3 = LessChecks[2], LESS4 = LessChecks[3], LESS5 = LessChecks[4], LESS6 = LessChecks[5], LESS7 = LessChecks[6], LESS8 = LessChecks[7], LESS9 = LessChecks[8], LESS10 = LessChecks[9], LESS11 = LessChecks[10], LESS12 = LessChecks[11], LESS13 = LessChecks[12], FORMAT1 = FormatChecks[0], FORMAT2 = FormatChecks[1], FORMAT3 = FormatChecks[2], Phone = user['Телефон'], About = user['О_себе'], Photo = photo)

@app.route("/search")
def search():
    user = WorkWithDB.FoundUserInDatabaseForToken(request.cookies.get('token'))
    if user == None:
        resp = make_response(redirect("/"))
        resp.set_cookie('token', '', expires = 0)
        resp.set_cookie('citycode', '', expires = 0)
        return resp
    if user['Роль'] == 'Репетитор':
        return render_template("searchStudent.html")
    else:
        return render_template("searchTutor.html")

@app.route("/messages")
def messages():
    user = WorkWithDB.FoundUserInDatabaseForToken(request.cookies.get('token'))
    if user == None:
        resp = make_response(redirect("/"))
        resp.set_cookie('token', '', expires = 0)
        resp.set_cookie('citycode', '', expires = 0)
        return resp
    ids = WorkWithDB.foundAllUsersDialog(user['ID'])
    resUSERS = ''
    if user['Роль'] == 'Репетитор':
        f = codecs.open('static/prefabs/prefabUserInTutorDialogs.html', encoding='utf-8', mode='r')
        prefab = f.read()
        f.close()
        if ids != None and len(ids) != 0:
            for idUser in ids:
                if idUser == -100:
                    continue
                prefabTEMP = prefab
                userM = WorkWithDB.FoundUserInDatabaseForID(idUser)
                if userM['Фотография'] == 'Стандарт':
                    photo = "https://api.adorable.io/avatars/234/" + str(userM['ID'])
                else:
                    photo = "/images/" + str(userM['ID']) + ".png"
                prefabTEMP = prefabTEMP.replace('{{PHOTO}}', photo)
                name = userM['Фамилия'] + ' ' + userM['Имя'][0] + '.'
                prefabTEMP = prefabTEMP.replace('{{NAME}}', name)
                prefabTEMP = prefabTEMP.replace('{{URL}}', '/messages?to=' + str(userM['ID']))
                resUSERS += prefabTEMP

        #БОТ:
        prefabTEMP = prefab
        photo = "/images/bot.jpg"
        prefabTEMP = prefabTEMP.replace('{{PHOTO}}', photo)
        name = "Бот Тимоха"
        prefabTEMP = prefabTEMP.replace('{{NAME}}', name)
        prefabTEMP = prefabTEMP.replace('{{URL}}', '/messages?to=bot')
        resUSERS += prefabTEMP
        #/БОТ
        
        idnow = request.args.get('to')
        userinfo = ''
        counter = ''
        photo2 = '<img class="usersinmessager" src="{{PHOTO}}">'

        f = codecs.open('static/prefabs/prefabUserMessageInfo.html', encoding='utf-8', mode='r')
        prefab = f.read()
        f.close()

        allMessages = ''

        toid = -1
        
        if idnow == None:
            userinfo = 'Выберите собеседника'
            counter = 'слева'
            photo2 = ''
        else:
            if idnow != 'bot':
                userM = WorkWithDB.FoundUserInDatabaseForID(idnow)
                toid = userM['ID']
                messages = WorkWithDB.getMessage(999, user['ID'], int(idnow)).listRes
                userinfo = 'Чат с ' + userM['Фамилия'] + ' ' + userM['Имя']
                counter = 'Всего ' + str(len(messages)) + ' сообщений'
                if userM['Фотография'] == 'Стандарт':
                    photo2 = photo2.replace('{{PHOTO}}', "https://api.adorable.io/avatars/234/" + str(userM['ID']))
                else:
                    photo2 = photo2.replace('{{PHOTO}}', "/images/" + str(userM['ID']) + ".png")
                if len(messages) != 0:
                    messages.reverse()
                    f = codecs.open('static/prefabs/prefabmesend.html', encoding='utf-8', mode='r')
                    prefabme = f.read()
                    f.close()
                    f = codecs.open('static/prefabs/prefabIsend.html', encoding='utf-8', mode='r')
                    prefabI = f.read()
                    f.close()
                    for mes in messages:
                        if mes['От'] == user['ID']:
                            prefabTEMP = prefabI
                            prefabTEMP = prefabTEMP.replace('{{DATE}}', mes['Дата и время'])
                            prefabTEMP = prefabTEMP.replace('{{MESSAGE}}', mes['Сообщение'])
                        else:
                            prefabTEMP = prefabme
                            prefabTEMP = prefabTEMP.replace('{{DATE}}', mes['Дата и время'])
                            prefabTEMP = prefabTEMP.replace('{{MESSAGE}}', mes['Сообщение'])
                            prefabTEMP = prefabTEMP.replace('{{NAME}}', userM['Имя'])
                        allMessages += prefabTEMP
            else:
                toid = -100
                messages = WorkWithDB.getMessage(999, user['ID'], -100).listRes
                userinfo = 'Чат с Тимохой!'
                counter = 'Всего ' + str(len(messages)) + ' сообщений'
                photo2 = photo2.replace('{{PHOTO}}', "/images/bot.jpg")
                if len(messages) != 0:
                    messages.reverse()
                    f = codecs.open('static/prefabs/prefabmesend.html', encoding='utf-8', mode='r')
                    prefabme = f.read()
                    f.close()
                    f = codecs.open('static/prefabs/prefabIsend.html', encoding='utf-8', mode='r')
                    prefabI = f.read()
                    f.close()
                    for mes in messages:
                        if mes['От'] == user['ID']:
                            prefabTEMP = prefabI
                            prefabTEMP = prefabTEMP.replace('{{DATE}}', mes['Дата и время'])
                            prefabTEMP = prefabTEMP.replace('{{MESSAGE}}', mes['Сообщение'])
                        else:
                            prefabTEMP = prefabme
                            prefabTEMP = prefabTEMP.replace('{{DATE}}', mes['Дата и время'])
                            prefabTEMP = prefabTEMP.replace('{{MESSAGE}}', mes['Сообщение'])
                            prefabTEMP = prefabTEMP.replace('{{NAME}}', 'Тимоха')
                        allMessages += prefabTEMP


        
        
        prefab = prefab.replace('{{WITH}}', userinfo)
        prefab = prefab.replace('{{COUNT}}', counter)
        prefab = prefab.replace('{{PHOTO}}', photo2)
        userNow = prefab


            
        return render_template("tutorMessages.html", USERS = Markup(resUSERS), ItUser = Markup(userNow), MESSAGES = Markup(allMessages), TOID = toid)
    else:
        f = codecs.open('static/prefabs/prefabUserInStudentDialogs.html', encoding='utf-8', mode='r')
        prefab = f.read()
        f.close()
        if ids != None and len(ids) != 0:
            for idUser in ids:
                if idUser == -100:
                    continue
                prefabTEMP = prefab
                userM = WorkWithDB.FoundUserInDatabaseForID(idUser)
                if userM['Фотография'] == 'Стандарт':
                    photo = "https://api.adorable.io/avatars/234/" + str(userM['ID'])
                else:
                    photo = "/images/" + str(userM['ID']) + ".png"
                prefabTEMP = prefabTEMP.replace('{{PHOTO}}', photo)
                name = userM['Фамилия'] + ' ' + userM['Имя'][0] + '.'
                prefabTEMP = prefabTEMP.replace('{{NAME}}', name)
                prefabTEMP = prefabTEMP.replace('{{URL}}', '/messages?to=' + str(userM['ID']))
                resUSERS += prefabTEMP


        #БОТ:
        prefabTEMP = prefab
        photo = "/images/bot.jpg"
        prefabTEMP = prefabTEMP.replace('{{PHOTO}}', photo)
        name = "Бот Тимоха"
        prefabTEMP = prefabTEMP.replace('{{NAME}}', name)
        prefabTEMP = prefabTEMP.replace('{{URL}}', '/messages?to=bot')
        resUSERS += prefabTEMP
        #/БОТ

        idnow = request.args.get('to')
        userinfo = ''
        counter = ''
        photo2 = '<img class="usersinmessager" src="{{PHOTO}}">'

        f = codecs.open('static/prefabs/prefabUserMessageInfo.html', encoding='utf-8', mode='r')
        prefab = f.read()
        f.close()
        
        allMessages = ''

        toid = -1

        if idnow == None:
            userinfo = 'Выберите собеседника'
            counter = 'слева'
            photo2 = ''
        else:
            if idnow != 'bot':
                userM = WorkWithDB.FoundUserInDatabaseForID(idnow)
                toid = userM['ID']
                messages = WorkWithDB.getMessage(999, user['ID'], int(idnow)).listRes
                userinfo = 'Чат с ' + userM['Фамилия'] + ' ' + userM['Имя']
                counter = 'Всего ' + str(len(messages)) + ' сообщений'
                if userM['Фотография'] == 'Стандарт':
                    photo2 = photo2.replace('{{PHOTO}}', "https://api.adorable.io/avatars/234/" + str(userM['ID']))
                else:
                    photo2 = photo2.replace('{{PHOTO}}', "/images/" + str(userM['ID']) + ".png")

                if len(messages) != 0:
                    messages.reverse()
                    f = codecs.open('static/prefabs/prefabmesend.html', encoding='utf-8', mode='r')
                    prefabme = f.read()
                    f.close()
                    f = codecs.open('static/prefabs/prefabIsend.html', encoding='utf-8', mode='r')
                    prefabI = f.read()
                    f.close()
                    for mes in messages:
                        if mes['От'] == user['ID']:
                            prefabTEMP = prefabI
                            prefabTEMP = prefabTEMP.replace('{{DATE}}', mes['Дата и время'])
                            prefabTEMP = prefabTEMP.replace('{{MESSAGE}}', mes['Сообщение'])
                        else:
                            prefabTEMP = prefabme
                            prefabTEMP = prefabTEMP.replace('{{DATE}}', mes['Дата и время'])
                            prefabTEMP = prefabTEMP.replace('{{MESSAGE}}', mes['Сообщение'])
                            prefabTEMP = prefabTEMP.replace('{{NAME}}', userM['Имя'])
                        allMessages += prefabTEMP

            else:
                toid = -100
                messages = WorkWithDB.getMessage(999, user['ID'], -100).listRes
                userinfo = 'Чат с Тимохой!'
                counter = 'Всего ' + str(len(messages)) + ' сообщений'
                photo2 = photo2.replace('{{PHOTO}}', "/images/bot.jpg")
                if len(messages) != 0:
                    messages.reverse()
                    f = codecs.open('static/prefabs/prefabmesend.html', encoding='utf-8', mode='r')
                    prefabme = f.read()
                    f.close()
                    f = codecs.open('static/prefabs/prefabIsend.html', encoding='utf-8', mode='r')
                    prefabI = f.read()
                    f.close()
                    for mes in messages:
                        if mes['От'] == user['ID']:
                            prefabTEMP = prefabI
                            prefabTEMP = prefabTEMP.replace('{{DATE}}', mes['Дата и время'])
                            prefabTEMP = prefabTEMP.replace('{{MESSAGE}}', mes['Сообщение'])
                        else:
                            prefabTEMP = prefabme
                            prefabTEMP = prefabTEMP.replace('{{DATE}}', mes['Дата и время'])
                            prefabTEMP = prefabTEMP.replace('{{MESSAGE}}', mes['Сообщение'])
                            prefabTEMP = prefabTEMP.replace('{{NAME}}', 'Тимоха')
                        allMessages += prefabTEMP
        
        prefab = prefab.replace('{{WITH}}', userinfo)
        prefab = prefab.replace('{{COUNT}}', counter)
        prefab = prefab.replace('{{PHOTO}}', photo2)
        userNow = prefab
        return render_template("studentMessages.html", USERS = Markup(resUSERS), ItUser = Markup(userNow), MESSAGES = Markup(allMessages), TOID = toid)

@app.route("/prefabs/teacher")
def templateteacher():
    f = codecs.open('static/prefabs/prefabResultWithTeacher.html', encoding='utf-8', mode='r')
    text = f.read()
    f.close()
    return text

@app.route("/prefabs/student")
def templatestudent():
    f = codecs.open('static/prefabs/prefabResultWithStudent.html', encoding='utf-8', mode='r')
    text = f.read()
    f.close()
    return text

@app.route("/prefabs/timetable")
def templatetimetable():
    f = codecs.open('static/prefabs/prefabSchedule.html', encoding='utf-8', mode='r')
    text = f.read()
    f.close()
    return text

@app.route("/api/sendmessage", methods=["post"])
def sendmess():
    message = request.form.get('mes')
    fromtoken = request.form.get('token')
    toid = request.form.get('to')
    user = WorkWithDB.FoundUserInDatabaseForToken(fromtoken)
    if user != None:
        WorkWithDB.sendMessege(user['ID'], int(toid), message)
        if toid == '-100':
            mesBot = BotGraf(user['ID'], message)
            WorkWithDB.sendMessege(-100, user['ID'], mesBot)
        return '1'
    return '0'

@app.route("/api/getmessagesize")
def getmessagesize():
    token = request.args.get('token')
    toid = request.args.get('toid')
    user = WorkWithDB.FoundUserInDatabaseForToken(token)
    if user != None:
        mes = WorkWithDB.getMessage(999, user['ID'], int(toid)).listRes
        return str(len(mes))
    return '-1'

@app.route("/api/newnote")
def newnoteapi():
    token = request.args.get('token')
    user = WorkWithDB.FoundUserInDatabaseForToken(token)
    if user != None:
        node = {'ID': user['ID']}
        node.update({'Дата': ''})
        node.update({'Предмет': ''})
        return(WorkWithDB.NewNode(node).getErrorMessage())
    return '-1'

@app.route("/api/savenotes", methods=["post"])
def savenoteapi():
    token = request.form.get('token')
    user = WorkWithDB.FoundUserInDatabaseForToken(token)
    if user != None:
        nodes = WorkWithDB.FindNode(user['ID']).listRes
        for node in nodes:
            idnow = node['idNote']
            date = request.form.get('date_'+str(idnow))
            mes = request.form.get('lesson_'+str(idnow))
            if date == '' and mes == '':
                WorkWithDB.DeleteNote(node)
                continue
            node['Дата'] = date
            node['Предмет'] = mes
            WorkWithDB.UpdateNode(node)
        return '0'
    return '-1'

@app.route("/api/found/teacher/")
def foundTeacher():
    _filter = {}
    cityinput = request.args.get('city')
    if cityinput == None:
        return "arg 'city' not found!"
    cityINT = int(cityinput)
    city = '-'
    if cityINT == 0:
        city = 'SAMARA'
    if cityINT == 1:
        city = 'MOSCOW'
    if cityINT == 2:
        city = 'KAZAN'
    if cityINT == 3:
        city = 'KRASNOYARSK'
    if cityINT == 4:
        city = 'SOCHI'
    if cityINT == 5:
        city = 'SARANSK'
    if city == '-':
        return "arg 'city' have a bad code!"
    
    expMin = request.args.get('expmin')
    expMax = request.args.get('expmax')
    if expMin != None and expMax != None:
        _filter.update({'Стаж_преподавания_в_годах': {"$gte": int(expMin), "$lte": int(expMax)}})
    elif expMin != None:
        _filter.update({'Стаж_преподавания_в_годах': {"$gte": int(expMin)}})
    elif expMax != None:
        _filter.update({'Стаж_преподавания_в_годах': {"$lte": int(expMax)}})
    
    stot = request.args.get('stot')
    ttos = request.args.get('ttos')
    distance = request.args.get('distance')
    formatLes = []
    if stot == '1':
        formatLes.append("Ученик ко мне")
    if ttos == '1':
        formatLes.append("Еду к ученику")
    if distance == '1':
        formatLes.append("Дистанционно")
    if len(formatLes) != 0:
        _filter.update({'Формат_занятий': { "$all" : formatLes }})

    math = request.args.get('math')
    rus = request.args.get('rus')
    phys = request.args.get('phys')
    inf = request.args.get('inf')
    chemistry = request.args.get('chemistry')
    bio = request.args.get('bio')
    history = request.args.get('history')
    social = request.args.get('social')
    literature = request.args.get('literature')
    geo = request.args.get('geo')
    economy = request.args.get('economy')
    eng = request.args.get('eng')
    dutch = request.args.get('dutch')
    lessons = []
    if math == '1':
        lessons.append("Математика")
    if rus == '1':
        lessons.append("Русский язык")
    if phys == '1':
        lessons.append("Физика")
    if inf == '1':
        lessons.append("Информатика")
    if chemistry == '1':
        lessons.append("Химия")
    if bio == '1':
        lessons.append("Биология")
    if history == '1':
        lessons.append("История")
    if social == '1':
        lessons.append("Обществознание")
    if literature == '1':
        lessons.append("Литература")
    if geo == '1':
        lessons.append("География")
    if economy == '1':
        lessons.append("Экономика")
    if eng == '1':
        lessons.append("Английский язык")
    if dutch == '1':
        lessons.append("Немецкий язык")
    if len(lessons) != 0:
        _filter.update({'Преподаваемые_предметы': { "$all" : lessons }})
    

    rateMin = request.args.get('ratemin')
    rateMax = request.args.get('ratemax')
    if rateMin != None and rateMax != None:
        _filter.update({'Ставка_в_час': {"$gte": int(rateMin), "$lte": int(rateMax)}})
    elif rateMin != None:
        _filter.update({'Ставка_в_час': {"$gte": int(rateMin)}})
    elif rateMax != None:
        _filter.update({'Ставка_в_час': {"$lte": int(rateMax)}})

    edstudent = request.args.get('edstudent')
    edaspir = request.args.get('edaspir')
    edteacher = request.args.get('edteacher')
    edprepod = request.args.get('edprepod')
    education = []
    if edstudent == '1':
        education.append("Студент")
    if edaspir == '1':
        education.append("Аспирант")
    if edteacher == '1':
        education.append("Учитель")
    if edprepod == '1':
        education.append("Преподаватель")
    if len(education) != 0:
        _filter.update({'Образование': {"$in": education}})

    sex = request.args.get('sex')
    if sex == 'm':
        _filter.update({"Пол": "Мужской"})
    elif sex == 'w':
        _filter.update({"Пол": "Женский"})

    res = WorkWithDB.GetRecordOnFilter(city, _filter, False)
    if res.isGood == False:
        return 'Bad request'
    return json.dumps(res.listRes, ensure_ascii=False)

@app.route("/api/found/student/")
def foundStudent():
    _filter = {}
    cityinput = request.args.get('city')
    if cityinput == None:
        return "arg 'city' not found!"
    cityINT = int(cityinput)
    city = '-'
    if cityINT == 0:
        city = 'SAMARA'
    if cityINT == 1:
        city = 'MOSCOW'
    if cityINT == 2:
        city = 'KAZAN'
    if cityINT == 3:
        city = 'KRASNOYARSK'
    if cityINT == 4:
        city = 'SOCHI'
    if cityINT == 5:
        city = 'SARANSK'
    if city == '-':
        return "arg 'city' have a bad code!"

    classMin = request.args.get('classmin')
    classMax = request.args.get('classmax')
    if classMin != None and classMax != None:
        _filter.update({'Класс': {"$gte": int(classMin), "$lte": int(classMax)}})
    elif classMin != None:
        _filter.update({'Класс': {"$gte": int(classMin)}})
    elif classMax != None:
        _filter.update({'Класс': {"$lte": int(classMax)}})

    sex = request.args.get('sex')
    if sex == 'm':
        _filter.update({"Пол": "Мужской"})
    elif sex == 'w':
        _filter.update({"Пол": "Женский"})

    stot = request.args.get('stot')
    ttos = request.args.get('ttos')
    distance = request.args.get('distance')
    formatLes = []
    if stot == '1':
        formatLes.append("Еду к преподавателю")
    if ttos == '1':
        formatLes.append("Преподаватель ко мне")
    if distance == '1':
        formatLes.append("Дистанционно")
    if len(formatLes) != 0:
        _filter.update({'Формат_занятий': { "$all" : formatLes }})

    math = request.args.get('math')
    rus = request.args.get('rus')
    phys = request.args.get('phys')
    inf = request.args.get('inf')
    chemistry = request.args.get('chemistry')
    bio = request.args.get('bio')
    history = request.args.get('history')
    social = request.args.get('social')
    literature = request.args.get('literature')
    geo = request.args.get('geo')
    economy = request.args.get('economy')
    eng = request.args.get('eng')
    dutch = request.args.get('dutch')
    lessons = []
    if math == '1':
        lessons.append("Математика")
    if rus == '1':
        lessons.append("Русский язык")
    if phys == '1':
        lessons.append("Физика")
    if inf == '1':
        lessons.append("Информатика")
    if chemistry == '1':
        lessons.append("Химия")
    if bio == '1':
        lessons.append("Биология")
    if history == '1':
        lessons.append("История")
    if social == '1':
        lessons.append("Обществознание")
    if literature == '1':
        lessons.append("Литература")
    if geo == '1':
        lessons.append("География")
    if economy == '1':
        lessons.append("Экономика")
    if eng == '1':
        lessons.append("Английский язык")
    if dutch == '1':
        lessons.append("Немецкий язык")
    if len(lessons) != 0:
        _filter.update({'Изучаемые_предметы': { "$all" : lessons }})

    res = WorkWithDB.GetRecordOnFilter(city, _filter, True)
    if res.isGood == False:
        return 'Bad request'
    return json.dumps(res.listRes, ensure_ascii=False)

@app.route("/dialog/")
def dialog():
    id1 = int(request.args.get('id1'))
    id2 = int(request.args.get('id2'))
    ids = WorkWithDB.foundAllUsersDialog(id1)
    if ids != None and id2 in ids:
        pass
    else:
        WorkWithDB.createNewDialog(id1, id2)
    return redirect('/messages?to='+str(id2))

@app.route("/timetable/")
def timetable():
    user = WorkWithDB.FoundUserInDatabaseForToken(request.cookies.get('token'))
    if user == None:
        resp = make_response(redirect("/"))
        resp.set_cookie('token', '', expires = 0)
        resp.set_cookie('citycode', '', expires = 0)
        return resp
    
    tables = WorkWithDB.FindNode(user['ID']).listRes

    res = ''

    if len(tables) != 0:
        f = codecs.open('static/prefabs/prefabSchedule.html', encoding='utf-8', mode='r')
        prefab = f.read()
        f.close()

        for rec in tables:
            pref = prefab
            pref = pref.replace('{{DATE}}', rec['Дата'])
            pref = pref.replace('{{TASK}}', rec['Предмет'])
            pref = pref.replace('{{DATEID}}', str(rec['idNote']))
            pref = pref.replace('{{LESSONID}}', str(rec['idNote']))
            res += pref
    

    if user['Роль'] == 'Репетитор':
        return render_template("tutorSchedule.html", REC = Markup(res))
    else:
        return render_template("studentSchedule.html", REC = Markup(res))

@app.route("/user/<idstr>")
def foundUser(idstr):
    id = 0
    try:
        id = int(idstr)
    except Exception:
        return 'Bad user ID, user not found!'

    iam = WorkWithDB.FoundUserInDatabaseForToken(request.cookies.get('token'))
    if iam == None:
        resp = make_response(redirect("/"))
        resp.set_cookie('token', '', expires = 0)
        resp.set_cookie('citycode', '', expires = 0)
        return resp
    
    _filter = {}
    _filter.update({'ID': id})

    user = WorkWithDB.FoundUserInDatabaseForID(idstr)

    if user == None:
        return 'Bad user ID, user not found!'
    
    if user['Фотография'] == 'Стандарт':
        photo = "https://api.adorable.io/avatars/234/" + str(user['ID'])
    else:
        photo = "/images/" + str(user['ID']) + ".png"

    messageURL = "document.location.href = '/dialog/?id1="+str(iam['ID'])+"&id2="+str(user['ID'])+"';";

    if user['Роль'] == 'Репетитор':
        lessons = ''
        for les in user['Преподаваемые_предметы']:
            lessons += '<br>' + les
        htmlLessons = Markup(lessons)
        formatLessons = ''
        for forLes in user['Формат_занятий']:
            formatLessons += '<br>' + forLes
        htmlFormatLessons = Markup(formatLessons)
        viewsLessons = ''
        for viewLes in user['Вид_занятий']:
            viewsLessons += '<br>' + viewLes
        htmlViewsLessons = Markup(viewsLessons)
        return render_template("tutorProfile.html", LastName = user['Фамилия'], FirstName = user['Имя'], BirthDay = user['День_рождения'], Education = user['Образование'], Experions = str(user['Стаж_преподавания_в_годах']), Phone = user['Телефон'], About = user['О_себе'], Lessons = htmlLessons, FormatLessons = htmlFormatLessons, ViewsLessons = htmlViewsLessons, Price = str(user['Ставка_в_час']), Photo = photo, Button = "Написать сообщение", DoCode = messageURL)
    else:
        lessons = ''
        for les in user['Изучаемые_предметы']:
            lessons += '<br>' + les
        htmlLessons = Markup(lessons)
        formatLes = ''
        for Fles in user['Формат_занятий']:
            formatLes += '<br>' + Fles
        htmlFormat = Markup(formatLes)
        return render_template("studentProfile.html", LastName = user['Фамилия'], FirstName = user['Имя'], BirthDay = user['День_рождения'], SchoolClass = str(user['Класс']), Phone = user['Телефон'], About = user['О_себе'], Lessons = htmlLessons, Format = htmlFormat, Photo = photo, Button = "Написать сообщение", DoCode = messageURL)

if __name__ == "__main__":
    app.run()
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=8080)