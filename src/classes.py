import requests


class HHApiDb:

    list_employers = {
                      'Sber': '3529',
                      'Rostelecom': '2748',
                      'Tochka': '2324020',
                      'Tinkoff': '78638',
                      'Yandex': '1740',
                      'Gazprombank': '3388',
                      'Medsi': '106571',
                      'VK': '15478',
                      'Sibur': '3809',
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
