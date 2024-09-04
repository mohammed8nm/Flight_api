from datetime import datetime
from const import DATE_FORMAT

class Flight:
    def __init__(self, flight_id: str, arrival: str, departure: str):
        self._flight_id = flight_id
        self._arrival = datetime.strptime(arrival, DATE_FORMAT)
        self._departure = datetime.strptime(departure, DATE_FORMAT)
        self._success = None

    @property
    def flight_id(self) -> str:
        return self._flight_id

    @property
    def arrival(self) -> datetime:
        return self._arrival

    @arrival.setter
    def arrival(self, arrival: str):
        self._arrival = datetime.strptime(arrival, DATE_FORMAT)

    @property
    def departure(self) -> datetime:
        return self._departure

    @departure.setter
    def departure(self, departure: str):
        self._departure = datetime.strptime(departure, DATE_FORMAT)

    @property
    def success(self) -> bool:
        return self._success

    @success.setter
    def success(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Success must be a boolean (True or False)")
        self._success = value

    def calculate_duration(self) -> int:
        """Calculate the duration of the flight in minutes."""
        duration = int((self._departure - self._arrival).total_seconds() / 60)
        return duration

    def __repr__(self):
        return f"Flight({self._flight_id}, Arrival: {self._arrival.strftime('%H:%M')}, Departure: {self._departure.strftime('%H:%M')}, Success: {self._success})"