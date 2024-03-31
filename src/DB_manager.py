import psycopg2
from configs.config import config

params_db = config()


class DBManager:
    def __init__(self, db_name):
        self.params_db = config()
        self.db_name = db_name

    def get_companies_and_vacancies_count(self):
        with psycopg2.connect(dbname=self.db_name, **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT company_name, COUNT(vacancy_name) '
                            'FROM companies '
                            'INNER JOIN vacancies USING (company_id)'
                            'GROUP BY company_id')
                answer = cur.fetchall()
        conn.close()
        return answer

    def get_all_vacancies(self):
        with psycopg2.connect(dbname=self.db_name, **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * '
                            'FROM vacancies')
                answer = cur.fetchall()
        conn.close()
        return answer

    def get_avg_salary(self):
        with psycopg2.connect(dbname=self.db_name, **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT AVG(salary) '
                            'FROM vacancies')
                answer = cur.fetchall()
        conn.close()
        return answer

    def get_vacancies_with_higher_salary(self):
        with psycopg2.connect(dbname=self.db_name, **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT vacancy_name '
                            'FROM vacancies '
                            'WHERE salary > (SELECT AVG(salary) FROM vacancies)')
                answer = cur.fetchall()
        conn.close()
        return answer

    def get_vacancies_with_keyword(self, keyword):
        with psycopg2.connect(dbname=self.db_name, **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT vacancy_name "
                            f"FROM vacancies "
                            f"WHERE vacancy_name LIKE '%{keyword}%'")
                answer = cur.fetchall()
        conn.close()
        return answer

    def save_to_database(self, list_employers, list_vacancies):
        with psycopg2.connect(dbname=self.db_name, **params_db) as conn:
            with conn.cursor() as cur:
                for employer in list_employers:
                    cur.execute(
                        f"INSERT INTO companies(company_name) "
                        f"VALUES ('{employer}')")
                    conn.commit()
                for vacancy in list_vacancies:
                    cur.execute(
                        "SELECT company_id FROM companies "
                        f"WHERE company_name = '{vacancy['employer']}'")
                    emp_id = cur.fetchone()[0]
                    cur.execute(
                        f"INSERT INTO vacancies(vacancy_name, salary, vacancy_url, company_id) "
                        f"VALUES"
                        f"('{vacancy['vacancy_name']}', '{int(vacancy['salary'])}', "
                        f"'{vacancy['url']}', {emp_id})")

        conn.close()
