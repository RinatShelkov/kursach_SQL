# Проект по БД
### В рамках проекта вам необходимо получить данные о компаниях и вакансиях с сайта hh.ru, спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.

## Основные шаги проекта
- Получить данные о работодателях и их вакансиях с сайта hh.ru. Для этого используйте публичный API hh.ru и библиотеку 
requests
.
- Выбрать не менее 10 интересных вам компаний, от которых вы будете получать данные о вакансиях по API.
- Спроектировать таблицы в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях. Для работы с БД используйте библиотеку 
psycopg2
.
- Реализовать код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.
### Создать класс DBManager для работы с данными в БД.

#### Создать класс DBManager, который будет подключаться к БД PostgreSQL и иметь следующие методы:
 
- get_companies_and_vacancies_count()
 — получает список всех компаний и количество вакансий у каждой компании.
 
- get_all_vacancies()
 — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
 
- get_avg_salary()
 — получает среднюю зарплату по вакансиям.
 
- get_vacancies_with_higher_salary()
 — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
 
- get_vacancies_with_keyword()
 — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
#### Класс DBManager должен использовать библиотеку psycopg2 для работы с БД.

### Для запуска проекта необходимо  запустить файл main.py
#### На экране будет понятное взаимодействие с пользователем:
    Для выбора операции над вакансиями выберите номер операции
    1 - получить список всех компаний и количество вакансий у каждой компании
    2 - получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию, описание
    3 - получить среднюю зарплату по вакансиям
    4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
    5 - получить список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
    Введите номер операции
#### При выборе пятой операции , необходимо будет ввести дополнительно ключеове слово
    Введите ключевое слово:

### Детали оформления решения 
- Проект выложен на GitHub.
- Оформлен файл README.md с информацией, о чем проект, как его запустить и как с ним работать.
- Есть Python-модуль для создания и заполнения данными таблиц БД.