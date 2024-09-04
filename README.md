# BondIT assignment - rest API

## Features

- Get info about a flight
- Update the csv file with flights as an input

## Assumptions:
- csv file are given (no need to create) 
- flight.csv already exist in /data
- flight id can't be repeated 

## run the app

-   downloand requirements
    pip install -r requirements.txt

- run code 
    ..BondIT> python.exe .\src\main.py

- input:
    data\input_data.csv

- result :
    generated csv file path : data\flight.csv

## API endpoints
- home: http://127.0.0.1:8000
 ```json
{
    {
        "command":"get" ,
        "url format":"127.0.0.1:8000/"
    }
]
```
- GET http://127.0.0.1:8000/flight/{flight_ID}
```json
[
    {
        "command":"GET" ,
        "url format":"127.0.0.1:8000/flight/A12"
    }
]
```
- POST:
```json
[
    {
        "flight_id": "A723",
        "arrival": "9:00",
        "departure": "13:00"
    },
    {
        "flight_id": "A23",
        "arrival": "9:00",
        "departure": "13:00"
    },
    {
        "flight_id": "A823",
        "arrival": "9:00",
        "departure": "13:00"
    }
]
```
# structure: 
root/
│
├── data/
│   ├── input_data.csv          # CSV file containing original flight data
│   └── flights.csv             # CSV file containing sorted and updated flight data
│
└── src/
│    ── main.py                 # Main entry point to start the FastAPI app
│   ├── flight_service.py       # Business logic for handling flights
│   ├── csv_repository.py       # Contains logic for reading/writing CSV
│   ├── const.py                # Defines constants for the application
│    ── crdependencies.py         # Defines FastAPI dependencies
│   ├── routers/                # Folder for route definitions
    │   ├── __init__.py         # Init file for routers module
    │   └── flight_routers.py   # Endpoints related to flights
    └── models/
        ├── flight.py           # Contains the Flight class
        └── flight_data.py      # Contains the FlightData Pydantic model

