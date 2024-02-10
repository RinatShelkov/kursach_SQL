from config import config
from src.dbmanager import DBManager
from src.utils import (
    api_hh,
    currency_to_string,
    salary_to_string,
    null_description,
    create_database,
    save_data_to_database,
)


def database_manager():
    # Создаем новую базу данных и таблицы для работы с проектом
    params = config()

    create_database("vacancy_hh", params)

    # Получаем данные по вакансиям чере апи запрос
    data_hh = api_hh()

    # Заполняем таблицы данными

    save_data_to_database(data_hh, "vacancy_hh", params)

    # Интерактив с пользователем

    print(
        """Для выбора операции над вакансиями выберите номер операции
    1 - получить список всех компаний и количество вакансий у каждой компании
    2 - получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию, описание
    3 - получить среднюю зарплату по вакансиям
    4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
    5 - получить список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
    )

    choice = int(input(f"Введите номер операции\n"))

    if choice == 1:
        for row in DBManager("vacancy_hh").get_companies_and_vacancies_count():
            print(f"{row[0]} - {row[1]} вакансий")

    elif choice == 2:
        for row in DBManager("vacancy_hh").get_all_vacancies():
            print(
                (
                    f"""Компания - {row[5]}, 
  вакансия: {row[0]}, 
  заработная плата {salary_to_string(row[1])}, валюта {currency_to_string(row[2])}, 
  ссылка на вакансию: {row[3]}, 
  краткое описание: {null_description(row[4])} """
                )
            )

    elif choice == 3:
        avg_salary = DBManager("vacancy_hh").get_avg_salary()
        print(
            f"""Средняя заработная плата по вакансиям:
в рублях {avg_salary[0]}
в тенге {avg_salary[1]}"""
        )

    elif choice == 4:
        for row in DBManager("vacancy_hh").get_vacancies_with_higher_salary():
            print(
                (
                    f"""Компания - {row[5]}, 
  вакансия: {row[0]}, 
  заработная плата {salary_to_string(row[1])}, валюта {currency_to_string(row[2])}, 
  ссылка на вакансию: {row[3]}, 
  краткое описание: {null_description(row[4])} """
                )
            )

    elif choice == 5:
        keyword = input("Введите ключевое слово:")
        list_search_keyword = DBManager("vacancy_hh").get_vacancies_with_keyword(keyword)
        if isinstance(list_search_keyword, str):
            return list_search_keyword
        else:
            for row in list_search_keyword:
                print(
                    (
                        f"""Компания - {row[5]}, 
  вакансия: {row[0]}, 
  заработная плата {salary_to_string(row[1])}, валюта {currency_to_string(row[2])}, 
  ссылка на вакансию: {row[3]}, 
  краткое описание: {null_description(row[4])} """
                    )
                )


if __name__ == "__main__":
    database_manager()
