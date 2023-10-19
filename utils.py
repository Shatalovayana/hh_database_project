from configparser import ConfigParser
import requests
import psycopg2

id_list_employers = ['1740', '87021', '2180', '4934', '3664', '1373', '78638', '565840', '80', '39305']


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


def get_hh_data():
    url = 'https://api.hh.ru/vacancies/'
    # Отправляем GET-запрос для получения данных о работодателях
    emp_vacancies_list = []
    for emp_id in id_list_employers:
        response = requests.get(url + f'?employer_id={emp_id}', headers={"User-Agent": "HH-User-Agent"}).json()
        emp_vacancies_list.extend(response['items'])
    return emp_vacancies_list


def get_employers_data():
    url = 'https://api.hh.ru/employers/'
    # Отправляем GET-запрос для получения данных о работодателях
    emp_list = []
    for emp_id in id_list_employers:
        response = requests.get(url + f'{emp_id}', headers={"User-Agent": "HH-User-Agent"}).json()
        emp_list.append({'id': response.get("id"),
                         'company_name': response.get("name"),
                         'url': response.get("site_url"),
                         'open_vacancies': response.get("open_vacancies")
                         })
    return emp_list


def format_data() -> list:
    """
    Форматирует полученные по АПИ данные в единый формат
    :return: vacancies: список вакансий в требуемом нам виде
    """
    vacancies = []
    hh_data = get_hh_data()
    for vacancy in hh_data:
        try:
            filtered_vacancies = {'vacancy': vacancy["name"],
                                  'salary_min': vacancy['salary']["from"],
                                  'url': vacancy["alternate_url"],
                                  'description': vacancy['snippet']["requirement"],
                                  'company_name': vacancy['employer']["name"],
                                  'company_id': vacancy['employer']["id"]}
        except (KeyError, TypeError, ValueError):
            filtered_vacancies = {'vacancy': vacancy["name"],
                                  'salary_min': 0,
                                  'url': vacancy["alternate_url"],
                                  'description': vacancy['snippet']["requirement"],
                                  'company_name': vacancy['employer']["name"],
                                  'company_id': vacancy['employer']["id"]}

        vacancies.append(filtered_vacancies)
    return vacancies


def save_data_to_database(database_name: str, params: dict):
    """Сохранение данных о каналах и видео в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)
    vacancy_data = format_data()
    with conn.cursor() as cur:
        for vacancy in vacancy_data:

            cur.execute(
                """
                INSERT INTO HH_vacancies (company_id, vacancy, salary_min, description, url)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING company_id
                """,
                (vacancy['company_id'], vacancy['vacancy'],
                 vacancy['salary_min'], vacancy['description'], vacancy['url'])
            )

        employer_data = get_employers_data()
        for employer in employer_data:
            cur.execute(
                """
                INSERT INTO HH_employers (company_id, company_name, open_vacancies, url)
                VALUES (%s, %s, %s, %s)
                RETURNING company_id
                """,
                (employer['id'], employer['company_name'], employer['open_vacancies'], employer['url']))
    conn.commit()
    conn.close()
