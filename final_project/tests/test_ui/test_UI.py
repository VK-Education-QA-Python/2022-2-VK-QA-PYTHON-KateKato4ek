import pytest
import allure
import json
import requests
from random import randrange

from tests.test_ui.base import BaseCase
from utils.data_faker import UserDataFaker
from conftest import mysql_builder

@allure.epic('Тестирование UI')
@allure.feature('Тестирование страницы авторизации')
class TestLoginPage(BaseCase):
    authorize = False
    
    @allure.description(
        'Проверка на то, что существующий пользователь может залогиниться'
    )
    @pytest.mark.UI
    def test_correct_login(self, mysql_builder):
        name, surname, middlename, username, email, password, access = UserDataFaker.create_valid_user_data(length=6)
        mysql_builder.add_user(name, surname, middlename, username, email, password, access)
        self.login_page.login(username, password)
        self.home_page.find(self.home_page.locators.LOG_OUT_BTN)
    
    @allure.description(
        'Проверка на то, что НЕсуществующий пользователь НЕ может залогиниться'
    )
    @pytest.mark.UI  
    def test_incorrect_login(self):
        _, _, _, username, _, password, _ = UserDataFaker.create_valid_user_data(length=6)
        self.login_page.login(username, password)
        self.login_page.find(self.login_page.locators.INVALID_USERNAME_OR_PASSWORD_WARNING)
    
    @allure.description(
        'Проверка на то, что заблокированный пользователь НЕ может залогиниться'
    )
    @pytest.mark.UI    
    def test_login_without_access(self, mysql_builder):
        name, surname, middlename, username, email, password, access = UserDataFaker.create_valid_user_data(length=6, access=0)
        mysql_builder.add_user(name, surname, middlename, username, email, password, access)
        self.login_page.login(username, password)
        self.login_page.find(self.login_page.locators.BLOCKED_ACCOUNT_WARNING)
    
    @allure.description(
        'Проверка на то, что у поля юзернейм указана минимальная и максимальная длина инпута'
    )
    @pytest.mark.UI    
    def test_check_username_length(self):
        assert self.login_page.check_username_input_validation(min_length=6, max_length=16)
    
    @allure.description(
        'Проверка на то, что поля авторизации обязательны к заполнению'
    )
    @pytest.mark.UI 
    @pytest.mark.parametrize(
        "id",
        ['username',
         'password']
    )
    def test_check_fields_validation(self, id):
        self.login_page.check_validation(id)
    
    @allure.description(
        'Проверка на то, что ссылка на страницу регистрации работает корректно'
    )
    @pytest.mark.UI    
    def test_move_to_registration_page(self):
        self.login_page.go_to_registration_page()
        self.register_page.find(self.register_page.locators.REGISTER_BUTTON)
    
    @allure.description(
        'Проверка на то, что vk_id пользователя с vk_id отображается на хоум пэйдже'
    )
    @pytest.mark.UI
    def test_has_vk_id(self, mysql_builder):
        name, surname, middlename, username, email, password, access = UserDataFaker.create_valid_user_data(length=6)
        mysql_builder.add_user(name, surname, middlename, username, email, password, access)
        
        vk_id = randrange(1000)
        data = json.dumps({'username': username, 'vk_id': vk_id})
        response = requests.post('http://127.0.0.1:8082/add', data=data)
        assert response.status_code == 201
        
        self.login_page.login(username, password)
        assert self.home_page.check_has_vk_id(vk_id)
    
    @allure.description(
        'Проверка на то, что у пользователя без vk_id vk_id не отображается на хоум пэйдже'
    )
    @pytest.mark.UI
    def test_no_vk_id(self, mysql_builder):
        name, surname, middlename, username, email, password, access = UserDataFaker.create_valid_user_data(length=6)
        mysql_builder.add_user(name, surname, middlename, username, email, password, access)
        self.login_page.login(username, password)
        assert self.home_page.check_no_vk_id()

@allure.epic('Тестирование UI')
@allure.feature('Тестирование страницы регистрации')
class TestRegistrationPage(BaseCase):
    authorize = False
    
    @allure.description(
        'Проверка на успешеую регистрацию'
    )
    @pytest.mark.UI
    def test_correct_registration(self):
        self.login_page.go_to_registration_page()
        name, surname, middlename, username, email, password, _ = UserDataFaker.create_valid_user_data(length=6)
        self.register_page.register(name, surname, middlename, username, email, password, confirmpassword=password)
        self.home_page.find(self.home_page.locators.LOG_OUT_BTN)

    @allure.description(
        'Проверка на то, что ссылка на логин пэйджу корректно работает'
    )
    @pytest.mark.UI
    def test_move_to_login_page(self):
        self.register_page.go_to_login_page()
        self.login_page.find(self.login_page.locators.LOGIN_BUTTON)
    
    # Бага, нет валидации по required
    @allure.description(
        'Проверка на то, что все поля кроме мидлнэйм обязательны к заполнению'
    )
    @pytest.mark.UI
    @pytest.mark.parametrize(
        "id",
        ['user_name',
         'user_surname',
         'username',
         'email',
         'password',
         'confirm',
         'term']
    )
    def test_check_fields_validation(self, id):
        self.login_page.go_to_registration_page()
        self.register_page.check_validation(id)
    
    # Бага, нет валидации по длине (surname, middlename, password)
    @allure.description(
        'Проверка на то, что у всех полей указана валидная длина инпута'
    )
    @pytest.mark.UI
    @pytest.mark.parametrize(
        "id, min_length, max_length",
        [('user_name', 1, 255),
         ('user_surname', 1, 255),
         ('user_middle_name', 0, 255),
         ('username', 6, 16),
         ('email', 6, 64),
         ('password', 1, 255)]
    )
    def test_fields_length(self, id, min_length, max_length):
        self.login_page.go_to_registration_page()
        assert self.register_page.check_field_length(id, min_length, max_length)
    
    @allure.description(
        'Проверка на то, что при регистрации с невалидной почтой выводится предупреждение'
    )
    @pytest.mark.UI
    def test_invalid_email(self):
        self.login_page.go_to_registration_page()
        name, surname, middlename, username, _, password, _ = UserDataFaker.create_valid_user_data(length=6)
        email = UserDataFaker.get_invalid_data(length=10)
        self.register_page.register(name, surname, middlename, username, email, password, confirmpassword=password)
        self.register_page.find(self.register_page.locators.WARNING_MESSAGE)
    
    @allure.description(
        'Проверка на выведение предупреждения если подтверждение пароля не совпадает с паролем'
    )
    @pytest.mark.UI
    def test_invalid_confirm_password(self):
        self.login_page.go_to_registration_page()
        name, surname, middlename, username, email, password, _ = UserDataFaker.create_valid_user_data(length=6)
        confirmpassword = UserDataFaker.get_invalid_data(length=10)
        self.register_page.register(name, surname, middlename, username, email, password, confirmpassword=confirmpassword)
        self.register_page.find(self.register_page.locators.WARNING_MESSAGE)
    
    @allure.description(
        'Проверка на выведение предупреждения если указан уже существующий юзернэйм'
    )
    @pytest.mark.UI
    def test_reg_with_existing_username(self, credentials):
        self.login_page.go_to_registration_page()
        name, surname, middlename, _, email, _, _ = UserDataFaker.create_valid_user_data(length=6)
        username=credentials[0]
        password=credentials[1]
        self.register_page.register(name, surname, middlename, username, email, password, confirmpassword=password)
        self.register_page.find(self.register_page.locators.USER_EXISTS_WARNING)
    
    # Бага internal server error
    @allure.description(
        'Проверка на регистрацию с уже существующей почтой'
    )
    @pytest.mark.UI
    def test_reg_with_existing_email(self, credentials):
        self.login_page.go_to_registration_page()
        name, surname, middlename, username, _, password, _ = UserDataFaker.create_valid_user_data(length=6)
        email=credentials[2]
        self.register_page.register(name, surname, middlename, username, email, password, confirmpassword=password)
        self.home_page.find(self.home_page.locators.LOG_OUT_BTN)
    
@allure.epic('Тестирование UI')
@allure.feature('Тестирование домашней страницы')
class TestHomePage(BaseCase):
    @allure.description(
        'Проверка на логаут'
    )
    @pytest.mark.UI
    def test_log_out(self):
        self.home_page.log_out()
        self.login_page.find(self.login_page.locators.LOGIN_BUTTON)
    
    @allure.description(
        'Проверка кнопки HOME'
    )
    @pytest.mark.UI
    def test_redirect_to_home_page(self):
        self.home_page.go_to_home_page()
        assert self.driver.current_url == 'http://127.0.0.1:8083/welcome/'
    
    @allure.description(
        'Проверка центральных кнопок'
    )
    @pytest.mark.UI
    @pytest.mark.parametrize(
        "title, expected",
        [('API', 'API'),
         ('Future of internet', 'Future of the Internet'),
         ('SMTP', 'SMTP')]
    )
    def test_redirect(self, title, expected):    
        assert self.home_page.check_redirect(title, expected)
    
    @allure.description(
        'Проверка присутствия факта о пайтоне'
    )
    @pytest.mark.UI
    def test_fact_exicsts(self):
        assert self.home_page.check_fact_about_python_precence()
