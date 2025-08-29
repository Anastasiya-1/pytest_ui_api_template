"""
Модуль содержит фикстуры для pytest:
- Загрузка тестовых данных и конфигурации;
- Настройка и завершение сессии браузера Chrome для автотестов.
"""

import configparser
import json

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='session')
def test_data():
    """
    Загружает тестовые данные из файла .json (один раз за сессию).
    """
    with open('config/test_data.json', encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture(scope='session')
def config():
    """
    Загружает конфигурацию из файла config.ini (один раз за сессию).
    """
    parser = configparser.ConfigParser()
    parser.read('config/config.ini')
    return parser

@pytest.fixture
def browser():
    """
    Запускает браузер Chrome в headless-режиме для каждого теста и корректно завершает сессию.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()
