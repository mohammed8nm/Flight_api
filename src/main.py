from fastapi import FastAPI
import uvicorn
import logging
from routers import flight_routers
from dependencies import initialize_flights

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI()

# Log application startup
logger.info("Starting the FastAPI application.")

# Load flights into memory at startup and update their statuses
initialize_flights()
logger.info("Initialized flight statuses from input CSV and saved to flights.csv.")


# Home page route
@app.get("/")
async def read_root():
    return "Hello to flight API"

# Include flight-related routes
app.include_router(flight_routers.router)
logger.info("Flight routers have been included in the FastAPI application.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)






