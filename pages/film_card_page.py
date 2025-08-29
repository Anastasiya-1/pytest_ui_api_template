"""
Модуль описывает PageObject для карточки фильма,
обеспечивая методы для проверки содержимого и взаимодействия с элементами
страницы карточки фильма с помощью Selenium WebDriver и интеграции с Allure.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import allure

class FilmCardPage:
    """
    PageObject для карточки фильма.

    Позволяет получать данные о фильме, списке актёров, наличии постера,
    а также выполнять взаимодействие с элементами карточки.
    """

    def __init__(self, driver: WebDriver):
        """
        Инициализация объекта FilmCardPage.

        Аргументы:
            driver (WebDriver): Экземпляр Selenium WebDriver.
        """
        self.driver = driver

    @allure.step("Открыть карточку фильма по URL: {url}")
    def open_by_url(self, url: str):
        """
        Открывает карточку фильма по заданному URL.

        Аргументы:
            url (str): URL страницы карточки фильма.
        """
        self.driver.get(url)

    @allure.step("Получить название фильма")
    def get_title(self) -> str:
        """
        Получает название фильма с карточки.

        Возвращает:
            str: Название фильма.
        """
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".film-title"))
        )
        return self.driver.find_element(By.CSS_SELECTOR, ".film-title").text

    @allure.step("Получить описание фильма")
    def get_description(self) -> str:
        """
        Получает описание фильма.

        Возвращает:
            str: Описание, либо пустая строка, если элемент не найден.
        """
        desc = self.driver.find_elements(By.CSS_SELECTOR, ".film-description")
        return desc.text if desc else ""

    @allure.step("Получить список актёров")
    def get_actors(self) -> list:
        """
        Получает список актёров, указанных на карточке фильма.

        Возвращает:
            list: Список имён актёров.
        """
        actors = self.driver.find_elements(By.CSS_SELECTOR, ".film-actors .actor")
        return [a.text for a in actors]

    @allure.step("Проверить наличие постера")
    def has_poster(self) -> bool:
        """
        Проверяет наличие изображения постера на карточке фильма.

        Возвращает:
            bool: True, если хотя бы один постер найден и отображён.
        """
        posters = self.driver.find_elements(By.CSS_SELECTOR, ".film-poster img")
        return bool(posters) and all(p.is_displayed() for p in posters)

    @allure.step("Кликнуть по имени актёра №{index}")
    def click_actor(self, index: int = 0):
        """
        Кликает по имени актёра с заданным индексом.

        Аргументы:
            index (int): Индекс актёра в списке (по умолчанию – первый).

        Исключения:
            IndexError: Если индекс вне диапазона списка актёров.
        """
        actors = self.driver.find_elements(By.CSS_SELECTOR, ".film-actors .actor")
        if index < len(actors):
            actors[index].click()
        else:
            raise IndexError("Actor index out of range.")

    @allure.step("Проверить наличие сообщения об ошибке или отсутствии карточки")
    def get_error_message(self) -> str:
        """
        Получает сообщение об ошибке (например, если карточка не найдена).

        Возвращает:
            str: Текст ошибки или пустая строка, если элемент не найден.
        """
        err = self.driver.find_elements(By.CSS_SELECTOR, ".error-message")
        return err.text if err else ""

    @allure.step("Проверить, открыт ли карточка фильма")
    def is_opened(self) -> bool:
        """
        Проверяет, открыт ли элемент с названием фильма.

        Возвращает:
            bool: True, если карточка открыта.
        """
        return len(self.driver.find_elements(By.CSS_SELECTOR, ".film-title")) > 0

    @allure.step("Клик по некликабельному элементу")
    def try_click_invalid_element(self):
        """
        Пытается кликнуть по некликабельному (disabled) элементу на карточке фильма.

        Исключения:
            NoSuchElementException: Если такой элемент не найден.
        """
        elems = self.driver.find_elements(By.CSS_SELECTOR, ".film-card [disabled]")
        if elems:
            try:
                elems.click()
            except Exception as e:
                allure.attach(str(e), name="Ошибка клика по некликабельному элементу",
                              attachment_type=allure.attachment_type.TEXT)
                raise
        else:
            raise NoSuchElementException("No invalid element found.")
