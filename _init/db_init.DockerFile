# This Dockerfile is used to build the image for the database initialization services.
# It is based on the python:3.11.0-slim-buster image and installs the necessary dependencies for MySQL and MS SQL.

# Use the python:3.11.0-slim-buster image as the base image
FROM --platform=linux/amd64 python:3.11.0-slim-buster

# Update the package lists for upgrades and new package installations
RUN apt-get update && apt-get upgrade -y

# Install the necessary dependencies for MySQL
RUN apt-get install -y gcc default-libmysqlclient-dev pkg-config

# Set the environment variable ACCEPT_EULA to Y, which is required for MS SQL
ENV ACCEPT_EULA=Y

# Install the necessary dependencies for MS SQL
RUN apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc-dev

# Add the Microsoft repository key and list, update the package lists, and install the MS SQL ODBC driver and tools
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && apt-get install -y --no-install-recommends --allow-unauthenticated msodbcsql17 mssql-tools \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# Copy the requirements.txt file from the host to the current directory in the image
COPY requirements.txt ./

# Install the Python packages listed in requirements.txt
RUN pip install -r requirements.txt

# Copy the db_init.py file from the host to the current directory in the image
COPY db_init.py ./
