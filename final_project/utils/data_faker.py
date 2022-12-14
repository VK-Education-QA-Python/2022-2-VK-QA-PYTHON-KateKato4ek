import faker

faker = faker.Faker()

class UserDataFaker:
    @staticmethod
    def create_valid_user_data(length, access=1):
        name = faker.first_name()
        surname = faker.last_name()
        middlename = faker.pystr(min_chars=length, max_chars=length)
        username = faker.pystr(min_chars=length, max_chars=length)
        email = str(f'{faker.pystr(max_chars=length)}@gmail.ru')
        password = faker.password(length=6)
        access=access
        
        return name, surname, middlename, username, email, password, access
    
    @staticmethod
    def get_invalid_data(length):
        invalid_data = faker.pystr(min_chars=length, max_chars=length)
        
        return invalid_data
