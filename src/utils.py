import psycopg2
from configs.config import config

params_db = config()


def create_database(database_name, params_db):

    conn = psycopg2.connect(dbname='postgres', **params_db)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')

    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()


def create_table(dbname, params):
    conn = psycopg2.connect(dbname=dbname, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
            company_id int primary key,
            company_name varchar unique not null,
            foreign key(company_name) references companies(company_name)
            )
            """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id serial primary key,
                vacancy_name text not null,
                salary int,
                company_name text not null,
                vacancy_url varchar not null
                )
                """)

    conn.commit()
    conn.close()
