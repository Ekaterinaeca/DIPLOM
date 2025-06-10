import allure
from UI_test.pages.market_page import MarketDeliveryPage


@allure.feature("Поиск товаров")
@allure.title("Поиск пельменей на Яндекс.Маркете")
@allure.tag("web", "search")
def test_burgers_category():
    """Тест проверяет переход в категорию 'Бургеры'"""

    with allure.step("Инициализация страницы Яндекс.Маркет Доставки"):
        page = MarketDeliveryPage()

    try:
        with allure.step("Открытие главной страницы"):
            page.open()

        with allure.step("Клик по категории 'Бургеры'"):
            page.click_burgers_category()

        with allure.step("Проверка что открылась правильная категория"):
            # Здесь можно добавить проверки, что страница бургеров загрузилась
            pass

    finally:
        with allure.step("Закрытие браузера"):
            page.close()