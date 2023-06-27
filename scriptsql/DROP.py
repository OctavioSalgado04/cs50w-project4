import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
  
    tabl4=text("SELECT * from producto")
    breaking=db.execute(tabl4).fetchone()

    db.commit()
    print(breaking)
if __name__ == "__main__":
    main()
