from csv_repository import CSVRepository
from flight_service import FlightService
from models.flight import Flight
from typing import Dict
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Initialize repository and service instances
repository = CSVRepository()
flight_service = None  # Initialize later to avoid circular imports

# Global in-memory dictionary of flights
in_memory_flights: Dict[str, Flight] = {}

def initialize_flights():
    """
    Load all flights from the input CSV file into memory at startup.
    """
    global in_memory_flights
    global flight_service  # Initialize here to avoid circular import

    # Initialize FlightService now that all dependencies are resolved
    flight_service = FlightService(repository)

    logger.info("Loading flights from input CSV into memory.")
    in_memory_flights = flight_service.load_all_flights()

    # Recalculate success status for all flights at startup
    flight_service.recalculate_success_status(in_memory_flights)
    logger.info("All flight statuses have been recalculated.")

    # Save the updated flights back to the result CSV
    sorted_flights = sorted(in_memory_flights.values(), key=lambda x: x.arrival)
    flight_service.save_flights(sorted_flights)
    logger.info("Flights have been saved back to the CSV file.")

def get_flight_service() -> FlightService:
    """
    Dependency function to provide a FlightService instance.
    """
    return flight_service

def get_in_memory_flights() -> Dict[str, Flight]:
    """
    Dependency function to provide the in-memory dictionary of flights.
    """
    return in_memory_flights