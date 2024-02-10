from typing import Any
import dotenv
import os
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


def get_list_vacancies_api(list_data: list[dict]) -> list[dict]:
    """Функция выборки нужной информации из АПИ запроса
    возвращает словарь с данными:
    - названии вакансии,
    - заработную плату,
    - валюта заработной платы,
    - ссылка на вакансию,
    - краткое описание

    :param list_data: list[dict]
    :return list_dict_vacancies list[dict]"""

    list_dict_vacancies = []

    for vacancy in list_data:
        dictionary = {
            "id": vacancy["id"],
            "vacancy_name": vacancy["name"],
            "vacancy_salary": dict_to_integer(vacancy["salary"]),
            "salary_currency": dict_to_currency(vacancy["salary"]),
            "vacancy_url": vacancy["url"],
            "vacancy_description": vacancy["snippet"]["requirement"],
            "employer_id": vacancy["employer"]["id"],
        }
        list_dict_vacancies.append(dictionary)
    return list_dict_vacancies


def get_list_company_api(list_data: list[dict]) -> list[dict]:
    """Функция выборки нужной информации из АПИ запроса
    возвращает словарь с данными:
    - название компании,
    - ссылка на компанию

    :param list_data: list[dict]
    :return list_dict_company list[dict]"""

    list_dict_company = []

    for vacancy in list_data:
        dictionary = {
            "id": vacancy["employer"]["id"],
            "company_name": vacancy["employer"]["name"],
            "company_url": vacancy["employer"]["url"],
        }
        list_dict_company.append(dictionary)
    return list_dict_company


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

def create_database(name_database:str, params:dict)->None:
    """Функция создания базы данных и таблиц
    :param name_database - название базы данных
    :param params - параметры необходымые для поделючения к БД"""

    conn = psycopg2.connect(dbname=name_database, **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {name_database}")
    cur.execute(f"CREATE DATABASE {name_database}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname = name_database, **params)
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

