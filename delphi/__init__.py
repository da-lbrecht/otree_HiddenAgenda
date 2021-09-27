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
result = 999


class Constants(BaseConstants):
    name_in_url = 'delphi'
    players_per_group = None
    num_rounds = 2

    fixed_pay = cu(5)
    avg_pay = 15
    group_bonus = cu(8)
    individual_share_of_group_bonus = cu(2)
    max_group_accuracy_bonus_per_round = cu(8)

    num_attention_checks = 5
    num_final_questions = 10

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
    group_accuracy_bonus = models.CurrencyField(initial=0,
                                                doc="Bonus earned based on the accuracy of the group estimates in one"
                                                    "particular round")
    hidden_agenda_bonus = models.CurrencyField(initial=0,
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
    feedback_order = models.FloatField(doc="Order in which feedback of fellow group members, except oneself is "
                                                    "seen (1: 1,2,3; 2: 1,3,2; 3: 2,1,3; 4: 2,3,1; 5:3,1,2; 6:3,2,1")

    # Response Variables for Questionnaire
    gender = models.IntegerField(label="<b>Which gender do you identify with?</b>",
                               choices=[
                                   [1, 'female'],
                                   [2, 'male'],
                                   [3, 'other'],
                               ],
                                doc = "Questionnaire: Which gender do you identify with? "
                                      "(1: female, "
                                      "2: male"
                                      "3: other"
                                )
    education = models.IntegerField(label="<b>If you think back to your time since starting primary school, how many"
                                          " years have you been following a formal education (school, vocational"
                                          " training, university,etc.) until today?</b>",
                                    min=0,
                                    max=100,
                                    doc="If you think back to your time since starting primary school, how many"
                                          " years have you been following a formal education (school, vocational"
                                          " training, university,etc.) until today?")
    field_of_studies = models.IntegerField(label="<b> What describes your current/most recent field of study"
                                                 " best?</b>",
                                            choices=[
                                                [1, 'Business and/or Economics'],
                                                [2, 'Social Sciences'],
                                                [3, 'Natural Sciences'],
                                                [4, 'Arts'],
                                                [5, 'Other'],
                                                [6, 'I did/do not follow any studies']
                                                ],
                                           doc="Questionnaire: What describes your current/most recent field of study "
                                               "best?, (1: Business and/or Economics; 2: Social Sciences; 3: Natural"
                                               "Sciences; 4: Arts; 5: Other; 6: I did/do not follow any studies)")

    years_of_working = models.IntegerField(label="<b> Do you have professional working experience? If so, for how long?"
                                                 "</b>",
                                            choices=[
                                                [0, 'No, I do not have professional working experience'],
                                                [6, 'less than 1 year'],
                                                [1, '1 year'],
                                                [2, '2 years'],
                                                [3, '3 years'],
                                                [4, '4 years'],
                                                [5, '5 years or more'],
                                                ],
                                           doc="Questionnaire: Do you have professional working experience? If so, for"
                                               " how long? (0: No I do not have professional working experience;"
                                               "1: 1 year; 2: 2 years; 3: 3 years; 4: 4 years; 5: 5 years or more; "
                                               "6: less than 1 year)")
    # Honesty module
    honesty_A = models.IntegerField(doc="If I want something from a person I dislike, I will act very nicely toward"
                                         " that person in order to get it. (1: strongly disagree; 2;3;4; 5: strongly "
                                        "agree)"
                                   )
    honesty_B = models.IntegerField(doc="If I knew that I could never get caught, I would be willing to steal a million"
                                        " euro. (1: strongly disagree; 2;3;4; 5: strongly agree)"
                                   )
    honesty_C = models.IntegerField(doc="I wouldn't use flattery to get a raise or promotion at work, even if I thought"
                                        " it would succeed. (1: strongly disagree; 2;3;4; 5: strongly agree)"
                                   )
    honesty_D = models.IntegerField(doc="I would be tempted to buy stolen property if I were financially tight."
                                        "(1: strongly disagree; 2;3;4; 5: strongly agree)"
                                   )
    honesty_E = models.IntegerField(doc="If I want something from someone, I will laugh at that person's worst jokes."
                                        "(1: strongly disagree; 2;3;4; 5: strongly agree)"
                                   )
    honesty_F = models.IntegerField(doc="I would never accept a bribe, even if it were very large."
                                        "(1: strongly disagree; 2;3;4; 5: strongly agree)"
                                   )
    honesty_G = models.IntegerField(doc="I wouldn't pretend to like someone just to get that person to do favors for me."
                                        "(1: strongly disagree; 2;3;4; 5: strongly agree)"
                                   )
    honesty_H = models.IntegerField(doc="I’d be tempted to use counterfeit money, if I were sure I could get away with"
                                        " it.(1: strongly disagree; 2;3;4; 5: strongly agree)"
                                   )
    # Task related questions
    understanding = models.IntegerField(doc="How would you rate your own understanding of the task you worked on "
                                            "throughout today's experiment?"
                                            "(1: very weak; 2;3;4; 5: very good)"
                                   )
    reliability = models.IntegerField(doc="From the perspective of someone who was involved in the estimation process,"
                                            "how reliable do you think the final estimates your group produced"
                                            "in the ten rounds of today's experiment are"
                                            "(1: very unreliable; 2;3;4; 5: very reliable)"
                                   )
    satisfaction = models.IntegerField(doc="Again from the perspective of someone who was involved in the estimation "
                                          ", how satisfying did you perceive the overall process and the interaction"
                                          "with your fellow group members?"
                                            "(1: very unsatisfying; 2;3;4; 5: very satisfying)"
                                   )
    strategy = models.StringField(label="<b>Please, briefly describe how you tried to solve the task in the experiment:</b> <br> <i>How "
                                      "did you evaluate your information, how did you transform it into your first estimate "
                                      "and the corresponding reasoning? What was your strategy for communicating your "
                                      "information to others? How did you take the input of others into account?</i>",
                                  doc="Please, briefly describe how you tried to solve the task in the experiment. How"
                                      "did you evaluate your information, how did you transform it into your first estimate "
                                      "and the corresponding reasoning? What was your strategy for communicating your "
                                      "information to others? How did you take the input of others into account?")
    wish = models.StringField(label="<b>Is there anything that would have helped you to better interact with your fellow group "
                                  "members or to solve the task better in general?</b>",
                              doc="Is there anything that would have helped you to better interact with your fellow group"
                                  "members or to solve the task better in general?")


# FUNCTIONS

# Randomization of task round dispay
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
                data["answer_q1"] == 10 and
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
                                data["answer_q1"] != 10,
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
        return player.round_displayed <= Constants.num_rounds


    @staticmethod
    def live_method(player: Player, data):
        global estimate_a, estimate_b, estimate_c, estimate_d, second_estimate_a, second_estimate_b, second_estimate_c,\
            second_estimate_d, indivarg_a, indivarg_b, indivarg_c, indivarg_d,num_estims, aggregate_estimate, \
            group_accuracy_bonus, random_number, feedback_order, result
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
                        "reasoning_b": indivarg_b,
                        "reasoning_c": indivarg_d,
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
                    if player.round_displayed == 1:
                        result = Constants.round_1_result
                    elif player.round_displayed == 2:
                        result = Constants.round_2_result
                    elif player.round_displayed == 3:
                        result = Constants.round_3_result
                    elif player.round_displayed == 4:
                        result = Constants.round_4_result
                    elif player.round_displayed == 5:
                        result = Constants.round_5_result
                    elif player.round_displayed == 6:
                        result = Constants.round_6_result
                    elif player.round_displayed == 7:
                        result = Constants.round_7_result
                    elif player.round_displayed == 8:
                        result = Constants.round_8_result
                    elif player.round_displayed == 9:
                        result = Constants.round_9_result
                    elif player.round_displayed == 10:
                        result = Constants.round_10_result
                    if result == 1:
                        if random_number > pow((1 - (aggregate_estimate/100)), 2):
                            group_accuracy_bonus = Constants.max_group_accuracy_bonus_per_round
                        elif random_number <= pow((1 - (aggregate_estimate/100)), 2):
                            group_accuracy_bonus = 0
                    elif result == 0:
                        if random_number > pow((aggregate_estimate/100), 2):
                            group_accuracy_bonus = Constants.max_group_accuracy_bonus_per_round
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

        # if player.round_number == Constants.num_rounds
        #     set_payoffs(player)


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['gender','education','field_of_studies', 'years_of_working',
                   'honesty_A', 'honesty_B', 'honesty_C', 'honesty_D', 'honesty_E', 'honesty_F', 'honesty_G', 'honesty_H',
                   'understanding', 'reliability', 'satisfaction', 'strategy', 'wish']

    @staticmethod
    def is_displayed(subsession: Subsession):
        return subsession.round_number == Constants.num_rounds


class Payoffs(Page):
    @staticmethod
    def is_displayed(subsession: Subsession):
        return subsession.round_number == Constants.num_rounds



page_sequence = [
                # Welcome,
                TaskIntro,
                Task_Trial,
                Task,
                Questionnaire,
                Payoffs
                ]