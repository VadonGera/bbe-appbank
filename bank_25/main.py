from util import *

if __name__ == '__main__':
    name_file = 'data.txt'
    data_dict = {}
    user_data = []
    log_file('Запуск приложения', 'OK')
    while True:
        print("  1. Восстановить данные аккаунта.")
        print("  2. Создать новый аккаунт.")
        print("  0. Выход из приложения.")
        operation = input("Введите номер операции: ")
        if operation == '1':  # 1. Восстановить данные
            try:
                f = open(name_file)
                f.close()
            except FileNotFoundError:
                print('- Восстановить данные невозможно. Файл данных отсутствует.')
                log_file('Восстановить данные аккаунта', 'ERROR')
                exit()

            user_account = input("Ваш аккаунт: ")
            data_dict = file_open(name_file)
            if user_account not in data_dict:
                print("- Указанный Вами аккаунт не существует!")
                log_file('Восстановить данные аккаунта', 'ERROR')
                print()
                print("Для продолжения введите номер операции.")
                continue

            if not input_password(user_account, input("Введите пароль: ")):
                print("- Введен неверный пароль!")
                log_file('Восстановить данные аккаунта', 'ERROR')
                print()
                print("Для продолжения введите номер операции.")
                continue
            else:
                user_data = data_dict[user_account]
                user_name = user_data[0]
                user_year = user_data[1]
                print()
                now_year = int(datetime.datetime.now().year)
                print(f'- Вы вошли в аккаунт: {user_name} ({now_year - user_year} лет)')
                log_file('Восстановить данные аккаунта', 'OK')
                print()
                print("Для продолжения введите номер операции.")
                break

        elif operation == '2':  # 2. Создать новый аккаунт
            user_account = input("Создайте аккаунт (используйте латиницу): ")
            if not check_account(user_account):
                print("- Аккаунт не создан! При создании аккаунта используйте латиницу!")
                print()
                print("Для продолжения введите номер операции.")
                log_file('Создать новый аккаунт', 'ERROR')
                continue
            try:
                f = open(name_file)
                f.close()
            except FileNotFoundError:
                f = open(name_file, 'w', encoding='utf-8')
                f.close()
            data_dict = file_open(name_file)
            if user_account in data_dict:
                print(f'- Аккаунт "{user_account}" уже существует в базе данных!')
                print()
                print("Для продолжения введите номер операции.")
                log_file('Создать новый аккаунт', 'ERROR')
                continue

            user_name = input("Введите ФИО: ")
            user_year = input_int("Введите год рожнения (для отмены операции введите 0): ")
            if user_year == 0:
                print("- Аккаунт не создан!")
                print()
                print("Для продолжения введите номер операции.")
                log_file('Создать новый аккаунт', 'ERROR')
                continue

            user_password = input("Создайте пароль для аккаунта: ")
            s = user_account + '.passwordhash.txt'
            with open(s, 'w') as file_hash:
                file_hash.write(hash_password(user_password))

            data_dict[user_account] = [user_name, user_year, 0, 1, [], []]
            file_save(name_file, data_dict)
            user_data = data_dict[user_account]

            now_year = int(datetime.datetime.now().year)
            print(
                f'- Аккаунт "{user_account}" создан! Пользователь "{user_name}" ({now_year - user_year} лет) успешно зарегистрирован.')
            print()
            print("Для продолжения введите номер операции.")
            log_file('Создать новый аккаунт', 'OK')
            break

        elif operation == '0':
            print()
            print("Спасибо за пользование нашей программой. До свидания!")
            log_file('Выход из приложения', 'OK')
            exit()
        else:
            print()
            print("Указан несуществующий номер операции. Повторите попытку.")

    while True:
        print("  1. Положить деньги на счет.")
        print("  2. Снять деньги.")
        print("  3. Вывести баланс на экран.")
        print("  4. Установить лимит на счет.")
        print("  5. Операции с ожидаемыми пополнениями.")
        print("  6. Операции с отложенными платежами.")
        print("  0. Выход из приложения.")
        operation = input("Введите номер операции: ")

        if operation == '1':  # 1. Положить деньги на счет.
            user_cash = input_int("Введите сумму пополнения (для отмены операции введите 0): ")
            if user_cash > 0:
                user_data[2] += user_cash
                file_save(name_file, data_dict)
                print(f'- Счёт успешно пополнен на сумму: {user_cash} руб.')
                print()
                log_file('Положить деньги на счет', 'OK')

                check_while = True
                while check_while:
                    pay_operation = input("Провести отложенные платежи (yes/no)?: ")
                    if pay_operation == "yes":
                        check_while = False
                        if input_password(user_account, input("Введите пароль: ")):
                            for s in make_payments(user_account, data_dict):
                                print(s)
                            file_save(name_file, data_dict)
                            log_file('Провести отложенные платежи', 'OK')
                        else:
                            print("- Введен неверный пароль!")

                    elif pay_operation == 'no':
                        check_while = False
                    else:
                        print("- Некорректная команда. Повторите попытку.")
                        print()

            else:
                log_file('Положить деньги на счет', 'ERROR')

            print()
            print("Для продолжения введите номер операции.")

        elif operation == '2':  # 2. Снять деньги.
            if input_password(user_account, input("Введите пароль: ")) == False:
                print("- Введен неверный пароль!")
                print()
                print("Для продолжения введите номер операции.")
                log_file('Снять деньги', 'ERROR')
            else:
                user_bank = user_data[2]
                print(f'Ваш текущий баланс: {user_bank} руб.')
                user_pick = input_int("Введите сумму для снятия: ")
                if user_pick > 0:
                    if user_bank - user_pick < 0:
                        print(f'- Выполнение операции невозможно! Ваш текущий баланс: {user_bank} руб.')
                        log_file('Снять деньги', 'ERROR')
                    else:
                        user_bank -= user_pick
                        user_data[2] = user_bank
                        file_save(name_file, data_dict)
                        print(f'- Снятие успешно завершено! Ваш баланс: {user_bank} руб.')
                        log_file('Снять деньги', 'OK')

                print()
                print("Для продолжения введите номер операции.")

        elif operation == '3':  # 3. Вывести баланс на экран.
            if input_password(user_account, input("Введите пароль: ")) == False:
                print("- Введен неверный пароль!")
                print()
                print("Для продолжения введите номер операции.")
                log_file('Вывести баланс на экран', 'ERROR')
            else:
                user_bank = user_data[2]
                print(f'- Ваш текущий баланс: {user_bank} руб.')
                log_file('Вывести баланс на экран', 'OK')

            print()
            print("Для продолжения введите номер операции.")

        elif operation == '4':  # 4. Установить лимит на счет.
            user_limit = user_data[3]
            print(f'На Ваш счет установлен лимит в {user_limit} руб.')
            user_limit = input_int("Изменить лимит на счет: ")
            user_data[3] = user_limit
            file_save(name_file, data_dict)
            print(f'- Установлен лимит на счет: {user_limit} руб.')
            log_file('Установка лимита на счет', 'OK')
            print()
            print("Для продолжения введите номер операции.")

        elif operation == '5':  # 5. Операции с ожидаемыми пополнениями.
            print()
            print("Для продолжения введите номер операции.")
            while True:
                print("  1. Запись ожидаемой транзакции (пополнения).")
                print("  2. Выполнить транзакции.")
                print("  3. Статистика по ожидаемым пополнениям.")
                print("  4. Фильтр по ожидаемым пополнениям.")
                print("  0. Вернуться в основное меню.")
                operation = input("Введите номер операции: ")

                if operation == '1':  # 1. Запись ожидаемой транзакции (пополнения)
                    trans_summ = input_int("Укажите сумму ожидаемой транзакции: ")
                    trans_note = input("Комментарий к ожидаемой транзакции: ")
                    user_transactions = user_data[4]
                    user_transactions.append([trans_summ, trans_note, 0])
                    file_save(name_file, data_dict)
                    print(f'- Ожидаемая транзакция "{trans_note}" на сумму {trans_summ} руб. установлена.')
                    log_file('Запись ожидаемой транзакции (пополнения)', 'OK')
                    count, summa = 0, 0
                    for trans in user_transactions:
                        if trans[2] == 0:
                            count += 1
                            summa += trans[0]
                    print(f'- Количество ожидаемых транзакций: {count} на сумму {summa} руб.')
                    print()
                    print("Для продолжения введите номер операции.")

                    continue

                elif operation == '2':  # 2. Выполнить транзакции.
                    user_transactions = user_data[4]
                    count = 0
                    for trans in ([item for item in user_transactions if item[2] == 0]):
                        count += 1
                        if user_data[2] + trans[0] <= user_data[3]:
                            trans[2] = 1
                            user_data[2] += trans[0]
                            print(f'- Транзакция {trans[1]} на сумму {trans[0]} руб. успешно применена.')
                        else:
                            print(
                                f'- Транзакция {trans[1]} на сумму {trans[0]} руб. не может быть применена. Превышение лимита')

                    if count == 0:
                        print("- Ожидаемых пополнений нет.")

                    file_save(name_file, data_dict)
                    log_file('Выполнить транзакции', 'OK')
                    print()
                    print("Для продолжения введите номер операции.")

                    continue

                elif operation == '3':  # 3. Статистика по ожидаемым пополнениям.
                    trans_dict = {}
                    user_transactions = user_data[4]
                    # count = 0
                    for summa, name, status in user_transactions:
                        if status == 0:
                            if name not in trans_dict:
                                trans_dict[name] = [1, summa]
                            else:
                                trans_dict[name] = [trans_dict[name][0] + 1, trans_dict[name][1] + summa]

                    if len(trans_dict) == 0:
                        print("Ожидаемых транзакций нет.")
                        print()
                        print("Для продолжения введите номер операции.")
                    else:
                        print("- Ожидаемые транзакции:")
                        for name, list in trans_dict.items():
                            print(
                                f'- Количество ожидаемых транзакций "{name}": {list[0]}, на общую сумму {list[1]} руб.')
                        print()
                        print("Для продолжения введите номер операции.")

                    log_file('Статистика по ожидаемым пополнениям', 'OK')
                    continue

                elif operation == '4':  # 4. Фильтр по ожидаемым пополнениям.
                    user_filter = input_int("Показать ожидаемые транзакции, сумма которых больше: ")
                    user_transactions = user_data[4]
                    count = 0
                    for summa, name, status in user_transactions:
                        if summa > user_filter and status == 0:
                            print(f'- Транзакция "{name}", на сумму {summa} руб.')
                            count += 1
                    if count == 0:
                        print(f'- Ожидаемых транзакции, сумма которых больше {user_filter} руб. нет.')

                    print()
                    print("Для продолжения введите номер операции.")
                    log_file('Фильтр по отложенным транзакциям', 'OK')
                    continue

                elif operation == '0':
                    print()
                    print("Для продолжения введите номер операции.")
                    break
                else:
                    print()
                    print("Указан несуществующий номер операции. Повторите попытку.")

        elif operation == '6':  # 6. Операции с отложенными платежами.
            print()
            print("Для продолжения введите номер операции.")
            while True:
                print("  1. Создать платеж.")
                print("  2. Список отложенных платежей.")
                print("  3. Провести отложенные платежи.")
                print("  0. Вернуться в основное меню.")
                operation = input("Введите номер операции: ")
                if operation == '1':  # 1. Создать платеж.
                    pay_account = input("Введите аккаунт получателя платежа: ")
                    if pay_account == user_account:
                        print("- Вы не можете сами себе осуществить платеж!")
                        print()
                        print("Для продолжения введите номер операции.")
                        log_file('Отложенный платеж', 'ERROR')
                        continue
                    if pay_account not in data_dict:
                        print("- Указанный Вами аккаунт не зарегистрирован!")
                        print()
                        print("Для продолжения введите номер операции.")
                        log_file('Отложенный платеж', 'ERROR')
                        continue
                    pay_summ = input_int(f'Укажите сумму платежа для "{pay_account}" (для отмены операции введите 0): ')
                    if pay_summ == 0:
                        print()
                        print("Для продолжения введите номер операции.")
                        log_file('Отложенный платеж', 'FAULT')
                        continue

                    if user_data[2] > pay_summ:
                        pay_status = 0
                        check_while = True
                        while check_while:
                            pay_operation = input("Провести платеж сейчас или отложить (yes/no)?: ")
                            if pay_operation == "yes":
                                check_while = False
                                pay_status = 1
                            elif pay_operation == 'no':
                                check_while = False
                            else:
                                print("- Некорректная команда. Повторите попытку.")
                                print()
                    else:
                        pay_status = 0

                    if pay_status == 1:
                        if not input_password(user_account, input("Введите пароль: ")):
                            pay_status = 0
                            print("- Введен неверный пароль!")
                            print("- Платеж будет создан, но не проведен.")

                    user_pay = user_data[5]
                    user_pay.append([pay_summ, pay_account, pay_status])

                    if pay_status == 1:
                        pay_data = data_dict[pay_account]
                        pay_data[2] += pay_summ
                        user_data[2] -= pay_summ
                        print(f'- Платеж для "{pay_account}" на сумму {pay_summ} создан и успешно проведен.')
                    else:
                        print(f'- Отложенный платеж для "{pay_account}" на сумму {pay_summ} руб. создан.')

                    file_save(name_file, data_dict)
                    print()
                    print("Для продолжения введите номер операции.")
                    log_file('Отложенный платеж', 'OK')
                    continue

                elif operation == '2':  # 2. Список отложенных платежей.
                    user_pay = user_data[5]
                    count = 0
                    for summa, account, status in user_pay:
                        if status == 0:
                            print(f'- Отложенный платеж: аккаунт "{account}", сумма {summa} руб.')
                            count += 1
                    if count == 0:
                        print(f'- Отложенных платежей нет.')

                    print()
                    print("Для продолжения введите номер операции.")
                    log_file('Список отложенных платежей', 'OK')
                    continue

                elif operation == '3':  # 3. Провести отложенные платежи.
                    if input_password(user_account, input("Введите пароль: ")):
                        for s in make_payments(user_account, data_dict):
                            print(s)
                        file_save(name_file, data_dict)
                        log_file('Провести отложенные платежи', 'OK')
                    else:
                        print("- Введен неверный пароль!")
                        log_file('Провести отложенные платежи', 'ERROR')

                    print()
                    print("Для продолжения введите номер операции.")
                    continue

                elif operation == '0':
                    print()
                    print("Для продолжения введите номер операции.")
                    break
                else:
                    print()
                    print("Указан несуществующий номер операции. Повторите попытку.")

        elif operation == '0':
            print()
            print("Спасибо за пользование нашей программой. До свидания!")
            log_file('Выход из приложения', 'OK')
            exit()
        else:
            print()
            print("Указан несуществующий номер операции. Повторите попытку.")
