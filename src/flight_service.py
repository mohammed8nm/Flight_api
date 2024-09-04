from typing import Dict, List
from models.flight import Flight
from csv_repository import CSVRepository
from const import SUCCESS_THRESHOLD_MINUTES, DATE_FORMAT, MAX_SUCCESS_FLIGHTS_SIMULTANEOUSLY
import logging

# Set up logging
logger = logging.getLogger(__name__)

class FlightService:
    def __init__(self, repository: CSVRepository):
        self._repository = repository

    def recalculate_success_status(self, in_memory_flights: Dict[str, Flight]) -> None:
        """
        Recalculate the success status of all flights using a two-pointer technique
        to ensure no more than the allowed number of successful flights exist simultaneously.
        """
        # Sort flights by arrival and departure times
        sorted_by_arrival = sorted(in_memory_flights.values(), key=lambda x: x.arrival)
        sorted_by_departure = sorted(in_memory_flights.values(), key=lambda x: x.departure)

        arrival_pointer = 0
        departure_pointer = 0
        success_count = 0

        # Reset all success statuses
        for flight in sorted_by_arrival:
            flight.success = False

        # Two-pointer approach to determine success status
        while arrival_pointer < len(sorted_by_arrival):
            current_arrival = sorted_by_arrival[arrival_pointer].arrival

            # Reduce success count based on departure
            while (departure_pointer < len(sorted_by_departure) and 
                   sorted_by_departure[departure_pointer].departure <= current_arrival):
                if sorted_by_departure[departure_pointer].success:
                    success_count -= 1
                    logger.info("Flight ID %s marked as not successful after departure.",
                                sorted_by_departure[departure_pointer].flight_id)
                departure_pointer += 1

            # Add success count based on arrival
            flight_to_check = sorted_by_arrival[arrival_pointer]
            duration = flight_to_check.calculate_duration()
            if duration >= SUCCESS_THRESHOLD_MINUTES and success_count < MAX_SUCCESS_FLIGHTS_SIMULTANEOUSLY:
                flight_to_check.success = True
                success_count += 1
                logger.info("Flight ID %s marked as successful.", flight_to_check.flight_id)
            else:
                flight_to_check.success = False
                logger.info("Flight ID %s not marked as successful due to the limit of %d successful flights or insufficient duration.",
                            flight_to_check.flight_id, MAX_SUCCESS_FLIGHTS_SIMULTANEOUSLY)

            arrival_pointer += 1

        logger.info("Recalculated success status for all flights. %d flights marked as successful.", success_count)

    def add_or_update_flight(self, new_flight: Flight, in_memory_flights: Dict[str, Flight]) -> Dict[str, Flight]:
        """
        Add a new flight to the in-memory dict or update it if it already exists,
        then recalculate the success status for all flights.
        """
        if new_flight.flight_id in in_memory_flights:
            # Update existing flight
            logger.info("Flight ID %s found. Updating flight data.", new_flight.flight_id)
            existing_flight = in_memory_flights[new_flight.flight_id]
            existing_flight.arrival = new_flight.arrival.strftime(DATE_FORMAT)
            existing_flight.departure = new_flight.departure.strftime(DATE_FORMAT)
        else:
            # Add new flight
            logger.info("Flight ID %s not found. Adding new flight.", new_flight.flight_id)
            in_memory_flights[new_flight.flight_id] = new_flight

        # Recalculate success status for all flights
        self.recalculate_success_status(in_memory_flights)

        # Save all flights (sorted by arrival time) back to the CSV
        sorted_flights = sorted(in_memory_flights.values(), key=lambda x: x.arrival)
        self.save_flights(sorted_flights)

        return in_memory_flights

    def load_all_flights(self) -> Dict[str, Flight]:
        """Load all flights from the input CSV file into a dictionary."""
        flights = self._repository.load_flights()
        flights_dict = {flight.flight_id: flight for flight in flights}
        logger.info("Loaded %d flights from input CSV file.", len(flights_dict))
        return flights_dict

    def save_flights(self, flights: List[Flight]):
        """Save flights to the result CSV file."""
        self._repository.save_flights(flights)
        logger.info("Flights have been saved to the CSV file.")

    def get_flight_by_id(self, flight_id: str, in_memory_flights: Dict[str, Flight]) -> Flight:
        """Retrieve a flight by its ID from the in-memory dictionary."""
        if flight_id in in_memory_flights:
            logger.info("Flight ID %s found in in-memory dictionary.", flight_id)
            return in_memory_flights[flight_id]
        else:
            logger.error("Flight with ID %s not found in in-memory dictionary.", flight_id)
            raise ValueError(f"Flight with ID {flight_id} not found")