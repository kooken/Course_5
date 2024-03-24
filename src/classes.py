import requests


class HH_api_db:

    list_employers = {
                      'СБЕР': '3529',
                      'Ростелеком': '2748',
                      'Точка': '2324020',
                      'Тинькофф': '78638',
                      'Яндекс': '1740',
                      'Газпромбанк': '3388',
                      'Медси': '106571',
                      'VK': '15478',
                      'Сибур':'3809',
                      'Ozon': '2180'
    }

    @staticmethod
    def get_request(employer_id) -> dict:
        params = {
            "page": 1,
            "per_page": 100,
            "employer_id": employer_id,
            "only_with_salary": True,
            "area": 113,
            "only_with_vacancies": True
        }
        return requests.get("https://api.hh.ru/vacancies/", params=params).json()['items']

    def get_vacancies(self):
        """Получение списка работодателей"""
        vacancies_list = []
        for employer in self.list_employers:
            emp_vacancies = self.get_request(self.list_employers[employer])
            for vacancy in emp_vacancies:
                if vacancy['salary']['from'] is None:
                    salary = 0
                else:
                    salary = vacancy['salary']['from']
                vacancies_list.append(
                    {'url': vacancy['alternate_url'], 'salary': salary,
                     'vacancy_name': vacancy['name'], 'employer': employer})
        return vacancies_list
