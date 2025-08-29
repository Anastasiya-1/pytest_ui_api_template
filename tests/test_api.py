"""
Модуль автотестов для проверки поиска фильмов через API.

Сценарии включают позитивные, негативные проверки,
а также работу с пустыми, длинными запросами и ошибкой авторизации.
"""

import pytest
import allure
import requests

@allure.feature("Поиск фильмов по API")
class TestMovieSearchAPI:
    """
    Набор тестов для проверки функционала поиска фильмов через публичный API.
    """

    @pytest.mark.parametrize(
        "search_query,expected_in_result",
        [            ("search_exact", True),      # Точный запрос, ожидается результат
            ("search_partial", True),    # Частичный запрос, ожидается результат
            ("search_en", True),         # Поиск на английском, ожидается результат
        ]
    )
    @allure.story("Позитивные проверки поиска фильмов")
    def test_search_movie_positive(self, test_data, config, search_query, expected_in_result):
        """
        Проверяет успешный поиск фильма: результат не пустой.
        """
        base_url = config['api']['base_url']
        api_key = test_data['api_key']
        query = test_data[search_query]

        with allure.step(f"Выполнить GET /movie/search?query={query}"):
            headers = {"X-API-KEY": api_key}
            params = {"query": query}
            response = requests.get(
                f"{base_url}/movie/search",
                params=params,
                headers=headers,
                timeout=10
            )
            assert response.status_code == 200
            results = response.json().get("docs", [])
            if expected_in_result:
                assert len(results) > 0, "Ожидался хотя бы один фильм в ответе"

    @pytest.mark.parametrize(
        "search_query",
        [            "search_fake",   # Несуществующий фильм
            "search_invalid" # Некорректные символы
        ]
    )
    @allure.story("Негативные проверки поиска фильмов")
    def test_search_movie_negative(self, test_data, config, search_query):
        """
        Проверяет, что поиск по некорректному 
        или несуществующему фильму возвращает пустой результат.
        """
        base_url = config['api']['base_url']
        api_key = test_data['api_key']
        query = test_data[search_query]

        with allure.step(f"Выполнить GET /movie/search?query={query}"):
            headers = {"X-API-KEY": api_key}
            params = {"query": query}
            response = requests.get(
                f"{base_url}/movie/search",
                params=params,
                headers=headers,
                timeout=10
            )
            assert response.status_code == 200
            results = response.json().get("docs", [])
            assert len(results) == 0, "Ожидался пустой список фильмов"

    @allure.story("Поиск с пустым запросом")
    def test_search_movie_empty_query(self, test_data, config):
        """
        Проверяет, что при пустом поисковом запросе фильм не находится.
        """
        base_url = config['api']['base_url']
        api_key = test_data['api_key']
        query = ""

        with allure.step("Выполнить GET /movie/search?query='' (пустой запрос)"):
            headers = {"X-API-KEY": api_key}
            params = {"query": query}
            response = requests.get(
                f"{base_url}/movie/search",
                params=params,
                headers=headers,
                timeout=10
            )
            assert response.status_code == 200
            results = response.json().get("docs", [])
            assert len(results) == 0, "Для пустого запроса должен быть пустой результат"

    @allure.story("Поиск по очень длинной строке (100+ символов)")
    def test_search_movie_long_query(self, test_data, config):
        """
        Проверяет обработку длинного поискового запроса (100+ символов) — 
        результат должен быть пустым.
        """
        base_url = config['api']['base_url']
        api_key = test_data['api_key']
        query = "a" * 120

        with allure.step("Выполнить GET /movie/search?query=('a'*120)"):
            headers = {"X-API-KEY": api_key}
            params = {"query": query}
            response = requests.get(
                f"{base_url}/movie/search",
                params=params,
                headers=headers,
                timeout=10
            )
            assert response.status_code == 200
            results = response.json().get("docs", [])
            assert len(results) == 0, "Ожидался пустой список для слишком длинного запроса"

    @allure.story("Запрос без API-ключа")
    def test_search_movie_without_apikey(self, test_data, config):
        """
        Проверяет, что при отсутствии API-ключа сервер возвращает ошибку авторизации.
        """
        base_url = config['api']['base_url']
        query = test_data["search_exact"]

        with allure.step("Выполнить GET /movie/search без API-KEY"):
            params = {"query": query}
            response = requests.get(
                f"{base_url}/movie/search",
                params=params,
                timeout=10
            )
            assert response.status_code in (401, 403), (
                "Должен быть статус 401 или 403 (ошибка авторизации)"
            )
