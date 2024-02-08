import os

import load_dotenv
import psycopg2

from src.utils import api_hh, get_list_vacancies_api, get_list_company_api

load_dotenv.load_dotenv()


def database_manager():
    # Создаем новую базу данных для работы с проектом
    # try:
    #     conn = psycopg2.connect(
    #         host="localhost", user="postgres", password=os.getenv("PASSWORD_BD"), client_encoding="UTF-8"
    #     )
    #     with conn.cursor() as cursor:
    #
    #         conn.autocommit = True
    #         cursor.execute("CREATE DATABASE vacancy_hh")
    #
    #     conn.close()
    #
    # finally:
    #     pass

    # Получаем данные по вакансиям чере апи запрос
    data_hh = api_hh()

    # Преобразуем данные из апи запроса в нужный формат для записи в БД
    data_vacancies = get_list_vacancies_api(data_hh)

    data_company = get_list_company_api(data_hh)

    # Создаем таблицы

    # with psycopg2.connect(
    #     host="localhost",
    #     database="vacancy_hh",
    #     user="postgres",
    #     password=os.getenv("PASSWORD_BD"),
    #     client_encoding="utf-8",
    # ) as conn:
    #
    #     with conn.cursor() as cursor:
    #
    #         cursor.execute(
    #             "CREATE TABLE employers(employer_id int PRIMARY KEY NOT NULL, "
    #             "company_name varchar(255), "
    #             "url varchar(255)); "
    #         )
    #         cursor.execute(
    #             "CREATE TABLE vacancies(vacancy_id int PRIMARY KEY NOT NULL, "
    #             "vacancy_name varchar(255), "
    #             "vacancy_salary int, "
    #             "salary_currency varchar(3), "
    #             "vacancy_url varchar(255), "
    #             "vacancy_description varchar(255), "
    #             "employer_id int REFERENCES employers(employer_id))"
    #         )

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
                            data["employer_id"]
                        ),
                    )

    finally:
        conn.close()


if __name__ == "__main__":
    database_manager()
