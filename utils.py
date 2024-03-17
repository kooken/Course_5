import psycopg2
from config import config
from classes import HH_api_db


params_db = config()


def create_database(database_name, params_db):

    conn = psycopg2.connect(dbname='HH_parser', **params_db)
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(f'DROP DATABASE {database_name}')
    except psycopg2.errors.InvalidCatalogName:
        print('База данных не существует')

        cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()


def create_table(params):

    conn = psycopg2.connect(dbname='HH_parser', **params)
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


def employers_to_db(self):
    with psycopg2.connect(dbname='HH_parser', **params_db) as conn:
        with conn.cursor() as cur:
            for employer in self.employers_dict:
                cur.execute(
                    f"INSERT INTO companies values ('{int(self.employers_dict[employer])}', '{employer}')")

    conn.commit()
    conn.close()


def vacancies_to_db(self):
    with psycopg2.connect(dbname='HH_parser', **params_db) as conn:
        with conn.cursor() as cur:
            for vacancy in self.get_vacancies():
                cur.execute(
                    f"INSERT INTO vacancies(vacancy_name, salary, company_name, vacancy_url) values "
                    f"('{vacancy['vacancy_name']}', '{int(vacancy['salary'])}', "
                    f"'{vacancy['employer']}', '{vacancy['url']}')")
    conn.commit()
    conn.close()
