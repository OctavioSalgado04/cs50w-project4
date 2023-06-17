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
        dato=text("SELECT id FROM categoria WHERE nombre='dispositivo'")
        id_categoria=db.execute(dato).fetchone()
        print(id_categoria)
        db.commit()
 
        for row in reader:    
            dato1=text("INSERT INTO producto (id_categoria, nombre, precio, cantidad, imagen) VALUES (:id_categoria, :nombre, :precio, :cantidad, :imagen)")
            db.execute(dato1,
                    {"id_categoria": id_categoria[0], "nombre": row["name"], "precio":row["precio"], "cantidad": 50,"imagen": row["foto"]})
            db.commit()
                    

def main():
    read_file('dispositivos.csv', ['foto', 'name', 'precio'])
    

if __name__ == "__main__":
    main()