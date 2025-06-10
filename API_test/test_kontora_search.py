import allure
from API_test.pages.api_client import YandexMarketDeliveryAPI


@allure.epic("API Тесты Яндекс.Доставки")
@allure.feature("Поиск с фолбэком")
@allure.story("Поиск по запросу 'контора' с проверкой альтернатив")
def test_search_kontora_with_fallback():
    api = YandexMarketDeliveryAPI()

    # Тестовые данные
    test_location = {
        "longitude": 30.33136653698719,
        "latitude": 60.05417412219289
    }
    search_query = "контора"

    with allure.step(f"Выполнение поиска по запросу '{search_query}'"):
        response = api.search_food_items(
            search_text=search_query,
            location=test_location
        )
        allure.attach(
            str(response),
            name="Полный ответ API",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("1. Проверка заголовка ответа"):
        assert "header" in response, "Должен быть заголовок ответа"
        assert "Ничего не нашли, но есть:" in response["header"]["text"], \
            "Ожидалось сообщение о отсутствии точных результатов"
        allure.attach(
            response["header"]["text"],
            name="Текст заголовка",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("2. Проверка наличия альтернативных вариантов"):
        assert "blocks" in response, "Должны быть блоки с результатами"
        assert len(response["blocks"]) > 0, "Должен быть хотя бы один блок с альтернативами"

    with allure.step("3. Поиск и проверка блока с местами"):
        places_block = next(
            (block for block in response["blocks"] if block["type"] == "places"),
            None
        )
        assert places_block is not None, "Должен быть блок с местами"
        assert len(places_block["payload"]) >= 3, "Должно быть несколько альтернативных мест"

    with allure.step("4. Проверка содержания альтернатив"):
        alternative_places = places_block["payload"]
        place_titles = [place["title"] for place in alternative_places]

        expected_alternatives = ["Яндекс Лавка", "Азбука вкуса", "ВкусВилл", "Бургер Кинг"]
        found_alternatives = [title for title in place_titles
                              if any(alt in title for alt in expected_alternatives)]

        assert len(found_alternatives) >= 2, \
            f"Должно быть хотя бы 2 из ожидаемых альтернатив: {expected_alternatives}"

        allure.attach(
            "\n".join(place_titles),
            name="Найденные альтернативы",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("5. Проверка типов заведений"):
        business_types = {place["business"] for place in alternative_places}
        assert {"restaurant", "shop", "store"}.intersection(business_types), \
            "Должны быть разные типы заведений"
        allure.attach(
            ", ".join(business_types),
            name="Типы заведений",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("6. Проверка информации о доставке"):
        delivery_info = []
        for place in alternative_places[:3]:
            assert "delivery" in place, "У места должна быть информация о доставке"
            assert "text" in place["delivery"], "Должно быть время доставки"
            assert "available" in place, "Должен быть статус доступности"
            assert isinstance(place["available"], bool), "Статус доступности должен быть boolean"
            delivery_info.append(
                f"{place['title']}: {place['delivery']['text']} (Доступен: {place['available']})"
            )

        allure.attach(
            "\n".join(delivery_info),
            name="Информация о доставке",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("7. Проверка меток о доставке"):
        chips_info = []
        for place in alternative_places:
            if "chips" in place:
                has_free_delivery = any(
                    chip["payload"]["text"]["value"] == "Бесплатная доставка"
                    for chip in place["chips"]
                )
                assert has_free_delivery, "Должна быть метка о бесплатной доставке"
                chips_info.append(f"{place['title']}: Бесплатная доставка - {'Да' if has_free_delivery else 'Нет'}")

        if chips_info:
            allure.attach(
                "\n".join(chips_info),
                name="Метки о доставке",
                attachment_type=allure.attachment_type.TEXT
            )

    with allure.step("Вывод альтернативных вариантов"):
        print("\nАльтернативные варианты:")
        for place in alternative_places[:3]:
            print(f"- {place['title']} ({place['business']}, {place['delivery']['text']})")