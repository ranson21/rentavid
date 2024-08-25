import csv
import requests
import time
import os

# TMDb API configuration
API_KEY = "d15a31974f3a0a2d8aab087ecd8b11f2"
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


def download_image(url, filename):
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Error downloading {filename}: {response.status_code}")
    else:
        print(f"No URL provided for {filename}")


def main():
    input_file = "film.csv"
    output_file = "movie_data.csv"
    image_folder = "movie_images"

    # Create image folder if it doesn't exist
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

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
            movie_id = int(row["film_id"]) + 10000
            movie_data = fetch_movie_data(movie_id)

            if movie_data:
                backdrop_path = movie_data.get("backdrop_path")
                poster_path = movie_data.get("poster_path")

                # Download backdrop image
                if backdrop_path:
                    backdrop_url = f"{IMAGE_BASE_URL}{backdrop_path}"
                    backdrop_filename = os.path.join(
                        image_folder, f"{movie_id}_backdrop.jpg"
                    )
                    download_image(backdrop_url, backdrop_filename)

                # Download poster image
                if poster_path:
                    poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                    poster_filename = os.path.join(
                        image_folder, f"{movie_id}_poster.jpg"
                    )
                    download_image(poster_url, poster_filename)

                csv_writer.writerow(
                    {
                        "film_id": row["film_id"],
                        "title": row["title"],
                        "description": row["description"],
                        "backdrop_path": f"{IMAGE_BASE_URL}{backdrop_path}",
                        "poster_path": f"{IMAGE_BASE_URL}{poster_path}",
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
                csv_writer.writerow(
                    {
                        "film_id": row["film_id"],
                        "title": row["title"],
                        "description": row["description"],
                        "backdrop_path": "",
                        "poster_path": "",
                        "release_year": row["release_year"],
                        "language_id": row["language_id"],
                        "original_language_id": row["original_language_id"],
                        "rental_duration": row["rental_duration"],
                        "rental_rate": row["rental_rate"],
                        "length": row["length"],
                        "replacement_cost": row["replacement_cost"],
                    }
                )
                print(f"Skipped movie ID: {movie_id}...")
            # Add a delay to avoid hitting API rate limits
            time.sleep(0.25)


if __name__ == "__main__":
    main()
