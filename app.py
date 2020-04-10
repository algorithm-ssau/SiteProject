import os
from flask import (
    Flask,
    render_template,
    send_from_directory,
    redirect,
    url_for,
    request,
)
from WorkWithDB import WorkWithDB, Result

app = Flask(__name__)


@app.route("/")
def login():
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
        user.update({"Формат_занятий": workform})
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
        user.update({"Изучаемые_предметы": lessons})
        res = WorkWithDB.AddToDatabase(city, False, user)
        if res.isGood == False:
            return render_template(
                "errorRegistration.html", errorMessage=res.getErrorMessage()
            )
        return redirect("/")
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
        user.update({"Формат_занятий": workform})
        user.update({"Образование": request.form.get("education")})
        user.update({"Стаж_преподавания_в_годах": request.form.get("experience")})
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
        user.update({"Вид_занятий": typesOfLessons})
        res = WorkWithDB.AddToDatabase(city, True, user)
        if res.isGood == False:
            return render_template(
                "errorRegistration.html", errorMessage=res.getErrorMessage()
            )
        return redirect("/")
    return render_template("newteacher.html")


@app.route("/favicon.ico")
def fav():
    return redirect(url_for("static", filename="favicon.ico"), code=302)


if __name__ == "__main__":
    app.run()
