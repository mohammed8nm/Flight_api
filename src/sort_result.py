import csv
from datetime import datetime
from typing import List

class Flight:
    def __init__(self, flight_id: str, arrival: str, departure: str, success: str):
        self.flight_id = flight_id
        self.arrival = datetime.strptime(arrival, "%H:%M")
        self.departure = datetime.strptime(departure, "%H:%M")
        self.success = success.lower() == 'true'  # Convert 'True'/'False' string to boolean

    def __repr__(self):
        return f"Flight({self.flight_id}, Arrival: {self.arrival.strftime('%H:%M')}, Departure: {self.departure.strftime('%H:%M')}, Success: {self.success})"

def sort_flights_by_arrival(flights: List[Flight]) -> List[Flight]:
    """Sort a list of Flight objects by their arrival time."""
    return sorted(flights, key=lambda flight: flight.arrival)

def read_flights_from_csv(file_path: str) -> List[Flight]:
    """Read flights from a CSV file and return a list of Flight objects."""
    flights = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                flight = Flight(
                    flight_id=row["flight ID"],
                    arrival=row["Arrival"],
                    departure=row["Departure"],
                    success=row["success"]
                )
                flights.append(flight)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
    return flights

def save_flights_to_csv(flights: List[Flight], file_path: str):
    """Save a list of Flight objects to a CSV file."""
    try:
        with open(file_path, mode='w', newline='') as file:
            fieldnames = ["flight ID", "Arrival", "Departure", "success"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for flight in flights:
                writer.writerow({
                    "flight ID": flight.flight_id,
                    "Arrival": flight.arrival.strftime("%H:%M"),
                    "Departure": flight.departure.strftime("%H:%M"),
                    "success": str(flight.success)  # Convert boolean back to 'True'/'False' string
                })
        print(f"Flights have been saved to {file_path}.")
    except Exception as e:
        print(f"An error occurred while saving to the CSV file: {e}")

# Example usage
if __name__ == "__main__":
    # Define the input and output CSV file paths
    csv_path = "data/flights.csv"  # The path to save sorted data

    # Read flights from the input CSV file
    flights = read_flights_from_csv(csv_path)
    
    print("Flights before sorting:")
    for flight in flights:
        print(flight)

    # Sort flights by arrival time
    sorted_flights = sort_flights_by_arrival(flights)

    print("\nFlights after sorting by arrival time:")
    for flight in sorted_flights:
        print(flight)

    # Save the sorted flights back to the output CSV file
    save_flights_to_csv(sorted_flights, csv_path)