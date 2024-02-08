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
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT employers.company_name, COUNT(vacancies.vacancy_id) FROM employers LEFT JOIN vacancies USING(employer_id) GROUP BY employers.company_name ")
            return cursor.fetchall()


