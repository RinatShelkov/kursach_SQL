import load_dotenv
import os
import psycopg2

load_dotenv.load_dotenv()


class DBManager():
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



