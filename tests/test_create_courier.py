import allure
import requests
from data.urls import CREATE_COURIER
from utils.helpers import generate_random_string


class TestCreateCourier:

    @allure.step("Отправить POST-запрос на создание курьера")
    def create_courier(self, payload):
        return requests.post(CREATE_COURIER, data=payload)

    @allure.title("Успешное создание курьера")
    @allure.description("Можно создать курьера, передав все обязательные поля. Ожидаем код 201 и тело {\"ok\":true}")
    def test_create_courier_success(self, courier_cleanup):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        # Передаем данные в фикстуру очистки для удаления после теста
        courier_cleanup.update(payload)

        response = self.create_courier(payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    @allure.description("При попытке создать курьера с уже существующим логином возвращается ошибка")
    def test_create_duplicate_courier(self, registered_courier):
        response = self.create_courier(registered_courier)

        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Нельзя создать курьера без логина")
    @allure.description("Если не передать логин — возвращается ошибка")
    def test_create_courier_without_login(self):
        payload = {
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        response = self.create_courier(payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Нельзя создать курьера без пароля")
    @allure.description("Если не передать пароль — возвращается ошибка")
    def test_create_courier_without_password(self):
        payload = {
            "login": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        response = self.create_courier(payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"