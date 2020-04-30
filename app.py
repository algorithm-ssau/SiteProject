import os, hashlib
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    make_response,
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
            return render_template("errorRegistration.html", errorMessage="Пользователь не существует!")
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
            workform.append("Еду_к_преподавателю")
        if request.form.get("option2") == "a2":
            workform.append("Преподаватель_ко_мне")
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
            lessons.append("Русский_язык")
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
            lessons.append("Английский_язык")
        if request.form.get("dutch") == "b13":
            lessons.append("Немецкий_язык")
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
            workform.append("Еду_к_ученику")
        if request.form.get("option2") == "a2":
            workform.append("Ученик_ко_мне")
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
            lessons.append("Русский_язык")
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
            lessons.append("Английский_язык")
        if request.form.get("dutch") == "b13":
            lessons.append("Немецкий_язык")
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
            typesOfLessons.append("Помощь_с_домашкой")
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

@app.route("/profile", methods=["post", "get"])
def profile():
    user = WorkWithDB.FoundUserInDatabaseForToken(request.cookies.get('token'))
    if user == None:
        resp = make_response(redirect("/"))
        resp.set_cookie('token', '', expires = 0)
        return resp
    if user['Роль'] == 'Репетитор':
        return render_template("tutorprofile.html", LastName = user['Фамилия'], FirstName = user['Имя'], BirthDay = user['День_рождения'], Education = user['Образование'], Experions = user['Стаж_преподавания_в_годах'], Phone = user['Телефон'], About = user['О_себе'])
    else:
        return None


if __name__ == "__main__":
    app.run()
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=8080)
