import os
from src.dbmanager import DBManager
import load_dotenv
import psycopg2

from src.utils import (
    api_hh,
    get_list_vacancies_api,
    get_list_company_api,
    currency_to_string,
    salary_to_string,
    null_description,
)

load_dotenv.load_dotenv()


def database_manager():
    # Создаем новую базу данных для работы с проектом
    try:
        conn = psycopg2.connect(
            host="localhost", user="postgres", password=os.getenv("PASSWORD_BD"), client_encoding="UTF-8"
        )
        with conn.cursor() as cursor:

            conn.autocommit = True
            cursor.execute("CREATE DATABASE vacancy_hh")

        conn.close()

    finally:
        pass

    # Получаем данные по вакансиям чере апи запрос
    data_hh = api_hh()

    # Преобразуем данные из апи запроса в нужный формат для записи в БД
    data_vacancies = get_list_vacancies_api(data_hh)

    data_company = get_list_company_api(data_hh)

    # Создаем таблицы

    with psycopg2.connect(
        host="localhost",
        database="vacancy_hh",
        user="postgres",
        password=os.getenv("PASSWORD_BD"),
        client_encoding="utf-8",
    ) as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                "CREATE TABLE employers(employer_id int PRIMARY KEY NOT NULL, "
                "company_name varchar(255), "
                "url varchar(255)); "
            )
            cursor.execute(
                "CREATE TABLE vacancies(vacancy_id int PRIMARY KEY NOT NULL, "
                "vacancy_name varchar(255), "
                "vacancy_salary int, "
                "salary_currency varchar(3), "
                "vacancy_url varchar(255), "
                "vacancy_description varchar(255), "
                "employer_id int REFERENCES employers(employer_id))"
            )

    # Заполняем таблицы данными

    conn = psycopg2.connect(
        host="localhost", database="vacancy_hh", user="postgres", password=os.getenv("PASSWORD_BD")
    )
    try:
        with conn:
            with conn.cursor() as cur:
                for data in data_company:
                    cur.execute(
                        "INSERT INTO employers(employer_id, company_name, url) VALUES ( %s, %s, %s) ON CONFLICT DO NOTHING",
                        (data["id"], data["company_name"], data["company_url"]),
                    )

    finally:
        conn.close()

    conn = psycopg2.connect(
        host="localhost", database="vacancy_hh", user="postgres", password=os.getenv("PASSWORD_BD")
    )
    try:
        with conn:
            with conn.cursor() as cur:
                for data in data_vacancies:
                    cur.execute(
                        "INSERT INTO vacancies(vacancy_id, vacancy_name, vacancy_salary, salary_currency,vacancy_url, vacancy_description, employer_id) VALUES ( %s, %s, %s, %s, %s, %s, %s)",
                        (
                            data["id"],
                            data["vacancy_name"],
                            data["vacancy_salary"],
                            data["salary_currency"],
                            data["vacancy_url"],
                            data["vacancy_description"],
                            data["employer_id"],
                        ),
                    )

    finally:
        conn.close()
    print(
        """Для выбора операции над вакансиями выберите номер операции
    1 - получить список всех компаний и количество вакансий у каждой компании
    2 - получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию, описание
    3 - получить среднюю зарплату по вакансиям
    4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
    5 - получить список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
    )

    choice = int(input(f"Введите номер операции\n"))
    print(type(choice))

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
