import os
import requests
from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
from helper import login_required
import datetime

app = Flask(__name__)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

formato_hora = datetime.datetime.now()
hora = formato_hora.strftime("el %d-%m-%Y a las %H:%M:%S")
print(hora)

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

        flash(f"bienvenido {name}")
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
            flash(f"ya ha sido registrado como {usuario}")
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


@app.route("/componentes")
def componentes():

    #tipo
    dato = text("SELECT producto.nombre, tipo_componente.nombre FROM producto INNER JOIN tipo_componente ON CAST(producto.id AS TEXT) = tipo_componente.id_producto")
    runaway=db.execute(dato)
    circles=runaway.fetchall()
    #print(circles)

    #precio
    precio=[]
    nombre=['regulador de voltaje fijo', 'amplificador operacional', 'temporizador IC', 'regulador de voltaje ajustable', 'amplificador de audio de bajo voltaje', 'resistencias', 'PNP transistores bipolares', '(FET)transistores de efecto de campo', 'transistores darlington', '(BJT)transistores de potencias bipolares', '(JFET)transistores de union de campo', 'MOSFET de potencia']
    for k in(nombre):
        dato2=text("SELECT precio FROM producto WHERE nombre= :nombre")
        precios=db.execute(dato2,
                            {"nombre":k}).fetchone()
        precio.append(precios[0])

    return render_template("componentes.html", name=circles, precio=precio)


@app.route("/dispositivos")
def dispositivos():
    #dispositivos
    dato1=text("SELECT imagen FROM producto WHERE id_categoria = '3'")
    imagen=db.execute(dato1).fetchall()

    #precios
    dato2=text("SELECT precio FROM producto WHERE id_categoria = '3'")
    precio=db.execute(dato2).fetchall()

    return render_template("dispositivos.html", imagen=imagen, precio=precio)


@app.route("/arduino")
def arduino():
    #arduinos
    dato1=text("SELECT imagen FROM producto WHERE id_categoria = '1'")
    imagen=db.execute(dato1).fetchall()
    
    #precios
    dato2=text("SELECT precio FROM producto WHERE id_categoria = '1'")
    precio=db.execute(dato2).fetchall()
    
    return render_template("arduino.html",imagen=imagen, precio=precio)


@app.route('/comprar', methods=['POST'])
def comprar():
    producto = request.form.get('producto')
    precio = request.form.get('precio')
    nombre = request.form.get('name')
    print(nombre)
    dato1=text("SELECT cantidad FROM producto WHERE nombre=:nombre")
    stock=db.execute(dato1,
                    {"nombre":nombre}).fetchone()
    print(stock)


    return render_template('comprar.html', producto=producto, precio=precio, nombre=nombre, stock=stock[0])

@app.route("/venta")
def venta():
    subtotal=""
    impuesto=0.05
    descuento=""
    total= subtotal*impuesto+descuento 
    fecha_venta= hora
    
    dato1=text("INSERT INTO venta (id_usuario, subtotal, impuesto, total, descuento, fecha_venta) VALUES (:id, :subtotal, :impuesto, :total, :descuento, :fecha_venta)")
    db.execute(dato1,
               {"id": session["user_id"], "subtotal": subtotal, "impuesto": impuesto,"total":total, "descuento":descuento, "fecha_venta":fecha_venta})

    db.commit()

@app.route("/detalle_venta")
def detalle_venta():
    nombre=""
    cantidad=""
    precio_unitario=""
    monto_total=cantidad*precio_unitario

    si=text("SELECT id FROM producto WHERE nombre= :nombre")
    id_producto=db.execute(si,
                        {"nombre":nombre}).fetchone()

    venta=text("SELECT id FROM venta WHERE id_usuario=:user")
    id_venta=db.execute(venta,
                        {"user":session["user_id"]}).fetchone()

    dato1=text("INSERT INTO detalle_venta (id_producto, id_venta, cantidad, precio_unitario, monto_total) VALUES (:id_producto, :id_venta, :cantidad, :precio_unitario, :monto_total)")
    db.execute(dato1,
                {"id_producto":id_producto, "id_venta":id_venta, "cantidad":cantidad, "precio_unitario":precio_unitario, "monto_total":monto_total})

    db.commit()

    @app.route("/historial")
    def detalle_venta():
        producto=''
        dato1=text("SELECT FROM id_venta FROM detalle_venta WHERE id_producto=:producto ")
        id_venta=db.execute(dato1,
                            {"producto":producto}).fetchone()
        id_usurio=session["user_id"]
        fecha= hora

        dato1=text("INSERT INTO historial (id_venta, id_venta, id_usuario, fecha_historial) VALUES (:id_venta, :id_usuario, :fecha_historial)")
        db.execute(dato1,
                    {"id_venta":id_venta, ":id_usuario":id_usuario, "fecha_historial":fecha})
