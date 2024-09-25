from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

password = "casaos"
engine = create_engine(f"mysql+mysqlconnector://root:{password}@localhost/yet_another_split")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


