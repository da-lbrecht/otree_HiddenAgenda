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
estimate_recovery_a = 999
estimate_recovery_b = 999
estimate_recovery_c = 999
estimate_recovery_d = 999
indivarg_a = "none"
indivarg_b = "none"
indivarg_c = "none"
indivarg_d = "none"
indivarg_recovery_a = "none"
indivarg_recovery_b = "none"
indivarg_recovery_c = "none"
indivarg_recovery_d = "none"
error_a = 0
error_b = 0
error_c = 0
error_d = 0
second_estimate_a = 999
second_estimate_b = 999
second_estimate_c = 999
second_estimate_d = 999
aggregate_estimate = 999
group_accuracy_bonus = 999
random_number = 999
feedback_order = 999
result = 999
hiddenagenda = 999
hiddenagenda_bonus = 0
overall_hiddenagenda_bonus = 0
overall_accuracy_bonus = 0
reset_required = 0


class Constants(BaseConstants):
    name_in_url = 'delphi_hiddenagenda_acc'
    players_per_group = None
    num_rounds = 2

    fixed_pay = cu(5)
    avg_pay = cu(15)
    group_bonus = cu(6)
    individual_share_of_group_bonus = cu(1.5)
    max_group_accuracy_bonus_per_round = cu(6)
    hiddenagenda_bonus = cu(1.5)

    num_attention_checks = 5
    num_final_questions = 10

    # Results of payoff relevant execution of Kara's program; 0=did not reach target area
    round_1_result = 0  # 0.1
    round_2_result = 1  # 0.2
    round_3_result = 0  # 0.3
    round_4_result = 0  # 0.4
    round_5_result = 1  # 0.45
    round_6_result = 0  # 0.55
    round_7_result = 1  # 0.6
    round_8_result = 1  # 0.7
    round_9_result = 1  # 0.8
    round_10_result = 1  # 0.9

    # Hidden agendas, based on random draw taken prior to experiment, i.e constant in all sessions
    round_1_hiddenagenda = 0
    round_2_hiddenagenda = 100
    round_3_hiddenagenda = 100
    round_4_hiddenagenda = 0
    round_5_hiddenagenda = 0
    round_6_hiddenagenda = 0
    round_7_hiddenagenda = 0
    round_8_hiddenagenda = 0
    round_9_hiddenagenda = 0
    round_10_hiddenagenda = 100


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
    hiddenagenda_bonus = models.CurrencyField(initial=0,
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
                                          label="Q3: What precisely do you need to estimate?",
                                          doc="What precisely do you need to estimate?"
                                              "(1: The chance that the ladybird reaches the target area"
                                              " 2: The chance that the ladybird does not reach the target area "
                                              " 3: The chance that the ladybird ends up at level 0 after ten steps)"
                                          )
    attention_check_4 = models.FloatField(initial=999,
                                          label="Q4: What kind of feedback do you receive in each round?",
                                          doc="Attention check: What kind of feedback do you receive in each round?"
                                              " (1: First estimates and corresponding reasoning of all group members,"
                                              " without knowing which belongs to whom; 2: All estimates and "
                                              "corresponding reasonings made by the other group members; 3: Only the "
                                              "reasoning of all group members, without knowing which belongs to whom")
    attention_check_5 = models.FloatField(initial=999,
                                          label="Q5: What do you know about the ladybird?",
                                          doc="Attention check: What do you know about the ladybird?"
                                              "(1: The precise chance of reaching the target area, "
                                              "2: The precise chance that it moves one level up in the first step, "
                                              "3: That the chance that it moves one level up is the same in each step"
                                              " in a given round)"
                                          )

    attention_check_6 = models.FloatField(inital=999,
                                          label="Q6: What does the bonus you can earn by solving the task"
                                                " depend on?",
                                          doc="Q6: What does the bonus you can earn by solving the task depend on?"
                                              "(1: Only on the accuracy of my own estimates;"
                                              "2: Only on the accuracy of the joint group estimate;"
                                              "3: Only on the time needed for solving the task")

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
    indivarg_recovery = models.StringField(doc="Reasoning given for first individual estimate given in Delphi procedure"
                                               "stored in case of erroneous inputs to redisplay when prompting to"
                                               "correct input")
    second_indivestim = models.FloatField(label="My second estimate:",
                                          doc="Second individual estimate given in Delphi procedure",
                                          min=0, max=100)
    length_indivarg = models.FloatField(doc="Number of characters in reasoning")
    erroneous_estimate = models.BooleanField(initial=True,
                                             doc="Error in first estimate")
    erroneous_reasoning = models.BooleanField(initial=True,
                                              doc="Error in reasoning")
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
                                 doc="Questionnaire: Which gender do you identify with? "
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
                                               [1, '1 up to 2 years'],
                                               [2, '2 up to 3 years'],
                                               [3, '3 up to 4 years'],
                                               [4, '4 up to 5 years'],
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
    honesty_G = models.IntegerField(doc="I wouldn't pretend to like someone just to get that person to do favors for "
                                        "me. (1: strongly disagree; 2;3;4; 5: strongly agree)"
                                    )
    honesty_H = models.IntegerField(doc="I’d be tempted to use counterfeit money, if I were sure I could get away with"
                                        " it.(1: strongly disagree; 2;3;4; 5: strongly agree)"
                                    )
    # Task related questions
    understanding = models.IntegerField(doc="How would you rate your own understanding of the task you worked on "
                                            "throughout today's experiment?"
                                            "(1: very weak; 2;3;4; 5: very good)"
                                        )
    reliability = models.IntegerField(doc="How reliable, do you think, are the final estimates your group produced?"
                                          "(1: very unreliable; 2;3;4; 5: very reliable)"
                                      )
    satisfaction = models.IntegerField(doc="How satisfying did you perceive the overall process and the interaction "
                                           "with your fellow group members? (1: very unsatisfying; 2;3;4; "
                                           "5: very satisfying)"
                                       )
    strategy_info = models.StringField(label="How did you evaluate your information and how did you transform it into"
                                             " an estimate?",
                                       doc="How did you evaluate your information and how did you transform it into"
                                           " an estimate?",
                                       blank=True
                                       )
    strategy_communication = models.StringField(label="What was your strategy for communicating your information to "
                                                      "others?",
                                                doc="What was your strategy for communicating your information to "
                                                    "others?",
                                                blank=True
                                                )
    strategy_others = models.StringField(label="How did you take the input of others into account?",
                                         doc="How did you take the input of others into account?",
                                         blank=True
                                         )
    wish = models.StringField(label="Finally, which changes to format of interaction would have helped you to better"
                                    " interact with your fellow group members or to solve the task better in general?",
                              doc="Finally, which changes to format of interaction would have helped you to better"
                                  " interact with your fellow group members or to solve the task better in general?",
                              blank=True
                              )


# FUNCTIONS

# Randomization of task round display
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        list_of_round_ids = range(1, Constants.num_rounds + 1)
        subsession_temp_list = list_of_round_ids
        # random.shuffle(subsession_temp_list) # Needed for randomization of round order
        for player in subsession.get_players():
            temp_list = subsession_temp_list
            for i in list_of_round_ids:
                player.in_round(i).round_displayed = temp_list[i - 1]


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
            player.attention_check_6 = data["answer_q6"]

        if (
                data["answer_q1"] == 2 and
                data["answer_q2"] == 3 and
                data["answer_q3"] == 1 and
                data["answer_q4"] == 1 and
                data["answer_q5"] == 3 and
                data["answer_q6"] == 2
        ):
            return {
                player.id_in_group: {"information_type": "no_error", "no_error": "Yeah!"},
            }
        else:
            player.failed_attention_check = True
            player.attention_check_tries = player.attention_check_tries + 1
            incorrect_answers = np.array([
                data["answer_q1"] != 2,
                data["answer_q2"] != 3,
                data["answer_q3"] != 1,
                data["answer_q4"] != 1,
                data["answer_q5"] != 3,
                data["answer_q6"] != 2,
            ], dtype=bool)
            # incorrect_answers.np.astype(int)
            questions = ' and '.join(np.array(['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'])[incorrect_answers])
            return {
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
        global estimate_a, estimate_b, estimate_c, estimate_d, second_estimate_a, second_estimate_b, second_estimate_c, \
            second_estimate_d, indivarg_a, indivarg_b, indivarg_c, indivarg_d, num_estims, aggregate_estimate, \
            group_accuracy_bonus, random_number, feedback_order, result, indivarg_recovery_a, indivarg_recovery_b, \
            indivarg_recovery_c, indivarg_recovery_d, estimate_recovery_a, estimate_recovery_b, \
            estimate_recovery_c, estimate_recovery_d, error_a, error_b, error_c, error_d, hiddenagenda, \
            overall_hiddenagenda_bonus, hiddenagenda_bonus, overall_accuracy_bonus, reset_required
        group = player.group
        players = group.get_players()
        if data["information_type"] == "estimate":
            # Check whether there is still old temporary data present
            if reset_required == 1:
                estimate_a = 999
                estimate_b = 999
                estimate_c = 999
                estimate_d = 999
                indivarg_a = "none"
                indivarg_b = "none"
                indivarg_c = "none"
                indivarg_d = "none"
                estimate_recovery_a = 999
                estimate_recovery_b = 999
                estimate_recovery_c = 999
                estimate_recovery_d = 999
                indivarg_recovery_a = "none"
                indivarg_recovery_b = "none"
                indivarg_recovery_c = "none"
                indivarg_recovery_d = "none"
                error_a = 0
                error_b = 0
                error_c = 0
                error_d = 0
                second_estimate_a = 999
                second_estimate_b = 999
                second_estimate_c = 999
                second_estimate_d = 999
                hiddenagenda = 999
                hiddenagenda_bonus = 0
                overall_hiddenagenda_bonus = 0
                overall_accuracy_bonus = 0
                reset_required = 0
                print("Reset completed")
            player.first_indivestim = data["estimate"]
            player.erroneous_estimate = 1
            if player.id_in_group == 1:
                estimate_recovery_a = data["estimate"]
            elif player.id_in_group == 2:
                estimate_recovery_b = data["estimate"]
            elif player.id_in_group == 3:
                estimate_recovery_c = data["estimate"]
            elif player.id_in_group == 4:
                estimate_recovery_d = data["estimate"]
            if (
                    type(data["estimate"]) == float
                    or type(data["estimate"]) == int
                    and 0 <= data["estimate"] <= 100
            ):
                num_estims += 1
                player.erroneous_estimate = 0
                if player.id_in_group == 1:
                    estimate_a = data["estimate"]
                elif player.id_in_group == 2:
                    estimate_b = data["estimate"]
                elif player.id_in_group == 3:
                    estimate_c = data["estimate"]
                elif player.id_in_group == 4:
                    estimate_d = data["estimate"]
            # if data["information_type"] == "reasoning":
            player.indivarg = data["reasoning"]
            player.length_indivarg = len(data["reasoning"])
            player.erroneous_reasoning = 1
            if player.id_in_group == 1:
                indivarg_recovery_a = data["reasoning"]
            elif player.id_in_group == 2:
                indivarg_recovery_b = data["reasoning"]
            elif player.id_in_group == 3:
                indivarg_recovery_c = data["reasoning"]
            elif player.id_in_group == 4:
                indivarg_recovery_d = data["reasoning"]
            if len(data["reasoning"]) >= 100:
                player.erroneous_reasoning = 0
                if player.id_in_group == 1:
                    indivarg_a = data["reasoning"]
                elif player.id_in_group == 2:
                    indivarg_b = data["reasoning"]
                elif player.id_in_group == 3:
                    indivarg_c = data["reasoning"]
                elif player.id_in_group == 4:
                    indivarg_d = data["reasoning"]
        # Identify potential errors in input
        if player.id_in_group == 1:
            if (
                    type(estimate_recovery_a) == float
                    or type(estimate_recovery_a) == int
                    and 0 <= estimate_recovery_a <= 100
            ):
                if len(indivarg_recovery_a) >= 100:  # No error
                    error_a = 0
                else:  # Only error in reasoning
                    error_a = 2
            else:
                if len(indivarg_recovery_a) >= 100:  # Only error in estimate
                    error_a = 1
                else:  # Error in estimate and reasoning
                    error_a = 3
        if player.id_in_group == 2:
            if (
                    type(estimate_recovery_b) == float
                    or type(estimate_recovery_b) == int
                    and 0 <= estimate_recovery_b <= 100
            ):
                if len(indivarg_recovery_b) >= 100:  # No error
                    error_b = 0
                else:  # Only error in reasoning
                    error_b = 2
            else:
                if len(indivarg_recovery_b) >= 100:  # Only error in estimate
                    error_b = 1
                else:  # Error in estimate and reasoning
                    error_b = 3
        if player.id_in_group == 3:
            if (
                    type(estimate_recovery_c) == float
                    or type(estimate_recovery_c) == int
                    and 0 <= estimate_recovery_c <= 100
            ):
                if len(indivarg_recovery_c) >= 100:  # No error
                    error_c = 0
                else:  # Only error in reasoning
                    error_c = 2
            else:
                if len(indivarg_recovery_c) >= 100:  # Only error in estimate
                    error_c = 1
                else:  # Error in estimate and reasoning
                    error_c = 3
        if player.id_in_group == 4:
            if (
                    type(estimate_recovery_d) == float
                    or type(estimate_recovery_d) == int
                    and 0 <= estimate_recovery_d <= 100
            ):
                if len(indivarg_recovery_d) >= 100:  # No error
                    error_d = 0
                else:  # Only error in reasoning
                    error_d = 2
            else:
                if len(indivarg_recovery_d) >= 100:  # Only error in estimate
                    error_d = 1
                else:  # Error in estimate and reasoning
                    error_d = 3
        # Send error messages to participants
        if player.id_in_group == 1:
            if error_a == 1:
                return {
                    player.id_in_group: {"information_type": "error_1",
                                         "estimate": estimate_recovery_a,
                                         "reasoning": indivarg_recovery_a},
                }
            elif error_a == 2:
                return {
                    player.id_in_group: {"information_type": "erroneous_reasoning",
                                         "estimate": estimate_recovery_a,
                                         "reasoning": indivarg_recovery_a},
                }
            elif error_a == 3:
                return {
                    player.id_in_group: {"information_type": "error_both",
                                         "estimate": estimate_recovery_a,
                                         "reasoning": indivarg_recovery_a},
                }
        if player.id_in_group == 2:
            if error_b == 1:
                return {
                    player.id_in_group: {"information_type": "error_1",
                                         "estimate": estimate_recovery_b,
                                         "reasoning": indivarg_recovery_b},
                }
            elif error_b == 2:
                return {
                    player.id_in_group: {"information_type": "erroneous_reasoning",
                                         "estimate": estimate_recovery_b,
                                         "reasoning": indivarg_recovery_b},
                }
            elif error_b == 3:
                return {
                    player.id_in_group: {"information_type": "error_both",
                                         "estimate": estimate_recovery_b,
                                         "reasoning": indivarg_recovery_b},
                }
        if player.id_in_group == 3:
            if error_c == 1:
                return {
                    player.id_in_group: {"information_type": "error_1",
                                         "estimate": estimate_recovery_c,
                                         "reasoning": indivarg_recovery_c},
                }
            elif error_c == 2:
                return {
                    player.id_in_group: {"information_type": "erroneous_reasoning",
                                         "estimate": estimate_recovery_c,
                                         "reasoning": indivarg_recovery_c},
                }
            elif error_c == 3:
                return {
                    player.id_in_group: {"information_type": "error_both",
                                         "estimate": estimate_recovery_c,
                                         "reasoning": indivarg_recovery_c},
                }
        if player.id_in_group == 4:
            if error_d == 1:
                return {
                    player.id_in_group: {"information_type": "error_1",
                                         "estimate": estimate_recovery_d,
                                         "reasoning": indivarg_recovery_d},
                }
            elif error_d == 2:
                return {
                    player.id_in_group: {"information_type": "erroneous_reasoning",
                                         "estimate": estimate_recovery_d,
                                         "reasoning": indivarg_recovery_d},
                }
            elif error_d == 3:
                return {
                    player.id_in_group: {"information_type": "error_both",
                                         "estimate": estimate_recovery_d,
                                         "reasoning": indivarg_recovery_d},
                }
        if (
                estimate_a != 999
                and estimate_b != 999
                and estimate_c != 999
                and estimate_d != 999
                and indivarg_a != "none"
                and indivarg_b != "none"
                and indivarg_c != "none"
                and indivarg_d != "none"
                and data["information_type"] != "second_estimate"
        ):
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
                    aggregate_estimate = (second_estimate_a + second_estimate_b + second_estimate_c +
                                          second_estimate_d) / 4
                    reset_required = 1
                    return {
                        1: {"information_type": "completion_indicator_a",
                            "group_estimate": aggregate_estimate,
                            "estimate_a": second_estimate_a,  # presented order of fellow group members' input: 2, 3, 4
                            "estimate_b": second_estimate_b,
                            "estimate_c": second_estimate_c,
                            "estimate_d": second_estimate_d},
                        2: {"information_type": "completion_indicator_b",
                            "group_estimate": aggregate_estimate,
                            "estimate_a": second_estimate_a,  # presented order of fellow group members' input: 1, 3, 4
                            "estimate_b": second_estimate_b,
                            "estimate_c": second_estimate_c,
                            "estimate_d": second_estimate_d},
                        3: {"information_type": "completion_indicator_c",
                            "group_estimate": aggregate_estimate,
                            "estimate_a": second_estimate_a,  # presented order of fellow group members' input: 1, 2, 4
                            "estimate_b": second_estimate_b,
                            "estimate_c": second_estimate_c,
                            "estimate_d": second_estimate_d},
                        4: {"information_type": "completion_indicator_d",
                            "group_estimate": aggregate_estimate,
                            "estimate_a": second_estimate_a,  # presented order of fellow group members' input: 1, 2, 3
                            "estimate_b": second_estimate_b,
                            "estimate_c": second_estimate_c,
                            "estimate_d": second_estimate_d},
                    }
                else:
                    return {
                        player.id_in_group: {"information_type": "wait_indicator"},
                    }
            else:
                return {
                    player.id_in_group: {"information_type": "error_2",
                                         "error": "estimate out of range"},
                }


@staticmethod
def before_next_page(player: Player, timeout_happened):
    # global num_estims, estimate_a, estimate_b, estimate_c, estimate_d, second_estimate_a, second_estimate_b, \
    #     second_estimate_c, second_estimate_d, indivarg_a, indivarg_b, indivarg_c, indivarg_d, estimate_recovery_a, \
    #     estimate_recovery_b, estimate_recovery_c, estimate_recovery_d, indivarg_recovery_a, indivarg_recovery_b, \
    #     indivarg_recovery_c, indivarg_recovery_d, error_a, error_b, error_c, error_d

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
        global estimate_a, estimate_b, estimate_c, estimate_d, second_estimate_a, second_estimate_b, second_estimate_c, \
            second_estimate_d, indivarg_a, indivarg_b, indivarg_c, indivarg_d, num_estims, aggregate_estimate, \
            group_accuracy_bonus, random_number, feedback_order, result, indivarg_recovery_a, indivarg_recovery_b, \
            indivarg_recovery_c, indivarg_recovery_d, estimate_recovery_a, estimate_recovery_b, \
            estimate_recovery_c, estimate_recovery_d, error_a, error_b, error_c, error_d, hiddenagenda, \
            overall_hiddenagenda_bonus, hiddenagenda_bonus, overall_accuracy_bonus, reset_required
        group = player.group
        players = group.get_players()
        if data["information_type"] == "estimate":
            # Check whether there is still old temporary data present, reset if yes
            if reset_required == 1:
                estimate_a = 999
                estimate_b = 999
                estimate_c = 999
                estimate_d = 999
                indivarg_a = "none"
                indivarg_b = "none"
                indivarg_c = "none"
                indivarg_d = "none"
                estimate_recovery_a = 999
                estimate_recovery_b = 999
                estimate_recovery_c = 999
                estimate_recovery_d = 999
                indivarg_recovery_a = "none"
                indivarg_recovery_b = "none"
                indivarg_recovery_c = "none"
                indivarg_recovery_d = "none"
                error_a = 0
                error_b = 0
                error_c = 0
                error_d = 0
                second_estimate_a = 999
                second_estimate_b = 999
                second_estimate_c = 999
                second_estimate_d = 999
                hiddenagenda = 999
                hiddenagenda_bonus = 0
                overall_hiddenagenda_bonus = 0
                overall_accuracy_bonus = 0
                reset_required = 0
                print("Reset completed")
            player.first_indivestim = data["estimate"]
            player.erroneous_estimate = 1
            if player.id_in_group == 1:
                estimate_recovery_a = data["estimate"]
            elif player.id_in_group == 2:
                estimate_recovery_b = data["estimate"]
            elif player.id_in_group == 3:
                estimate_recovery_c = data["estimate"]
            elif player.id_in_group == 4:
                estimate_recovery_d = data["estimate"]
            if (
                    type(data["estimate"]) == float
                    or type(data["estimate"]) == int
                    and 0 <= data["estimate"] <= 100
            ):
                num_estims += 1
                player.erroneous_estimate = 0
                if player.id_in_group == 1:
                    estimate_a = data["estimate"]
                elif player.id_in_group == 2:
                    estimate_b = data["estimate"]
                elif player.id_in_group == 3:
                    estimate_c = data["estimate"]
                elif player.id_in_group == 4:
                    estimate_d = data["estimate"]
            # if data["information_type"] == "reasoning":
            player.indivarg = data["reasoning"]
            player.length_indivarg = len(data["reasoning"])
            player.erroneous_reasoning = 1
            if player.id_in_group == 1:
                indivarg_recovery_a = data["reasoning"]
            elif player.id_in_group == 2:
                indivarg_recovery_b = data["reasoning"]
            elif player.id_in_group == 3:
                indivarg_recovery_c = data["reasoning"]
            elif player.id_in_group == 4:
                indivarg_recovery_d = data["reasoning"]
            if len(data["reasoning"]) >= 100:
                player.erroneous_reasoning = 0
                if player.id_in_group == 1:
                    indivarg_a = data["reasoning"]
                elif player.id_in_group == 2:
                    indivarg_b = data["reasoning"]
                elif player.id_in_group == 3:
                    indivarg_c = data["reasoning"]
                elif player.id_in_group == 4:
                    indivarg_d = data["reasoning"]
        # Identify potential errors in input
        if player.id_in_group == 1:
            if (
                    type(estimate_recovery_a) == float
                    or type(estimate_recovery_a) == int
                    and 0 <= estimate_recovery_a <= 100
            ):
                if len(indivarg_recovery_a) >= 100:  # No error
                    error_a = 0
                else:  # Only error in reasoning
                    error_a = 2
            else:
                if len(indivarg_recovery_a) >= 100:  # Only error in estimate
                    error_a = 1
                else:  # Error in estimate and reasoning
                    error_a = 3
        if player.id_in_group == 2:
            if (
                    type(estimate_recovery_b) == float
                    or type(estimate_recovery_b) == int
                    and 0 <= estimate_recovery_b <= 100
            ):
                if len(indivarg_recovery_b) >= 100:  # No error
                    error_b = 0
                else:  # Only error in reasoning
                    error_b = 2
            else:
                if len(indivarg_recovery_b) >= 100:  # Only error in estimate
                    error_b = 1
                else:  # Error in estimate and reasoning
                    error_b = 3
        if player.id_in_group == 3:
            if (
                    type(estimate_recovery_c) == float
                    or type(estimate_recovery_c) == int
                    and 0 <= estimate_recovery_c <= 100
            ):
                if len(indivarg_recovery_c) >= 100:  # No error
                    error_c = 0
                else:  # Only error in reasoning
                    error_c = 2
            else:
                if len(indivarg_recovery_c) >= 100:  # Only error in estimate
                    error_c = 1
                else:  # Error in estimate and reasoning
                    error_c = 3
        if player.id_in_group == 4:
            if (
                    type(estimate_recovery_d) == float
                    or type(estimate_recovery_d) == int
                    and 0 <= estimate_recovery_d <= 100
            ):
                if len(indivarg_recovery_d) >= 100:  # No error
                    error_d = 0
                else:  # Only error in reasoning
                    error_d = 2
            else:
                if len(indivarg_recovery_d) >= 100:  # Only error in estimate
                    error_d = 1
                else:  # Error in estimate and reasoning
                    error_d = 3
        # Send error messages to participants
        if player.id_in_group == 1:
            if error_a == 1:
                return {
                    player.id_in_group: {"information_type": "error_1",
                                         "estimate": estimate_recovery_a,
                                         "reasoning": indivarg_recovery_a},
                }
            elif error_a == 2:
                return {
                    player.id_in_group: {"information_type": "erroneous_reasoning",
                                         "estimate": estimate_recovery_a,
                                         "reasoning": indivarg_recovery_a},
                }
            elif error_a == 3:
                return {
                    player.id_in_group: {"information_type": "error_both",
                                         "estimate": estimate_recovery_a,
                                         "reasoning": indivarg_recovery_a},
                }
        if player.id_in_group == 2:
            if error_b == 1:
                return {
                    player.id_in_group: {"information_type": "error_1",
                                         "estimate": estimate_recovery_b,
                                         "reasoning": indivarg_recovery_b},
                }
            elif error_b == 2:
                return {
                    player.id_in_group: {"information_type": "erroneous_reasoning",
                                         "estimate": estimate_recovery_b,
                                         "reasoning": indivarg_recovery_b},
                }
            elif error_b == 3:
                return {
                    player.id_in_group: {"information_type": "error_both",
                                         "estimate": estimate_recovery_b,
                                         "reasoning": indivarg_recovery_b},
                }
        if player.id_in_group == 3:
            if error_c == 1:
                return {
                    player.id_in_group: {"information_type": "error_1",
                                         "estimate": estimate_recovery_c,
                                         "reasoning": indivarg_recovery_c},
                }
            elif error_c == 2:
                return {
                    player.id_in_group: {"information_type": "erroneous_reasoning",
                                         "estimate": estimate_recovery_c,
                                         "reasoning": indivarg_recovery_c},
                }
            elif error_c == 3:
                return {
                    player.id_in_group: {"information_type": "error_both",
                                         "estimate": estimate_recovery_c,
                                         "reasoning": indivarg_recovery_c},
                }
        if player.id_in_group == 4:
            if error_d == 1:
                return {
                    player.id_in_group: {"information_type": "error_1",
                                         "estimate": estimate_recovery_d,
                                         "reasoning": indivarg_recovery_d},
                }
            elif error_d == 2:
                return {
                    player.id_in_group: {"information_type": "erroneous_reasoning",
                                         "estimate": estimate_recovery_d,
                                         "reasoning": indivarg_recovery_d},
                }
            elif error_d == 3:
                return {
                    player.id_in_group: {"information_type": "error_both",
                                         "estimate": estimate_recovery_d,
                                         "reasoning": indivarg_recovery_d},
                }
        if (
                estimate_a != 999
                and estimate_b != 999
                and estimate_c != 999
                and estimate_d != 999
                and indivarg_a != "none"
                and indivarg_b != "none"
                and indivarg_c != "none"
                and indivarg_d != "none"
                and data["information_type"] != "second_estimate"
        ):
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
                    reset_required = 1
                    random_number = random.uniform(0, 1)
                    if player.round_displayed == 1:
                        result = Constants.round_1_result
                        hiddenagenda = Constants.round_1_hiddenagenda
                    elif player.round_displayed == 2:
                        result = Constants.round_2_result
                        hiddenagenda = Constants.round_2_hiddenagenda
                    elif player.round_displayed == 3:
                        result = Constants.round_3_result
                        hiddenagenda = Constants.round_3_hiddenagenda
                    elif player.round_displayed == 4:
                        result = Constants.round_4_result
                        hiddenagenda = Constants.round_4_hiddenagenda
                    elif player.round_displayed == 5:
                        result = Constants.round_5_result
                        hiddenagenda = Constants.round_5_hiddenagenda
                    elif player.round_displayed == 6:
                        result = Constants.round_6_result
                        hiddenagenda = Constants.round_6_hiddenagenda
                    elif player.round_displayed == 7:
                        result = Constants.round_7_result
                        hiddenagenda = Constants.round_7_hiddenagenda
                    elif player.round_displayed == 8:
                        result = Constants.round_8_result
                        hiddenagenda = Constants.round_8_hiddenagenda
                    elif player.round_displayed == 9:
                        result = Constants.round_9_result
                        hiddenagenda = Constants.round_9_hiddenagenda
                    elif player.round_displayed == 10:
                        result = Constants.round_10_result
                        hiddenagenda = Constants.round_10_hiddenagenda
                    if result == 1:
                        if random_number > pow((1 - (aggregate_estimate / 100)), 2):
                            group_accuracy_bonus = Constants.max_group_accuracy_bonus_per_round
                        elif random_number <= pow((1 - (aggregate_estimate / 100)), 2):
                            group_accuracy_bonus = 0
                    elif result == 0:
                        if random_number > pow((aggregate_estimate / 100), 2):
                            group_accuracy_bonus = Constants.max_group_accuracy_bonus_per_round
                        elif random_number <= pow((aggregate_estimate / 100), 2):
                            group_accuracy_bonus = 0
                    if hiddenagenda == 0:
                        if random_number <= pow((1 - (aggregate_estimate / 100)), 2):
                            hiddenagenda_bonus = Constants.hiddenagenda_bonus
                        elif random_number > pow((1 - (aggregate_estimate / 100)), 2):
                            hiddenagenda_bonus = 0
                        overall_hiddenagenda_bonus += hiddenagenda_bonus
                    elif hiddenagenda == 100:
                        if random_number <= pow((aggregate_estimate / 100), 2):
                            hiddenagenda_bonus = Constants.hiddenagenda_bonus
                        elif random_number > pow((aggregate_estimate / 100), 2):
                            hiddenagenda_bonus = 0
                        overall_hiddenagenda_bonus += hiddenagenda_bonus
                    overall_accuracy_bonus += group_accuracy_bonus
                    return {
                        1: {"information_type": "completion_indicator_a",
                            "group_estimate": aggregate_estimate,
                            "estimate_a": second_estimate_a,  # presented order of fellow group members' input: 2, 3, 4
                            "estimate_b": second_estimate_b,
                            "estimate_c": second_estimate_c,
                            "estimate_d": second_estimate_d},
                        2: {"information_type": "completion_indicator_b",
                            "group_estimate": aggregate_estimate,
                            "estimate_a": second_estimate_a,  # presented order of fellow group members' input: 1, 3, 4
                            "estimate_b": second_estimate_b,
                            "estimate_c": second_estimate_c,
                            "estimate_d": second_estimate_d},
                        3: {"information_type": "completion_indicator_c",
                            "group_estimate": aggregate_estimate,
                            "estimate_a": second_estimate_a,  # presented order of fellow group members' input: 1, 2, 4
                            "estimate_b": second_estimate_b,
                            "estimate_c": second_estimate_c,
                            "estimate_d": second_estimate_d},
                        4: {"information_type": "completion_indicator_d",
                            "group_estimate": aggregate_estimate,
                            "estimate_a": second_estimate_a,  # presented order of fellow group members' input: 1, 2, 3
                            "estimate_b": second_estimate_b,
                            "estimate_c": second_estimate_c,
                            "estimate_d": second_estimate_d},
                    }
                else:
                    return {
                        player.id_in_group: {"information_type": "wait_indicator"},
                    }
            else:
                return {
                    player.id_in_group: {"information_type": "error_2",
                                         "error": "estimate out of range"},
                }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # global num_estims, estimate_a, estimate_b, estimate_c, estimate_d, second_estimate_a, second_estimate_b, \
        #     second_estimate_c, second_estimate_d, hiddenagenda_bonus, indivarg_a, indivarg_b, indivarg_c, indivarg_d, \
        #     estimate_recovery_a, estimate_recovery_b, estimate_recovery_c, estimate_recovery_d, indivarg_recovery_a,\
        #     indivarg_recovery_b, indivarg_recovery_c, indivarg_recovery_d, error_a, error_b, error_c, error_d

        player.random_number = random_number
        player.aggregate_estimate = aggregate_estimate
        player.group_accuracy_bonus = group_accuracy_bonus * 0.25
        player.payoff += group_accuracy_bonus * 0.25
        player.feedback_order = feedback_order

        if player.id_in_group >= 3:
            player.hiddenagenda_bonus = hiddenagenda_bonus
            player.payoff += hiddenagenda_bonus

        if player.round_number == 1:
            player.start_of_round = player.end_of_trial
        else:
            player.start_of_round = player.in_round(player.round_number - 1).end_of_round

        # if player.round_number == Constants.num_rounds
        #     set_payoffs(player)


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['gender', 'education', 'field_of_studies', 'years_of_working',
                   'honesty_A', 'honesty_B', 'honesty_C', 'honesty_D', 'honesty_E', 'honesty_F', 'honesty_G',
                   'honesty_H',
                   'understanding', 'reliability', 'satisfaction', 'strategy_info', 'strategy_communication',
                   'strategy_others', 'wish']

    @staticmethod
    def is_displayed(subsession: Subsession):
        return subsession.round_number == Constants.num_rounds


class Payoffs(Page):
    @staticmethod
    def is_displayed(subsession: Subsession):
        return subsession.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        global overall_hiddenagenda_bonus
        player
        return {
            "overall_hiddenagenda_bonus": cu(overall_hiddenagenda_bonus),
            "overall_accuracy_bonus": cu(overall_accuracy_bonus / 4),
        }


page_sequence = [
    # Welcome,
    # TaskIntro,
    Task_Trial,
    Task,
    Questionnaire,
    Payoffs
]
