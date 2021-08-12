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
    # Temporarily stored variables during Delphi process
    estimate_a = models.FloatField
    estimate_b = models.FloatField
    estimate_c = models.FloatField
    estimate_d = models.FloatField
    num_estims = models.FloatField


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Process variables
    starting_time = models.LongStringField(doc="Time at which Informed Consent is given and experiment starts")
    begintrial_time = models.LongStringField(doc="Time at which trial round is started")

    endround_time = models.LongStringField(doc="Time at which a task round is started")

    round_displayed = models.IntegerField(doc="Position in which estimation task was displayed, ranging from 1 to "
                                              "num_rounds")

    # Response variables for attention checks
    attention_check_1 = models.IntegerField(label="Q1: How many rounds of the task will you play after the trial round?",
                                            doc="Attention check: How many rounds of the task will you play after the "
                                                "trial round?")
    attention_check_2 = models.IntegerField(label="Q2: How many rounds of the task will you play after the trial round?",
                                            doc="Attention check: How many rounds of the task will you play after the "
                                                "trial round?")
    attention_check_3 = models.IntegerField(label="Q3: How many rounds of the task will you play after the trial round?",
                                            doc="Attention check: How many rounds of the task will you play after the "
                                                "trial round?")
    attention_check_4 = models.IntegerField(label="Q4: How many rounds of the task will you play after the trial round?",
                                            doc="Attention check: How many rounds of the task will you play after the "
                                                "trial round?")
    attention_check_5 = models.IntegerField(label="Q5: How many rounds of the task will you play after the trial round?",
                                            doc="Attention check: How many rounds of the task will you play after the "
                                                "trial round?")
    failed_attention_check = models.BooleanField(initial=False,
                                                 doc="True if attention check has not been passed at first attempt")

    attention_check_tries = models.IntegerField(initial=1,
                                                doc="Number of attempts needed to pass attention check questions")

    # Response variables for estimation
    first_indivestim = models.FloatField(label="My first estimate:",
                                         doc="First individual estimate given in Delphi procedure")
    indivarg = models.IntegerField(label="My reasoning behind my first estimate",
                                   doc="Reasoning given for first individual estimate given in Delphi procedure")
    second_indivestim = models.FloatField(label="My second estimate:",
                                          doc="Second individual estimate given in Delphi procedure")


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
    def is_displayed(player: Player):
        return player.round_number == 1


class TaskIntro(Page):
    form_model = 'player'
    form_fields = ['begintrial_time',
                   'attention_check_1',
                   'attention_check_2',
                   'attention_check_3',
                   'attention_check_4',
                   'attention_check_5']

    @staticmethod
    def is_displayed(player: Player):
        if (
                player.round_number == 1
                and player.failed_attention_check == False
        ):
            return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if (
                player.attention_check_1 == Constants.num_rounds
                and player.attention_check_2 == Constants.num_rounds
                and player.attention_check_3 == Constants.num_rounds
                and player.attention_check_4 == Constants.num_rounds
                and player.attention_check_5 == Constants.num_rounds
        ):
            player.failed_attention_check = False
        else:
            player.failed_attention_check = True
            player.attention_check_tries = player.attention_check_tries + 1


class FailedAttentionCheck(Page):
    form_model = 'player'
    form_fields = ['begintrial_time',
                   'attention_check_1',
                   'attention_check_2',
                   'attention_check_3',
                   'attention_check_4',
                   'attention_check_5']

    @staticmethod
    def is_displayed(player: Player):
        if (
                player.failed_attention_check == True
        ):
            return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if (
                player.attention_check_1 == Constants.num_rounds
                and player.attention_check_2 == Constants.num_rounds
                and player.attention_check_3 == Constants.num_rounds
                and player.attention_check_4 == Constants.num_rounds
                and player.attention_check_5 == Constants.num_rounds
        ):
            player.failed_second_attention_check = False
        else:
            player.failed_second_attention_check = True
            player.attention_check_tries = player.attention_check_tries + 1

    @staticmethod
    def error_message(player: Player, values):
        if (
                player.attention_check_1 != Constants.num_rounds
                or player.attention_check_2 != Constants.num_rounds
                or player.attention_check_3 != Constants.num_rounds
                or player.attention_check_4 != Constants.num_rounds
                or player.attention_check_5 != Constants.num_rounds
        ):
            incorrect_answers = np.array([ values['attention_check_1'] != Constants.num_rounds,
                                values['attention_check_2'] != Constants.num_rounds,
                                values['attention_check_3'] != Constants.num_rounds,
                                values['attention_check_4'] != Constants.num_rounds,
                                values['attention_check_5'] != Constants.num_rounds,
                                ], dtype=bool)
            # incorrect_answers.np.astype(int)
            questions  = ' and '.join(np.array(['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])[incorrect_answers])
            return 'Your answers to the following questions are still incorrect: ' + questions


class Task_Round_1(Page):
    form_model = 'player'
    form_fields = ['endround_time', 'first_indivestim', 'indivarg', 'second_indivestim']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_displayed == 1

    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        players = group.get_players()
        if data["information_type"] == "estimate":
            if player.id_in_group == 1:
                player.first_indivestim = data["estimate"]
                Subsession.estimate_a = player.first_indivestim
                Subsession.num_estims = Subsession.num_estims + 1
                # player.indivarg = data["indivarg"]
            elif player.id_in_group == 2:
                player.first_indivestim = data["estimate"]
                Subsession.estimate_b = player.first_indivestim
                Subsession.num_estims = Subsession.num_estims + 1
                # player.indivarg = data["indivarg"]
            elif player.id_in_group == 3:
                player.first_indivestim = data["estimate"]
                Subsession.estimate_c = player.first_indivestim
                Subsession.num_estims = Subsession.num_estims + 1
                # player.indivarg = data["indivarg"]
            elif player.id_in_group == 4:
                player.first_indivestim = data["estimate"]
                Subsession.estimate_d = player.first_indivestim
                Subsession.num_estims = Subsession.num_estims + 1
                # player.indivarg = data["indivarg"]

        if Subsession.num_estims == 4:
            return {0: {"information_type": "estimate_a", "estimate_a": Subsession.estimate_a},
            }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        Subsession.num_estims = 0


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


page_sequence = [#Welcome, TaskIntro, FailedAttentionCheck,
                 Task_Round_1, Task_Round_2,
                 Results]
