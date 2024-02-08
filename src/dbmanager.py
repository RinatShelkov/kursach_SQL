import os
import pprint
import re

import load_dotenv
import psycopg2

load_dotenv.load_dotenv()


class DBManager:
    def __init__(self, database):
        self.database = database
        self.conn = psycopg2.connect(
            host="localhost", database=database, user="postgres", password=os.getenv("PASSWORD_BD")
        )

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "SELECT employers.company_name, COUNT(vacancies.vacancy_id) FROM employers LEFT JOIN vacancies USING(employer_id) GROUP BY employers.company_name "
                )
                return cursor.fetchall()
        finally:
            self.conn.close()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию, описание"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "SELECT vacancy_name, vacancy_salary, salary_currency, vacancy_url, vacancy_description, employers.company_name FROM vacancies LEFT JOIN employers USING(employer_id)"
                )
                return cursor.fetchall()
        finally:
            self.conn.close()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT vacancy_salary, salary_currency FROM vacancies")
                sum_rur = 0
                count_rur = 0
                sum_kzt = 0
                count_kzt = 0
                for row in cursor.fetchall():
                    if row[1] == "RUR":
                        sum_rur = sum_rur + row[0]
                        count_rur += 1
                    elif row[1] == "KZT":
                        sum_kzt = sum_kzt + row[0]
                        count_kzt += 1
                if (sum_rur != 0) and (sum_kzt != 0):
                    return [round(sum_rur / count_rur), round(sum_kzt / count_kzt)]
                elif sum_rur != 0:
                    return [round(sum_rur / count_rur), 0]
                elif sum_kzt != 0:
                    return [0, round(sum_kzt / count_kzt)]
        finally:
            self.conn.close()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""

        avg_salary = self.get_avg_salary()
        # сделал так , потому соединение закрывается с базой данных после avg_salary = self.get_avg_salary()
        list_all_vacancies = DBManager(self.database).get_all_vacancies()

        list_above_average = []

        for row in list_all_vacancies:
            if (row[2] == "RUR") and (avg_salary[0] != 0) and (row[1] >= avg_salary[0]):
                list_above_average.append(row)
            elif (row[2] == "KZT") and (avg_salary[1] != 0) and (row[1] >= avg_salary[1]):
                list_above_average.append(row)
        return list_above_average

    def get_vacancies_with_keyword(self, keyword):

        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""

        list_search_vacancies = []
        for row in self.get_all_vacancies():
            if row[0] is not None:
                if (re.search(keyword, row[0], flags=re.IGNORECASE)):
                        list_search_vacancies.append(row)
            elif row[4] is not None:
                if (re.search(keyword, row[4], flags=re.IGNORECASE)):
                        list_search_vacancies.append(row)
        return list_search_vacancies


pprint.pprint(DBManager('vacancy_hh').get_vacancies_with_keyword("аналитик"))
