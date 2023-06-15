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
    password TEXT NOT NULL,
    admin INT NOT NULL
    );   
    """)
    db.execute(tabla1)

    tabla2=text("""CREATE TABLE componentes (
    id SERIAL PRIMARY KEY,
    tipo TEXT NOT NULL,
    name TEXT NOT NULL,
    precio TEXT NOT NULL,
    cantidad INT DEFAULT 50
    );   
    """)
    db.execute(tabla2)

    db.commit()

if __name__ == "__main__":
    main()
