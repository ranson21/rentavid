import csv
import requests
import time
import os
import sys

# TMDb API configuration
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.themoviedb.org/3/movie/"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


def fetch_movie_data(movie_id):
    url = f"{BASE_URL}{movie_id}"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for movie ID {movie_id}: {response.status_code}")
        return None


def main():
    input_file = "film.csv"
    output_file = "movie_data.csv"

    with open(input_file, "r") as csv_file, open(
        output_file, "w", newline=""
    ) as output_csv:
        csv_reader = csv.DictReader(csv_file)
        fieldnames = [
            "film_id",
            "title",
            "description",
            "backdrop_path",
            "poster_path",
            "release_year",
            "language_id",
            "original_language_id",
            "rental_duration",
            "rental_rate",
            "length",
            "replacement_cost",
        ]
        csv_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        csv_writer.writeheader()

        for row in csv_reader:
            movie_data = None
            for i in range(5):  # Try up to 5 times
                movie_id = int(row["film_id"]) + 10000 + (i * 10)
                movie_data = fetch_movie_data(movie_id)
                if movie_data:
                    break
                time.sleep(0.25)  # Add a delay to avoid hitting API rate limits

            if movie_data:
                backdrop_path = (
                    f"{IMAGE_BASE_URL}{movie_data.get('backdrop_path', '')}"
                    if movie_data.get("backdrop_path")
                    else ""
                )
                poster_path = (
                    f"{IMAGE_BASE_URL}{movie_data.get('poster_path', '')}"
                    if movie_data.get("poster_path")
                    else ""
                )

                csv_writer.writerow(
                    {
                        "film_id": row["film_id"],
                        "title": row["title"],
                        "description": row["description"],
                        "backdrop_path": backdrop_path,
                        "poster_path": poster_path,
                        "release_year": row["release_year"],
                        "language_id": row["language_id"],
                        "original_language_id": row["original_language_id"],
                        "rental_duration": row["rental_duration"],
                        "rental_rate": row["rental_rate"],
                        "length": row["length"],
                        "replacement_cost": row["replacement_cost"],
                    }
                )
                print(f"Processed movie ID: {movie_id}")
            else:
                print(f"Failed to fetch data for movie ID: {row['film_id']}")
                print("Terminating the script due to missing movie data.")
                sys.exit(1)  # Exit the script with an error code


if __name__ == "__main__":
    main()
