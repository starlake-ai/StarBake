# Docker Compose Configuration for Different Database Servers

This repository includes a Docker Compose file which allows you to set up three different types of database servers (MySQL, PostgreSQL, and MS SQL Server), initialize them with dummy data, and also includes Adminer UI for database management.

Additionally, a `Dockerfile` (`db_init.DockerFile`) is provided in order to create an image for initializing the databases.

## How to Use

Before proceeding, make sure you have installed [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).


To run a specific database with the respective database initializer and Adminer, use the following command that includes the appropriate profile:

- For MySQL:

    ```bash
    docker-compose --profile mssql  up --build --force-recreate  --renew-anon-volumes
    ```
- For PostgreSQL:

    ```bash
    docker-compose --profile postgres  up --build --force-recreate  --renew-anon-volumes
    ```
- For MS SQL:

    ```bash
    docker-compose --profile mssql  up --build --force-recreate  --renew-anon-volumes
    ```

3. Interact with the databases:
    - MySQL works at: `localhost:3306`
    - PostgreSQL works at: `localhost:5432`
    - MS SQL Server works at: `localhost:1433`

   Use the appropriate credentials as defined in the `docker-compose.yml` file to connect to these services.

## `db_init.DockerFile`

This Dockerfile setups a Python environment and install the necessary dependencies to run the `db_init.py` script which is used to initialize the respective databases.

The base image is `python:3.11.0-slim-buster` and it installs the necessary packages for connecting to all three databases.

