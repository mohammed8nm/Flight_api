from pydantic import BaseModel

class FlightData(BaseModel):
    flight_id: str
    arrival: str
    departure: str