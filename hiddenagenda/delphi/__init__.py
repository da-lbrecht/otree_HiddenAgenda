from otree.api import *
import random
import numpy as np

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'delphi'
    players_per_group = None
    num_rounds = 10

    fixed_pay = 5
    avg_pay = 12

    num_attention_checks = 5

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Process variables
    starting_time = models.LongStringField(doc="Time at which Informed Consent is given and experiment starts")
    begintrial_time = models.LongStringField(doc="Time at which trial round is started")

    endround_time = models.LongStringField(doc="Time at which a task round is started")

    round_displayed = models.IntegerField(doc="Position in which estimation task was displayed, ranging from 1 to num_rounds")

    # Response variables for attention checks
    attention_check_1 = models.IntegerField(label="How many rounds of the task will you play after the trial round?",
                                            doc="Attention check: How many rounds of the task will you play after the trial round?")
    attention_check_2 = models.IntegerField(label="How many rounds of the task will you play after the trial round?",
                                            doc="Attention check: How many rounds of the task will you play after the trial round?")
    attention_check_3 = models.IntegerField(label="How many rounds of the task will you play after the trial round?",
                                            doc="Attention check: How many rounds of the task will you play after the trial round?")
    attention_check_4 = models.IntegerField(label="How many rounds of the task will you play after the trial round?",
                                            doc="Attention check: How many rounds of the task will you play after the trial round?")
    attention_check_5 = models.IntegerField(label="How many rounds of the task will you play after the trial round?",
                                            doc="Attention check: How many rounds of the task will you play after the trial round?")

    # Response variables for estimation
    first_indivestim = models.FloatField(label="My first estimate:")
    second_indivestim = models.FloatField(label="My second estimate:")

# FUNCTIONS
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        list_of_round_ids = range(1, Constants.num_rounds + 1)
        subsession_temp_list = list_of_round_ids
        # random.shuffle(subsession_temp_list) # Needed for randomization of round order
        for player in subsession.get_players():
            temp_list = subsession_temp_list
            for i in list_of_round_ids:
                player.in_round(i).round_displayed = temp_list[i-1]

# PAGES
class Welcome(Page):
    form_model = 'player'
    form_fields = ['starting_time']

    @staticmethod
    def is_displayed(subsession: Subsession):
        return subsession.round_number == 1

class TaskIntro(Page):
    form_model = 'player'
    form_fields = ['begintrial_time',
                   'attention_check_1', 'attention_check_2', 'attention_check_3', 'attention_check_4', 'attention_check_5']

    @staticmethod
    def is_displayed(subsession: Subsession):
        return subsession.round_number == 1


class Task_Round_1(Page):
    form_model = 'player'
    form_fields = ['endround_time', 'first_indivestim', 'second_indivestim']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_displayed == 1


class Task_Round_2(Page):
    form_model = 'player'
    form_fields = ['endround_time', 'first_indivestim', 'second_indivestim']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_displayed == 2


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    @staticmethod
    def is_displayed(subsession: Subsession):
        return subsession.round_number == Constants.num_rounds


page_sequence = [Welcome, TaskIntro,
                 Task_Round_1, Task_Round_2,
                 Results]
