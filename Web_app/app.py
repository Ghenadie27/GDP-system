from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, logout_user, LoginManager
import sqlite3
import json
from database import users
from flask_mail import Mail, Message

app = Flask(__name__)

app.secret_key = "your_app_key"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=1)

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'your_email'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email'
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)
login = LoginManager()
login.init_app(app)
login.login_view = 'login'
db = SQLAlchemy(app)


@login.user_loader
def load_user(id):
    return users.query.get(int(id))


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        message = request.form.get('message')

        if not first_name or not last_name or not phone or not email or not message:
            flash("All Form Fields Required...")
            return render_template('contact.html', faulthandler=True)
        else:
            msg = Message(subject="your_subject",
                          sender="your_email",
                          recipients=[f"{email}"])
            msg.body = f"Dear {first_name},\nyour_message."
            mail.send(msg)

            msg_1 = Message(subject=f"Mail from {email}", body=f"Name: {first_name, last_name}\nE-mail:"
                                                               f"{email}\nPhone: {phone} \n\n{message}",
                            sender="your_email",
                            recipients=["email"])
            mail.send(msg_1)
            return render_template("contact.html", success=True)
    return render_template('contact.html')


@app.route("/utilizatori")
def utilizatori():
    if current_user.is_authenticated and current_user.username != "Admin":
        return redirect(url_for("index"))
    elif current_user.is_authenticated is False:
        return redirect(url_for("index"))
    return render_template('utilizatori.html', user=current_user.username)


@app.route('/proces_date', methods=['POST', 'GET'])
def proces():
    conn = sqlite3.connect('path_to_the_database')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute(
        "SELECT denumire, timp, temperatura, umiditatea from sensors ORDER BY timp DESC LIMIT 10000").fetchall()
    conn.commit()
    conn.close()
    return json.dumps([dict(ix) for ix in rows])


@app.route('/proces_utilizator', methods=['POST', 'GET'])
def proces_u():
    conn = sqlite3.connect('path_to_the_users_database')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    conn.commit()
    conn.close()
    return json.dumps([dict(ix) for ix in rows])


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect('/partener')
    if request.method == 'POST':
        email = request.form['email']
        user = users.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            if user.username == "Admin":
                return redirect(url_for("utilizatori"))
            else:
                return redirect(url_for("user"))
        else:
            return redirect(url_for("register"))
    return render_template('login.html')


@app.route('/inregistrare', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        flash("Sunteți deja înregistrat!")
        return redirect(url_for("login"))
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password_2 = request.form['password_2']
        if users.query.filter_by(username=username).first():
            flash('Sunteși înregistrat deja. Vă rugăm să Vă autentificați!')
            return redirect(url_for("login"))
        if email and username:
            user = users(email=email, username=username)
        else:
            flash('Vă rugăm să introduceți date valide!')
            return redirect(url_for("register"))
        if password == password_2 and password:
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Ați fost înregistrat cu succes!")
            return redirect('/login')
        else:
            flash('Parola nu a fost confirmată!')
            return redirect(url_for("register"))
    return render_template('inregistrare.html')


@app.route("/partener", methods=["POST", "GET"])
def user():
    if current_user.is_authenticated:
        return render_template("partener.html", user=current_user.username)
    else:
        flash("Nu sunteți atentificat!!!")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash(f"Ați fost deconectat!")
    session.pop("user", None)
    session.pop("email", None)
    session.pop("password", None)
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    #app.run(host='0.0.0.0')
