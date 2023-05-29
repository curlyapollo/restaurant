import json
import requests

from Utils import read_command

ord_id = -1


# create request to server to print menu
def menu():
    res = requests.post('http://localhost:3000/api/menu').text
    res = json.loads(res)
    print('=' * 75)
    print(' ' * 36, "MENU")
    print('=' * 75)
    for key in res:
        print(key, end='')
        print(' ' * (74 - len(key) - len(str(res[key]['price']))), end='')
        print(res[key]['price'], '₽', sep='')
        print('\t', res[key]['description'])
        print('-' * 75)


def create_order(user_id: int):
    global ord_id
    res = json.loads(requests.post('http://localhost:3000/api/menu').text)
    i = 1
    print("Ваш заказ: ")
    index_2_id = [1]
    for key in res:
        print(i, ". ", key, sep='')
        i += 1
        index_2_id.append(res[key]['id'])
    print("закончить заказ")
    x = -1
    order = []
    while x != 0:
        x = read_command(i)
        if x == i:
            break
        else:
            order.append(index_2_id[x])
    ord_id = int(requests.post('http://localhost:3000/api/create_order', json={'data': '_'.join(map(str, order)),
                                                                               'id': user_id}).text)
    print("заказ принят")


def status():
    if ord_id == -1:
        print("корзина пуста")
    order_status = requests.post('http://localhost:3000/api/status', json={'ord_id': ord_id}).text
    print(f"Состояние заказа: {order_status}.")


def guest(user_info: dict) -> int:
    print('1. Меню')
    print('2. Создание заказа')
    print('3. Информация о заказе')
    print('4. Выход')
    command = read_command(4)
    if command == 4:
        return -1
    elif command == 1:
        menu()
    elif command == 2:
        create_order(user_info['id'])
    else:
        status()
    return 0


def new_dish():
    print("Название блюда:")
    name = input()
    print("Описание блюда:")
    disc = input()
    print("Цена блюда:")
    cost = read_command(300)
    print("Количество блюда:")
    cou = read_command(30)
    res = json.loads(requests.post('http://localhost:3000/api/add',
                                   json={'name': name, 'disc': disc, 'cost': cost, 'cou': cou}).text)


def manager(user_info: dict) -> int:
    print('1. Управление блюдом')
    print('2. Выход')
    command = read_command(2)
    if command == 2:
        return -1
    res = json.loads(requests.post('http://localhost:3000/api/menu').text)
    i = 1
    index_2_id = [1]
    print("Какое блюдо изменить?")
    for key in res:
        index_2_id.append(res[key]['id'])
        print(i, ") ", key, sep='')
        i += 1
    print("Новое блюдо")
    x = read_command(i)
    if x == i:
        new_dish()
        return 0
    print("Что делать с блюдом?")
    print('1. Удалить.')
    print('2. Добавить несколько штук.')
    print('3. Убрать несколько штук.')
    y = read_command(3)
    if y != 1:
        print("Количество:")
        delta = read_command(10)
        if y == 3:
            delta = -delta
    else:
        delta = 0
    res = json.loads(requests.post('http://localhost:3000/api/change', json={'delta': delta, 'id': index_2_id[x]}).text)
    print(f"Новове количество блюда {res['name']}: {res['count']} штук.")


def chef(user_info: dict) -> int:
    print('1. Приготовить блюдо')
    print('2. Выход')
    command = read_command(2)
    if command == 2:
        return -1
    res = requests.post('http://localhost:3000/api/cook')
    if res.status_code == 200:
        print(f'Готов заказ для {res.text}.')
    else:
        print(f'Готовых заказов нет')


# client main function
def main():
    try:
        info_file = open('info.txt')
        session_id = int(info_file.read())
        info_file.close()
        data = {
            'session_id': session_id,
        }
        res = requests.post('http://localhost:3000/api/session', json=data)
        user_info = json.loads(res.text)
        if res.status_code == 200:
            print(f'{user_info["role"]} {user_info["name"]} авторизован.')
        else:
            raise Exception
    except:
        print('Требуется авторизация или регистрация.')
        return 0

    while True:
        if user_info['role'] == 'гость':
            res = guest(user_info)
        elif user_info['role'] == 'менеджер':
            res = manager(user_info)
        else:
            res = chef(user_info)
        if res == -1:
            print("Сессия завершена.")
            return 0


main()
