import ast
import datetime


def log_file(name, result):
    with open("log.txt", 'a', encoding='utf-8') as file_log:
        s = f'[{datetime.datetime.now()}] [{name}] [{result}]'
        file_log.write(s + '\n')


def make_payments(user_account, data_dict):
    user_data = data_dict[user_account]
    user_pay = user_data[5]
    count = 0
    for payment in user_pay:
        if payment[2] == 0:
            count += 1
            if payment[1] in data_dict:
                if user_data[2] > payment[0]:
                    pay_data = data_dict[payment[1]]
                    pay_data[2] = pay_data[2] + payment[0]
                    user_data[2] = user_data[2] - payment[0]
                    payment[2] = 1
                    yield f'- Платеж на сумму {payment[0]} руб. для "{payment[1]}" успешно проведен.'
                else:
                    yield f'- Платеж на сумму {payment[0]} руб. для "{payment[1]}" не проведен. Не хватает средств на счете.'
            else:
                yield f'- Платеж на сумму {payment[0]} руб. для "{payment[1]}" не проведен. Указанный аккаунт не зарегистрирован!'

    if count == 0:
        yield f'- Отложенных платежей нет.'


def file_open(name_file):
    with open(name_file, encoding='utf-8') as file_in:
        data_dict = {}
        for line in file_in.readlines():
            line_split = line.strip().split("@")
            data_dict[line_split[0]] = ast.literal_eval(line_split[1])
    return data_dict


def check_account(a):
    for s in a:
        if not ((ord(s) >= 48 and ord(s) <= 57) or (ord(s) >= 65 and ord(s) <= 90) or (ord(s) >= 97 and ord(s) <= 122)):
            return False
    return True


def input_password(user_account, user_password):
    hash_input = hash_password(user_password)
    s = user_account + '.passwordhash.txt'
    with open(s) as file_hash:
        hash_read = file_hash.read()
    if hash_input == hash_read:
        return True
    else:
        return False


def input_int(input_text):
    type_check = False
    while type_check == False:
        try:
            number = int(input(input_text))
            type_check = True
        except ValueError:
            print('- Необходимо указать числовое значение!')
            print()
    return number


def hash_password(a):
    b, c, d = 0, 1, 1230456789
    for letter in a:
        b = b + ord(letter)
        c = c * ord(letter)
    return f'{b % d}{c % d}'


def file_save(name_file, data_dict):
    with open(name_file, 'w', encoding='utf-8') as file_out:
        for key, data in data_dict.items():
            file_out.write(f'{key}@{data}' + "\n")
