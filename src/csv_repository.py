import csv
from typing import List
from models.flight import Flight
from const import INPUT_DATA_FILE_PATH, OUTPUT_DATA_FILE_PATH, DATE_FORMAT
import logging

# Set up logging
logger = logging.getLogger(__name__)

class CSVRepository:
    def load_flights(self) -> List[Flight]:
        """Load flights from a CSV file."""
        flights = []
        try:
            with open(INPUT_DATA_FILE_PATH, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    flight = Flight(
                        flight_id=row["flight ID"],
                        arrival=row["Arrival"],
                        departure=row["Departure"]
                    )
                    flights.append(flight)
            logger.info("Loaded %d flights from input CSV file.", len(flights))
        except FileNotFoundError:
            logger.error("The input file input_data.csv was not found.")
        except Exception as e:
            logger.error(f"An error occurred while loading flights: {str(e)}")
        return flights

    def save_flights(self, flights: List[Flight]):
        """Save flights to a CSV file."""
        try:
            with open(OUTPUT_DATA_FILE_PATH, mode="w", newline="") as file:
                fieldnames = ["flight ID", "Arrival", "Departure", "success"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for flight in flights:
                    writer.writerow({
                        "flight ID": flight.flight_id,
                        "Arrival": flight.arrival.strftime(DATE_FORMAT),
                        "Departure": flight.departure.strftime(DATE_FORMAT),
                        "success": str(flight.success)  # Convert boolean back to 'True'/'False' string
                    })
            logger.info("Saved %d flights to result CSV file.", len(flights))
        except Exception as e:
            logger.error(f"An error occurred while saving flights: {str(e)}")