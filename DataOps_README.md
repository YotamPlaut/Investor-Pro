# InvestorPro DataOps

## Overview

This guide will walk you through the InvestorPro DataOps semi-project. To effectively use this project, you'll need:

1. **TASE HUB API Account**: This is the Israeli stock market API used in this project. You can also choose any other API, but remember to update the API calls accordingly.
2. **Postgres Instance on GCP**: This will serve as our database for the project.
3. **Docker & Airflow**: We use Airflow for running our ETL processes, and Docker to containerize the environment.

## Project Structure

After cloning the InvestorPro project to your local machine, you will find two main folders:

- **`dataOps-dev`**: This is our development environment. It is used for testing and manually performing operations against the TASE HUB API and the database.
- **`airflow`**: This folder contains our production environment. It includes all the ETL processes required to supply the application with necessary data.