import allure
from UI_test.pages.market_page import MarketDeliveryPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Поиск товаров")
@allure.title("Поиск пельменей на Яндекс.Маркете")
@allure.tag("web", "search")
def test_search_market():
    """Тест проверяет поиск товара 'пельмени' на Яндекс.Маркете"""
    page = MarketDeliveryPage()

    try:
        with allure.step("Открыть главную страницу"):
            page.open()
            WebDriverWait(page.driver, 45).until(
                EC.presence_of_element_located(("css selector", "input[data-testid='search-input']"))
            )

        with allure.step("Выполнить поиск товара 'пельмени'"):
            page.search_product("пельмени")

    finally:
        with allure.step("Закрыть браузер"):
            page.close()