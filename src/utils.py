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
            company_id serial primary key,
            company_name varchar unique not null
            )
            """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id serial primary key,
                vacancy_name text not null,
                salary int,
                vacancy_url varchar not null,
                company_id serial,
                foreign key(company_id) references companies(company_id)
                )
                """)

    conn.commit()
    conn.close()
