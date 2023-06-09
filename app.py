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
    return render_template("index.html")

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

        return render_template("inicio.html")
    else:
        return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    session.clear()
    if request.method == "get":
        return render_template('register.html')
    usuario = request.form.get("usuario")
    password = request.form.get("password")
    confirma = request.form.get("confirmar")

    if not usuario:
        flash("ingrese un usuario")
        return render_template('register.html')
    if not password:
        flash("ingrese una contraseña valida")
        render_template('register.html')
    if not confirma:
        flash("ingrese una contraseña igual")
        return render_template('register.html')
    if password != confirma:
        flash("claves distintas")
        return render_template('register.html')
    dato1 = text("SELECT * FROM usuario WHERE name = :usuario")
    consulta = db.execute(dato1,{"usuario":usuario}).fetchone()

    if consulta == None:
        sesion = text("INSERT INTO usuario (name, password) VALUES(:usuario,:password)")
        db.execute(sesion,
                {"usuario": usuario, "password": password })

        db.commit()

        dato2 = text("SELECT * FROM usuario WHERE name = :usuario")
        row = db.execute(dato2,{"usuario":usuario}).fetchone()
        session["user_id"] = row[0]
        return redirect("/inicio")

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
    print(session["user_id"])
    return render_template("inicio.html")