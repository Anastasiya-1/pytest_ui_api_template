# pytest_ui_api_template
Цель: Автоматизация UI и тест API-кейсов для Кинопоиска.

Структура:

tests/ — тесты

страницы/ — классы PageObject

api/ — классы API

data/ — тестовые данные

Запуск:

pip install -r requirements.txt

pytest test/test_ui.py

pytest test/test_api.py

pytest(все тесты)

pytest --alluredir=allure_files(отчет)

allure generate allure_files -o allure_report

allure open allure_report

# FINAL_PROJ: Pytest UI & API Autotests для Кинопоиска

## Описание задачи

Данный проект предназначен для автоматизации тестирования веб-интерфейса и API Кинопоиска с использованием фреймворка **Pytest**, библиотеки **Selenium** для UI-тестов и **requests** для API.  
Тесты покрывают позитивные и негативные сценарии: проверки авторизации, поиск фильмов через сайт и API, работу с ошибкой авторизации и некорректными запросами.

---

## Структура проекта

pytest_ui_api_template/
│
├── pages/ # PageObject модели для UI-тестов
│ ├── init.py
│ ├── auth_page.py # Модель страницы авторизации
│ ├── search_page.py # Модель страницы поиска
│ └── film_card_page.py # Модель карточки фильма
│
├── config/
│ ├── test_data.json # Тестовые данные и запросы для API/UI (создать по примеру)
│ └── config.ini # Настройки билдов, URL и ключи
│
├── tests/
│ ├── test_ui.py # UI-тесты
│ └── test_api.py # API-тесты
│
├── README.md # Описание проекта и инструкции
├── requirements.txt # Список зависимостей
└── pytest.ini # Конфиг Pytest


---

## Как запустить тесты

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/<ВАШ-GITHUB-USERNAME>/<ВАШ-REPO>.git
   cd <ВАШ-REPO>
Создайте и активируйте виртуальное окружение (рекомендуется):

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate  # Linux/Mac

Установите зависимости:

pip install -r requirements.txt

Используйте файл с тестовыми данными (config/test_data.json) 

Запуск тестов:

Все API-тесты:

pytest tests/test_api.py

Все UI-тесты:

pytest tests/test_ui.py

Запуск с отчетом для Allure:

pytest --alluredir=allure-results
allure serve allure-results

Ссылка на финальный проект https://github.com/Anastasiya-1/pytest_ui_api_template
