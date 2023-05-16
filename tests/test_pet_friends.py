import pytest
import os

from api import PetFriends
from settings import valid_email, valid_password
from settings import invalid_email, invalid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """ Проверяем что запрос api ключа возвращает статус 403, указанная комбинация электронной почты пользователя
    и пароля неверна, в результате отсутствует слово key."""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_valid_email_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа возвращает статус 403, если указан верный электронный адрес и неверный пароль,
    в результате отсутствует слово key."""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_invalid_email_valid_password(email=invalid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403, если указан неверный электронный адрес и верный пароль,
    в результате отсутствует слово key."""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_without_photo_with_valid_data(name='Муся', animal_type='Чихуахуа', age='2'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_without_photo_with_invalid_name(name='', animal_type='Чихуахуа', age='2'):
    """Проверяем что можно добавить питомца с пустым значением name, запрос возвращает статус 200"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_without_photo_with_invalid_name2(name=777, animal_type='Чихуахуа', age='2'):
    """Проверяем что невозможно добавить питомца с недопустимым параметром name, запрос возвращает статус 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] != name

def test_add_new_pet_without_photo_with_invalid_type(name='Муся', animal_type=555, age='2'):
    """Проверяем что невозможно добавить питомца с недопустимым параметром animal_type, запрос возвращает статус 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert result['animal_type'] != animal_type

def test_add_new_pet_without_photo_with_invalid_data(name='', animal_type='', age=''):
    """Проверяем что невозможно добавить питомца с пустыми параметрами, запрос возвращает статус 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] == name

def test_add_photo_pet(pet_photo='images/pet_photo2.jpg'):
    """Проверяем возможность добавления фото в карточку питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Муся", "Чихуахуа", "2")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo='images/pet_photo2.jpg')

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert result['pet_photo'] != ""

def test_update_pet_info(name='Кеша', animal_type='Попугай', age=1):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцев нет")

def test_update_pet_info_invalid_age(name='Кеша', animal_type='Попугай', age=-200):
    """Проверяем возможность обновления информации о питомце c отрицательным значением параметра age"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
        assert result['age'] != age
    else:
        raise Exception("Питомцев нет")

def test_add_new_pet_photo(name='Сёма', animal_type='Кошка', age='3', pet_photo= 'images/pet_photo.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_pet():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_photo(auth_key, "Сёма", "Кошка", "3", "images/pet_photo.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


