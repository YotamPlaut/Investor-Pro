# InvestorPro-Dataops

## Overview 
This file will guide you throw the InvestorPro Dataops semi_project
In order to use this project you will need: 
 1. An account in TASE HUB API (the Israeli stock market API we worked against in this project), or you can just choose to use any other API you want, just remember to replace the API calls :)
 2. Postgres instance located on GCP, this will be our DB in this project. 
 3. Docker & airflow ,In this project, we are using airflow to run our ETL's, we used it locally on our own machine,so we will also need  docker to run it.

Assuming you already cloned the InvestorPro Project into your one local machine,you should be able to see the 2 main folder this part uses:
- dataOps-dev -> this is our development plaform, we use it for testing, and manually preform operation against the TASE HUB API (will be adrass soon) and the CG