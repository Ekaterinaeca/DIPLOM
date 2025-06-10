import allure
from UI_test.pages.market_page import MarketDeliveryPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Поиск товаров")
@allure.title("Поиск тапочек на Яндекс.Маркете")
def test_search_tovar():
    """Тест проверяет поиск товара 'тапочки'"""
    page = MarketDeliveryPage()

    try:
        with allure.step("Открытие главной страницы"):
            page.open()

        with allure.step("Поиск товара 'тапочки'"):
            assert page.search_product("тапочки")

    finally:
        page.close()