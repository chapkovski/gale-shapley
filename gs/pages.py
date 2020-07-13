from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class FirstWP(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'set_small_groups'


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [
    FirstWP,
    MyPage,
]
