import allure

from mysql.model import UsersTable

class MysqlBuilder():
    def __init__(self, client):
        self.client = client
    
    @allure.step('Добавление пользователя в БД')
    def add_user(self, name, surname, middlename, username, email, password, access=1):
        user = UsersTable(
            name=name,
            surname=surname,
            middle_name=middlename,
            username=username,
            email=email,
            password=password,
            access=access
        )
        
        self.client.session.add(user)
        self.client.session.commit()
    
    @allure.step('Получение данных пользователя из БД по юзернэйму')    
    def get_user_by_username(self, username):
        return self.client.session.query(UsersTable).filter(UsersTable.username == username).first()
    
    @allure.step('Получение значения параметра active из БД')
    def get_active_value(self, username):
        user = self.get_user_by_username(username)
        active_value = user.active
        
        return active_value
