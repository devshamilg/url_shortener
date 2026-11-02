## URL Shortener

A full-stack URL shortener built with FastAPI, PostgreSQL, and Redis. The application allows users to generate short links from long URLs, with Redis-based rate limiting to help prevent API abuse.

### Features
- URL Shortening: Convert long URLs into short, shareable links.
- URL Redirection: Redirect users to the original URL using a short code.
- Rate Limiting: Use Redis to limit request frequency and help prevent API abuse.
- Database Migrations: Manage database schema changes with Alembic.
- Containerization: Run the application and its dependencies using Docker.
- Web Interface: Provide a simple interface built with HTML, CSS, and JavaScript.

### Tech Stack

- Backend: FastAPI, SQLAlchemy, Docker, Redis, Alembic
- Frontend: Vanilla HTML/CSS, JavaScript
