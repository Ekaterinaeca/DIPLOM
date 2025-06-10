import allure
from API_test.pages.api_client import YandexMarketDeliveryAPI


@allure.epic("Yandex Market Delivery API")
@allure.feature("Поиск товаров")
@allure.story("Обработка бессмысленных запросов")
@allure.title("Поиск с бессмысленным текстом и проверка fallback-результатов")
def test_nonsense_search_with_fallback():
    api = YandexMarketDeliveryAPI()

    # Тестовые данные
    test_location = {
        "longitude": 30.33136653698719,
        "latitude": 60.05417412219289
    }

    with allure.step("Выполнить поиск с бессмысленным текстом 'hhghg'"):
        response = api.search_food_items(
            search_text="hhghg",
            location=test_location
        )
        allure.attach(str(response), name="Полный ответ API", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверить заголовок с сообщением о отсутствии результатов"):
        assert "header" in response, "Должен быть заголовок ответа"
        assert "Ничего не нашли, но есть:" in response["header"]["text"], \
            "Ожидалось сообщение о отсутствии результатов для бессмысленного запроса"

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

        expected_alternatives = ["Яндекс Лавка", "ВкусВилл", "Бургер Кинг", "Азбука вкуса"]
        found_alternatives = [title for title in place_titles
                              if any(alt in title for alt in expected_alternatives)]

        allure.attach("\n".join(found_alternatives),
                      name="Найденные альтернативы",
                      attachment_type=allure.attachment_type.TEXT)

        assert len(found_alternatives) >= 2, \
            f"Должно быть хотя бы 2 популярных альтернативы: {expected_alternatives}"

    with allure.step("Проверить время доставки для альтернатив"):
        delivery_info = []
        for place in alternative_places[:3]:
            assert "delivery" in place, "У места должна быть информация о доставке"
            delivery_text = place["delivery"]["text"]
            assert "мин" in delivery_text, "Время доставки должно быть в минутах"

            delivery_times = [int(s) for s in delivery_text.split() if s.isdigit()]
            assert len(delivery_times) == 2, "Должен быть диапазон времени доставки"
            assert delivery_times[0] < delivery_times[1], "Некорректный диапазон времени"

            delivery_info.append(f"{place['title']}: {delivery_text}")

        allure.attach("\n".join(delivery_info),
                      name="Информация о доставке",
                      attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверить информацию о доступности"):
        available_places = [p for p in alternative_places if p["available"]]
        unavailable_places = [p for p in alternative_places if not p["available"]]

        allure.attach(f"Доступных мест: {len(available_places)}\n" +
                      f"Недоступных мест: {len(unavailable_places)}",
                      name="Статистика доступности",
                      attachment_type=allure.attachment_type.TEXT)

        assert len(available_places) > 0, "Должны быть доступные для заказа места"

    with allure.step("Вывести информацию о предложенных альтернативах"):
        alternatives_info = []
        for place in alternative_places[:3]:
            status = "Доступен" if place["available"] else "Не доступен"
            alternatives_info.append(f"- {place['title']} ({status}, доставка: {place['delivery']['text']})")

        allure.attach("Предложенные альтернативы для запроса 'hhghg':\n" +
                      "\n".join(alternatives_info),
                      name="Результаты поиска",
                      attachment_type=allure.attachment_type.TEXT)