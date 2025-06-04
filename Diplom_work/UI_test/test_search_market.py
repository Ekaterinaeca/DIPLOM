import allure
from UI_test.pages.market_page import MarketDeliveryPage


@allure.feature("Поиск магазинов")
@allure.title("Поиск магазина 'Пятёрочка'")
def test_search_market():
    """Тест проверяет поиск магазина 'Пятёрочка' в Яндекс.Маркете"""
    with allure.step("Инициализация страницы"):
        page = MarketDeliveryPage()

    try:
        with allure.step("Открытие главной страницы"):
            page.open()

        with allure.step("Поиск магазина 'Пятёрочка'"):
            page.search_product("Пятёрочка")  # Исправлено search_produkt -> search_product

    finally:
        with allure.step("Завершение теста: закрытие браузера"):
            page.close()