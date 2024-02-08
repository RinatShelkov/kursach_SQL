import pprint
from typing import Any

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
        response = requests.get("https://api.hh.ru/vacancies?",
                                params={"employer_id": (1740, 3529, 87021, 78638, 824486, 3388, 92972, 3776, 414, 2180),
                                        "per_page": 100}
                                )
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.HTTPError as err:
        return f"Ошибка запроса requests.get -> {err}"

    return data["items"]


def get_list_vacancies_api(list_vacancies: list[dict]) -> list[dict]:
    """Функция выборки нужной информации из АПИ запроса
    возвращает словарь с данными:
    - название компании,
    - названии вакансии,
    - заработную плату,
    - валюта заработной платы,
    - ссылка на вакансию,
    - краткое описание

    :param list_vacancies: list[dict]
    :return list_dict_vacancies list[dict]"""

    list_dict_vacancies = []

    for vacancy in list_vacancies:
        dictionary = {
            "company_name": vacancy["employer"]["name"],
            "vacancy_name": vacancy["name"],
            "vacancy_salary": dict_to_integer(vacancy["salary"]),
            "salary_currency": dict_to_currency(vacancy["salary"]),
            "vacancy_url": vacancy["url"],
            "vacancy_description": vacancy["snippet"]["requirement"]
        }
        list_dict_vacancies.append(dictionary)
    return list_dict_vacancies


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


def get_all_values(list_dict: list[dict]) -> list[tuple]:
    """Функция преобразования списка словарей в список кортежей dict.values,
    для записи данных в БД

    :param list_dict: list[dict]
    :return list[tuple]"""

    result_list_turple = []

    for dictionary in list_dict:
        values = dictionary.values()
        turple_values = tuple(values)
        result_list_turple.append(turple_values)

    return result_list_turple

