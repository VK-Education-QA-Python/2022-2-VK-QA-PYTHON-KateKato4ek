import pytest
import allure

from tests.test_api.base import ApiBase
from utils.data_faker import UserDataFaker
from conftest import mysql_builder

@allure.epic('Тестирование API')
@allure.feature('Тестирование страницы логин')
class TestApiLoginPage(ApiBase):
    @allure.description(
        'Проверка на то, что существующий пользователь может залогиниться'
    )
    @pytest.mark.API
    def test_user_exist_auth(self):
        self.api_client.login(self.api_client.session_without_auth, username=self.api_client.username, password=self.api_client.password)

    @allure.description(
        'Проверка на то, что НЕсуществующий пользователь НЕ может залогиниться'
    )
    @pytest.mark.API
    def test_user_not_exist_auth(self):
        _, _, _, username, _, password, _ = UserDataFaker.create_valid_user_data(length=6)
        self.api_client.login(self.api_client.session_without_auth, username=username, password=password, expected_status=401)
    
    @allure.description(
        'Проверка на то, что заблокированный пользователь НЕ может залогиниться'
    )
    @pytest.mark.API
    def test_auth_blocked_user(self, mysql_builder):
        name, surname, _, username, email, password, access = UserDataFaker.create_valid_user_data(length=6, access=0)
        mysql_builder.add_user(name, surname, username, email, password, access)
        response = self.api_client.login(self.api_client.session_without_auth, username=username, password=password, expected_status=401)
        
        assert response.text.find("Ваша учетная запись заблокирована") != 0
    
    # Бага с валидацией длины username
    @allure.description(
        'Проверка на то, что на некорректную длину username при логине приходит ответ 400 и предупреждение'
    )
    @pytest.mark.API
    def test_auth_incorrect_username_length(self):
        _, _, _, username, _, password, _ = UserDataFaker.create_valid_user_data(length=2)
        response = self.api_client.login(self.api_client.session_without_auth, username=username, password=password, expected_status=400)
        
        assert response.text.find("Incorrect username length") != 0

@allure.epic('Тестирование API')
@allure.feature('Тестирование страницы регистрации')
class TestApiRegisterPage(ApiBase):
    @allure.description(
        'Проверка на успешеую регистрацию пользователя'
    )
    @pytest.mark.API
    def test_correct_reg(self, mysql_builder):
        name, surname, middlename, username, email, password, _ = UserDataFaker.create_valid_user_data(length=6)
        self.api_client.reg_user(self.api_client.session_without_auth, name, surname, middlename, username, email, password, confirmpassword=password, expected_status=200)
        user = mysql_builder.get_user_by_username(username)
    
        assert user != None
    
    # Бага с валидацией длины пароля
    @allure.description(
        'Проверка на то, что при введении слишком длинного пароля при регистрации приходит ответ 400'
    )
    @pytest.mark.API
    def test_reg_with_too_long_password(self):
        name, surname, middlename, username, email, _ , _ = UserDataFaker.create_valid_user_data(length=6)
        password = UserDataFaker.get_invalid_data(length=300)
        self.api_client.reg_user(self.api_client.session_without_auth, name, surname, middlename, username, email, password, confirmpassword=password, expected_status=400)
    
    # Бага с валидацией длины middlename
    @allure.description(
        'Проверка на то, что при введении слишком длинного мидлнэйма при регистрации приходит ответ 400'
    )
    @pytest.mark.API
    def test_reg_with_too_long_middlename(self):
        name, surname, _, username, email, password, _ = UserDataFaker.create_valid_user_data(length=6)
        middlename = UserDataFaker.get_invalid_data(length=300)
        self.api_client.reg_user(self.api_client.session_without_auth, name, surname, middlename, username, email, password, confirmpassword=password, expected_status=400)
        user = mysql_builder.get_user_by_username(username)
        
        assert user == None
    
    @allure.description(
        'Проверка на то, что при введении невадилной почты при регистрации приходит ответ 400 и предупреждение'
    )
    @pytest.mark.API
    def test_reg_with_invalid_email(self):
        name, surname, middlename, username, _, password, _ = UserDataFaker.create_valid_user_data(length=6)
        email = UserDataFaker.get_invalid_data(length=7)
        response = self.api_client.reg_user(self.api_client.session_without_auth, name, surname, middlename, username, email, password, confirmpassword=password, expected_status=400)
        
        assert response.text.find("Invalid email address") != 0
    
    @allure.description(
        'Проверка на то, что при регистрации с уже существующим юзернэймом приходит ответ 409 и предупреждение'
    )
    @pytest.mark.API
    def test_reg_with_existing_username(self, credentials):
        name, surname, middlename, _, email, _, _ = UserDataFaker.create_valid_user_data(length=6)
        username=credentials[0]
        password=credentials[1]
        response = self.api_client.reg_user(self.api_client.session_without_auth, name, surname, middlename, username, email, password, confirmpassword=password, expected_status=409)
        
        assert response.text.find("User already exist") != 0
    
    # Бага с проверкой уникальности email-а
    @allure.description(
        'Проверка на то, что при регистрации с уже существующей почтой приходит ответ 409'
    )
    @pytest.mark.API
    def test_reg_with_existing_email(self, credentials):
        name, surname, middlename, username, _, password, _ = UserDataFaker.create_valid_user_data(length=6)
        email = credentials[2]
        self.api_client.reg_user(self.api_client.session_without_auth, name, surname, middlename, username, email, password, confirmpassword=password, expected_status=409)
