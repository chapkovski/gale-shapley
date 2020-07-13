from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


def r():
    return random.choice([True, False])


class PlayerBot(Bot):
    def _cq_data(self):
        q = self.player.prefs.all()
        name = 'prefs'
        field_name = 'position'
        full_answers = {}
        for i, j in enumerate(q):
            full_answers[f'{name}-{i}-id'] = j.id
            full_answers[f'{name}-{i}-owner'] = self.player.pk
            full_answers[f'{name}-{i}-{field_name}'] = i + 1
        return {
            f'{name}-TOTAL_FORMS': q.count(),
            f'{name}-INITIAL_FORMS': q.count(),
            f'{name}-MIN_NUM_FORMS': '0',
            f'{name}-MAX_NUM_FORMS': '1000',
            **full_answers
        }

    def play_round(self):
        yield pages.Prefs, dict(trump=r(), abortion=r())
        yield pages.PrefsOverOthers, self._cq_data()
