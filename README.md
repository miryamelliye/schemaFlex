# Data Management System

This project is a backend system designed to allow users to dynamically manage data schemas, perform CRUD operations, and handle large data imports efficiently. The system provides secure, flexible APIs for schema management, data operations, and user notifications, ensuring scalability and robustness.

## Features

### Schema Management

- **Create, update, and delete tables and fields**: Users can dynamically define tables and fields, update the schema by adding new fields, and delete tables entirely.
- Example: Create a `Customer` table with fields like `name`, `email`, and `created_at`.
- Update the schema by adding a `phone_number` field to the existing `Customer` table.

### CRUD Operations with Search

- **Perform CRUD (Create, Read, Update, Delete) operations** on dynamically generated tables.
- **Search functionality**: The read operation supports filtering data with exact or partial matches on any field. Results are paginated, and sorting options are available for large data sets.

### Data Import

- **Large data import support**: Users can import data (e.g., 100,000+ records) in CSV format, with schema validation and error reporting for invalid records (e.g., missing fields or format errors).
- **Asynchronous processing**: Large imports are handled using Celery to process the data efficiently in the background.
- **CSV Import Example**: Import customer data into the `Customer` table, ensuring email uniqueness and required fields validation.

### Email Notifications

- Upon successful import completion, users receive an email confirmation using an integrated email service.

### Security

- **JWT token-based authentication**: Secure all API endpoints using JWT authentication, ensuring that only authorized users can perform actions.

## Dockerization

The project is dockerized and can be run using the following command:

```sh
docker-compose up -d --build
