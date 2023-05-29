import json

import requests
import hashlib

from Utils import read_command, read_email

# create request to server to create new user
def registration() -> None:
    print('Имя: ')
    name = input()
    print('Email: ')
    email = read_email()
    print('Пароль: ')
    password = input()
    print('Выберите роль:')
    print('1. повар')
    print('2. гость')
    print('3. менеджер')
    role = read_command(3)

    data = {
        'username': name,
        'email': email,
        'password_hash': hashlib.sha256(password.encode()).hexdigest(),
        'role': ['chef', 'customer', 'manager'][role - 1]
    }
    res = requests.post('http://localhost:3000/api/register', json=data)
    if res.status_code == 200:
        print('Регистрация успешна.')
    elif res.status_code == 409:
        print('Пользователь уже зарегистрирован')
    else:
        print('Error 404')


# create request to server to login user
def login() -> None:
    print('Email:')
    email = read_email()
    print('Пароль:')
    password = input()
    data = {
        'email': email,
        'password_hash': hashlib.sha256(password.encode()).hexdigest(),
    }
    res = requests.post('http://localhost:3000/api/login', json=data)
    if res.status_code == 200:
        print('Авторизация успешна')
        info_file = open('info.txt', 'w')
        print(res.text, file=info_file)
        info_file.close()
    elif res.status_code == 409:
        print('Неверный логин или пароль')
    else:
        print('Error 404')


# create request to server to get info about user
def info():
    try:
        info_file = open('info.txt')
        session_id = int(info_file.read())
        info_file.close()
        data = {
            'session_id': session_id,
        }
        res = requests.post('http://localhost:3000/api/session', json=data)
        if res.status_code == 200:
            res = json.loads(res.text)
            print(f'Авторизация пользователя {res["role"]} {res["name"]} успешна')
        elif res.status_code == 409:
            print('Cессия завершена')
        elif res.status_code == 404:
            print('Вход не выполнен')
        else:
            print('Error 404')
    except:
        print('Вход не выполнен ')


# client main function
def main():
    while True:
        print('Выберите:')
        print('1. регистрация')
        print('2. авторизация')
        print('3. информация о пользователе')
        print('4. закрыть приложение')
        print('Выбор:')

        command = read_command(4)
        if command == 1:
            registration()
        elif command == 2:
            login()
        elif command == 3:
            info()
        else:
            break

main()
