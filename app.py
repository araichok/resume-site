from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.secret_key = "resume_secret_key"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def home():
    lang = request.args.get("lang")

    if lang:
        session["lang"] = lang

    lang = session.get("lang", "ru")

    documents = [
        {
            "title_ru": "Титульный лист отчета",
            "title_kz": "Есептің титул парағы",
            "file": "1. Титульный лист отчета.docx"
        },
        {
            "title_ru": "Трехсторонний договор",
            "title_kz": "Үшжақты келісім-шарт",
            "file": "2. Трехсторонний договор на проведение профессиональной практики.docx"
        },
        {
            "title_ru": "Направление",
            "title_kz": "Жолдама",
            "file": "3. Направление.docx"
        },
        {
            "title_ru": "Рабочий план-график",
            "title_kz": "Жұмыс жоспары",
            "file": "4. Рабочий план-график.docx"
        },
        {
            "title_ru": "Дневник-отчет о прохождении практики",
            "title_kz": "Күнделік-тәжірибеден өту туралы есеп",
            "file": "5. Дневник-отчет о прохождении практики.docx"
        },
        {
            "title_ru": "Характеристика на обучающегося",
            "title_kz": "Білім алушыға мінездеме",
            "file": "6. Характеристика на обучающегося.docx"
        }
    ]

    return render_template("home.html", documents=documents, lang=lang)

@app.route("/builder", methods=["GET", "POST"])
def builder():
    lang = request.args.get("lang")

    if lang:
        session["lang"] = lang

    lang = session.get("lang", "ru")

    if request.method == "POST":
        photo = request.files.get("photo")
        filename = None

        if photo and photo.filename != "":
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        data = {
            "name": request.form.get("name"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "city": request.form.get("city"),
            "about": request.form.get("about"),
            "education": request.form.get("education"),
            "experience": request.form.get("experience"),
            "skills": request.form.get("skills"),
            "sport_achievements": request.form.get("sport_achievements"),
            "photo": filename
        }

        session["resume"] = data
        return redirect(url_for("resume"))

    return render_template("builder.html", lang=lang)


@app.route("/resume")
def resume():
    data = session.get("resume")

    if not data:
        return redirect(url_for("builder"))

    return render_template("resume.html", data=data)


if __name__ == "__main__":
    if __name__ == "__main__":
        app.run()