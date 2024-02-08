import os

import load_dotenv
import psycopg2

load_dotenv.load_dotenv()


class DBManager:
    def __init__(self, database):
        self.conn = psycopg2.connect(
            host='localhost',
            database=database,
            user="postgres",
            password=os.getenv('PASSWORD_BD')
        )

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "SELECT employers.company_name, COUNT(vacancies.vacancy_id) FROM employers LEFT JOIN vacancies USING(employer_id) GROUP BY employers.company_name ")
                return cursor.fetchall()
        finally:
            self.conn.close()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "SELECT vacancy_name, vacancy_salary, salary_currency, vacancy_url, employers.company_name FROM vacancies LEFT JOIN employers USING(employer_id)")
                return cursor.fetchall()
        finally:
            self.conn.close()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "SELECT vacancy_salary, salary_currency FROM vacancies")
                sum_rur = 0
                count_rur = 0
                sum_kzt = 0
                count_kzt = 0
                for row in cursor.fetchall():
                    if row[1] == 'RUR':
                        sum_rur = sum_rur + row[0]
                        count_rur += 1
                    elif row[1] == 'KZT':
                        sum_kzt = sum_kzt + row[0]
                        count_kzt += 1
                if (sum_rur != 0) and (sum_kzt != 0):
                    return (f"Средняя зарплата по вакансиям у которых заработная плата в рублях: {round(sum_rur / count_rur)}\n"
                            f"Средняя зарплата по вакансиям у которых заработная плата в тенге: {round(sum_kzt / count_kzt)}")
                elif sum_rur != 0:
                    return f"Средняя зарплата по вакансиям у которых заработная плата в рублях: {round(sum_rur / count_rur)}"
                elif sum_kzt != 0:
                    return f"Средняя зарплата по вакансиям у которых заработная плата в тенге: {round(sum_kzt / count_kzt)}"



        finally:
            self.conn.close()
