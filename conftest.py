import pytest
import requests
from data.urls import CREATE_COURIER, LOGIN_COURIER
from utils.helpers import generate_random_string


@pytest.fixture
def courier_cleanup():
    courier_data = {}
    yield courier_data
    # Teardown: удаляем курьера после теста, если он был зарегистрирован
    if courier_data.get("login") and courier_data.get("password"):
        login_res = requests.post(
            LOGIN_COURIER,
            data={"login": courier_data["login"], "password": courier_data["password"]}
        )
        if login_res.status_code == 200:
            courier_id = login_res.json().get("id")
            requests.delete(f"{CREATE_COURIER}/{courier_id}")


@pytest.fixture
def registered_courier():
    # Setup: регистрируем курьера как предусловие
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    requests.post(CREATE_COURIER, data=payload)

    yield payload

    # Teardown: удаляем созданного курьера после завершения теста
    login_res = requests.post(
        LOGIN_COURIER,
        data={"login": login, "password": password}
    )
    if login_res.status_code == 200:
        courier_id = login_res.json().get("id")
        requests.delete(f"{CREATE_COURIER}/{courier_id}")