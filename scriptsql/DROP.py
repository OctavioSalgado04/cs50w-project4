import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
  
    dato1=text("DROP TABLE producto")
    db.execute(dato1)

    db.commit()

if __name__ == "__main__":
    main()
