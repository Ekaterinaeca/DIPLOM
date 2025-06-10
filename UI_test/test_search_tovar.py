import allure
from UI_test.pages.market_page import MarketDeliveryPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Поиск товаров")
@allure.title("Поиск тапочек на Яндекс.Маркете")
def test_search_market():
    """Тест проверяет поиск товара 'тапочки'"""
    page = MarketDeliveryPage()

    try:
        with allure.step("Открыть главную страницу и выполнить поиск"):
            page.open()
            WebDriverWait(page.driver, 45).until(
                EC.presence_of_element_located(("css selector", "input[data-testid='search-input']"))
            )
            page.search_product("тапочки")

    finally:
        page.close()