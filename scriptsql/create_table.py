import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    
    tabla1=text("""CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    correo TEXT NOT NULL,
    password TEXT NOT NULL,
    admin INT NOT NULL
    );   
    """)
    db.execute(tabla1)

    tabla2=text("""CREATE TABLE componentes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    precio TEXT NOT NULL,
    cantidad INT DEFAULT 50
    );   
    """)
    tabla3=text("""CREATE TABLE arduino (
    id SERIAL PRIMARY KEY,
    foto TEXT NOT NULL,
    tipo TEXT NOT NULL,
    name TEXT NOT NULL,
    precio TEXT NOT NULL,
    cantidad INT DEFAULT 50
    );   
    """)
    db.execute(tabla3)

    tabla4=text("""CREATE TABLE carrito (
    id SERIAL PRIMARY KEY,
    producto TEXT NOT NULL,
    precio TEXT NOT NULL,
    cantidad TExT NOT NULL,
    id_user TExT NOT NULL
    );   
    """)
    db.execute(tabla4)
    
    tabla5=text("""CREATE TABLE dispositivos (
    id SERIAL PRIMARY KEY,
    categoria TEXT NOT NULL,
    foto TEXT NOT NULL,
    name TEXT NOT NULL,
    precio TEXT NOT NULL,
    cantidad INT DEFAULT 50
    );   
    """)
    db.execute(tabla5)

    tabla6=text("""CREATE TABLE venta (
    id SERIAL PRIMARY KEY,
    id_user INT NOT NULL,
    subtotal TEXT NOT NULL,
    total INT NOT NULL,
    descuento TEXT NOT NULL,
    fecha_venta TEXT NOT NULL
    );   
    """)
    db.execute(tabla6)

    tabla7=text("""CREATE TABLE detalle_venta (
    id SERIAL PRIMARY  KEY,
    id_producto INT NOT NULL,
    id_venta INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario TEXT NOT NULL,
    monto_total INT NOT NULL
    );
    """)
    db.execute(tabla7)

    tabla8=text("""CREATE TABLE categoria(
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL 
    );
    """)
    db.execute(tabla8)

    tabla9=text("""CREATE TABLE producto(
    id SERIAL PRIMARY KEY,
    id_categoria INT NOT NULL,
    nombre TEXT NOT NULL,
    precio TEXT NOT NULL,
    cantidad INT NOT NULL,
    imagen TEXT NOT NULL
    );
    """)
    db.execute(tabla9)

    tabla0=text("""CREATE TABLE tipo_componente(
    id SERIAL PRIMARY KEY,
    id_producto TEXT NOT NULL,
    nombre TEXT NOT NULL
    );
    """)
    db.execute(tabla0)

    tabla0=text("""CREATE TABLE historial(
    id SERIAL PRIMARY KEY,
    id_venta INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_historial INT NOT NULL
    );
    """)
    db.execute(tabla0)

    tabl4=text("""CREATE TABLE informacion_personal(
    id SERIAL PRIMARY KEY,  
    id_user int not null,
    usuario text NOT NULL,
    direccion text NOT NULL,
    url TEXT NOT NULL,
    descripcion text NOT NULL
    );
    """)
    db.execute(tabl4)

    db.commit()

if __name__ == "__main__":
    main()
