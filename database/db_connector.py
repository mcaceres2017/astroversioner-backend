from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the database URL, you can change this according to your database
# DATABASE_URL = "postgresql://username:password@localhost:5432/astrocollab"

# CREDENTIALS
"""
USER="servicio_web"
PASSWORD="Cheeseburger2023."
"""


USER = "servicio_web"
PASSWORD = "Cheeseburger2023."

HOST = "172.17.0.1"  # on ubuntu
# HOST = "127.0.0.1"  # on windows
PORT = "5433"
DATABASE = "astroversioner"


DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

print(DATABASE_URL)

# Create a SQLAlchemy database engine
engine = create_engine(DATABASE_URL)

# Create a sessionmaker with specific settings
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for declarative models
Base = declarative_base()


def get_db():
    """
    Get a database session.

    Returns:
        generator: A generator that yields a database session.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()  # Rollback any changes made in the session
        print(f"[ERROR] An error occurred while trying to connect to astrocollab: {e}")
        raise  # Re-raise the exception to propagate it further
    finally:
        db.close()
