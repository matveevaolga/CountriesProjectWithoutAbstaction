from Classes import Army, Economy, Country, InputError
import random


def start_a_war(country1: Country, country2: Country) -> None:
    if country1.army_money <= 0 or not country2.army_money <= 0:
        print(f"Невозможно начать атаку, так как в одной или обеих из выбранных стран нет денег на армию.")
        return
# деньги нужны только на найм
    print(f"Выбор атакующей армии для страны {country1.country_name}:")
    army1 = choose_army(country1)
    print(f"Выбор атакующей армии для страны {country2.country_name}:")
    army2 = choose_army(country2)
# не работает при отсутствии армий
    if not army1 or not army2:
        print(f"Невозможно начать атаку, так как в одной или обеих из стран нет созданных армий.")
        return

    if not army1.number_of_soldiers or not army2.number_of_soldiers:
        print(f"Невозможно начать атаку, так как в одной или обеих из выбранных армий нет солдат.")
        return

    soldiers_lost1 = random.randint(0, country1.number_of_soldiers)
    soldiers_lost2 = random.randint(0, country2.number_of_soldiers)

    result1 = (country1.number_of_soldiers + country1.possible_number_of_recruits -
               soldiers_lost1) * army1.army_strength * (country1.army_money if country1.army_money > 0 else 1)
    result2 = (country2.number_of_soldiers + country2.possible_number_of_recruits -
               soldiers_lost2) * army2.army_strength * (country2.army_money if country2.army_money > 0 else 1)
# с 31 до 43 в отдельную ф-цию
    army1.fights_total += 1
    army2.fights_total += 1

    army1.number_of_soldiers -= soldiers_lost1
    army2.number_of_soldiers -= soldiers_lost2

    country1.population -= soldiers_lost1
    country2.population -= soldiers_lost2

    army1.loss_of_money += soldiers_lost1 * 5
    army2.loss_of_money += soldiers_lost2 * 5
    country1.army_money += soldiers_lost2 * 5 - soldiers_lost1 * 5
    country2.army_money += soldiers_lost1 * 5 - soldiers_lost2 * 5
# тоже в отдельную ф-цию до 54
    if result1 > result2:
        army1.fights_won += 1
        army2.fights_lost += 1
        winner, loser = country1, country2
        wlost, llost = soldiers_lost1, soldiers_lost2
    else:
        army2.fights_won += 1
        army1.fights_lost += 1
        winner, loser = country2, country1
        wlost, llost = soldiers_lost2, soldiers_lost1

    print(f"Армия страны {winner.country_name} побеждает, потеряв {wlost} солдат.")
    print(f"Армия страны {loser.country_name} проигрывает, потеряв {llost} солдат.")


def recruit_soldiers(country: Country) -> None:
    army = choose_army(country)
    while True:
        try:
            amount = int(input(f"Введите желаемое количество солдат для рекрутинга (всего доступно {country.possible_number_of_recruits})."))
            if amount > country.possible_number_of_recruits:
                raise InputError
            break
        except ValueError:
            print("Введено не число.")
        except InputError:
            print("Введенное количество солдат превышает максимально возможное для рекрутинга.")
    army.number_of_soldiers += amount
    country.army_money += amount * 5
    country.economy_money -= amount * 5
    print(f"{amount} солдат были рекрутированы.")


def retire_soldiers(country: Country) -> None:
    army = choose_army(country)
    while True:
        try:
            amount = int(input(f"Введите желаемое количество солдат для отставки (всего доступно {army.number_of_soldiers})."))
            if amount > army.number_of_soldiers:
                raise InputError
            break
        except ValueError:
            print("Введено не число.")
        except InputError:
            print("Введенное количество солдат превышает максимально возможное для отставки.")
    army.number_of_soldiers -= amount
    country.army_money -= amount * 5
    country.economy_money += amount * 5
    print(f"{amount} солдат были отправлены в отставку.")


# нет денег -> другое действие, а не while
def buy_upgrades(country: Country) -> None:
    cost = country.economy.upgrade_cost
    maxamount = country.economy_money // cost
    if maxamount <= 0:
        print("Невозможно купить улучшения из-за недостатка денег.")
        return
    while True:
        try:
            amount = int(input(f"Введите желаемое количество улучшений (всего доступно {maxamount})."))
            if amount > maxamount:
                raise InputError
            print("Улучшения куплены.")
            break
        except ValueError:
            print("Введено не число.")
        except InputError:
            print("Введенное количество улучшений превышает максимально возможное.")
    country.economy_money -= amount * cost
    country.economy_money += amount * 1000


def create_country(taken_names: list[str]) -> (Country, str):
    economy = Economy()
    country = Country()
    for_economy = ["upgrade_cost", "number_of_upgrades"]
    for_country = ["country_name", "population", "economy_money", "army_money", "income"]
# в отдельную ф-цию заполнение страны и отд. для заполнения экономики
    for row in for_economy:
        while True:
            try:
                info = int(input(f"Заполнение поля {row}: "))
                if info <= 0:
                    raise InputError
                setattr(economy, row, info)
                break
            except ValueError:
                print(f"Введено не число.")
            except InputError:
                print("Данное поле не может принимать введенное значение.")

    for row in for_country:
        if row == "country_name":
            while True:
                try:
                    info = input(f"Заполнение поля {row}: ")
                    if info in taken_names:
                        raise InputError
                    setattr(country, row, info)
                    break
                except InputError:
                    print("Страна с данным именем уже существует.")
        else:
            while True:
                try:
                    info = int(input(f"Заполнение поля {row}: "))
                    if info <= 0:
                        raise InputError
                    setattr(country, row, info)
                    break
                except ValueError:
                    print(f"Введено не число.")
                except InputError:
                    print("Данное поле не может принимать введенное значение.")

    country.economy = economy
    return country, country.country_name


# тоже fill_army
def create_army() -> Army:
    army = Army()
    for_army = ["general", "number_of_soldiers"]
    for row in for_army:
        if row == "general":
            while True:
                try:
                    info = input(f"Заполнение поля {row}: ")
                    if not info.isalpha():
                        raise InputError
                    setattr(army, row, info)
                    break
                except InputError:
                    print("Генерал не может иметь введенное имя.")
        else:
            while True:
                try:
                    info = int(input(f"Заполнение поля {row}: "))
                    if info <= 0:
                        raise InputError
                    setattr(army, row, info)
                    break
                except ValueError:
                    print(f"Введено не число.")
                except InputError:
                    print("Данное поле не может принимать введенное значение.")
    print(f"Армия успешно создана.")
    return army


def choose_army(country: Country) -> Army:
    while True:
        try:
            army_number = int(input(f"Введите номер армии. Всего у страны {country.country_name} "
                                    f"{len(country.armies)} армий."))
            if not (0 <= army_number <= len(country.armies)):
                raise InputError
            break
        except ValueError:
            print("Вы ввели не число.")
        except InputError:
            print("Данное поле не может принимать введенное значение.")
    return country.armies[army_number - 1]


# перенести деньги на экономику с армии + еще одно действие
def economy_stage(active_country: Country) -> None:
    actions = {1: "Купить улучшения", 2: "Пропустить ход"}
    # убрать zip
    for n, a in zip(actions.keys(), actions.values()): print(f"{n}: {a}")
    # тоже можно убрать while
    while True:
        try:
            chosen_command = int(input("Введите номер команды: "))
            if chosen_command not in actions.keys():
                raise InputError
            break
        except ValueError:
            print("Введено не число.")
        except InputError:
            print("Команды под введенном номером не существует.")
    match int(chosen_command):
        case 1:
            buy_upgrades(active_country)
        case 2:
            print(f"Страна {active_country.country_name} пропустила ход")
        case _:
            pass


def military_stage(active_country: Country, passive_country: Country) -> None:
    actions = {1: "Нанять солдат", 2: "Отправить солдат в отставку", 3: "Начать войну"}
    for n, a in zip(actions.keys(), actions.values()): print(f"{n}: {a}")
    while True:
        try:
            chosen_command = int(input("Введите номер команды: "))
            if chosen_command not in actions.keys():
                raise InputError
            break
        except ValueError:
            print("Введено не число.")
        except InputError:
            print("Команды под введенном номером не существует.")
    match int(chosen_command):
        case 1:
            recruit_soldiers(active_country)
        case 2:
            retire_soldiers(active_country)
        case 3:
            start_a_war(active_country, passive_country)
        case _:
            pass

        
def make_a_move(active_country: Country, passive_country: Country) -> None:
    print(f"Ход страны {active_country.country_name}:")

    print("Стадия 1(экономическая):")
    economy_stage(active_country)

    print("Стадия 2(военная):")
    military_stage(active_country, passive_country)

    print("Стадия 3(экономическая):")
    economy_stage(active_country)

    print(f"Ход страны {active_country.country_name} закончен")
