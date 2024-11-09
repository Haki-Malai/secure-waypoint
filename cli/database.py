import psycopg2
import typer
from sqlalchemy import create_engine, inspect

from app.models import Base
from core.config import config

app = typer.Typer()


@app.command()
def init():
    """Initialize the database."""
    engine = create_engine(
        config.SQLALCHEMY_DATABASE_URI, pool_size=30, max_overflow=20, echo=False
    )
    Base.metadata.create_all(engine)
    print("Database initialized")


@app.command()
def drop(tables: str = typer.Argument(None)):
    """Drop all tables in the database.

    :param tables: The tables to drop. Default is 'all'.
    """
    if tables == "all":
        engine = create_engine(
            config.SQLALCHEMY_DATABASE_URI, pool_size=30, max_overflow=20, echo=False
        )
        Base.metadata.drop_all(engine)
        print("All tables dropped")
        return

    DROP_TABLES_SCRIPT = """
        DO $$
        DECLARE
            r RECORD;
        BEGIN
            FOR r IN (SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name LIKE %s)
            LOOP
                EXECUTE 'DROP TABLE ' || quote_ident(r.table_name) || ' CASCADE';
            END LOOP;
        END $$;
    """
    try:
        conn = psycopg2.connect(config.SQLALCHEMY_DATABASE_URI)
        cursor = conn.cursor()
        cursor.execute(DROP_TABLES_SCRIPT, (f"{tables}%",))
        conn.commit()
        print("Tables dropped successfully.")
    except psycopg2.Error as e:
        print("Error dropping tables:", e)
    finally:
        if conn is not None:
            conn.close()


@app.command()
def view():
    """View all tables in the database."""
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables in the database:")
    for table in tables:
        print(table)


if __name__ == "__main__":
    app()
