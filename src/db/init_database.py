from sqlalchemy import create_engine

def initialize_database(sql_file_path="init.sql"):
    """
    Lee un archivo SQL con múltiples sentencias y lo ejecuta en SQLite
    usando la conexión nativa (raw_connection) del engine de SQLAlchemy.
    """

    print(sql_file_path)

    # 1. Definir la URL de conexión de SQLite (creará un archivo 'app.db' localmente)
    DATABASE_URL = "sqlite:///app.db"
    engine = create_engine(DATABASE_URL)

    # 2. Leer el contenido del archivo SQL
    try:
        with open(sql_file_path, "r", encoding="utf-8") as file:
            sql_script = file.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {sql_file_path}")
        return

    # 3. Ejecutar el script usando la conexión cruda (DBAPI) del engine
    with engine.raw_connection() as raw_conn:
        try:
            cursor = raw_conn.cursor()
            
            # executescript es una función nativa de sqlite3 para ejecutar
            # múltiples instrucciones SQL separadas por punto y coma (;)
            cursor.executescript(sql_script)
            
            # Confirmar los cambios en la base de datos
            raw_conn.commit()
            print("Base de datos inicializada con éxito.")
            
        except Exception as e:
            # Revertir los cambios si ocurre cualquier error durante la ejecución
            raw_conn.rollback()
            print(f"Error al ejecutar el script SQL: {e}")
            
        finally:
            # Asegurar que el cursor se cierre siempre al terminar
            cursor.close()