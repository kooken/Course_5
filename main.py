from configs.config import config
from src.DB_manager import DBManager
from src.classes import HHApiDb
from src.utils import create_database, create_table


def main():
    params_db = config()
    create_database('hh_db', params_db)
    create_table('hh_db', params_db)

    initial_info = HHApiDb()
    all_employers = initial_info.list_employers
    all_vacancies = initial_info.get_vacancies()

    database_final = DBManager('hh_db')
    database_final.save_to_database(all_employers, all_vacancies)

    while True:
        task = input(
            "Enter 1 to get a list of all companies and the number of vacancies for each company\n"
            "Enter 2 to get a list of all vacancies with the company name, "
            "job title and salary, and links to the vacancy\n"
            "Enter 3 to get the average salary for vacancies\n"
            "Enter 4 to get a list of all vacancies with a salary higher than the average for all vacancies\n"
            "Enter 5 to get a list of all vacancies whose title contains the words passed to the method\n"
            "Enter Stop to terminate\n"
        )

        if task == "Stop":
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
            keyword = input('Enter keyword: ')
            print(database_final.get_vacancies_with_keyword(keyword))
            print()
        else:
            print('Incorrect query')


if __name__ == '__main__':
    main()
