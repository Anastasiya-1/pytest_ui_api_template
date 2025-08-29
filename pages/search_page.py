"""
Модуль описывает PageObject для страницы поиска фильмов,
реализует методы для открытия страницы, выполнения поиска
и получения результатов при помощи Selenium WebDriver и Allure.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class SearchPage:
    """
    PageObject для страницы поиска фильмов.

    Позволяет открывать страницу поиска, выполнять поиск по запросу,
    получать список найденных названий фильмов.
    """

    def __init__(self, driver: WebDriver, base_url: str):
        """
        Инициализация объекта SearchPage.

        Аргументы:
            driver (WebDriver): Экземпляр Selenium WebDriver.
            base_url (str): Базовый URL страницы поиска.
        """
        self.driver = driver
        self.url = base_url

    @allure.step("Открыть главную страницу")
    def open(self):
        """
        Открывает главную страницу поиска фильмов.
        """
        self.driver.get(self.url)

    @allure.step("Выполнить поиск по '{query}'")
    def search(self, query: str):
        """
        Выполняет поиск по заданному запросу.

        Аргументы:
            query (str): Строка поискового запроса.
        """
        search_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='search']")
        search_field.clear()
        search_field.send_keys(query)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    @allure.step("Получить названия найденных фильмов")
    def get_found_titles(self) -> list:
        """
        Получает список названий фильмов, найденных по поисковому запросу.

        Возвращает:
            list: Список названий фильмов.
        """
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".movie-title"))
        )
        return [el.text for el in self.driver.find_elements(By.CSS_SELECTOR, ".movie-title")]
