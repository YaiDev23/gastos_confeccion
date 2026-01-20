from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Construir URL de conexión a PostgreSQL
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("HOST")
db_name = os.getenv("DATABASE")
db_port = os.getenv("PORT_DB", "5432")

# Construir la URL de conexión
db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def create_db_engine():
    """
    Crea el motor de la base de datos PostgreSQL.
    Retorna: Engine de SQLAlchemy
    """
    if not db_url:
        print(f"Error: No se encontró la URL de conexión a la base de datos")
        return None

    try:
        # Crear engine con configuración optimizada para PostgreSQL
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False  # Set to True for debugging SQL queries
        )
        return engine
    except Exception as e:
        print(f"Error al crear el motor de la base de datos: {e}")
        return None


def get_db():
    """
    Obtiene una sesión de la base de datos.
    Uso con FastAPI: como dependencia en endpoints
    """
    try:
        engine = create_db_engine()
        if engine is None:
            raise Exception("No se pudo crear el motor de la base de datos")
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            yield db
        finally:
            db.close()
    except Exception as err:
        print(f"Error al conectar a la base de datos: {err}")
        raise


def close_connection(conn):
    """Cierra la conexión a la base de datos"""
    if conn:
        conn.close()


def test_db_connection():
    """
    Prueba la conexión a la base de datos PostgreSQL.
    Retorna: (es_conectado: bool, mensaje: str)
    """
    db = None
    try:
        engine = create_db_engine()
        if engine is None:
            return False, "❌ Error: No se pudo crear el motor de la base de datos"
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Ejecutar una consulta de prueba
        db.execute(text("SELECT 1"))
        
        return True, "✅ Conexión a la base de datos PostgreSQL exitosa"
    except Exception as e:
        return False, f"❌ Error al conectar a la base de datos: {str(e)}"
    finally:
        if db:
            close_connection(db)


if __name__ == "__main__":
    # Add project root to sys.path for direct script execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    es_conectado, mensaje = test_db_connection()
    print(mensaje)