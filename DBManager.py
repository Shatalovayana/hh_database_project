from pprint import pprint

import psycopg2

from utils import config


class DBManager:

    def __init__(self, database_name):
        self.database_name = database_name

    @staticmethod
    def get_companies_and_vacancies_count():
        """Получает список всех компаний и количество вакансий у каждой компании."""
        params = config()
        conn = psycopg2.connect(dbname='HeadHunter', **params)

        with conn.cursor() as cur:
            cur.execute("""
                    SELECT company_name, open_vacancies FROM HH_employers
                """)
            print(cur.fetchall())
        conn.close()

    @staticmethod
    def get_all_vacancies():
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию."""
        params = config()
        conn = psycopg2.connect(dbname='HeadHunter', **params)

        with conn.cursor() as cur:
            cur.execute("""
                    SELECT HH_employers.company_name, vacancy, salary_min, HH_vacancies.url from HH_vacancies 
                    JOIN HH_employers USING (company_id)
                        """)
            cur.fetchall()
            print(cur.fetchall())
        conn.close()

    @staticmethod
    def get_avg_salary():
        """Получает среднюю зарплату по вакансиям."""
        params = config()
        conn = psycopg2.connect(dbname='HeadHunter', **params)

        with conn.cursor() as cur:
            cur.execute("""
                         SELECT AVG(salary_min) FROM HH_vacancies
                     """)
            print(cur.fetchall())
        conn.close()

    @staticmethod
    def get_vacancies_with_higher_salary():
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        params = config()
        conn = psycopg2.connect(dbname='HeadHunter', **params)

        with conn.cursor() as cur:
            cur.execute("""
                        SELECT vacancy, salary_min from HH_vacancies
                        WHERE salary_min > (SELECT AVG(salary_min) FROM HH_vacancies)
                     """)
            cur.fetchall()
            print(cur.fetchall())
        conn.close()

    @staticmethod
    def get_vacancies_with_keyword():
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        params = config()
        conn = psycopg2.connect(dbname='HeadHunter', **params)

        with conn.cursor() as cur:
            cur.execute("""
                       SELECT vacancy from HH_vacancies
                       WHERE vacancy IN ('Оператор видеонаблюдения')
                    """)
            print(cur.fetchall())
        conn.close()


DBManager.get_companies_and_vacancies_count()
DBManager.get_all_vacancies()
DBManager.get_avg_salary()
DBManager.get_vacancies_with_higher_salary()
DBManager.get_vacancies_with_keyword()
