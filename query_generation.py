from pathlib import Path
import sqlite3

from mellea import generative

DEFAULT_DATABASE_PATH = Path(__file__).resolve().with_name("movielens.db")

@generative
def generate_sql_query(topic: str, schema: str) -> str:
    """Translate the request into one read-only SQLite query.

    The current database schema is provided in `schema`. Treat it as
    authoritative: use only its tables and columns, and follow its declared
    keys when joining tables. Interpret aggregation according to the request;
    for movie rating questions, "highest rated" means highest average rating,
    not the highest individual rating. Return only one SQLite SELECT statement,
    with no Markdown fences or explanation.
    """


def get_database_schema(connection: sqlite3.Connection) -> str:
    """Return the database's declared table definitions."""
    rows = connection.execute(
        """
        SELECT sql
        FROM sqlite_master
        WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    ).fetchall()
    return "\n\n".join(statement for (statement,) in rows if statement)


def validate_query(query: str, database_path: str | Path = DEFAULT_DATABASE_PATH) -> tuple[bool, str]:
    """Check that SQL executes against the database without writes."""
    database_uri = f"{Path(database_path).resolve().as_uri()}?mode=ro"
    try:
        connection = sqlite3.connect(database_uri, uri=True)
        try:
            for _ in connection.execute(query):
                pass
        finally:
            connection.close()
    except sqlite3.Error as error:
        return False, f"SQLite could not execute the query: {error}"

    return True, ""
