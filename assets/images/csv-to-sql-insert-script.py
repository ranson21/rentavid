import csv
import re


def sanitize_string(s):
    """Sanitize a string for use in an SQL statement."""
    if s is None:
        return "NULL"
    return "'" + s.replace("'", "''") + "'"


def main():
    input_file = "movie_data.csv"
    output_file = "movie_inserts.sql"

    with open(input_file, "r", newline="", encoding="utf-8") as csvfile, open(
        output_file, "w", encoding="utf-8"
    ) as sqlfile:

        reader = csv.DictReader(csvfile)

        # Process each row
        for row in reader:
            # Sanitize and prepare values
            values = {
                "film_id": row["film_id"],
                "title": sanitize_string(row["title"]),
                "description": sanitize_string(row["description"]),
                "backdrop_path": sanitize_string(row["backdrop_path"]),
                "poster_path": sanitize_string(row["poster_path"]),
                "release_year": row["release_year"],
                "language_id": row["language_id"],
                "original_language_id": row["original_language_id"],
                "rental_duration": row["rental_duration"],
                "rental_rate": sanitize_string(row["rental_rate"]),
                "length": row["length"],
                "replacement_cost": sanitize_string(row["replacement_cost"]),
            }

            # Create the INSERT statement
            insert_statement = f"""INSERT INTO film VALUES ({values['film_id']}, {values['title']}, {values['description']}, {values['backdrop_path']}, {values['poster_path']}, {values['release_year']}, {values['language_id']}, {values['original_language_id']}, {values['rental_duration']}, {values['rental_rate']}, {values['length']}, {values['replacement_cost']});"""

            sqlfile.write(insert_statement)
            sqlfile.write("\n")

    print(f"SQL INSERT statements have been written to {output_file}")


if __name__ == "__main__":
    main()
