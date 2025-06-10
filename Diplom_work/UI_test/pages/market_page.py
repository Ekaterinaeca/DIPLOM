import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class MarketDeliveryPage:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)

    @allure.step("Открытие Яндекс.Маркет Доставки")
    def open(self):
        """Открывает Яндекс.Маркет Доставку"""
        with allure.step("Переход на страницу Яндекс.Маркет Доставки"):
            self.driver.get("https://market-delivery.yandex.ru")

    @allure.step("Клик по категории 'Бургеры'")
    def click_burgers_category(self):
        """Нажимает на категорию 'Бургеры'"""
        with allure.step("Ожидание и клик по элементу категории 'Бургеры'"):
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.BURGERS_CATEGORY)
            ).click()

    @allure.step("Клик по категории 'Суши'")
    def click_sushi_category(self):
        """Нажимает на категорию 'Суши'"""
        with allure.step("Ожидание и клик по элементу категории 'Суши'"):
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.SUSHI_CATEGORY)
            ).click()

    @allure.step("Поиск товара: {product_name}")
    def search_product(self, product_name):
        """Поиск товара на Яндекс.Маркет Доставке"""
        with allure.step(f"Ввод текста '{product_name}' в поле поиска"):
            search_field = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[id='id_1']"))
            )
            search_field.send_keys(product_name)

        with allure.step("Клик по кнопке 'Найти'"):
            search_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Найти')]]"))
            )
            search_button.click()
        header = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        return header.is_displayed()

    @allure.step("Закрытие браузера")
    def close(self):
        """Закрывает браузер"""
        with allure.step("Завершение работы драйвера"):
            self.driver.quit()

    # Локаторы (можно также добавить в Allure-описание)
    BURGERS_CATEGORY = (By.XPATH, "//a[contains(@href, 'burgers') or contains(., 'Бургеры')]")
    SUSHI_CATEGORY = (By.XPATH, "//a[contains(@href, 'sushi') or contains(., 'Суши')]")