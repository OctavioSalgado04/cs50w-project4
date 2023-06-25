import csv
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def read_file(filename, col_list):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)

        dato=text("SELECT id from categoria WHERE nombre='componente'")
        id_categoria=db.execute(dato).fetchone()
        db.commit()

        for row in reader:    
                    dato1=text("INSERT INTO producto (id_categoria, nombre, precio, cantidad, imagen) VALUES (:id_categoria, :nombre, :precio, :cantidad, :imagen)")
                    db.execute(dato1,
                            {"id_categoria":id_categoria[0], "nombre": row["tipo"], "precio":row["precio"], "cantidad":50, "imagen":'default'})
                    
                    db.commit()

        nombre = []
        for i in reader:
            nombre .append(i["name"])
        print(nombre)
        
        dato2=text("SELECT id FROM producto WHERE id_categoria = :id")
        id=db.execute(dato2,
                        {"id":id_categoria[0]})
        k=0
        for i in (id):
            for j in (i):
                dato3=text("INSERT INTO tipo_componente (id_producto, nombre) VALUES (:id_producto, :nombre)")       
                db.execute(dato3,
                            {"id_producto":j, "nombre":nombre[k]})
                k+=1
                            
                db.commit()

def main():
    read_file('componentes.csv', ['tipo', 'name', 'precio'])
    
    


if __name__ == "__main__":
    main()