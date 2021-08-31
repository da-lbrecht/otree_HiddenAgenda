from otree.api import *
import random
import numpy as np

doc = """
Your app description
"""

# Temporarily stored variables during Delphi process
num_estims = 0
estimate_a = 999
estimate_b = 999
estimate_c = 999
estimate_d = 999
indivarg_a = "none"
indivarg_b = "none"
indivarg_c = "none"
indivarg_d = "none"


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

    end_of_trial = models.StringField(initial=999,
                                      doc="Time at which the trial round was completed")
    start_of_round = models.StringField(initial=999,
                                        doc="Starting time of an estimation round")
    end_of_round = models.StringField(initial=999,
                                      doc="Time at which an estimation round is completed")

    round_displayed = models.IntegerField(doc="Position in which estimation task was displayed, ranging from 1 to "
                                              "num_rounds")

    # Response variables for attention checks
    attention_check_1 = models.FloatField(initial=999,
                                          label="Q1: How many rounds of the task will you play after the trial round?",
                                            doc="Attention check: How many rounds of the task will you play after the "
                                                "trial round?")
    attention_check_2 = models.FloatField(initial=999,
                                          label="Q2: Which rounds will contribute to your personal payoff?",
                                            doc="Attention check: Which rounds will contribute to your personal payoff?"
                                                )
    attention_check_3 = models.FloatField(initial=999,
                                          label="Q3: What inputs do you need to provide in each round?",
                                            doc="Attention check: What inputs do you need to provide in each round?")
    attention_check_4 = models.FloatField(initial=999,
                                          label="Q4: What kind of feedback do you receive in each round?",
                                            doc="Attention check: What kind of feedback do you receive in each round?")
    attention_check_5 = models.FloatField(initial=999,
                                          label="Q5: What don't you know about Kara?",
                                            doc="Attention check: What don't you know about Kara?")

    failed_attention_check = models.BooleanField(initial=False,
                                                 doc="True if attention check has not been passed at first attempt")

    attention_check_tries = models.IntegerField(initial=1,
                                                doc="Number of attempts needed to pass attention check questions")

    # Response variables for estimation
    first_indivestim = models.FloatField(label="My first estimate:",
                                         doc="First individual estimate given in Delphi procedure",
                                         min=0, max=100)
    indivarg = models.StringField(label="My reasoning behind my first estimate",
                                   doc="Reasoning given for first individual estimate given in Delphi procedure")
    second_indivestim = models.FloatField(label="My second estimate:",
                                          doc="Second individual estimate given in Delphi procedure",
                                          min=0, max=100)


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
    form_fields = ['begintrial_time']

    @staticmethod
    def is_displayed(player: Player):
        if (
                player.round_number == 1
                and player.failed_attention_check == False
        ):
            return True

    @staticmethod
    def live_method(player: Player, data):
        if (
            data["information_type"] == "answer" and
            player.attention_check_tries == 1
        ):
            player.attention_check_1 = data["answer_q1"]
            player.attention_check_2 = data["answer_q2"]
            player.attention_check_3 = data["answer_q3"]
            player.attention_check_4 = data["answer_q4"]
            player.attention_check_5 = data["answer_q5"]

        if (
                data["answer_q1"] == Constants.num_rounds and
                data["answer_q2"] == Constants.num_rounds and
                data["answer_q3"] == Constants.num_rounds and
                data["answer_q4"] == Constants.num_rounds and
                data["answer_q5"] == Constants.num_rounds
        ):
            return{
                player.id_in_group: {"information_type": "no_error", "no_error": "Yeah!"},
            }
        else:
            player.failed_attention_check = True
            player.attention_check_tries = player.attention_check_tries + 1
            incorrect_answers = np.array([
                                data["answer_q1"] != Constants.num_rounds,
                                data["answer_q2"] != Constants.num_rounds,
                                data["answer_q3"] != Constants.num_rounds,
                                data["answer_q4"] != Constants.num_rounds,
                                data["answer_q5"] != Constants.num_rounds,
                                ], dtype=bool)
            # incorrect_answers.np.astype(int)
            questions = ' and '.join(np.array(['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])[incorrect_answers])
            return{
                player.id_in_group: {"information_type": "error", "error": questions},
            }


class Task_Trial(Page):
    form_model = 'player'
    form_fields = ['end_of_trial']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_displayed == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"round_number": player.round_number}

    @staticmethod
    def live_method(player: Player, data):
        global estimate_a, estimate_b, estimate_c, estimate_d, indivarg_a, indivarg_b, indivarg_c, indivarg_d,\
            num_estims
        group = player.group
        players = group.get_players()
        if data["information_type"] == "estimate":
            if 0 <= data["estimate"] <= 100:
                player.first_indivestim = data["estimate"]
                num_estims += 1
                if player.id_in_group == 1:
                    estimate_a = data["estimate"]
                elif player.id_in_group == 2:
                    estimate_b = data["estimate"]
                elif player.id_in_group == 3:
                    estimate_c = data["estimate"]
                elif player.id_in_group == 4:
                    estimate_d = data["estimate"]
            else:
                return{
                    player.id_in_group: {"information_type": "error_1",
                                         "error": "estimate out of range"},
                }
        if data["information_type"] == "reasoning":
            player.indivarg = data["reasoning"]
            if player.id_in_group == 1:
                indivarg_a = data["reasoning"]
            elif player.id_in_group == 2:
                indivarg_b = data["reasoning"]
            elif player.id_in_group == 3:
                indivarg_c = data["reasoning"]
            elif player.id_in_group == 4:
                indivarg_d = data["reasoning"]
        if num_estims >= 4 and data["information_type"] != "second_estimate":
            return {
                1: {"player.id_in_group": "a",
                    "estimate_a": estimate_a,
                    "estimate_b": estimate_b,
                    "estimate_c": estimate_c,
                    "estimate_d": estimate_d,
                    "reasoning_a": indivarg_a,
                    "reasoning_b": indivarg_b,
                    "reasoning_c": indivarg_c,
                    "reasoning_d": indivarg_d},
                2: {"player.id_in_group": "b",
                    "estimate_a": estimate_a,
                    "estimate_b": estimate_b,
                    "estimate_c": estimate_c,
                    "estimate_d": estimate_d,
                    "reasoning_a": indivarg_a,
                    "reasoning_b": indivarg_b,
                    "reasoning_c": indivarg_c,
                    "reasoning_d": indivarg_d},
                3: {"player.id_in_group": "c",
                    "estimate_a": estimate_a,
                    "estimate_b": estimate_b,
                    "estimate_c": estimate_c,
                    "estimate_d": estimate_d,
                    "reasoning_a": indivarg_a,
                    "reasoning_b": indivarg_b,
                    "reasoning_c": indivarg_c,
                    "reasoning_d": indivarg_d},
                4: {"player.id_in_group": "d",
                    "estimate_a": estimate_a,
                    "estimate_b": estimate_b,
                    "estimate_c": estimate_c,
                    "estimate_d": estimate_d,
                    "reasoning_a": indivarg_a,
                    "reasoning_b": indivarg_b,
                    "reasoning_c": indivarg_c,
                    "reasoning_d": indivarg_d},
            }
        if data["information_type"] == "second_estimate":
            if 0 <= data["second_estimate"] <= 100:
                player.second_indivestim = data["second_estimate"]
                return{
                    player.id_in_group: {"information_type": "completion_indicator"},
                }
            else:
                return{
                    player.id_in_group: {"information_type": "error_2",
                                         "error": "estimate out of range"},
                }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        global num_estims
        num_estims = 0
        if player.round_number == 1:
            pass
        else:
            player.start_of_round = player.in_round(player.round_number-1).end_of_round

class Task_Round_1(Page):
    form_model = 'player'
    form_fields = ['end_of_round']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_displayed == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"round_number": player.round_number}

    @staticmethod
    def live_method(player: Player, data):
        global estimate_a, estimate_b, estimate_c, estimate_d, indivarg_a, indivarg_b, indivarg_c, indivarg_d,\
            num_estims
        group = player.group
        players = group.get_players()
        if data["information_type"] == "estimate":
            if 0 <= data["estimate"] <= 100:
                player.first_indivestim = data["estimate"]
                num_estims += 1
                if player.id_in_group == 1:
                    estimate_a = data["estimate"]
                elif player.id_in_group == 2:
                    estimate_b = data["estimate"]
                elif player.id_in_group == 3:
                    estimate_c = data["estimate"]
                elif player.id_in_group == 4:
                    estimate_d = data["estimate"]
            else:
                return{
                    player.id_in_group: {"information_type": "error_1",
                                         "error": "estimate out of range"},
                }
        if data["information_type"] == "reasoning":
            player.indivarg = data["reasoning"]
            if player.id_in_group == 1:
                indivarg_a = data["reasoning"]
            elif player.id_in_group == 2:
                indivarg_b = data["reasoning"]
            elif player.id_in_group == 3:
                indivarg_c = data["reasoning"]
            elif player.id_in_group == 4:
                indivarg_d = data["reasoning"]
        if num_estims >= 4 and data["information_type"] != "second_estimate":
            return {
                1: {"player.id_in_group": "a",
                    "estimate_a": estimate_a,
                    "estimate_b": estimate_b,
                    "estimate_c": estimate_c,
                    "estimate_d": estimate_d,
                    "reasoning_a": indivarg_a,
                    "reasoning_b": indivarg_b,
                    "reasoning_c": indivarg_c,
                    "reasoning_d": indivarg_d},
                2: {"player.id_in_group": "b",
                    "estimate_a": estimate_a,
                    "estimate_b": estimate_b,
                    "estimate_c": estimate_c,
                    "estimate_d": estimate_d,
                    "reasoning_a": indivarg_a,
                    "reasoning_b": indivarg_b,
                    "reasoning_c": indivarg_c,
                    "reasoning_d": indivarg_d},
                3: {"player.id_in_group": "c",
                    "estimate_a": estimate_a,
                    "estimate_b": estimate_b,
                    "estimate_c": estimate_c,
                    "estimate_d": estimate_d,
                    "reasoning_a": indivarg_a,
                    "reasoning_b": indivarg_b,
                    "reasoning_c": indivarg_c,
                    "reasoning_d": indivarg_d},
                4: {"player.id_in_group": "d",
                    "estimate_a": estimate_a,
                    "estimate_b": estimate_b,
                    "estimate_c": estimate_c,
                    "estimate_d": estimate_d,
                    "reasoning_a": indivarg_a,
                    "reasoning_b": indivarg_b,
                    "reasoning_c": indivarg_c,
                    "reasoning_d": indivarg_d},
            }
        if data["information_type"] == "second_estimate":
            if 0 <= data["second_estimate"] <= 100:
                player.second_indivestim = data["second_estimate"]
                return{
                    player.id_in_group: {"information_type": "completion_indicator"},
                }
            else:
                return{
                    player.id_in_group: {"information_type": "error_2",
                                         "error": "estimate out of range"},
                }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        global num_estims
        num_estims = 0
        if player.round_number == 1:
            player.start_of_round = player.end_of_trial
        else:
            player.start_of_round = player.in_round(player.round_number-1).end_of_round


class Task_Round_2(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_displayed == 2

    @staticmethod
    def vars_for_template(player: Player):
        return {"round_number": player.round_number}

    @staticmethod
    def live_method(player: Player, data):
        global estimate_a, estimate_b, estimate_c, estimate_d, indivarg_a, indivarg_b, indivarg_c, indivarg_d, \
            num_estims
        group = player.group
        players = group.get_players()
        if data["information_type"] == "estimate":
            if 0 <= data["estimate"] <= 100:
                player.first_indivestim = data["estimate"]
                num_estims += 1
                if player.id_in_group == 1:
                    estimate_a = data["estimate"]
                elif player.id_in_group == 2:
                    estimate_b = data["estimate"]
                elif player.id_in_group == 3:
                    estimate_c = data["estimate"]
                elif player.id_in_group == 4:
                    estimate_d = data["estimate"]
            else:
                return {
                    player.id_in_group: {"information_type": "error_1",
                                         "error": "estimate out of range"},
                }
        if data["information_type"] == "reasoning":
            player.indivarg = data["reasoning"]
            if player.id_in_group == 1:
                indivarg_a = data["reasoning"]
            elif player.id_in_group == 2:
                indivarg_b = data["reasoning"]
            elif player.id_in_group == 3:
                indivarg_c = data["reasoning"]
            elif player.id_in_group == 4:
                indivarg_d = data["reasoning"]
        if num_estims >= 4 and data["information_type"] != "second_estimate":
            return {
                1: {"player.id_in_group": "a",
                    "estimate_a": estimate_a,
                    "estimate_b": estimate_b,
                    "estimate_c": estimate_c,
                    "estimate_d": estimate_d,
                    "reasoning_a": indivarg_a,
                    "reasoning_b": indivarg_b,
                    "reasoning_c": indivarg_c,
                    "reasoning_d": indivarg_d},
                2: {"player.id_in_group": "b",
                    "estimate_a": estimate_a,
                    "estimate_b": estimate_b,
                    "estimate_c": estimate_c,
                    "estimate_d": estimate_d,
                    "reasoning_a": indivarg_a,
                    "reasoning_b": indivarg_b,
                    "reasoning_c": indivarg_c,
                    "reasoning_d": indivarg_d},
                3: {"player.id_in_group": "c",
                    "estimate_a": estimate_a,
                    "estimate_b": estimate_b,
                    "estimate_c": estimate_c,
                    "estimate_d": estimate_d,
                    "reasoning_a": indivarg_a,
                    "reasoning_b": indivarg_b,
                    "reasoning_c": indivarg_c,
                    "reasoning_d": indivarg_d},
                4: {"player.id_in_group": "d",
                    "estimate_a": estimate_a,
                    "estimate_b": estimate_b,
                    "estimate_c": estimate_c,
                    "estimate_d": estimate_d,
                    "reasoning_a": indivarg_a,
                    "reasoning_b": indivarg_b,
                    "reasoning_c": indivarg_c,
                    "reasoning_d": indivarg_d},
            }
        if data["information_type"] == "second_estimate":
            if 0 <= data["second_estimate"] <= 100:
                player.second_indivestim = data["second_estimate"]
                return {
                    player.id_in_group: {"information_type": "completion_indicator"},
                }
            else:
                return {
                    player.id_in_group: {"information_type": "error_2",
                                         "error": "estimate out of range"},
                }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        global num_estims
        num_estims = 0


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    @staticmethod
    def is_displayed(subsession: Subsession):
        return subsession.round_number == Constants.num_rounds


page_sequence = [Welcome, TaskIntro,
                 Task_Trial,
                 Task_Round_1, Task_Round_2,
                 Results]