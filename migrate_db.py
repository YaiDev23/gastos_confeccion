"""
Script para migrar la base de datos y agregar las columnas faltantes
"""
from app.db.connection import create_db_engine
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_missing_columns():
    """Agregar columnas faltantes a la tabla delivered_pieces"""
    engine = create_db_engine(is_development=True)
    
    with engine.connect() as connection:
        try:
            # Verificar si la columna 'rib' existe
            result = connection.execute(text("""
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'delivered_pieces' AND COLUMN_NAME = 'rib'
            """))
            
            if not result.fetchone():
                logger.info("Agregando columna 'rib'...")
                connection.execute(text("ALTER TABLE delivered_pieces ADD COLUMN rib VARCHAR(100) NULL"))
                connection.commit()
                logger.info("✅ Columna 'rib' agregada")
            else:
                logger.info("✅ Columna 'rib' ya existe")
            
            # Verificar si la columna 'type_fabric' existe
            result = connection.execute(text("""
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'delivered_pieces' AND COLUMN_NAME = 'type_fabric'
            """))
            
            if not result.fetchone():
                logger.info("Agregando columna 'type_fabric'...")
                connection.execute(text("ALTER TABLE delivered_pieces ADD COLUMN type_fabric VARCHAR(100) NULL"))
                connection.commit()
                logger.info("✅ Columna 'type_fabric' agregada")
            else:
                logger.info("✅ Columna 'type_fabric' ya existe")
            
            # Verificar si la columna 'id_group' existe
            result = connection.execute(text("""
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'delivered_pieces' AND COLUMN_NAME = 'id_group'
            """))
            
            if not result.fetchone():
                logger.info("Agregando columna 'id_group'...")
                connection.execute(text("ALTER TABLE delivered_pieces ADD COLUMN id_group VARCHAR(50) NULL"))
                connection.commit()
                logger.info("✅ Columna 'id_group' agregada")
            else:
                logger.info("✅ Columna 'id_group' ya existe")
            
            logger.info("\n✅ ¡Migración completada exitosamente!")
            
        except Exception as e:
            logger.error(f"❌ Error durante la migración: {str(e)}")
            raise

if __name__ == "__main__":
    logger.info("Iniciando migración de base de datos...")
    add_missing_columns()
