import allure
from API_test.pages.api_client import YandexMarketDeliveryAPI


@allure.epic("Yandex Market Delivery API")
@allure.feature("Поиск товаров")
@allure.story("Поиск с отсутствием прямых результатов")
def test_search_with_no_direct_results():
    api = YandexMarketDeliveryAPI()

    # Тестовые данные
    test_location = {
        "longitude": 30.33136653698719,
        "latitude": 60.05417412219289
    }

    with allure.step("Выполнить поиск товара с текстом 'вотон'"):
        response = api.search_food_items(
            search_text="вотон",
            location=test_location
        )

    with allure.step("Проверить заголовок с сообщением о отсутствии точных результатов"):
        assert "header" in response, "Должен быть заголовок ответа"
        assert "Ничего не нашли, но есть:" in response["header"]["text"], \
            "Ожидалось сообщение о отсутствии точных результатов"

    with allure.step("Проверить наличие альтернативных вариантов"):
        assert "blocks" in response, "Должны быть блоки с результатами"
        assert len(response["blocks"]) > 0, "Должен быть хотя бы один блок с альтернативами"

    with allure.step("Проверить структуру альтернативных предложений"):
        places_block = next(
            (block for block in response["blocks"] if block["type"] == "places"),
            None
        )
        assert places_block is not None, "Должен быть блок с местами"
        assert len(places_block["payload"]) >= 3, "Должно быть несколько альтернативных мест"

    with allure.step("Проверить содержание альтернатив"):
        alternative_places = places_block["payload"]
        place_titles = [place["title"] for place in alternative_places]

        # Проверяем, что есть ожидаемые альтернативы
        expected_alternatives = ["ВкусВилл", "Яндекс Лавка", "Азбука вкуса"]
        found_alternatives = [title for title in place_titles
                            if any(alt in title for alt in expected_alternatives)]

        assert len(found_alternatives) >= 2, \
            f"Должно быть хотя бы 2 из ожидаемых альтернатив: {expected_alternatives}"

    with allure.step("Проверить информацию о доставке для альтернатив"):
        for place in alternative_places[:3]:  # Проверяем первые 3 места
            assert "delivery" in place, "У места должна быть информация о доставке"
            assert "text" in place["delivery"], "Должно быть время доставки"
            assert "available" in place, "Должен быть статус доступности"

    with allure.step("Вывести информацию об альтернативных вариантах"):
        allure.attach("\n".join([f"- {place['title']} ({place['delivery']['text']})"
                               for place in alternative_places[:3]]),
                     name="Альтернативные варианты",
                     attachment_type=allure.attachment_type.TEXT)