import allure
from API_test.pages.api_client import YandexMarketDeliveryAPI


@allure.epic("Yandex Market Delivery API")
@allure.feature("Поиск магазинов")
@allure.story("Поиск магазина 'Пятерочка'")
@allure.title("Поиск магазина Пятерочка и проверка товаров")
def test_search_pyaterochka():
    api = YandexMarketDeliveryAPI()

    # Тестовые данные
    test_location = {
        "longitude": 30.33136653698719,
        "latitude": 60.05417412219289
    }

    with allure.step("Выполнить поиск магазина 'Пятерочка'"):
        response = api.search_food_items(
            search_text="пятерочка",
            location=test_location
        )
        allure.attach(str(response), name="Полный ответ API", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверить структуру ответа"):
        assert isinstance(response, dict), "Ответ должен быть словарем"
        assert "header" in response, "Должен быть заголовок с результатами"
        assert "blocks" in response, "Должны быть блоки с результатами"

    with allure.step("Проверить заголовок с количеством результатов"):
        assert "Найден 1 результат" in response["header"]["text"], "Неверное количество результатов"

    with allure.step("Найти блоки с магазинами"):
        blocks = response["blocks"]
        assert len(blocks) > 0, "Должен быть хотя бы один блок"

        found_places = []
        for block in blocks:
            if block.get("type") == "places" and "payload" in block:
                found_places.extend(block["payload"])

        allure.attach(str(len(found_places)), name="Количество найденных магазинов",
                      attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверить наличие магазина Пятерочка"):
        assert len(found_places) > 0, "Должен быть найден хотя бы один магазин"
        first_place = found_places[0]
        allure.attach(first_place["title"], name="Название найденного магазина",
                      attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверить товары в магазине"):
        assert "items" in first_place, "У места должны быть товары"
        assert len(first_place["items"]) >= 4, "Должно быть несколько товаров"

        products = first_place["items"]
        allure.attach(str(len(products)), name="Количество найденных товаров",
                      attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверить наличие конкретных товаров"):
        product_names = [p["title"].lower() for p in products]

        # Проверка кетчупа
        has_ketchup = any("кетчуп" in name for name in product_names)
        allure.attach(str(has_ketchup), name="Найден ли кетчуп",
                      attachment_type=allure.attachment_type.TEXT)
        assert has_ketchup, "Должен быть кетчуп"

        # Проверка соуса
        has_sauce = any("соус" in name for name in product_names)
        allure.attach(str(has_sauce), name="Найден ли соус",
                      attachment_type=allure.attachment_type.TEXT)
        assert has_sauce, "Должен быть соус"

    with allure.step("Вывести информацию о товарах"):
        products_info = [f"Найдено товаров в магазине: {len(products)}"]
        products_info.extend([f"- {product['title']} ({product['price']})" for product in products[:3]])

        allure.attach("\n".join(products_info), name="Информация о товарах",
                      attachment_type=allure.attachment_type.TEXT)