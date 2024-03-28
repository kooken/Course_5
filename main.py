from configs.config import config
from src.DB_manager import DBManager
from src.classes import HH_api_db
from src.utils import create_database, create_table


def main():
    params_db = config()
    create_database('hh_db', params_db)
    create_table('hh_db', params_db)

    initial_info = HH_api_db()
    all_employers = initial_info.list_employers
    all_vacancies = initial_info.get_vacancies()

    database_final = DBManager('hh_db')
    database_final.save_to_database(all_employers, all_vacancies)

    while True:
        task = input(
            "Введите 1, чтобы получить список всех компаний и количество вакансий у каждой компании\n"
            "Введите 2, чтобы получить список всех вакансий с указанием названия компании, "
            "названия вакансии и зарплаты и ссылки на вакансию\n"
            "Введите 3, чтобы получить среднюю зарплату по вакансиям\n"
            "Введите 4, чтобы получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
            "Введите 5, чтобы получить список всех вакансий, в названии которых содержатся переданные в метод слова\n"
            "Введите Стоп, чтобы завершить работу\n"
        )

        if task == "Стоп":
            break
        elif task == '1':
            print(database_final.get_companies_and_vacancies_count())
            print()
        elif task == '2':
            print(database_final.get_all_vacancies())
            print()
        elif task == '3':
            print(database_final.get_avg_salary())
            print()
        elif task == '4':
            print(database_final.get_vacancies_with_higher_salary())
            print()
        elif task == '5':
            keyword = input('Введите ключевое слово: ')
            print(database_final.get_vacancies_with_keyword(keyword))
            print()
        else:
            print('Неправильный запрос')


if __name__ == '__main__':
    main()
