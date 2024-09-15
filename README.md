# Job Listings Data Project

A project to collect, store, and manage data about companies and job vacancies from the HH.ru API, and interact with the data using a PostgreSQL database. Key features include:

- **API Integration**: Gathers job and company data from the HH.ru API.
- **Database Design**: PostgreSQL tables designed to store company and job vacancy data.
- **Automated Data Ingestion**: Populates the database using `psycopg2`.
- **DBManager Class**: Implements methods to retrieve company and vacancy data, including vacancy counts, salary analysis, and keyword searches.
- **Technologies**: Python, requests, PostgreSQL, psycopg2

The information in the configs/database.ini file must be filled in with your data!