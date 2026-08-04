from pathlib import Path
from sqlalchemy import create_engine

_SQL_PATH = Path(__file__).resolve().parent / "init.sql"
DB_PATH = Path(__file__).resolve().parent / "app.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"


def initialize_database(sql_file_path=_SQL_PATH):
    """
    Lee un archivo SQL con múltiples sentencias y lo ejecuta en SQLite
    usando la conexión nativa (raw_connection) del engine de SQLAlchemy.
    """

    print(sql_file_path)

    engine = create_engine(DATABASE_URL)

    try:
        with open(sql_file_path, "r", encoding="utf-8") as file:
            sql_script = file.read()
    except FileNotFoundError as error:
        print(error)
        print(f"Error: No se encontró el archivo {sql_file_path}")
        return

    with engine.raw_connection() as raw_conn:
        try:
            cursor = raw_conn.cursor()
            cursor.executescript(sql_script)
            raw_conn.commit()
            print("Base de datos inicializada con éxito.")

        except Exception as e:
            raw_conn.rollback()
            print(f"Error al ejecutar el script SQL: {e}")

        finally:
            cursor.close()
