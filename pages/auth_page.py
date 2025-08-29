"""
Модуль для автоматизации тестирования страницы авторизации
с помощью Selenium WebDriver и интеграцией с Allure.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure

class AuthPage:
    """
    Позволяет открывать страницу, выполнять вход, получать сообщения об ошибках 
    и проверять успешную авторизацию пользователя.
    """

    def __init__(self, driver: WebDriver, base_url: str):
        """
        Инициализация страницы авторизации.

        Аргументы:
            driver (WebDriver): Экземпляр Selenium WebDriver.
            base_url (str): Базовый URL тестируемого приложения.
        """
        self.driver = driver
        self.url = base_url + "/login"

    @allure.step("Открыть страницу авторизации")
    def open(self):
        """
        Открывает страницу авторизации в браузере.
        """
        self.driver.get(self.url)

    @allure.step("Войти по email или телефону: {username}")
    def login(self, username: str, password: str):
        """
        Выполняет ввод логина и пароля, отправляет форму авторизации.

        Аргументы:
            username (str): Email или телефон пользователя.
            password (str): Пароль пользователя.
        """
        try:
            self.driver.find_element(By.CSS_SELECTOR, "input[name='login']").send_keys(username)
            self.driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(password)
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        except (NoSuchElementException, TimeoutException) as e:
            allure.attach(str(e), name="Ошибка при вводе логина/пароля",
                          attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Получить сообщение об ошибке")
    def get_error(self) -> str:
        """
        Получает текст сообщения об ошибке при неудачной авторизации.

        Возвращает:
            str: Текст сообщения об ошибке, либо пустая строка если его нет.
        """
        try:
            error = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-message"))
            )
            return error.text
        except TimeoutException:
            return ""
        except NoSuchElementException:
            return ""

    @allure.step("Проверка, что пользователь авторизован")
    def is_logged_in(self) -> bool:
        """
        Проверяет, что пользователь успешно авторизовался.

        Возвращает:
            bool: True, если признак авторизации обнаружен, иначе False.
        """
        return "logout" in self.driver.page_source
