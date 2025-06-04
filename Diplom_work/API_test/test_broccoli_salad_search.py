import allure
from API_test.pages.api_client import YandexMarketDeliveryAPI


@allure.epic("API Тесты Яндекс.Доставки")
@allure.feature("Поиск блюд")
@allure.story("Поиск салатов с брокколи")
def test_search_broccoli_salad():
    api = YandexMarketDeliveryAPI()

    # Тестовые данные
    test_location = {
        "longitude": 30.33136653698719,
        "latitude": 60.05417412219289
    }
    search_query = "Салат с брокколи"

    with allure.step(f"Выполнение поиска по запросу '{search_query}'"):
        response = api.search_food_items(
            search_text=search_query,
            location=test_location
        )

    with allure.step("Проверка структуры ответа"):
        allure.dynamic.title(f"Поиск: {search_query} - Проверка структуры ответа")
        assert isinstance(response, dict), "Ответ должен быть словарем"
        assert "blocks" in response, "В ответе должен быть ключ 'blocks'"
        allure.attach(
            str(response),
            name="Полный ответ API",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Анализ результатов поиска"):
        blocks = response["blocks"]
        assert len(blocks) > 0, "Должен быть хотя бы один блок"

        found_items = []
        for block in blocks:
            if block.get("type") == "places" and "payload" in block:
                for place in block["payload"]:
                    if "items" in place:
                        found_items.extend(place["items"])

        broccoli_salads = [
            item for item in found_items
            if "брокколи" in item.get("title", "").lower()
        ]

    with allure.step("Проверка найденных салатов с брокколи"):
        allure.dynamic.description(
            f"Найдено {len(broccoli_salads)} салатов с брокколи"
        )
        assert len(broccoli_salads) > 0, "Должен быть хотя бы один салат с брокколи"

        if broccoli_salads:
            allure.attach(
                "\n".join([f"{item['title']} - {item['price']}"
                           for item in broccoli_salads[:3]]),
                name="Первые 3 найденных салата",
                attachment_type=allure.attachment_type.TEXT
            )

    with allure.step("Проверка деталей первого найденного салата"):
        first_salad = broccoli_salads[0]
        assert "price" in first_salad, "У блюда должна быть указана цена"
        assert "weight" in first_salad, "У блюда должен быть указан вес"

        allure.attach(
            f"Название: {first_salad.get('title')}\n"
            f"Цена: {first_salad.get('price')}\n"
            f"Вес: {first_salad.get('weight')}",
            name="Детали первого салата",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Вывод статистики"):
        print(f"Найдено салатов с брокколи: {len(broccoli_salads)}")