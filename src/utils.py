from typing import Any

import psycopg2
import requests


def api_hh() -> Any:
    """Функция выполняет апи запрос на сайт hh.ru по 10
    компаниям и получает вакансии каждой компании
    Перечень компаний(вместе с идентификаторами):
    1740 Яндекс
    3529 Сбер
    87021 WILDBERRIES
    78638 Тинькофф
    824486 Магнитогорский металлургический комбинат
    3388 Газпромбанк
    92972 Совкомбанк Страхование Жизни
    3776 МТС Диджитал
    414 Металлокомплект-М
    2180 OZon

    :return list[dictionary]"""

    try:
        response = requests.get(
            "https://api.hh.ru/vacancies?",
            params={"employer_id": (1740, 3529, 87021, 78638, 824486, 3388, 92972, 3776, 414, 2180), "per_page": 100},
        )
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.HTTPError as err:
        return f"Ошибка запроса requests.get -> {err}"

    return data["items"]


def dict_to_integer(dictionary: dict | None) -> int:
    """Функция записи заработной платы для HeadHunter из словаря в число

    :param dictionary: dict
    :return value: integer"""

    if dictionary is None:
        return 0
    for key, value in dictionary.items():
        if key == "from" and value is not None:
            if value > 0:
                return value
        if key == "to" and value is not None:
            if value > 0:
                return value


def dict_to_currency(dictionary: dict | None) -> str | int:
    """Функция записи валюты заработной платы для HeadHunter из словаря

    :param dictionary: dict
    :return value: str"""

    if dictionary is None:
        return 0
    for key, value in dictionary.items():
        if key == "currency" and value is not None:
            return value


def salary_to_string(salary: int) -> str | int:
    """Преобразование нуля в заработной плате в понятную строку для пользователя, если заработная плата не указана"""
    if salary == 0:
        return "не указана"
    else:
        return salary


def currency_to_string(currency: int | str) -> str | int:
    """Преобразование нуля в валюте  в понятную строку для пользователя, если валюта не указана"""

    if currency == "0":
        return "не указана"
    else:
        if currency == "RUR":
            return "Российский рубль"
        else:
            return "Казахстанский тенге"


def null_description(description: None | str) -> str:
    """Преобразование None в строку понятную для пользователя, при отсутствии описания"""

    if description is None:
        return "не указано"
    else:
        return description


def create_database(name_database: str, params: dict) -> None:
    """Функция создания базы данных и таблиц
    :param name_database - название базы данных
    :param params - параметры необходымые для поделючения к БД"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {name_database}")
    cur.execute(f"CREATE DATABASE {name_database}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=name_database, **params)
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
    conn.commit()
    conn.close()


def save_data_to_database(data_bd: list[dict[str, Any]], name_database: str, params: dict) -> None:
    """Функция записи данных в таблицы БД
    :param data_bd-данные для записи в таблицы
    :param name_database название БД куда будет записываться
    :param params - параметры необходымые для поделючения к БД
    """
    conn = psycopg2.connect(dbname=name_database, **params)
    with conn.cursor() as cur:
        for data in data_bd:
            cur.execute(
                "INSERT INTO employers(employer_id, company_name, url) VALUES ( %s, %s, %s) ON CONFLICT DO NOTHING",
                (data["employer"]["id"], data["employer"]["name"], data["employer"]["url"]),
            )

            cur.execute(
                "INSERT INTO vacancies(vacancy_id, vacancy_name, vacancy_salary, salary_currency,vacancy_url, vacancy_description, employer_id) VALUES ( %s, %s, %s, %s, %s, %s, %s)",
                (
                    data["id"],
                    data["name"],
                    dict_to_integer(data["salary"]),
                    dict_to_currency(data["salary"]),
                    data["url"],
                    data["snippet"]["requirement"],
                    data["employer"]["id"],
                ),
            )
    conn.commit()
    conn.close()
