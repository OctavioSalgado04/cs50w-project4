import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    name="admin"
    password="admin"
  
    dato1=text("INSERT INTO usuario (name, password, admin) VALUES (:name, :password, :admin)")
    db.execute(dato1,
               {"name": name, "password": password, "admin": 1 })
               

    db.commit()

if __name__ == "__main__":
    main()
