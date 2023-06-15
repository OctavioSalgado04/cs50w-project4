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
 
        for row in reader:    
            dato1=text("INSERT INTO componentes (tipo, name, precio) VALUES (:tipo, :name, :precio)")
            db.execute(dato1,
                    {"tipo": row["tipo"], "name": row["name"], "precio":row["precio"]})
            db.commit()
                    

def main():
    read_file('componentes.csv', ['tipo', 'name', 'precio'])
    
    


if __name__ == "__main__":
    main()