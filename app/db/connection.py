from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

db_config_dev = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("HOST"),
    "database": os.getenv("DATABASE"),
    "port": int(os.getenv("PORTDB"))
}

db_config_prod = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("HOST"),
    "database": os.getenv("DATABASE"),
    "port": int(os.getenv("PORTDB"))
}


def create_db_engine(is_development=True):
    config = db_config_dev if is_development else db_config_prod
    
    # Use PyMySQL instead of mysql-connector for better compatibility
    if is_development:
        connection_string = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    else:
        connection_string = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}/{config['database']}"
    
    # Create engine with additional connection options
    engine = create_engine(
        connection_string,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False  # Set to True for debugging SQL queries
    )
    return engine

def get_db(is_development=True):
    try:
        engine = create_db_engine(is_development)
        try:
            from .base import Base
        except ImportError:
            from app.db.base import Base
        # This ensures the metadata is bound to this engine
        Base.metadata.bind = engine
        
        # Create tables if they don't exist
        try:
            Base.metadata.create_all(bind=engine)
        except Exception as e:
            print(f"Warning: Could not create tables: {e}")
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Test the connection
        db.execute(text("SELECT 1"))
        
        return db
    except Exception as err:
        print(f"Error al conectar a la base de datos: {err}")
        print(f"Tipo de error: {type(err).__name__}")
        return None

def close_connection(conn):
    if conn:
        conn.close()

def test_db_connection(is_development=True):
    """
    Prueba la conexión a la base de datos.
    Retorna: (es_conectado, mensaje)
    """
    db = None
    try:
        db = get_db(is_development)
        if db is None:
            return False, "Error: No se pudo obtener la sesión de la base de datos"
        
        # Ejecutar una consulta de prueba
        db.execute(text("SELECT 1"))
        return True, "✅ Conexión a la base de datos exitosa"
    except Exception as e:
        return False, f"❌ Error al conectar a la base de datos: {str(e)}"
    finally:
        if db:
            close_connection(db)

if __name__ == "__main__":
    # Add project root to sys.path for direct script execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    es_conectado, mensaje = test_db_connection(is_development=True)
    print(mensaje)