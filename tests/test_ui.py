"""
UI-тесты для проверки авторизации и поиска фильмов на сайте.
Покрывает позитивные и негативные сценарии для разных вариантов входа и поиска.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import allure

from pages.auth_page import AuthPage
from pages.search_page import SearchPage

@allure.feature("UI Авторизация")
class TestAuthUI:
    """
    Тесты UI авторизации через email и телефон.
    """

    @allure.story("Позитивные проверки: Авторизация")
    @pytest.mark.parametrize(
        "login,password",
        [            ("valid_email", "valid_password"),
            ("valid_phone", "valid_password"),
        ]
    )
    def test_auth_login_positive(self, browser, config, test_data, login, password):
        """
        Проверка авторизации с правильными данными EMAIL/PHONE.
        """
        auth = AuthPage(browser, config['ui']['base_url'])
        auth.open()
        auth.login(test_data[login], test_data[password])
        assert auth.is_logged_in(), "Пользователь должен авторизоваться"

    @allure.story("Негативные проверки: Авторизация")
    @pytest.mark.parametrize(
        "login,password,expected_error",
        [            ("", "", "Введите данные для входа"),
            ("valid_email", "", "Введите пароль"),
            ("", "valid_password", "Введите email или телефон"),
            ("invalid_email", "valid_password", "Неверные данные"),
        ]
    )
    def test_auth_login_negative(self, browser, config, test_data, login, password, expected_error):
        """
        Проверка авторизации с некорректными/пустыми данными.
        """
        auth = AuthPage(browser, config['ui']['base_url'])
        auth.open()
        auth.login(test_data.get(login, login), test_data.get(password, password))
        assert expected_error in auth.get_error(), (
            f"Сообщение об ошибке '{expected_error}'"
        )

@allure.feature("UI Поиск фильмов")
class TestSearchUI:
    """
    Тесты UI поиска фильмов по разным типам запросов.
    """

    @allure.story("Позитивные проверки поиска")
    @pytest.mark.parametrize(
        "search_term,should_find",
        [            ("search_exact", True),
            ("search_partial", True),
            ("search_en", True),
        ]
    )
    def test_search_film_positive(self, browser, config, test_data, search_term, should_find):
        """
        Проверка поиска по точному, частичному и английскому названию фильма.
        """
        page = SearchPage(browser, config['ui']['base_url'])
        page.open()
        page.search(test_data[search_term])
        found_titles = page.get_found_titles()
        if should_find:
            assert len(found_titles) > 0, "Должен быть найден хотя бы один фильм"
        else:
            assert len(found_titles) == 0, "Фильмы не должны быть найдены"

    @allure.story("Негативные проверки поиска")
    @pytest.mark.parametrize(
        "search_term",
        [            "search_fake",    # Несуществующий фильм
            "search_invalid", # Набор спецсимволов
            "",               # Пустой запрос
        ]
    )
    def test_search_film_negative(self, browser, config, test_data, search_term):
        """
        Проверка поиска с несуществующим, некорректным запросом или пустым.
        """
        page = SearchPage(browser, config['ui']['base_url'])
        page.open()
        page.search(test_data.get(search_term, search_term))
        found_titles = page.get_found_titles()
        assert len(found_titles) == 0, (
            "Результаты должны быть пустыми для некорректного запроса"
        )
