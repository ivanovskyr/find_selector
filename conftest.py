from settings import valid_email, valid_password
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pytest
import uuid

@pytest.fixture(autouse=True, scope="session")
def browser():
    pytest.driver = webdriver.Chrome('C:/Users/sholopkin/PycharmProjects/chromedriver.exe')
    pytest.driver.set_window_size(1200, 1000)

    # активируем неявное ожидание (даем браузеру время на загрузку страницы, построение ДОМ дерева и тд)
    pytest.driver.implicitly_wait(10)

    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    # Очищаем поле и вводим email
    field_email = pytest.driver.find_element(By.ID, 'email')
    field_email.clear()
    field_email.send_keys(valid_email)

    # Очищаем поле и вводим пароль
    field_pass = pytest.driver.find_element(By.ID, 'pass')
    field_pass.clear()
    field_pass.send_keys(valid_password)
    time.sleep(2)

    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Проверяем, что находимся на главной странице пользователя

    if not pytest.driver.current_url == 'https://petfriends.skillfactory.ru/all_pets':
        pytest.driver.quit()
        raise Exception("Некорректный email или пароль")

    # ЕСЛИ ОКНО БРАУЗЕРА УЗКОЕ, т.е. на экране есть иконка, чтобы увидеть кнопку Мои питомцы, надо нажать на иконку
    if pytest.driver.find_element(By.XPATH, "//body/nav[1]/button[1]").is_displayed():
        time.sleep(2)
        pytest.driver.find_element(By.XPATH, "//body/nav[1]/button[1]").click()
        time.sleep(2)

    # Нажимаем на ссылку "Мои питомцы"
    pytest.driver.find_element(By.XPATH, "//a[contains(text(),'Мои питомцы')]").click()

    # Проверяем, что перешли на страницу "Мои питомцы"

    if not pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets':
        pytest.driver.quit()
        raise Exception("Это не страница Мои питомцы")

    yield

    pytest.driver.quit()