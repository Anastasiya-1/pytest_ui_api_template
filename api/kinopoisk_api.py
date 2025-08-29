"""
Модуль для взаимодействия с API Кинопоиска.
"""

import requests
import allure

class KinopoiskApi:
    """
    Позволяет выполнять поиск фильмов по названию и получать
    детальную информацию о фильме через HTTP-запросы с использованием ключа API.
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Инициализация класса.

        Аргументы:
            base_url (str): Базовый URL для запросов к API Кинопоиска.
            api_key (str): API-ключ для аутентификации запросов.
        """
        self.base_url = base_url
        self.api_key = api_key

    @allure.step("Поиск фильма через API по запросу: {query}")
    def search_movie(self, query: str) -> dict:
        """
        Выполняет поиск фильма с помощью API Кинопоиска.

        Аргументы:
            query (str): Поисковый запрос для фильма.

        Возвращает:
            dict: Словарь с результатами поиска из API.

        Исключения:
            requests.RequestException: В случае возникновения ошибки при выполнении запроса к API.
        """
        headers = {"X-API-KEY": self.api_key}
        params = {"query": query}
        try:
            response = requests.get(
                f"{self.base_url}/movie/search",
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            allure.attach(str(e), name="Ошибка API", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Получение информации о фильме с ID: {movie_id}")
    def get_movie(self, movie_id: int) -> dict:
        """
        Получает подробную информацию о фильме по его ID.

        Аргументы:
            movie_id (int): Идентификатор фильма на Кинопоиске.

        Возвращает:
            dict: Словарь с информацией о фильме.

        Исключения:
            requests.RequestException: В случае ошибки при выполнении запроса к API.
        """
        headers = {"X-API-KEY": self.api_key}
        try:
            response = requests.get(
                f"{self.base_url}/movie/{movie_id}",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            allure.attach(str(e), name="Ошибка API", attachment_type=allure.attachment_type.TEXT)
            raise
