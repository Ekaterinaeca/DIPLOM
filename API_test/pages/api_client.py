import requests
import allure


class YandexMarketDeliveryAPI:
    def __init__(self):
        self.base_url = "https://market-delivery.yandex.ru"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    @allure.step("Поиск блюд по тексту '{search_text}'")
    def search_food_items(self, search_text, location, filters=None):
        """
        Поиск блюд по тексту
        :param search_text: Текст для поиска (название блюда)
        :param location: Словарь с координатами {"longitude": float, "latitude": float}
        :param filters: Список фильтров (опционально)
        :return: Ответ API в формате JSON
        """
        with allure.step("Формирование тела запроса"):
            payload = {
                "text": search_text,
                "filters": filters or [],
                "selector": "all",
                "location": location
            }
            allure.attach(
                str(payload),
                name="Тело запроса",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step(f"Отправка POST запроса на {self.base_url}/eats/v1/full-text-search/v1/search"):
            response = requests.post(
                f"{self.base_url}/eats/v1/full-text-search/v1/search",
                json=payload,
                headers=self.headers
            )

            allure.attach(
                f"Status Code: {response.status_code}\nHeaders: {dict(response.headers)}",
                name="Детали ответа",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Проверка статус-кода"):
            response.raise_for_status()

        with allure.step("Парсинг JSON ответа"):
            json_response = response.json()
            allure.attach(
                str(json_response),
                name="Тело ответа",
                attachment_type=allure.attachment_type.JSON
            )
            return json_response