# Event Planner API

This project provides an API for geting events, weather data, and flights.

## Setup Instructions

1. Navigate to the project directory: `cd event-planner-api`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Apply the database migrations: `python manage.py migrate`
4. Start the development server: `python manage.py runserver`

The API will be accessible at `http://localhost:8000/`.

## Endpoints

### Events

- List all events: `GET /events/`
- Retrieve a specific event: `GET /events/<event_id>/`

### Weather

- Retrieve weather data for an event: `GET /events/weather/<event_id>/`

### Flights

- Retrieve flights arriving at an airport for an event: `GET /events/flight/<event_id>/<user_airport_iata_code>/`

##### Author : Abdulkareem Abunabhan