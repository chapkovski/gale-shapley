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
from django.db import models as djmodels
from django.db.models import F, Q, Case, When

author = 'Philipp Chapkovski'

doc = """
prefs exposure, and supergroup sorter
"""


class Constants(BaseConstants):
    name_in_url = 'sorter'
    players_per_group = 16
    num_rounds = 1
    subgroups = ['A', 'B']


class Subsession(BaseSubsession):
    def creating_session(self):
        # assigning subgroup membership
        for p in self.get_players():
            p.subgroup = Constants.subgroups[p.id_in_group % 2]
            p.save()
        prefs_to_create = []
        for p in self.get_players():
            prefs_to_add = [Pref(owner=p, item=i) for i in list(p.get_other_subgroup_members())]
            prefs_to_create.extend(prefs_to_add)
        Pref.objects.bulk_create(prefs_to_create)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    subgroup = models.StringField()
    prefs_over_others = models.StringField()
    trump = models.BooleanField(label='Who do you prefer:', choices=[[True, 'Donald Trump'],
                                                                     [False, 'Joe Biden']],
                                widget=widgets.RadioSelectHorizontal)
    abortion = models.BooleanField(label='your preferences:', choices=[[True, 'Pro-choice'],
                                                                       [False, 'Pro-life']],
                                   widget=widgets.RadioSelectHorizontal)

    def get_other_subgroup_members(self):
        q = self.group.player_set.filter(subgroup__isnull=False).exclude(subgroup=self.subgroup)
        return q


class Pref(djmodels.Model):
    class Meta:
        unique_together = ['owner', 'item', 'position']

    owner = djmodels.ForeignKey(to=Player, on_delete=models.CASCADE, related_name='prefs')
    item = djmodels.ForeignKey(to=Player, on_delete=models.CASCADE, related_name='statedpositions')
    position = models.IntegerField()
