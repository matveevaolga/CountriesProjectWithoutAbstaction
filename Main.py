from Functions import *


countries = {}
commands = {1: 'Создать страну', 2: 'Информация о стране', 3: 'Информация об экономике страны',
            4: 'Информация об армии страны', 5: 'Начать войну', 6: 'Рекрутировать солдат',
            7: 'Отправить солдат в отставку', 8: 'Купить улучшения', 9: 'Создать армию для страны', 10: 'Выйти'}


def country_choice(taken_n=-1) -> int:
    for numb, name in zip(range(1, len(countries) + 1), countries.keys()):
        print(numb, ': ', name, sep='')
    while True:
        try:
            n = int(input("Выберите страну: "))
            if n == taken_n:
                print("Эта страна уже выбрана.")
                continue
            if n not in range(1, len(countries) + 1):
                raise InputError
            break
        except ValueError:
            print("Введено не число.")
        except InputError:
            print("Страны под введенном номером не существует.")
    return n


def command_choice() -> int:
    for numb, comm in commands.items():
        print(numb, ': ', comm, sep='')
    while True:
        try:
            command_num = int(input("Выберите номер команды: "))
            if not len(countries) and command_num != 1:
                raise InputError
            break
        except ValueError:
            print("Введено не число.")
        except InputError:
            print('Вы еще не создали ни одной страны.')
    return command_num


def manage_war() -> None:
    if len(countries) == 1:
        print(f'Стране {list(countries.keys())[0]} не с кем воевать.')
        return
    print('Выбор атакующей страны:')
    n1 = country_choice()
    country1 = countries[list(countries.keys())[n1]]
    print('Выбор защищающейся страны:')
    n2 = country_choice(n1)
    country2 = countries[list(countries.keys())[n2]]
    for _ in range(2):
        make_a_move(country1, country2)
        make_a_move(country2, country1)


def start():
    while True:
        command = command_choice()
        match command:
            case 1:
                country, country_name = create_country(list(countries.keys()))
                countries[country.country_name] = country
            case 2:
                n = country_choice()
                country = list(countries.values())[n]
                print(country)
            case 3:
                n = country_choice()
                country = list(countries.values())[n]
                print(country.economy)
            case 4:
                n = country_choice()
                country = list(countries.values())[n]
                army = choose_army(country)
                print(army)
            case 5:
                manage_war()
            case 6:
                n = country_choice()
                country = list(countries.keys())[n]
                country = countries[country]
                recruit_soldiers(country)
            case 7:
                n = country_choice()
                country = list(countries.keys())[n]
                country = countries[country]
                retire_soldiers(country)
            case 8:
                n = country_choice()
                country = list(countries.keys())[n]
                buy_upgrades(countries[country])
            case 9:
                n = country_choice()
                country = list(countries.values())[n]
                country.armies.append(create_army(country))
            case 10:
                break
            case _:
                print('Неверный номер команды.')


if __name__ == '__main__':
    start()
