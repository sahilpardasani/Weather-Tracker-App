# Weather-Tracker-App

A full-stack weather tracking application with user authentication, search history, built with Streamlit frontend, FastAPI backend, PostgreSQL database, and Docker.

**Features**
User registration & login
Fetch current weather data via WeatherAPI.com
Save & retrieve recent search history
Clear search history
Dockerized with Docker Compose

**Tech Stack**
Python 3.10
FastAPI
Streamlit
PostgreSQL 14
SQLAlchemy
Docker & Docker Compose

**Project Structure**
Docker & Docker Compose installed
WeatherAPI.com API key
.env file in project root:
WEATHER_API_KEY=<your_weatherapi_key>
DATABASE_URL=postgresql://postgres:yourpassword@db:5432/weather_app

**Installation & Running**
Clone the repository:
git clone <repo-url>
cd project-root

Create a .env file with your credentials as shown above.

Build and start services:
docker-compose up --build

Access services:
Streamlit UI: http://localhost:8501
FastAPI docs (Swagger UI): http://localhost:8000/docs

**Database Models**

User Table:

id (Integer, PK)
username (String, unique)
password (String, hashed)
created_at (Timestamp)


SearchHistory Table

id (Integer, PK)
user_id (Integer, FK -> users.id)
city_name (String)
searched_at (Timestamp)

**Future Enhancements**
Add HTTPS support via a reverse proxy (e.g., Nginx)
Implement JWT-based authentication
Deploy to cloud platforms



