from .general_types import Man, Woman
import logging

logger = logging.getLogger(__name__)


def to_shapley(subsession):
    """We take a subsession data on otree. We split each group into A and B (based on player's subgroup property),
    and feed them group by group to a gale_shapley. We add resulting pairs into a resulting group matrix and return
    it so subsession.set_group_matrix can be assigned"""
    resulting_matrix = []
    for g in subsession.group_set.all():
        males = g.player_set.filter(participant__sorter_player__subgroup='A')
        females = g.player_set.filter(participant__sorter_player__subgroup='B')
        male_dict = {m.id: m.participant.vars['prefs'] for m in males}
        female_dict = {m.id: m.participant.vars['prefs'] for m in females}
        sub_matrix = gale_shapley(male_dict, female_dict)
        resulting_matrix.extend(sub_matrix)
    return resulting_matrix


def gale_shapley(males, females):
    guys = sorted(males.keys())
    gals = sorted(females.keys())
    guy_objs = []
    gals_objs = []
    for i in guys:
        g = Man(name=i)
        guy_objs.append(g)

    for i in gals:
        g = Woman(name=i)
        gals_objs.append(g)

    # set prefs
    def get_obj_by_name(name, l):
        return next((i for i in l if i == name))

    for i in guy_objs:
        i.original_prefs = [get_obj_by_name(j, gals_objs) for j in males[i.name]]
        i.prefs = i.original_prefs[:]
    for i in gals_objs:
        i.original_prefs = [get_obj_by_name(j, guy_objs) for j in females[i.name]]
        i.prefs = i.original_prefs[:]

    # matching starts
    freeguys = [i for i in guy_objs if not i.married_to]

    while freeguys:
        male_candidate = freeguys.pop(0)
        female_candidate = male_candidate.retrieve_most_preferred()
        # if the first most preferred is not married, then let them get married.
        if not female_candidate.married_to:
            male_candidate.married_to = female_candidate
            female_candidate.married_to = male_candidate
        else:
            if female_candidate.accepts(male_candidate):
                free_hubby = female_candidate.married_to
                freeguys.append(free_hubby)
                male_candidate.married_to = female_candidate
                female_candidate.married_to = male_candidate
            else:
                freeguys.append(male_candidate)
    """We actually don't need this, this is just to check that our algorithm works correctly"""
    if check(guy_objs, gals_objs):
        return [[i.name, i.married_to.name] for i in guy_objs]


def check(guy_objs, gals_objs):
    for guy in guy_objs:
        if guy.married_to:
            more_preferred = guy.get_more_preferred(guy.married_to)
            for girl in more_preferred:
                if girl.married_to:
                    preferred_by_girl = girl.get_more_preferred(girl.married_to)
                    if guy in preferred_by_girl:
                        raise Exception('not stable matching')
    for gal in gals_objs:
        if gal.married_to:
            more_preferred = gal.get_more_preferred(gal.married_to)
            for dude in more_preferred:
                if dude.married_to:
                    preferred_by_dude = dude.get_more_preferred(dude.married_to)
                    if gal in preferred_by_dude:
                        raise Exception('not stable matching')
    return True
