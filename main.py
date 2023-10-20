from DBManager import DBManager
from utils import save_data_to_database, config, format_companies_and_vacancies_count, format_all_vacancies, \
    format_avg_salary, format_vacancies_with_higher_salary, format_vacancies_with_keyword


def main():
    params = config()
    save_data_to_database(database_name='HeadHunter', params=params)
    while True:
        user_input = input("""
1 - Вывести все компании и количество открытых вакансий,
2 - Вывести все вакансии,
3 - Вывести среднюю минимальную зарплату по всем вакансиям,
4 - Вывести все вакансии с зарплатой выше средней,
5 - Вывести вакансии по ключевому слову,
Exit - Выйти из программы.
        \n""")
        if user_input == '1':
            data = DBManager.get_companies_and_vacancies_count()
            format_data = format_companies_and_vacancies_count(data)
        elif user_input == '2':
            result = DBManager.get_all_vacancies()
            format_data = format_all_vacancies(result)
        elif user_input == '3':
            data_avg = DBManager.get_avg_salary()
            format_data = format_avg_salary(data_avg)
        elif user_input == '4':
            data_high_salary = DBManager.get_vacancies_with_higher_salary()
            format_data = format_vacancies_with_higher_salary(data_high_salary)
        elif user_input == '5':
            print('Введите вакансию для поиска:')
            user_input_keyword = input()
            for keyword in user_input_keyword:
                result = DBManager.get_vacancies_with_keyword(keyword)
                format_data = format_vacancies_with_keyword(result)
        elif user_input.lower() == "exit":
            print('До свидания!')
            break
        print(format_data)


if __name__ == '__main__':
    main()
