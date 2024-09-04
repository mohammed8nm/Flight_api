from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
import logging
from models.flight import Flight
from models.flight_data import FlightData
from flight_service import FlightService
from dependencies import get_flight_service, get_in_memory_flights

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/flight/{flight_id}")
async def get_flight(
    flight_id: str,
    flight_service: FlightService = Depends(get_flight_service),
    in_memory_flights: Dict[str, Flight] = Depends(get_in_memory_flights)
):
    try:
        logger.info("Received request to get flight ID %s", flight_id)
        flight = flight_service.get_flight_by_id(flight_id, in_memory_flights)
        return {
            "flight_id": flight.flight_id,
            "arrival": flight.arrival.strftime("%H:%M"),
            "departure": flight.departure.strftime("%H:%M"),
            "success": flight.success
        }
    except ValueError as e:
        logger.error(f"Flight not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/flights")
async def add_or_update_flights(
    new_flights: List[FlightData],
    flight_service: FlightService = Depends(get_flight_service),
    in_memory_flights: Dict[str, Flight] = Depends(get_in_memory_flights)
):
    try:
        logger.info("Received request to add or update %d flights", len(new_flights))
        
        for data in new_flights:
            new_flight = Flight(data.flight_id, data.arrival, data.departure)
            in_memory_flights = flight_service.add_or_update_flight(new_flight, in_memory_flights)

        return {"message": "Flights processed successfully", "total_flights": len(in_memory_flights)}
    except ValueError as e:
        logger.error(f"Invalid flight data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to process flights: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process flights")