from Classes import Army, Economy, Country, InputError


def update_fights_stats(active_country: Country, passive_country: Country, fight_info: dict) -> None:
    active_army, passive_army = fight_info['active_army'], fight_info['passive_army']
    active_result, passive_result = fight_info['active_result'], fight_info['passive_result']

    active_army.fights_info['fights_total'] += 1
    if passive_army: passive_army.fights_info['fights_total'] += 1

    if active_result > passive_result:
        active_army.fights_info['fights_won'] += 1
        if passive_army: passive_army.fights_info['fights_lost'] += 1
        winner, loser = active_country, passive_country
    else:
        passive_army.fights_info['fights_won'] += 1
        active_army.fights_info['fights_lost'] += 1
        winner, loser = passive_country, active_country

    print(f"Армия страны {winner.country_name} побеждает.")
    print(f"Армия страны {loser.country_name} проигрывает.")


def start_a_war(active_country: Country, passive_country: Country) -> bool:
    print(f"Выбор атакующей армии для страны {active_country.country_name}:")
    active_army = choose_army(active_country)
    print(f"Выбор атакующей армии для страны {passive_country.country_name}:")
    passive_army = choose_army(passive_country)

    if not active_army or not active_army.number_of_soldiers:
        print(f"Невозможно начать атаку, так как в атакующей стране"
              f" нет созданных армий или в выбранной армии нет солдат.")
        return False

    active_result = (active_country.number_of_soldiers * active_army.army_strength *
                     (active_country.army_money if active_country.army_money > 0 else 1))
    passive_result = -1 if (not passive_army or not passive_country.number_of_soldiers) else \
        (passive_country.number_of_soldiers * passive_army.army_strength *
         (passive_country.army_money if passive_country.army_money > 0 else 1))

    fight_info = {'active_army': active_army, 'passive_army': passive_army,
                  'active_result': active_result, 'passive_result': passive_result}

    update_fights_stats(active_country, passive_country, fight_info)

    return True


def recruit_soldiers(country: Country, given_army=None) -> bool:
    army = choose_army(country) if not given_army else given_army
    if not army:
        print(f"У страны {country.country_name} нет созданных армий.")
        return False
    try:
        amount = int(input(f"Введите желаемое количество солдат для рекрутинга"
                           f" (всего доступно {country.possible_number_of_recruits})."))
        if amount > country.possible_number_of_recruits:
            raise InputError
        army.number_of_soldiers += amount
        print(f"{amount} солдат были рекрутированы.")
        return True
    except ValueError:
        print("Введено не число.")
    except InputError:
        print("Введенное количество солдат превышает максимально возможное для рекрутинга.")
    return False


def retire_soldiers(country: Country) -> bool:
    army = choose_army(country)
    if not army:
        print(f"У страны {country.country_name} нет созданных армий.")
        return False
    try:
        amount = int(input(f"Введите желаемое количество солдат для"
                           f" отставки (всего доступно {army.number_of_soldiers})."))
        if amount > army.number_of_soldiers:
            raise InputError
        army.number_of_soldiers -= amount
        print(f"{amount} солдат были отправлены в отставку.")
        return True
    except ValueError:
        print("Введено не число.")
    except InputError:
        print("Введенное количество солдат превышает максимально возможное для отставки.")
    return False


def buy_upgrades(country: Country) -> bool:
    cost = country.economy.upgrade_cost
    maxamount = country.economy_money // cost
    if maxamount <= 0:
        print("Невозможно купить улучшения из-за недостатка денег.")
        return False
    try:
        amount = int(input(f"Введите желаемое количество улучшений (всего доступно {maxamount})."))
        if amount > maxamount:
            raise InputError
        print("Улучшения куплены.")
        country.economy_money -= amount * cost
        country.economy_money += amount * 1000
        return True
    except ValueError:
        print("Введено не число.")
    except InputError:
        print("Введенное количество улучшений превышает максимально возможное.")
    return False


def fill_economy() -> Economy:
    rows = ["upgrade_cost", "number_of_upgrades"]
    economy = Economy()
    for row in rows:
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
    return economy


def fill_country(taken_names: list[str]) -> Country:
    country = Country()
    for_country = ["country_name", "population", "economy_money", "army_money", "income"]
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
        return country


def create_country(taken_names: list[str]) -> (Country, str):
    country = fill_country(taken_names)
    country.economy = fill_economy()
    return country, country.country_name


def fill_army(country: Country) -> Army:
    army = Army()
    while True:
        try:
            info = input(f"Заполнение поля general: ")
            if not info.isalpha():
                raise InputError
            setattr(army, "general", info)
            break
        except InputError:
            print("Генерал не может иметь введенное имя.")
    print("Заполнение поля number_of_soldiers: ")
    while not recruit_soldiers(country, army):
        print("Заполнение поля number_of_soldiers: ")
    return army


def create_army(country: Country) -> Army:
    army = fill_army(country)
    print(f"Армия успешно создана.")
    return army


def choose_army(country: Country):
    if not len(country.armies):
        return None
    print(f"Вот информация об армиях страны {country.country_name}:")
    for i in range(len(country.armies)): print(f"Армия {i}:\n{country.armies[i]}")
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


def get_money_for_army(country: Country) -> bool:
    try:
        amount = int(input(f"Введите желаемое количество денег для перевода (всего доступно {country.economy_money}."))
        if amount > country.economy_money:
            raise InputError
        print("Деньги переведены.")
        country.economy_money -= amount
        country.army_money += amount
        return True
    except ValueError:
        print("Введено не число.")
    except InputError:
        print("Введенное количество денег превышает максимально доступное.")
    return False


def get_money_for_economy(country: Country) -> bool:
    try:
        amount = int(input(f"Введите желаемое количество денег для перевода (всего доступно {country.army_money}."))
        if amount > country.army_money:
            raise InputError
        print("Деньги переведены.")
        country.army_money -= amount
        country.economy_money += amount
        return True
    except ValueError:
        print("Введено не число.")
    except InputError:
        print("Введенное количество денег превышает максимально доступное.")
    return False


def choose_command(actions: dict) -> int:
    print("Доступные действия: ")
    for n, a in actions.items(): print(f"{n}: {a}")
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
    return chosen_command


def economy_stage(active_country: Country) -> None:
    actions = {1: "Купить улучшения", 2: "Пропустить ход", 3: "Перевести деньги на экономику с армии"}
    is_successful = False
    while not is_successful:
        chosen_command = choose_command(actions)
        match chosen_command:
            case 1:
                is_successful = buy_upgrades(active_country)
            case 2:
                is_successful = True
                print(f"Страна {active_country.country_name} пропустила ход")
            case 3:
                is_successful = get_money_for_economy(active_country)
            case _:
                pass


def military_stage(active_country: Country, passive_country: Country) -> None:
    actions = {1: "Нанять солдат", 2: "Отправить солдат в отставку",
               3: "Начать войну", 4: "Перевести деньги на армию с экономики", 5: "Пропустить ход"}
    is_successful = False
    while not is_successful:
        chosen_command = choose_command(actions)
        match int(chosen_command):
            case 1:
                is_successful = recruit_soldiers(active_country)
            case 2:
                is_successful = retire_soldiers(active_country)
            case 3:
                is_successful = start_a_war(active_country, passive_country)
            case 4:
                is_successful = get_money_for_army(active_country)
            case 5:
                is_successful = True
                print(f"Страна {active_country.country_name} пропустила ход")
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
