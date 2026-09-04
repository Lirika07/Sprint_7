import allure
import requests
from data.urls import GET_ORDERS


class TestGetOrders:

    @allure.title("Получение списка заказов")
    @allure.description("В теле ответа возвращается список заказов")
    def test_get_orders_list(self):
        response = requests.get(GET_ORDERS)

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)