import psycopg2
from configs.config import config

params_db = config()


class DBManager:
    def __init__(self):
        self.params_db = config()

    @classmethod
    def get_companies_and_vacancies_count(cls):
        with psycopg2.connect(dbname='postgres', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT company_name, COUNT(vacancy_name) '
                            'FROM vacancies '
                            'GROUP BY company_name')
                answer = cur.fetchall()
        conn.close()
        return answer

    @classmethod
    def get_all_vacancies(cls):
        with psycopg2.connect(dbname='postgres', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * '
                            'FROM vacancies')
                answer = cur.fetchall()
        conn.close()
        return answer

    @classmethod
    def get_avg_salary(cls):
        with psycopg2.connect(dbname='postgres', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT AVG(salary) '
                            'FROM vacancies')
                answer = cur.fetchall()
        conn.close()
        return answer

    @classmethod
    def get_vacancies_with_higher_salary(cls):
        with psycopg2.connect(dbname='postgres', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT vacancy_name '
                            'FROM vacancies '
                            'WHERE salary > (SELECT AVG(salary) FROM vacancies)')
                answer = cur.fetchall()
        conn.close()
        return answer

    @classmethod
    def get_vacancies_with_keyword(cls, keyword):
        with psycopg2.connect(dbname='postgres', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT vacancy_name "
                            f"FROM vacancies "
                            f"WHERE vacancy_name LIKE '%{keyword}%'")
                answer = cur.fetchall()
        conn.close()
        return answer

    @classmethod
    def save_to_database(cls, list_employers, list_vacancies):
        with psycopg2.connect(dbname='postgres', **params_db) as conn:
            with conn.cursor() as cur:
                for employer in list_employers:
                    cur.execute(
                        f"INSERT INTO companies(company_name) "
                        f"VALUES ('{employer}')")
                for vacancy in list_vacancies:
                    cur.execute(
                        f"INSERT INTO vacancies(vacancy_name, salary, company_name, vacancy_url) "
                        f"VALUES"
                        f"('{vacancy['vacancy_name']}', '{int(vacancy['salary'])}', "
                        f"'{vacancy['employer']}', '{vacancy['url']}')")

        conn.close()
