import psycopg2
from configs.config import config

params_db = config()


class DBManager:
    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432'):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        with psycopg2.connect(dbname='HH_parser', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT company_name, COUNT(vacancy_name) '
                            'FROM vacancies '
                            'GROUP BY company_name')
                answer = cur.fetchall()
        conn.close()
        return answer

    def get_all_vacancies(self):
        with psycopg2.connect(dbname='HH_parser', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * '
                            'FROM vacancies')
                answer = cur.fetchall()
        conn.close()
        return answer

    def get_avg_salary(self):
        with psycopg2.connect(dbname='HH_parser', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT AVG(salary) '
                            'FROM vacancies')
                answer = cur.fetchall()
        conn.close()
        return answer

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with psycopg2.connect(dbname='HH_parser', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT vacancy_name '
                            'FROM vacancies '
                            'WHERE salary > (SELECT AVG(salary) FROM vacancies)')
                answer = cur.fetchall()
        conn.close()
        return answer

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        with psycopg2.connect(dbname='HH_parser', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT vacancy_name "
                            f"FROM vacancies "
                            f"WHERE vacancy_name LIKE '%{keyword}%'")
                answer = cur.fetchall()
        conn.close()
        return answer