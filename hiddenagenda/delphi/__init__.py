from otree.api import *
import numpy as np
import random

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
second_estimate_a = 999
second_estimate_b = 999
second_estimate_c = 999
second_estimate_d = 999
aggregate_estimate = 999
group_accuracy_bonus = 999
random_number = 999
feedback_order = 999


class Constants(BaseConstants):
    name_in_url = 'delphi'
    players_per_group = None
    num_rounds = 10

    fixed_pay = 5
    avg_pay = 12

    num_attention_checks = 5

    # Results of payoff relevant execution of Kara's program; 0=did not reach target area
    round_1_result = 0  # 0.1
    round_2_result = 0  # 0.2
    round_3_result = 0  # 0.3
    round_4_result = 0  # 0.4
    round_5_result = 0  # 0.45
    round_6_result = 1  # 0.55
    round_7_result = 0  # 0.6
    round_8_result = 1  # 0.7
    round_9_result = 0  # 0.8
    round_10_result = 1  # 0.9


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Payoff variables
    random_number = models.FloatField(initial=999,
                                      doc="Random number drawn for calculation of binarized scoring rule bonus")
    group_accuracy_bonus = models.CurrencyField(initial=999,
                                                doc="Bonus earned based on the accuracy of the group estimates")
    hidden_agenda_bonus = models.CurrencyField(initial=999,
                                               doc="Bonus earned based on the individual hidden agenda")

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
                                          label="Q1: How many rounds of the task will you need to solve after the trial"
                                                " round?",
                                            doc="Attention check: How many rounds of the task will you need to solve "
                                                "after the trial round? (integer)")
    attention_check_2 = models.FloatField(initial=999,
                                          label="Q2: Which rounds will contribute to your personal payoff?",
                                            doc="Attention check: Which rounds will contribute to your personal payoff?"
                                                " (1: One randomly selected round; 2: Only the last round; 3: All rounds"
                                                " after the trial round)"
                                                )
    attention_check_3 = models.FloatField(initial=999,
                                          label="Q3: What kind of inputs do you need to provide in each round?",
                                            doc="Attention check: What kind of inputs do you need to provide in each "
                                                "round? (1: Two numerical estimates and a corresponding reasoning"
                                                " for the first of them; 2: Two numerical estimates and two "
                                                " corresponding reasonings; 3: One estimate and a corresponding"
                                                " reasoning")
    attention_check_4 = models.FloatField(initial=999,
                                          label="Q4: What kind of feedback do you receive in each round?",
                                            doc="Attention check: What kind of feedback do you receive in each round?"
                                                " (1: First estimates and corresponding reasoning of all group members,"
                                                " without knowing which belongs to whom; 2: All estimates and "
                                                "corresponding reasonings made by the other group members; 3: Only the "
                                                "reasoning of all group members, without knowing which belongs to whom")
    attention_check_5 = models.FloatField(initial=999,
                                          label="Q5: What don't you know about Kara?",
                                            doc="Attention check: What don't you know about Kara? "
                                                "(1: How many steps she will make in a given round, "
                                                "2: Whether the chance that she moves one level up is the same each step"
                                                " in a given round, "
                                                "3: The chance that she moves one level up in the first step")

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

    # Aggregated estimates
    aggregate_estimate = models.FloatField(doc="Group estimate, derived by unweighted averaging of second individual "
                                               "estimates",
                                           min=0, max=100)

    # Randomization Variables
    feedback_order = models.IntegerField(doc="Order in which feedback of fellow group members, except oneself is "
                                                    "seen (1: 1,2,3; 2: 1,3,2; 3: 2,1,3; 4: 2,3,1; 5:3,1,2; 6:3,2,1")


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
                data["answer_q2"] == 3 and
                data["answer_q3"] == 1 and
                data["answer_q4"] == 1 and
                data["answer_q5"] == 3
        ):
            return{
                player.id_in_group: {"information_type": "no_error", "no_error": "Yeah!"},
            }
        else:
            player.failed_attention_check = True
            player.attention_check_tries = player.attention_check_tries + 1
            incorrect_answers = np.array([
                                data["answer_q1"] != Constants.num_rounds,
                                data["answer_q2"] != 3,
                                data["answer_q3"] != 1,
                                data["answer_q4"] != 1,
                                data["answer_q5"] != 3,
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
            if (
                    type(data["estimate"]) == float
                    or type(data["estimate"]) == int
                    and 0 <= data["estimate"] <= 100
            ):
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
        if (
            estimate_a != 999
            and estimate_b != 999
            and estimate_c != 999
            and estimate_d != 999
            and data["information_type"] != "second_estimate"
        ):
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
            if (
                    type(data["second_estimate"]) == float
                    or type(data["second_estimate"]) == int
                    and 0 <= data["second_estimate"] <= 100
            ):
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
        global num_estims, estimate_a, estimate_b, estimate_c, estimate_d, second_estimate_a, second_estimate_b,\
            second_estimate_c, second_estimate_d

        num_estims = 0
        estimate_a = 999
        estimate_b = 999
        estimate_c = 999
        estimate_d = 999
        second_estimate_a = 999
        second_estimate_b = 999
        second_estimate_c = 999
        second_estimate_d = 999

        if player.round_number == 1:
            pass
        else:
            player.start_of_round = player.in_round(player.round_number-1).end_of_round

class Task(Page):
    form_model = 'player'
    form_fields = ['end_of_round']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_displayed <= 10


    @staticmethod
    def live_method(player: Player, data):
        global estimate_a, estimate_b, estimate_c, estimate_d, second_estimate_a, second_estimate_b, second_estimate_c,\
            second_estimate_d, indivarg_a, indivarg_b, indivarg_c, indivarg_d,num_estims, aggregate_estimate, \
            group_accuracy_bonus, random_number, feedback_order
        group = player.group
        players = group.get_players()
        if data["information_type"] == "estimate":
            if (
                    type(data["estimate"]) == float
                    or type(data["estimate"]) == int
                    and 0 <= data["estimate"] <= 100
            ):
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
        if (
            estimate_a != 999
            and estimate_b != 999
            and estimate_c != 999
            and estimate_d != 999
            and data["information_type"] != "second_estimate"
        ):
            feedback_order = round((random.uniform(0, 1)*5+0.5), 0)
            if feedback_order == 1:
                return {
                    1: {"player.id_in_group": "a",  # presented order of fellow group members' input: 2, 3, 4
                        "estimate_a": estimate_a,
                        "estimate_b": estimate_b,
                        "estimate_c": estimate_c,
                        "estimate_d": estimate_d,
                        "reasoning_a": indivarg_a,
                        "reasoning_b": indivarg_b,
                        "reasoning_c": indivarg_c,
                        "reasoning_d": indivarg_d},
                    2: {"player.id_in_group": "b",  # presented order of fellow group members' input: 1, 3, 4
                        "estimate_a": estimate_a,
                        "estimate_b": estimate_b,
                        "estimate_c": estimate_c,
                        "estimate_d": estimate_d,
                        "reasoning_a": indivarg_a,
                        "reasoning_b": indivarg_b,
                        "reasoning_c": indivarg_c,
                        "reasoning_d": indivarg_d},
                    3: {"player.id_in_group": "c",  # presented order of fellow group members' input: 1, 2, 4
                        "estimate_a": estimate_a,
                        "estimate_b": estimate_b,
                        "estimate_c": estimate_c,
                        "estimate_d": estimate_d,
                        "reasoning_a": indivarg_a,
                        "reasoning_b": indivarg_b,
                        "reasoning_c": indivarg_c,
                        "reasoning_d": indivarg_d},
                    4: {"player.id_in_group": "d",  # presented order of fellow group members' input: 1, 2, 3
                        "estimate_a": estimate_a,
                        "estimate_b": estimate_b,
                        "estimate_c": estimate_c,
                        "estimate_d": estimate_d,
                        "reasoning_a": indivarg_a,
                        "reasoning_b": indivarg_b,
                        "reasoning_c": indivarg_c,
                        "reasoning_d": indivarg_d},
                }
            elif feedback_order == 2:
                return {
                    1: {"player.id_in_group": "a",  # presented order of fellow group members' input: 2, 4, 3 (b, d, c)
                        "estimate_a": estimate_a,
                        "estimate_b": estimate_b,
                        "estimate_c": estimate_d,
                        "estimate_d": estimate_c,
                        "reasoning_a": indivarg_a,
                        "reasoning_b": indivarg_d,
                        "reasoning_c": indivarg_b,
                        "reasoning_d": indivarg_c},
                    2: {"player.id_in_group": "b",  # presented order of fellow group members' input: 1, 4, 3 (a, d, c)
                        "estimate_a": estimate_a,
                        "estimate_b": estimate_b,
                        "estimate_c": estimate_d,
                        "estimate_d": estimate_c,
                        "reasoning_a": indivarg_a,
                        "reasoning_b": indivarg_b,
                        "reasoning_c": indivarg_d,
                        "reasoning_d": indivarg_c},
                    3: {"player.id_in_group": "c",  # presented order of fellow group members' input: 1, 4, 2 (a, d, b)
                        "estimate_a": estimate_a,
                        "estimate_b": estimate_d,
                        "estimate_c": estimate_c,
                        "estimate_d": estimate_b,
                        "reasoning_a": indivarg_a,
                        "reasoning_b": indivarg_d,
                        "reasoning_c": indivarg_c,
                        "reasoning_d": indivarg_b},
                    4: {"player.id_in_group": "d",  # presented order of fellow group members' input: 1, 3, 2 (a, c, b)
                        "estimate_a": estimate_a,
                        "estimate_b": estimate_c,
                        "estimate_c": estimate_b,
                        "estimate_d": estimate_d,
                        "reasoning_a": indivarg_a,
                        "reasoning_b": indivarg_c,
                        "reasoning_c": indivarg_b,
                        "reasoning_d": indivarg_d},
                }
            elif feedback_order == 3:
                return {
                    1: {"player.id_in_group": "a",  # presented order of fellow group members' input: 3, 2, 4 (c, b, d)
                        "estimate_a": estimate_a,
                        "estimate_b": estimate_c,
                        "estimate_c": estimate_b,
                        "estimate_d": estimate_d,
                        "reasoning_a": indivarg_a,
                        "reasoning_b": indivarg_c,
                        "reasoning_c": indivarg_b,
                        "reasoning_d": indivarg_d},
                    2: {"player.id_in_group": "b",  # presented order of fellow group members' input: 3, 1, 4 (c, a, d)
                        "estimate_a": estimate_c,
                        "estimate_b": estimate_b,
                        "estimate_c": estimate_a,
                        "estimate_d": estimate_d,
                        "reasoning_a": indivarg_c,
                        "reasoning_b": indivarg_b,
                        "reasoning_c": indivarg_a,
                        "reasoning_d": indivarg_d},
                    3: {"player.id_in_group": "c",  # presented order of fellow group members' input: 2, 1, 4 (b, a, d)
                        "estimate_a": estimate_b,
                        "estimate_b": estimate_a,
                        "estimate_c": estimate_c,
                        "estimate_d": estimate_d,
                        "reasoning_a": indivarg_b,
                        "reasoning_b": indivarg_a,
                        "reasoning_c": indivarg_c,
                        "reasoning_d": indivarg_d},
                    4: {"player.id_in_group": "d",  # presented order of fellow group members' input: 2, 1, 3 (b, a, c)
                        "estimate_a": estimate_b,
                        "estimate_b": estimate_a,
                        "estimate_c": estimate_c,
                        "estimate_d": estimate_d,
                        "reasoning_a": indivarg_b,
                        "reasoning_b": indivarg_a,
                        "reasoning_c": indivarg_c,
                        "reasoning_d": indivarg_d},
                }
            elif feedback_order == 4:
                return {
                    1: {"player.id_in_group": "a",  # presented order of fellow group members' input: 3, 4, 2 (c, d, b)
                        "estimate_a": estimate_a,
                        "estimate_b": estimate_c,
                        "estimate_c": estimate_d,
                        "estimate_d": estimate_b,
                        "reasoning_a": indivarg_a,
                        "reasoning_b": indivarg_c,
                        "reasoning_c": indivarg_d,
                        "reasoning_d": indivarg_b},
                    2: {"player.id_in_group": "b",  # presented order of fellow group members' input: 3, 4, 1 (c, d, a)
                        "estimate_a": estimate_c,
                        "estimate_b": estimate_b,
                        "estimate_c": estimate_d,
                        "estimate_d": estimate_a,
                        "reasoning_a": indivarg_c,
                        "reasoning_b": indivarg_b,
                        "reasoning_c": indivarg_d,
                        "reasoning_d": indivarg_a},
                    3: {"player.id_in_group": "c",  # presented order of fellow group members' input: 2, 4, 1 (b, d, a)
                        "estimate_a": estimate_b,
                        "estimate_b": estimate_d,
                        "estimate_c": estimate_c,
                        "estimate_d": estimate_a,
                        "reasoning_a": indivarg_b,
                        "reasoning_b": indivarg_d,
                        "reasoning_c": indivarg_c,
                        "reasoning_d": indivarg_a},
                    4: {"player.id_in_group": "d",  # presented order of fellow group members' input: 2, 3, 1 (b, c, a)
                        "estimate_a": estimate_b,
                        "estimate_b": estimate_c,
                        "estimate_c": estimate_a,
                        "estimate_d": estimate_d,
                        "reasoning_a": indivarg_b,
                        "reasoning_b": indivarg_c,
                        "reasoning_c": indivarg_a,
                        "reasoning_d": indivarg_d},
                }
            elif feedback_order == 5:
                return {
                    1: {"player.id_in_group": "a",  # presented order of fellow group members' input: 4, 2, 3 (d, b, c)
                        "estimate_a": estimate_a,
                        "estimate_b": estimate_d,
                        "estimate_c": estimate_b,
                        "estimate_d": estimate_c,
                        "reasoning_a": indivarg_a,
                        "reasoning_b": indivarg_d,
                        "reasoning_c": indivarg_b,
                        "reasoning_d": indivarg_c},
                    2: {"player.id_in_group": "b",  # presented order of fellow group members' input: 4, 1, 3 (d, a, c)
                        "estimate_a": estimate_d,
                        "estimate_b": estimate_b,
                        "estimate_c": estimate_a,
                        "estimate_d": estimate_c,
                        "reasoning_a": indivarg_d,
                        "reasoning_b": indivarg_b,
                        "reasoning_c": indivarg_a,
                        "reasoning_d": indivarg_c},
                    3: {"player.id_in_group": "c",  # presented order of fellow group members' input: 4, 1, 2 (d, a, b)
                        "estimate_a": estimate_d,
                        "estimate_b": estimate_a,
                        "estimate_c": estimate_c,
                        "estimate_d": estimate_b,
                        "reasoning_a": indivarg_d,
                        "reasoning_b": indivarg_a,
                        "reasoning_c": indivarg_c,
                        "reasoning_d": indivarg_b},
                    4: {"player.id_in_group": "d",  # presented order of fellow group members' input: 3, 1, 2 (c, a, b)
                        "estimate_a": estimate_c,
                        "estimate_b": estimate_a,
                        "estimate_c": estimate_b,
                        "estimate_d": estimate_d,
                        "reasoning_a": indivarg_c,
                        "reasoning_b": indivarg_a,
                        "reasoning_c": indivarg_b,
                        "reasoning_d": indivarg_d},
                }
            elif feedback_order == 6:
                return {
                    1: {"player.id_in_group": "a",  # presented order of fellow group members' input: 4, 3, 2 (d, c, b)
                        "estimate_a": estimate_a,
                        "estimate_b": estimate_d,
                        "estimate_c": estimate_c,
                        "estimate_d": estimate_b,
                        "reasoning_a": indivarg_a,
                        "reasoning_b": indivarg_d,
                        "reasoning_c": indivarg_c,
                        "reasoning_d": indivarg_b},
                    2: {"player.id_in_group": "b",  # presented order of fellow group members' input: 4, 3, 1 (d, c, a)
                        "estimate_a": estimate_d,
                        "estimate_b": estimate_b,
                        "estimate_c": estimate_c,
                        "estimate_d": estimate_a,
                        "reasoning_a": indivarg_d,
                        "reasoning_b": indivarg_b,
                        "reasoning_c": indivarg_c,
                        "reasoning_d": indivarg_a},
                    3: {"player.id_in_group": "c",  # presented order of fellow group members' input: 4, 2, 1 (d, b, a)
                        "estimate_a": estimate_d,
                        "estimate_b": estimate_b,
                        "estimate_c": estimate_c,
                        "estimate_d": estimate_a,
                        "reasoning_a": indivarg_d,
                        "reasoning_b": indivarg_b,
                        "reasoning_c": indivarg_c,
                        "reasoning_d": indivarg_a},
                    4: {"player.id_in_group": "d",  # presented order of fellow group members' input: 3, 2, 1 (c, b, a)
                        "estimate_a": estimate_c,
                        "estimate_b": estimate_b,
                        "estimate_c": estimate_a,
                        "estimate_d": estimate_d,
                        "reasoning_a": indivarg_c,
                        "reasoning_b": indivarg_b,
                        "reasoning_c": indivarg_a,
                        "reasoning_d": indivarg_d},
                }
        if data["information_type"] == "second_estimate":
            if (
                    type(data["second_estimate"]) == float
                    or type(data["second_estimate"]) == int
                    and 0 <= data["second_estimate"] <= 100
            ):
                player.second_indivestim = data["second_estimate"]
                if player.id_in_group == 1:
                    second_estimate_a = data["second_estimate"]
                elif player.id_in_group == 2:
                    second_estimate_b = data["second_estimate"]
                elif player.id_in_group == 3:
                    second_estimate_c = data["second_estimate"]
                elif player.id_in_group == 4:
                    second_estimate_d = data["second_estimate"]
                if (
                    second_estimate_a != 999
                    and second_estimate_b != 999
                    and second_estimate_c != 999
                    and second_estimate_d != 999
                ):
                    aggregate_estimate = (second_estimate_a+second_estimate_b+second_estimate_c+second_estimate_d)/4
                    random_number = random.uniform(0, 1)
                    if Constants.round_1_result == 1:
                        if random_number > pow((1 - (aggregate_estimate/100)), 2):
                            group_accuracy_bonus = 4
                        elif random_number <= pow((1 - (aggregate_estimate/100)), 2):
                            group_accuracy_bonus = 0
                    elif Constants.round_1_result == 0:
                        if random_number > pow((aggregate_estimate/100), 2):
                            group_accuracy_bonus = 4
                        elif random_number <= pow((aggregate_estimate/100), 2):
                            group_accuracy_bonus = 0
                    estimate_a = 999
                    estimate_b = 999
                    estimate_c = 999
                    estimate_d = 999
                    second_estimate_a = 999
                    second_estimate_b = 999
                    second_estimate_c = 999
                    second_estimate_d = 999
                    return {
                        0: {"information_type": "completion_indicator"},
                    }
                else:
                    return{
                        player.id_in_group: {"information_type": "wait_indicator"},
                    }
            else:
                return{
                    player.id_in_group: {"information_type": "error_2",
                                         "error": "estimate out of range"},
                }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        global num_estims, estimate_a, estimate_b, estimate_c, estimate_d, second_estimate_a, second_estimate_b, \
            second_estimate_c, second_estimate_d

        player.random_number = random_number
        player.aggregate_estimate = aggregate_estimate
        player.group_accuracy_bonus = group_accuracy_bonus*0.25
        player.payoff += group_accuracy_bonus*0.25
        player.feedback_order = feedback_order

        if player.round_number == 1:
            player.start_of_round = player.end_of_trial
        else:
            player.start_of_round = player.in_round(player.round_number-1).end_of_round

#
# class Task_Round_2(Page):
#     form_model = 'player'
#
#     @staticmethod
#     def is_displayed(player: Player):
#         return player.round_displayed == 2
#
#     @staticmethod
#     def vars_for_template(player: Player):
#         return {"round_number": player.round_number}
#
#     @staticmethod
#     def live_method(player: Player, data):
#         global estimate_a, estimate_b, estimate_c, estimate_d, indivarg_a, indivarg_b, indivarg_c, indivarg_d, \
#             num_estims, feedback_order
#         group = player.group
#         players = group.get_players()
#         if data["information_type"] == "estimate":
#             if (
#                     type(data["estimate"]) == float
#                     or type(data["estimate"]) == int
#                     and 0 <= data["estimate"] <= 100
#             ):
#                 player.first_indivestim = data["estimate"]
#                 num_estims += 1
#                 if player.id_in_group == 1:
#                     estimate_a = data["estimate"]
#                 elif player.id_in_group == 2:
#                     estimate_b = data["estimate"]
#                 elif player.id_in_group == 3:
#                     estimate_c = data["estimate"]
#                 elif player.id_in_group == 4:
#                     estimate_d = data["estimate"]
#             else:
#                 return {
#                     player.id_in_group: {"information_type": "error_1",
#                                          "error": "estimate out of range"},
#                 }
#         if data["information_type"] == "reasoning":
#             player.indivarg = data["reasoning"]
#             if player.id_in_group == 1:
#                 indivarg_a = data["reasoning"]
#             elif player.id_in_group == 2:
#                 indivarg_b = data["reasoning"]
#             elif player.id_in_group == 3:
#                 indivarg_c = data["reasoning"]
#             elif player.id_in_group == 4:
#                 indivarg_d = data["reasoning"]
#         if num_estims >= 4 and data["information_type"] != "second_estimate":
#             feedback_order = np.round(np.random.random_sample() * 6, decimals=0) + 1
#             return {
#                 1: {"player.id_in_group": "a",
#                     "estimate_a": estimate_a,
#                     "estimate_b": estimate_b,
#                     "estimate_c": estimate_c,
#                     "estimate_d": estimate_d,
#                     "reasoning_a": indivarg_a,
#                     "reasoning_b": indivarg_b,
#                     "reasoning_c": indivarg_c,
#                     "reasoning_d": indivarg_d},
#                 2: {"player.id_in_group": "b",
#                     "estimate_a": estimate_a,
#                     "estimate_b": estimate_b,
#                     "estimate_c": estimate_c,
#                     "estimate_d": estimate_d,
#                     "reasoning_a": indivarg_a,
#                     "reasoning_b": indivarg_b,
#                     "reasoning_c": indivarg_c,
#                     "reasoning_d": indivarg_d},
#                 3: {"player.id_in_group": "c",
#                     "estimate_a": estimate_a,
#                     "estimate_b": estimate_b,
#                     "estimate_c": estimate_c,
#                     "estimate_d": estimate_d,
#                     "reasoning_a": indivarg_a,
#                     "reasoning_b": indivarg_b,
#                     "reasoning_c": indivarg_c,
#                     "reasoning_d": indivarg_d},
#                 4: {"player.id_in_group": "d",
#                     "estimate_a": estimate_a,
#                     "estimate_b": estimate_b,
#                     "estimate_c": estimate_c,
#                     "estimate_d": estimate_d,
#                     "reasoning_a": indivarg_a,
#                     "reasoning_b": indivarg_b,
#                     "reasoning_c": indivarg_c,
#                     "reasoning_d": indivarg_d},
#             }
#         if data["information_type"] == "second_estimate":
#             if (
#                     type(data["second_estimate"]) == float
#                     or type(data["second_estimate"]) == int
#                     and 0 <= data["second_estimate"] <= 100
#             ):
#                 player.second_indivestim = data["second_estimate"]
#                 return {
#                     player.id_in_group: {"information_type": "completion_indicator"},
#                 }
#             else:
#                 return {
#                     player.id_in_group: {"information_type": "error_2",
#                                          "error": "estimate out of range"},
#                 }
#
#     @staticmethod
#     def before_next_page(player: Player, timeout_happened):
#         global num_estims
#         num_estims = 0


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    @staticmethod
    def is_displayed(subsession: Subsession):
        return subsession.round_number == Constants.num_rounds


page_sequence = [ #Welcome, TaskIntro,
                 # Task_Trial,
                 Task,
                 Results]