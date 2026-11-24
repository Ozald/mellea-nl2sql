import query_generation
import sqlite3

from mellea import start_session
from mellea.stdlib.requirements import req, simple_validate
from mellea.stdlib.sampling import RepairTemplateStrategy, RejectionSamplingStrategy

def main():
    con = sqlite3.connect(query_generation.DEFAULT_DATABASE_PATH)
    try:
        m = start_session()
        schema = query_generation.get_database_schema(con)
        if not schema:
            raise RuntimeError(
                "No tables found in movielens.db; run db_setup.py first."
            )

        query_requirements = [
            req(
                "Return exactly one read-only SQLite SELECT statement. Do not "
                "return Markdown, explanations, or multiple statements."
            ),
            req(
                "Use only tables and columns in the supplied schema, and use "
                "declared key relationships when joining tables."
            ),
            req(
                "Answer the request directly. For highest-rated movies, use "
                "average user rating rather than the highest individual rating."
            ),
            req(
                "For this request, return the movie title, average rating, and "
                "rating count. Break ties by rating count descending, then title "
                "ascending."
            ),
            req(
                "The query must parse and execute successfully against the "
                "SQLite database.",
                validation_fn=simple_validate(query_generation.validate_query),
            ),
        ]

        result = query_generation.generate_sql_query(
            m=m,
            topic=(
                "Find the movie with the highest average user rating. Return its "
                "title, average rating, and number of ratings. Break ties by "
                "rating count, then title. Return only one movie."
            ),
            schema=schema,
            requirements=query_requirements,
            strategy=RejectionSamplingStrategy(loop_budget=5),
        )

        is_valid, validation_error = query_generation.validate_query(result)
        if not is_valid:
            raise RuntimeError(
                f"Generated SQL query failed validation: {validation_error}"
            )

        rows = con.execute(result).fetchall()
        print("RESULT:")
        if rows:
            for row in rows:
                print(f"\t{row}")
        else:
            print("\tNo results found.")
    finally:
        con.close()


if __name__ == "__main__":
    main()