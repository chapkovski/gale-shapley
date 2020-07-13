from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from .galeshapley import to_shapley

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'gs'
    players_per_group = None
    num_rounds = 1


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class Subsession(BaseSubsession):
    def set_small_groups(self):
        newmat = to_shapley(self)

        print('New matrix:', newmat)
        self.set_group_matrix(matrix=newmat)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
