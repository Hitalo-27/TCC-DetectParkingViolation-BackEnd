from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configurações do MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DB = "tcc"

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# Dependência para injetar sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
