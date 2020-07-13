from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from django.db.models import F
from .forms import PFormset
import json


class Prefs(Page):
    form_model = 'player'
    form_fields = ['trump', 'abortion']


class PrefsWaitPage(WaitPage):
    pass


class PrefsOverOthers(Page):

    def get_formset(self, data=None):
        return PFormset(instance=self.player,
                        data=data,
                        )

    def get_form(self, data=None, files=None, **kwargs):
        # here if this page was forced by admin to continue we just submit an empty form (with no formset data)
        # if we need this data later on that can create some problems. But that's the price we pay for autosubmission
        if data and data.get('timeout_happened'):
            return super().get_form(data, files, **kwargs)
        if not data:
            return self.get_formset()
        formset = self.get_formset(data=data)
        return formset

    def before_next_page(self):
        self.participant.vars['subgroup'] = self.player.subgroup
        # we may think about storing the data in some more user-friendly format (participant codes?)
        # Right now it is just a very compact way to pass the ids of players of the next app, where
        # Gale Shapley will be applied. It's easy but not very informative for the analysis
        other_ids = list(self.player.prefs.all().order_by('position').annotate(
            gs_id=F('item__participant__sorter_player__id')).values_list('gs_id', flat=True))
        self.player.prefs_over_others = json.dumps(other_ids)
        self.participant.vars['prefs'] = other_ids


page_sequence = [
    Prefs,
    PrefsWaitPage,
    PrefsOverOthers,

]
