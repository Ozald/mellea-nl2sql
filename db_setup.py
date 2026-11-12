import sqlite3
import pandas as pd

print("Creating MovieLens database. Please standby...")
try:
    connection = sqlite3.connect("movielens.db")
except sqlite3.Error as e:
    print(f"Error connecting to database: {e}")
    raise

print("Reading CSV files...")
try:
    links = pd.read_csv("samples/links.csv")
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
    links.to_sql("links", connection, if_exists="replace", index=False)
    print("\tSuccessfully created 'links' table.")

    movies.to_sql("movies", connection, if_exists="replace", index=False)
    print("\tSuccessfully created 'movies' table.")

    ratings.to_sql("ratings", connection, if_exists="replace", index=False)
    print("\tSuccessfully created 'ratings' table.")

    tags.to_sql("tags", connection, if_exists="replace", index=False)
    print("\tSuccessfully created 'tags' table.")

except Exception as e:
    print(f"Error writing tables to SQLite: {e}")
    raise

print("SQLite MovieLens database has been successfully generated!")

