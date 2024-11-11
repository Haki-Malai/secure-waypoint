# secure-waypoint
A FastAPI backend for secure authentication and user management. Features CRUD operations, pagination, filtering, and search, all within a Docker setup for easy deployment. Reliably built and tested for high coverage.


## Features

Secure-Waypoint is built with a focus on security and efficiency, offering the following features:

  - Authentication and Authorization: Implements robust mechanisms for user authentication and role-based access control. Supported operations include:
    - User login with basic authentication and token refresh capabilities.
    - Role-based access control with predefined roles.

  - User Management: Provides comprehensive CRUD operations for managing user accounts, as well as additional capabilities:
    - Create, update, and delete user profiles.
    - Fetch single user details or list all users with support for pagination and filtering by creation year.
    - Search users by username.

  - API Documentation: Automatically generated OpenAPI documentation, making it easy to understand and interact with the API.

  - Secure Deployment: Dockerized environment with separate services for the application, PostgreSQL database, and Nginx web server, ensuring easy and secure deployments.

  - Testing: Comprehensive test suite with high coverage, ensuring the reliability and correctness of the application.

  - Logging: Centralized logging with log rotation and log level configuration for monitoring and debugging.

  - Scalability: Uses best practices for building scalable, maintainable and secure applications.

  - CLI Management: Provides a CLI tool for database management, shell access, and other administrative tasks.

## Prerequisites

Before you begin, ensure you have Docker installed on your machine. You will also need Poetry for Python dependency management.
Setup

1. Environment File:
    - Copy the .env.example file to create a .env file:
        ```bash
        cp .env.example .env
        ```
    - Adjust the .env file parameters according to your environment needs.

2. Building and Running the Application:

    - To build and start the services in detached mode:
        ```bash
        docker-compose up -d --build
        ```

    - Initialize the database and create the initial admin user:
        ```bash
        docker-compose exec api python -m cli db init
        ```

    - The application will be accessible at `http://localhost:8000` and `http://localhost`.

## Testing

To run the automated tests:

1. Install Dependencies:
    - Install the required packages using Poetry:
        ```bash
        poetry install
        ```

2.  Configure Test Environment:
    - Ensure the `POSTGRES_HOST` in the `.env` file is set to `localhost` to allow connectivity from your local machine for testing.

3. Run Tests:

    - Execute the tests using pytest:
        ```bash
        poetry run pytest
        ```

## Deployment

The application is ready for deployment using Docker, facilitating easy scaling and management within containerized environments.
