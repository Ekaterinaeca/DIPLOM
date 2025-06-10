import allure
from pages.market_page import MarketDeliveryPage


@allure.feature("Категории товаров")
@allure.title("Проверка категории 'Суши'")
def test_sushi_category():
    """Тест проверяет переход в категорию 'Суши'"""
    with allure.step("Подготовка: инициализация страницы"):
        page = MarketDeliveryPage()

    try:
        with allure.step("1. Открыть главную страницу"):
            page.open()

        with allure.step("2. Перейти в категорию 'Суши'"):
            page.click_sushi_category()

    finally:
        with allure.step("Завершение: закрыть браузер"):
            page.close()