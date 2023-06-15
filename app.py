import os
import requests
from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
from helper import login_required

app = Flask(__name__)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    #regulador de voltaje fijo
    dato1=text("SELECT name FROM componentes where tipo='regulador de voltaje fijo'")
    name=db.execute(dato1).fetchall()
    dato2=text("SELECT precio FROM componentes where tipo='regulador de voltaje fijo'")
    precio=db.execute(dato2).fetchone()
    #amplificador operacional
    dat1=text("SELECT name FROM componentes where tipo='amplificador operacional'")
    name2=db.execute(dat1).fetchall()
    dat2=text("SELECT precio FROM componentes where tipo='amplificador operacional'")
    precio2=db.execute(dat2).fetchone()
    #temporizador ic
    dat01=text("SELECT name FROM componentes where tipo='temporizador IC'")
    name3=db.execute(dat01).fetchall()
    dat02=text("SELECT precio FROM componentes where tipo='temporizador IC'")
    precio3=db.execute(dat02).fetchone()
    #regulador de voltaje ajustable
    dataso1=text("SELECT name FROM componentes where tipo='regulador de voltaje ajustable'")
    name4=db.execute(dataso1).fetchall()
    dataso2=text("SELECT precio FROM componentes where tipo='regulador de voltaje ajustable'")
    precio4=db.execute(dataso2).fetchone()
    #amplificador de audio de bajo voltaje
    datas1=text("SELECT name FROM componentes where tipo='regulador de voltaje ajustable'")
    name5=db.execute(datas1).fetchall()
    datas2=text("SELECT precio FROM componentes where tipo='regulador de voltaje ajustable'")
    precio5=db.execute(datas2).fetchone()
    #resistencias
    datas01=text("SELECT name FROM componentes where tipo='resistencias'")
    name6=db.execute(datas01).fetchall()
    datas02=text("SELECT precio FROM componentes where tipo='resistencias'")
    precio6=db.execute(datas02).fetchone()
    #transistores pnp bipolar
    trnas1=text("SELECT name FROM componentes where tipo='PNP transistores bipolares'")
    name7=db.execute(trnas1).fetchall()
    trnas2=text("SELECT precio FROM componentes where tipo='PNP transistores bipolares'")
    precio7=db.execute(trnas2).fetchone()
    #(FET)transistores de efecto de campo
    trans1=text("SELECT name FROM componentes where tipo='(FET)transistores de efecto de campo'")
    name8=db.execute(trans1).fetchall()
    trans2=text("SELECT precio FROM componentes where tipo='(FET)transistores de efecto de campo'")
    precio8=db.execute(trans2).fetchone()
    return render_template("index.html", name=name, precio=precio,name2=name2, precio2=precio2,name3=name3, precio3=precio3,name4=name4, precio4=precio4,name5=name5, precio5=precio5,name6=name6, precio6=precio6, name7=name7, precio7=precio7, name8=name8, precio8=precio8)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        name = request.form.get("usuario")
        password = request.form.get("password")
        if not password and not name:
            flash("campos vacios")
            return render_template('login.html')
        if not name:
            flash("ingrese su usuario")
            return render_template('login.html')
        if not password:
            flash("ingrese su contraseña")
            return render_template('login.html')

        dato1 =text("SELECT * FROM usuario WHERE name = :name")
        existe=db.execute(dato1,{"name":name}).fetchone()
        if existe == None or existe[2] != password:
            flash("Usuario mal ingresado o clave incorrecta")
            return render_template('login.html')
        session["user_id"]= existe[0]

        return redirect("/")
    else:
        return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    session.clear()
    if request.method == "get":
        return render_template('register.html')
    else:
        usuario = request.form.get("usuario")
        password = request.form.get("password")
        confirma = request.form.get("confirmar")

        if not usuario and not password and not confirma:
            flash("campos vacios")
            return render_template('register.html')
        if not password:
            flash("ingrese una contraseña")
            render_template('register.html')
        if not confirma:
            flash("ingrese una contraseña")
            return render_template('register.html')
        if password != confirma:
            flash("claves distintas")
            return render_template('register.html')
        dato1 = text("SELECT * FROM usuario WHERE name = :usuario")
        consulta = db.execute(dato1,{"usuario":usuario}).fetchone()

        if consulta == None:
            sesion = text("INSERT INTO usuario (name, password,admin) VALUES(:usuario,:password,:admin)")
            db.execute(sesion,
                    {"usuario": usuario, "password": password, "admin": 0 })

            db.commit()

            dato2 = text("SELECT * FROM usuario WHERE name = :usuario")
            row = db.execute(dato2,{"usuario":usuario}).fetchone()
            session["user_id"] = row[0]
            return redirect("/")

        if consulta[1] == usuario:
            flash("nombre ya en uso")
            return render_template('register.html')

        if consulta[1] == usuario and consulta[2] == password and consulta[2] == confirma:
            flash("usuario ya existente")
            return render_template('register.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/inicio")
@login_required
def inicio():
    componentes=1
    print(session["user_id"])
    return render_template("inicio.html")

@app.route("/componentes")
def componentes():
    return render_template("componentes.html")

@app.route("/dispositivos")
def dispositivos():
    return render_template("dispositivos.html")


@app.route("/arduino")
def arduino():
    return render_template("arduino.html")