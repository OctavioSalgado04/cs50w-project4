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
    dato1=text("SELECT imagen, nombre FROM producto WHERE id_categoria = '1'")
    imagen=db.execute(dato1).fetchall()

    #precios
    dato2=text("SELECT precio FROM producto WHERE id_categoria = '1'")
    precio=db.execute(dato2).fetchall()

    return render_template("arduino.html",imagen=imagen, precio=precio)


@app.route('/comprar', methods=['GET','POST'])
def comprar():
    if request.method == "POST":
        producto = request.form.get('producto')
        precio = request.form.get('precio')
        nombre = request.form.get('name')
        print(nombre)
        dato1=text("SELECT cantidad FROM producto WHERE nombre=:nombre")
        stock=db.execute(dato1,
                        {"nombre":nombre}).fetchone()
        print(stock)


        return render_template('comprar.html', producto=producto, precio=precio, nombre=nombre, stock=stock[0])
    else:
        return redirect('/')

@app.route("/carrito", methods=['GET', 'POST'])
@login_required
def carrito():
    id=session["user_id"]
    if request.method == "POST":

        precio=request.form.get('precio')
        stock=request.form.get('stock')
        nombre=request.form.get('nombre')
        cantidad=request.form.get('cantidad')
        id_producto=""
        try:
            tipo=request.form.get('tipo')
        except:
            tipo='none'

        if not stock:
            flash("producto agotado")
            return render_template("comprar.html")

        if not cantidad:
            flash("ingrese cuanto necesitas")
            return render_template("comprar.html")

        if cantidad >= stock:
            flash("cantidad mayor a lo que hay disponible")
            return render_template("comprar.html")

        if tipo == None:
            dato1=text("SELECT id FROM producto where nombre = :nombre")
            id_producto=db.execute(dato1,
                                    {"nombre":nombre}).fetchone()
            print("no hay tipo")
        else:
            dato = text("SELECT tipo_componente.id FROM producto INNER JOIN tipo_componente ON CAST(producto.id AS TEXT) = tipo_componente.id_producto WHERE tipo_componente.nombre =:tipo")
            id_producto=db.execute(dato,
                                {"tipo":tipo}).fetchone()
        producto=id_producto[0]

        try:
            a=text("INSERT INTO carrito (producto, precio, cantidad, id_user) VALUES(:producto, :precio, :cantidad, :id_user)")
            db.execute(a,{"producto":producto, "precio":str(precio), "cantidad":str(cantidad), "id_user":str(id)})
            db.commit()
        except OperationalError:
            print("Error connecting to the database :/")

        a=text("SELECT * FROM carrito WHERE id_user=:id")
        carrito=db.execute(a,
                        {"id":str(id)}).fetchall()
        
        conteo = len(carrito)
        nombre=""
        for i in carrito:
            print(i[1])
            why=text("SELECT nombre from producto WHERE id = :id")
            nombre=db.execute(why,{"id":producto}).fetchall()
        print(nombre)
        price = 0
        cantidades= 0
        for i in range(conteo):
            price = price + int(carrito[i][2])
            cantidades= cantidades + int(carrito[i][3])
        
        subtotal= cantidades*price

        return render_template('carrito.html', nombre=nombre[0], muchos=conteo, carrito=carrito, subtotal=subtotal)

    else:
        
        a = text("SELECT * FROM carrito WHERE id_user=:id")
        carrito = db.execute(a, {"id": str(id)}).fetchall()

        if not carrito:
            flash("carrito vacio")
            return render_template("index.html")

        nombre=""
        for i in carrito:
            print(i[1])
            why=text("SELECT nombre from producto WHERE id = :id")
            nombre=db.execute(why,{"id":i[1]}).fetchall()

        conteo = len(carrito)
        price = 0
        cantidades= 0
        for i in range(conteo):
            price = price + int(carrito[i][2])
            cantidades= cantidades + int(carrito[i][3])
        
        subtotal= cantidades*price

        return render_template('carrito.html', nombre=nombre[0], muchos=conteo, carrito=carrito, subtotal=subtotal)


@app.route("/venta", methods=['GET', 'POST'])
def venta():
    if request.method == "POST":

        subtotal= int(request.form.get("subtotal"))
        impuesto=0.05
        descuento=0
        totali= int(subtotal*impuesto+descuento) 
        total=subtotal-totali
        fecha_venta= hora  
        
        dato1=text("INSERT INTO venta (id_user, subtotal, total, descuento, fecha_venta) VALUES (:id, :subtotal, :total, :descuento, :fecha_venta)")
        db.execute(dato1,
                {"id": session["user_id"], "subtotal": subtotal, "total":total, "descuento":descuento, "fecha_venta":fecha_venta})

        venta=text("SELECT id FROM venta WHERE id_user=:user")
        id_venta=db.execute(venta,
                            {"user":session["user_id"]}).fetchone()

        a = text("SELECT * FROM carrito WHERE id_user=:id")
        carrito = db.execute(a, {"id":str(session["user_id"])}).fetchall()

        conteo = len(carrito)
        for i in range(conteo):
            monto_total= int(carrito[i][3]) * int(carrito[i][2])
            dato1=text("INSERT INTO detalle_venta (id_producto, id_venta, cantidad, precio_unitario, monto_total) VALUES (:id_producto, :id_venta, :cantidad, :precio_unitario, :monto_total)")
            db.execute(dato1,
                        {"id_producto":int(carrito[i][1]), "id_venta":id_venta[0], "cantidad":int(carrito[i][3]), "precio_unitario":carrito[i][2], "monto_total":monto_total})
            db.commit()

        return render_template("venta.html", subtotal=subtotal, impuesto=impuesto, fecha_venta=fecha_venta, descuento=descuento,total=total)
    else:
        return redirect("/")


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
