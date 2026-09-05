import allure
import requests
from data.urls import LOGIN_COURIER
from utils.helpers import generate_random_string, register_new_courier_and_return_login_password


@allure.epic("Яндекс.Самокат API")
@allure.feature("Авторизация курьера")
class TestLoginCourier:

    @allure.title("Курьер может успешно авторизоваться")
    def test_login_courier_success(self):
        login, password, _ = register_new_courier_and_return_login_password()
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Нельзя авторизоваться без логина")
    def test_login_without_login(self):
        payload = {
            "password": generate_random_string(10)
        }
        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 400
        assert response.json().get("message") == "Недостаточно данных для входа"

    @allure.title("Нельзя авторизоваться без пароля")
    def test_login_without_password(self):
        payload = {
            "login": generate_random_string(10),
            "password": ""
        }
        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 400
        assert response.json().get("message") == "Недостаточно данных для входа"

    @allure.title("Ошибка авторизации с неправильным логином")
    def test_login_with_wrong_login(self):
        login, password, _ = register_new_courier_and_return_login_password()
        payload = {
            "login": f"{login}_wrong",
            "password": password
        }
        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 404
        assert response.json().get("message") == "Учетная запись не найдена"

    @allure.title("Ошибка авторизации с неправильным паролем")
    def test_login_with_wrong_password(self):
        login, password, _ = register_new_courier_and_return_login_password()
        payload = {
            "login": login,
            "password": "wrong_password"
        }
        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 404
        assert response.json().get("message") == "Учетная запись не найдена"

    @allure.title("Ошибка авторизации несуществующего пользователя")
    def test_login_nonexistent_user(self):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }
        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 404
        assert response.json().get("message") == "Учетная запись не найдена"