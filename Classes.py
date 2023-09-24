class Army:
    def __init__(self, general: str = "Unknown", number_of_soldiers: int = 0) -> None:
        self.general = general
        self.fights_info = {
            'fights_total': 0,
            'fights_won': 0,
            'fights_lost': 0,
        }
        self.loss_of_money = 0
        self.number_of_soldiers = number_of_soldiers

    @property
    def army_strength(self) -> float:
        return self.number_of_soldiers * (1 + self.fights_info['fights_total'] / 100) * \
               (2 + self.fights_info['fights_won'] / 100)

    def __repr__(self) -> str:
        return ('Генерал: {}\nОбщее количество битв: {}\nКоличество выигранных битв: {}\nКоличество проигранных битв:'
                '{}\nУбыток денег: {}\nСила армии: {}'
                .format(self.general, self.fights_info['fights_total'], self.fights_info['fights_won'],
                        self.fights_info['fights_lost'], self.loss_of_money, self.army_strength))


class Economy:
    def __init__(self, upgrade_cost: int = 0, number_of_upgrades: int = 0) -> None:
        self.upgrade_cost = upgrade_cost
        self.number_of_upgrades = number_of_upgrades

    def __repr__(self) -> str:
        return ('Количество улучшений: {}\nСтоимость улучшения: {}'
                .format(self.number_of_upgrades, self.upgrade_cost))


class Country:
    def __init__(self, population: int = 0, economy_money: int = 0, income: int = 0,
                 army_money: int = 0, country_name: str = "Unknown", economy: Economy = None) -> None:
        self.population = population
        self.economy_money = economy_money
        self.army_money = army_money
        self.country_name = country_name
        self.income = income
        self.economy = economy
        self.armies = []

    @property
    def civilians(self):
        return self.population - self.number_of_soldiers

    @property
    def possible_number_of_recruits(self) -> int:
        difference = self.population // 2 - self.civilians if self.population // 2 < self.civilians else 0
        return self.civilians + difference

    @property
    def current_income(self) -> int:
        return self.income + self.economy.number_of_upgrades * 1000

    @property
    def number_of_soldiers(self):
        return sum([army.number_of_soldiers for army in self.armies])

    def __repr__(self) -> str:
        return ('Население страны: {}\nКоличество военных: {}\nМирное население: {}\n'
                'Деньги на экономику: {}\nДеньги на армию: {}\nНазвание страны: {}\n'
                'Доход: {}\nТекущий доход: {}\nВозможное количество рекрутов: {}'
                .format(self.population,
                        self.number_of_soldiers,
                        self.civilians,
                        self.economy_money,
                        self.army_money,
                        self.country_name,
                        self.income,
                        self.current_income,
                        self.possible_number_of_recruits))


class InputError(Exception):
    pass

