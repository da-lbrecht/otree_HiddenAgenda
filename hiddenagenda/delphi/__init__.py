from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'delphi'
    players_per_group = None
    num_rounds = 10

    fixed_pay = 5
    avg_pay = 12


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    starting_time = models.LongStringField(doc="Time at which Informed Consent is given and experiment starts")
    begintrial_time = models.LongStringField(doc="Time at which trial round is started")

    endround_time = models.LongStringField(doc="Time at which a task round is started")


    first_indivestim = models.FloatField(label="My first estimate:")
    second_indivestim = models.FloatField(label="My second estimate:")



# PAGES
class Welcome(Page):
    form_model = 'player'
    form_fields = ['starting_time']

class TaskIntro(Page):
    form_model = 'player'
    form_fields = ['begintrial_time']

class Task(Page):
    form_model = 'player'
    form_fields = ['endround_time', 'first_indivestim', 'second_indivestim']


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Welcome, TaskIntro, Task, MyPage, ResultsWaitPage, Results]
