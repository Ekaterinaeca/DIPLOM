import allure
from UI_test.pages.market_page import MarketDeliveryPage


@allure.feature("Поиск товаров")
@allure.title("Поиск тапочек на Яндекс.Маркете")
def test_search_market():
    """Тест проверяет поиск товара 'тапочки'"""
    page = MarketDeliveryPage()

    try:
        with allure.step("Открыть главную страницу и выполнить поиск"):
            page.open()
            page.search_product("тапочки")

    finally:
        page.close()