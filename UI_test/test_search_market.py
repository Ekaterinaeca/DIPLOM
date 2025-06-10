import allure
from UI_test.pages.market_page import MarketDeliveryPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
            assert page.search_product("Пятёрочка")


    finally:
        with allure.step("Завершение теста: закрытие браузера"):
            page.close()