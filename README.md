# Data Management System

**Note**: Due to time constraints, the project was implemented with a focus on dynamic schema management. As a result, JWT authentication was not included in this implementation, despite being used in my previous projects. The primary emphasis was on the dynamic aspects of the system.

This project is a backend system designed to allow users to dynamically manage data schemas, perform CRUD operations, and handle large data imports efficiently. The system provides secure, flexible APIs for schema management, data operations, and user notifications, ensuring scalability and robustness.

## Features

### Schema Management
- **User Interface Assumptions**: In this project, I assumed that the user interface would follow a step-by-step approach for schema management. Specifically, we designed the API with the assumption that: Users would first create tables before adding fields. This aligns with a typical workflow where a table structure is defined before specifying its individual components. Once a table is created, users would then proceed to add fields one by one. This sequential approach allows for a clear and organized way of defining the schema.
- **How it works**: When a table is created, the create_table function is invoked. This function dynamically generates the model for the table and creates it in the database using Django's schema_editor. When a field is created, the update_table_schema function is called. This function updates the existing table schema by adding the new field. It ensures that the schema in the database is consistent with the user-defined schema. This implementation focuses on dynamically managing schemas, allowing users to flexibly define and modify their database structure.

### CRUD Operations with Search

- **Perform CRUD (Create, Read, Update, Delete) operations** on dynamically generated tables by mentionning the table id in URL.
- **Search functionality**: The read operation supports filtering data with exact or partial matches on any field. Results are paginated, and sorting options are available for large data sets.

### Data Import

- **Large data import support**: Users can import data (e.g., 100,000+ records) in CSV format, with schema validation and error reporting for invalid records (e.g., missing fields or format errors).
- **Asynchronous processing**: Large imports are handled using Celery to process the data efficiently in the background.
- **CSV Import Example**: Import customer data into the `Customer` table, ensuring email uniqueness and required fields validation.

### Email Notifications (CELERY TASK)

- Upon successful import completion, users receive an email confirmation using an integrated email service.


## Dockerization

The project is dockerized and can be run using the following command:

```sh
docker-compose up -d --build
