import sqlite3
import pandas as pd

print("Creating MovieLens database. Please standby...")
try:
    connection = sqlite3.connect("movielens.db")
    connection.execute("PRAGMA foreign_keys = ON")
except sqlite3.Error as e:
    print(f"Error connecting to database: {e}")
    raise

print("Reading CSV files...")
try:
    links = pd.read_csv("samples/links.csv", dtype={"imdbId": str})
    print("\tSuccessfully read 'links' CSV file.")

    movies = pd.read_csv("samples/movies.csv")
    print("\tSuccessfully read 'movies' CSV file.")

    ratings = pd.read_csv("samples/ratings.csv")
    print("\tSuccessfully read 'ratings' CSV file.")

    tags = pd.read_csv("samples/tags.csv")
    print("\tSuccessfully read 'tags' CSV file.")

except Exception as e:
    print(f"Error loading CSV files: {e}")
    raise

print("Converting CSV files into SQLite database tables...")
try:
    connection.executescript("""
        DROP TABLE IF EXISTS ratings;
        DROP TABLE IF EXISTS tags;
        DROP TABLE IF EXISTS links;
        DROP TABLE IF EXISTS movies;

        CREATE TABLE movies (
            movieId INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            genres TEXT NOT NULL
        );

        CREATE TABLE links (
            movieId INTEGER PRIMARY KEY,
            imdbId TEXT,
            tmdbId INTEGER,
            FOREIGN KEY (movieId) REFERENCES movies(movieId)
        );

        CREATE TABLE ratings (
            ratingId INTEGER PRIMARY KEY,
            userId INTEGER NOT NULL,
            movieId INTEGER NOT NULL,
            rating REAL NOT NULL,
            timestamp INTEGER NOT NULL,
            FOREIGN KEY (movieId) REFERENCES movies(movieId)
        );

        CREATE TABLE tags (
            tagId INTEGER PRIMARY KEY,
            userId INTEGER NOT NULL,
            movieId INTEGER NOT NULL,
            tag TEXT NOT NULL,
            timestamp INTEGER NOT NULL,
            FOREIGN KEY (movieId) REFERENCES movies(movieId)
        );
    """)

    movies.to_sql("movies", connection, if_exists="append", index=False)
    print("\tSuccessfully created 'movies' table.")

    links.to_sql("links", connection, if_exists="append", index=False)
    print("\tSuccessfully created 'links' table.")

    ratings.to_sql("ratings", connection, if_exists="append", index=False)
    print("\tSuccessfully created 'ratings' table.")

    tags.to_sql("tags", connection, if_exists="append", index=False)
    print("\tSuccessfully created 'tags' table.")

    violations = connection.execute("PRAGMA foreign_key_check").fetchall()
    if violations:
        raise sqlite3.IntegrityError(
            f"Foreign key violations found: {violations[:5]}"
        )

except Exception as e:
    print(f"Error writing tables to SQLite: {e}")
    raise
finally:
    connection.close()

print("SQLite MovieLens database has been successfully generated!")

