import allure
import pytest
import requests
from data.urls import CREATE_ORDER
from data.order_data import ORDER_DATA


class TestCreateOrder:

    @allure.title("Создание заказа с указанием цвета")
    @allure.description("Можно указать один цвет, оба цвета или не указывать цвет вообще. В ответе должен быть track")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors(self, color):
        payload = ORDER_DATA.copy()
        payload["color"] = color

        response = requests.post(CREATE_ORDER, json=payload)

        assert response.status_code == 201
        assert "track" in response.json()