import os
import re
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
hora2 = formato_hora.strftime("el %d-%m-%Y")
print(hora)

def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None

@app.route("/")
def index():
    simon=session['img']
    dato = text("UPDATE informacion_personal SET url=:nuevo WHERE id = :id")
    db.execute(dato, {"nuevo": simon, "id": session["user_id"]})
    db.commit()
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

        dato1 =text("SELECT * FROM usuario WHERE name = :name or correo =:nace")
        existe=db.execute(dato1,{"name":name, "nace":name}).fetchone()
        if existe == None or existe[3] != password:
            flash("Usuario mal ingresado o clave incorrecta")
            return render_template('login.html')
        session["user_id"]= existe[0]
        session["usuario"]= existe[1]

        mcr= text("SELECT url FROM informacion_personal WHERE id_user=:id")
        img= db.execute(mcr, {"id":int(existe[0])}).fetchone()

        if img == None:
            session["img"]="/static/image/perfil.webp"
        else:
            session["img"]= img[0]

        flash(f"bienvenido {existe[1]}")
        return redirect("/")
    else:
        return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    session.clear()
    if request.method == "get":
        return render_template('register.html')
    else:
        correo = request.form.get('correo')
        usuario = request.form.get("usuario")
        password = request.form.get("password")
        confirma = request.form.get("confirmar")

        if not correo  or not usuario  or not password or not confirma:
            flash("rellene todos los campos")
            return render_template('register.html')

        if not validar_correo(correo):
            flash("Correo electrónico inválido.")
            return render_template("register.html")

        if password != confirma:
            flash("claves distintas")
            return render_template('register.html')

        dato1 = text("SELECT * FROM usuario WHERE name = :usuario")
        consulta = db.execute(dato1,{"usuario":usuario}).fetchone()

        if consulta == None:
            sesion = text("INSERT INTO usuario (name, correo,password,admin) VALUES(:usuario, :correo,:password,:admin)")
            db.execute(sesion, {"usuario": usuario, "correo":correo,"password": password, "admin": 0 })

            db.commit()

            dato2 = text("SELECT * FROM usuario WHERE name = :usuario")
            row = db.execute(dato2,{"usuario":usuario}).fetchone()
            session["user_id"] = row[0]
            session["usuario"]= row[1]
            session["img"]="/static/image/perfil.webp"

            perfi=text("INSERT INTO informacion_personal (id_user, usuario, direccion, url, descripcion) VALUES(:id, :usuario, :direccion, :url, :descripcion)")
            db.execute(perfil, {":id":row[0], "usuario":row[1], "direccion":'ninguna', "url":'/static/image/perfil.webp', "descripcion":'ninguna'})
            db.commit()
            flash(f"ya ha sido registrado como {usuario}")
            return redirect("/")

        if consulta[1] == usuario:
            flash("nombre ya en uso")
            return render_template('register.html')

        if consulta[1] == usuario and consulta[3] == password and consulta[3] == confirma and consulta[2] == correo:
            flash("usuario ya existente")
            return render_template('register.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/delete")
def delete():
    id=session["user_id"]
    
    dele=text("DELETE FROM usuario WHERE id=:id")
    db.execute(dele, {"id":id})
    delet=text("DELETE FROM venta WHERE id_user=:id")
    db.execute(delet, {"id":id})
    delete=text("DELETE FROM informacion_personal WHERE id_user=:id")
    db.execute(delete, {"id":id})
    deleta=text("DELETE FROM detalle_venta WHERE id_user=:id")
    db.execute(deleta, {"id":id})
    delets=text("DELETE FROM historial WHERE id_usario=:id")
    db.execute(delets, {"id":id})
    db.commit()
    session.clear()
    return redirect("/login")

@app.route("/perfil")
@login_required
def perfil():
    mcr= text("SELECT correo FROM usuario WHERE id=:id")
    correo= db.execute(mcr, {"id": session["user_id"]}).fetchone()

    dato1= text("SELECT * from informacion_personal where id_user=:id")
    info= db.execute(dato1, {"id":session["user_id"]}).fetchone()
    print(info[2])
    
    a = text("SELECT * FROM historial WHERE id_usuario=:id")
    carrito = db.execute(a, {"id": str(session["user_id"])}).fetchall()

    producto=[]
    fecha=[]
    cantidad=[]
    fecha=[]
    precio=[]
    for i in carrito:
        print(i[1])
        why=text("SELECT * from detalle_venta WHERE id_venta = :id")
        produ=db.execute(why,{"id":i[1]}).fetchone()
        producto.append(produ[1])
        cantidad.append(produ[3])
        precio.append(produ[4])
        fecha.append(i[3])
        
    nombre=[]
    categoria=[]
    for i in producto:
        print(i)
        why=text("SELECT nombre, categoria from producto WHERE id = :id")
        nombe=db.execute(why,{"id":i}).fetchone()
        nombre.append(nombe[0])
        categoria.append(nombe[1])

    conteo = len(producto)

    return render_template("perfil.html", f=session['usuario'], img=session['img'], correo=correo[0], descripcion=info[5], nombre=nombre, conteo=conteo, precio=precio, fecha=fecha, categoria=categoria)

@app.route("/user-profile")
@login_required
def user_profile():

    dato1= text("SELECT * from informacion_personal where id_user=:id")
    info= db.execute(dato1, {"id":session["user_id"]}).fetchone()
    print(info[2])
    return render_template("usuario-perfil.html",f=info[2], img=info[4],  direccion=info[3], descripcion=info[5])

@app.route("/contraseña")
@login_required
def contraseña():

    return render_template("user-profile.html")

@app.route("/guardar_cambios", methods=['POST', "GET"])
def guardar_cambios():
    if request.method == "POST":
        correo = request.form.get('correo')
        confirmar = request.form.get('nuevo_correo')

        dato1=text("SELECT correo FROM usuario where id=:id")
        simon=db.execute(dato1, {"id": session["user_id"]}).fetchone()

        if simon != correo:
            flash('los correos no coinciden')
            return rennder_template("usuario-perfil.html")
        
        if correo and confirmar:
            print("el correo")
            nuevo_correo= text ("UPDATE usuario SET correo=:nuevo WHERE id_user= :id")
            db.execute(nuevo_correo, {"nuevo": confirmar,"id": session["user_id"]})
            db.commit()
        else:
            flash('No se ha ingresado ningún correo')
            return rennder_template("usuario-perfil.html")
        
        # Aquí puedes realizar las operaciones necesarias con los datos actualizados
        flash('Cambios guardados')
        return render_template("usuario-perfil.hmtl")
    else:
        return redirect("/")

@app.route("/direccion", methods=['GET', 'POST'])
def direccion():
    if request.method == "POST":
        direccion = request.form.get('direccion')
        descripcion = datos.get('descripcion')
        if direccion:
                print("la direccion")
                nuevo_direccion= text ("UPDATE informacion_personal SET direccion=:nuevo WHERE id_user= :id")
                db.execute(nuevo_direccion, { "nuevo": direccion,"id": session["user_id"]})
        else:
            flash('No se ha ingresado ninguna direccion')
            return rennder_template("usuario-perfil.html")
        if descripcion:
            print("la descripcion")
            nuevo_descripcion= text ("UPDATE informacion_personal SET descripcion=:nuevo WHERE id_user= :id")
            db.execute(nuevo_descripcion, { "nuevo": descripcion,"id": session["user_id"]})

        db.commit()
        flash('Cambios guardados')
        return render_template("usuario-perfil.html")
    else:
        return redirect("/")

@app.route('/upload', methods=['POST', "get"])
def upload():
    if request.method == "POST":
        # Verificar si se envió un archivo

        foto = request.files['foto']
        nuevo_nombre = request.form.get('nombre')

        if not foto:
            flash('No se ha enviado ningún archivo')
            return render_template("usuario-perfil.html")

        if not nuevo_nombre:
            flash('No se ha ingresado ningún nombre')
            return rennder_template("usuario-perfil.html")
        else:

            dato1 = text("UPDATE informacion_personal SET usuario=:nuevo WHERE id = :id")
            db.execute(dato1, {"nuevo": nuevo_nombre, "id": session["user_id"]})

            nuevo_nombre2 = text("UPDATE usuario SET name=:nuevo WHERE id = :id")
            db.execute(nuevo_nombre2, {"nuevo": nuevo_nombre, "id": session["user_id"]})
            
            db.commit()
            session["usuario"]=nuevo_nombre
        # Verificar si el archivo tiene un nombre
        if foto.filename == '':
            flash('El archivo no tiene un nombre válido')
            return rennder_template("usuario-perfil.html")

        # Guardar el archivo en el servidor
        ruta_guardada = os.path.join('static/image/perfiles', foto.filename)
        foto.save(ruta_guardada)

        dato = text("UPDATE informacion_personal SET url=:nuevo WHERE id = :id")
        db.execute(dato, {"nuevo": ruta_guardada, "id": session["user_id"]})
        db.commit()
        session['img'] = ruta_guardada
        print(session['img'])
        flash('La foto se ha guardado exitosamente')
        return render_template("usuario-perfil.html")
    
    else:
        return redirect("/")


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

    
    j=0
    for i in (nombre):
        j+=1

    return render_template("componentes.html", j=j,name=circles, precio=precio, fecha=hora2)


@app.route("/dispositivos")
def dispositivos():
    #dispositivos
    dato1=text("SELECT imagen FROM producto WHERE id_categoria = '3'")
    imagen=db.execute(dato1).fetchall()

    #precios
    dato2=text("SELECT precio FROM producto WHERE id_categoria = '3'")
    precio=db.execute(dato2).fetchall()
    #nombre
    dato3=text("SELECT nombre FROM producto WHERE id_categoria = '3'")
    nombre=db.execute(dato3).fetchall()

    j=0
    for i in (nombre):
        j+=1

    return render_template("dispositivos.html", imagen=imagen, precio=precio, nombre=nombre, j=j, fecha=hora2)


@app.route("/arduino")
def arduino():
    #arduinos
    dato1=text("SELECT imagen FROM producto WHERE id_categoria = '1'")
    imagen=db.execute(dato1).fetchall()

    #precios
    dato2=text("SELECT precio FROM producto WHERE id_categoria = '1'")
    precio=db.execute(dato2).fetchall()
    
    #nombre
    dato3=text("SELECT nombre FROM producto WHERE id_categoria = '1'")
    nombre=db.execute(dato3).fetchall()

    j=0
    for i in (nombre):
        j+=1

    return render_template("arduino.html", j=j,imagen=imagen, precio=precio, nombre=nombre,fecha=hora2)


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

@app.route('/comprar2', methods=['GET','POST'])
def comprar2():
    if request.method == "POST":
        producto = request.form.get('producto')
        print(producto)
        dato1=text("SELECT cantidad, precio FROM producto WHERE nombre=:nombre")
        stock=db.execute(dato1,
                        {"nombre":producto}).fetchone()
        print(stock)

        return render_template('comprar.html', producto=producto, precio=stock[1],stock=stock[0])
    else:
        return redirect('/')

@app.route("/carrito", methods=['GET', 'POST'])
@login_required
def carrito():
    id=session["user_id"]
    if request.method == "POST":

        precio=request.form.get('precio')
        nombre=request.form.get('nombre')
        cantidad=request.form.get('cantidad')
        id_producto=""
        id_poducto=""
        dato1=text("SELECT cantidad FROM producto WHERE nombre=:nombre")
        stock=db.execute(dato1,
                        {"nombre":nombre}).fetchone()
        isa=0
        for i in stock:
            isa=i
        
        try:
            tipo=request.form.get('tipo')
            print(tipo)
        except:
            tipo='none'

        if not stock:
            flash("producto agotado")
            return render_template("comprar.html")

        if not cantidad:
            flash("ingrese cuanto necesitas")
            return render_template("comprar.html")

        if int(cantidad) > isa:
            flash("cantidad mayor a lo que hay disponible")
            return render_template("comprar.html")

        if tipo == None:
            dato1=text("SELECT id FROM producto where nombre = :nombre")
            id_producto=db.execute(dato1,
                                    {"nombre":nombre}).fetchone()
            
            print("no hay tipo")
        else:
            dato = text("SELECT producto.id, tipo_componente.id FROM producto INNER JOIN tipo_componente ON CAST(producto.id AS TEXT) = tipo_componente.id_producto WHERE tipo_componente.nombre =:tipo")
            id_poducto=db.execute(dato,
                                {"tipo":tipo}).fetchone()
            id_producto=id_poducto
        producto=id_producto[0]
        print(producto)
        acu=text("SELECT producto FROM carrito WHERE id_user = :id_user")
        acun=db.execute(acu, {"id_user":str(id)}).fetchall()

        print(f" my wolrd is ending i wish {acun}")

        if not acun:

            try:
                a=text("INSERT INTO carrito (producto, precio, cantidad, id_user) VALUES(:producto, :precio, :cantidad, :id_user)")
                db.execute(a,{"producto":producto, "precio":str(precio), "cantidad":str(cantidad), "id_user":str(id)})
                db.commit()
            except OperationalError:
                print("Error connecting to the database :/")

        else:
            if int(producto) in [int(i[0]) for i in acun]:
                print("Aquí estoy")
                actualiza = text("UPDATE carrito SET cantidad = CAST((CAST(cantidad AS INTEGER) + :cantidad) AS TEXT) WHERE id_user = :id")
                db.execute(actualiza, {"cantidad": str(cantidad), "id": str(id)})
                db.commit()
            else:
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
        nombre=[]
        for i in carrito:
            print(i[1])
            why=text("SELECT nombre from producto WHERE id = :id")
            nombe=db.execute(why,{"id":i[1]}).fetchone()
            nombre.append(nombe[0])
        price = 0
        cantidades= 0
        for i in range(conteo):
            price = price + int(carrito[i][2])
            cantidades= cantidades + int(carrito[i][3])
        
        subtotal= cantidades*price

        return render_template('carrito.html', nombre=nombre, muchos=conteo, carrito=carrito, subtotal=subtotal)

    else:
        
        a = text("SELECT * FROM carrito WHERE id_user=:id")
        carrito = db.execute(a, {"id": str(id)}).fetchall()

        if not carrito:
            flash("carrito vacio")
            return render_template("index.html")

        nombre=[]
        for i in carrito:
            print(i[1])
            why=text("SELECT nombre from producto WHERE id = :id")
            nombe=db.execute(why,{"id":i[1]}).fetchone()
            nombre.append(nombe[0])

        conteo = len(carrito)
        price = 0
        cantidades= 0
        for i in range(conteo):
            price = price + int(carrito[i][2])
            cantidades= cantidades + int(carrito[i][3])
        
        subtotal= cantidades*price

        return render_template('carrito.html', nombre=nombre, muchos=conteo, carrito=carrito, subtotal=subtotal)


@app.route("/venta", methods=['GET', 'POST'])
def venta():
    if request.method == "POST":

        subtotal= int(request.form.get("subtotal"))
        impuesto=0.05
        descuento=0
        fecha_venta= hora

        a = text("SELECT * FROM carrito WHERE id_user=:id")
        carrito = db.execute(a, {"id":str(session["user_id"])}).fetchall()

        conteo = len(carrito)
        for i in range(conteo):

            mono_total = int(carrito[i][3]) * int(carrito[i][2])
            print(mono_total)
            monto_total = mono_total + int(round(mono_total * 0.5))
            print(monto_total)

            dato1=text("INSERT INTO venta (id_user, subtotal, total, descuento, fecha_venta) VALUES (:id, :subtotal, :total, :descuento, :fecha_venta)")
            db.execute(dato1,
                    {"id": session["user_id"], "subtotal": mono_total, "total":monto_total, "descuento":descuento, "fecha_venta":fecha_venta})


        venta=text("SELECT id FROM venta WHERE id_user=:user")
        id_venta=db.execute(venta,
                            {"user":session["user_id"]}).fetchone()

        for i in range(conteo):

            mono_total = int(carrito[i][3]) * int(carrito[i][2])
            monto_total = mono_total + int(round(mono_total * 0.5))

            dato1=text("INSERT INTO detalle_venta (id_producto, id_venta, cantidad, precio_unitario, monto_total) VALUES (:id_producto, :id_venta, :cantidad, :precio_unitario, :monto_total)")
            db.execute(dato1,
                        {"id_producto":int(carrito[i][1]), "id_venta":id_venta[0], "cantidad":int(carrito[i][3]), "precio_unitario":carrito[i][2], "monto_total":monto_total})
            db.commit()

            datoi=text("INSERT INTO historial (id_venta, id_venta, id_usuario, fecha_historial) VALUES (:id_venta, :id_usuario, :fecha_historial)")
            db.execute(datoi,
                        {"id_venta":id_venta[0], ":id_usuario":session["user_id"], "fecha_historial":fecha_venta})

        impuestos="5%"
        monto=[]
        nombre=[]
        t0tal=[]
        for i in carrito:
            why=text("SELECT nombre from producto WHERE id = :id")
            nombe=db.execute(why,{"id":i[1]}).fetchone()
            nombre.append(nombe[0])

            mono=int(i[3]) * int(i[2])
            ttal=mono + int(round(mono * 0.5))
            t0tal.append(ttal)
            monto.append(mono)

        f=text("SELECT fecha_venta FROM venta WHERE id_user=:id")
        fecha=db.execute(f,{"id":session["user_id"]}).fetchall()

        nosi=sum(t0tal)


        return render_template("venta.html", conteo=conteo, producto=nombre, subtotal=monto, impuesto=impuestos, fecha_venta=fecha, descuento=descuento,total=t0tal, nosi=nosi)
    else:
        return redirect("/")

@app.route("/pagar", methods=['POST'])
def pagar():
     
    return render_template("pagar.html")

@app.route('/procesar-pago', methods=['POST'])
def procesar_pago():
    nombre_tarjeta = request.form.get('nombre-tarjeta')
    numero_tarjeta = request.form.get('numero-tarjeta')
    fecha_expiracion = request.form.get('fecha-expiracion')
    cvv = request.form.get('cvv')

    a=text("SELECT * FROM carrito WHERE id_user=:id")
    carrito=db.execute(a,
                    {"id":str(session["user_id"])}).fetchall()
    if carrito == None:
        return redirect("/")
    else:
        for i in carrito:
            print(i[0], i[3])
            dato1=text("UPDATE producto SET cantidad = cantidad - :cantidad WHERE id=:id")
            db.execute(dato1, {"cantidad":int(i[3]), "id":i[1]})
            print("simon")
            db.commit()
    
    deli=text("DELETE FROM carrito WHERE id_user=:id")
    db.execute(deli, {"id":str(session["user_id"])})

    deli2=text("DELETE FROM venta WHERE id_user=:id")
    db.execute(deli2, {"id":session["user_id"]})
    db.commit()

    return f"Pago recibido. Tarjeta: {numero_tarjeta}, Nombre: {nombre_tarjeta}"

