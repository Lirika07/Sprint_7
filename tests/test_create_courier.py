import allure
import requests
from data.urls import CREATE_COURIER
from utils.helpers import generate_random_string, register_new_courier_and_return_login_password


class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    @allure.description("Можно создать курьера, передав все обязательные поля. Ожидаем код 201 и тело {\"ok\":true}")
    def test_create_courier_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(CREATE_COURIER, data=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    @allure.description("При попытке создать курьера с уже существующим логином возвращается ошибка")
    def test_create_duplicate_courier(self):
        login_pass = register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        first_name = login_pass[2]

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(CREATE_COURIER, data=payload)

        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Нельзя создать курьера без логина")
    @allure.description("Если не передать логин — возвращается ошибка")
    def test_create_courier_without_login(self):
        payload = {
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        response = requests.post(CREATE_COURIER, data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Нельзя создать курьера без пароля")
    @allure.description("Если не передать пароль — возвращается ошибка")
    def test_create_courier_without_password(self):
        payload = {
            "login": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        response = requests.post(CREATE_COURIER, data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"