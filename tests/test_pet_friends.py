from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_invalid_password(email=valid_email, password=""):
    """ Проверяем что при отсутствии пароля при запросе api ключа возвращается
     статус 403 (сервер понял запрос, но отказывается его авторизовать)
     и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_invalid_email(email="", password=valid_password):
    """ Проверяем что при отсутствии введенного email при запросе api ключа возвращается
     статус 403 (сервер понял запрос, но отказывается его авторизовать)
     и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем что при некорректном ключе авторизации запрос всех питомцев не возвращает список """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] = '123'
    status, result = pf.get_list_of_pets(auth_key, filter)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

def test_add_new_pet_with_invalid_APIkey(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo = '../images/cat1.jpg'):
    """Проверяем что невозможно добавить питомца при некорректном API ключе"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # присваиваем переменой auth_key некорректное значение ключа
    auth_key ['key'] = '123'
    # ПРобуем добавить питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

def test_add_new_pet_with_empty_pet_data(name='', animal_type='',
                                     age='', pet_photo = '../images/emptyFile.jpg'):
    """Проверяем можно ли добавить питомца с полностью отсутствующими данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200

def test_add_new_pet_with_invalid_age(name='Барбоскин', animal_type='двортерьер',
                                     age='-4', pet_photo='../images/emptyFile.jpg'):
    """Проверяем что невозможно добавить питомца с отрицательным значением переменной возраст"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом - сервер не пустил запрос на добавление питомца
    # с отрицательным значениемм возраста
    assert status != 200

def test_successful_delete_self_pet_with_invalid_ID():
    """Проверяем возможность удаления питомца c некорректным ID"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = 'incorrect number'
    print (pet_id)
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа не равен 200
    assert status != 200

def test_successful_delete_self_pet_with_invalid_APIkey():
    """Проверяем возможность удаления питомца с некорректным API ключом"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    incorrect_auth_key = auth_key
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(incorrect_auth_key, pet_id)

    # Проверяем что статус ответа равен 403 - сервер не пустил запрос на удаление с некорректным API ключом
    assert status == 403


def test_successful_update_self_pet_with_empty_info(name='', animal_type='', age=0):
    """Проверяем возможность обновления информации о питомце с пустыми значениями"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа не равен 200 и сервер не пустил запрос на изменение с пустыми данными
        assert status != 200

def test_successful_update_self_pet_info_with_negative_age(name='Филя', animal_type='пёса', age= -251):
    """Проверяем невозможность обновления информации о питомце с отрицательным значением возраста"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа не равен 200 и сервер не пустил запрос на изменение с пустыми данными
        assert status != 200
