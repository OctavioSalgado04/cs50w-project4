import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
  
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
