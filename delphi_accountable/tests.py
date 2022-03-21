from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot
import datetime


class PlayerBot(Bot):
    def play_round(self):
        if self.player.id_in_group != 1 and self.round_number == 1:
            yield Welcome, {"starting_time": datetime.datetime.now()}
            yield TaskIntro, {"begintrial_time": datetime.datetime.now()}
            yield Task_Trial, {"endtrial_time": datetime.datetime.now()}


def call_live_method(method, **kwargs):
        # TaskIntro
        method(2, {"information_type": "answer",
                   "answer_q1" :10,
                   "answer_q2": 3,
                   "answer_q3": 1,
                   "answer_q4": 1,
                   "answer_q5": 3,
                   },
               )
        method(3, {"information_type": "answer",
                   "answer_q1" :10,
                   "answer_q2": 3,
                   "answer_q3": 1,
                   "answer_q4": 1,
                   "answer_q5": 3,
                   },
               )
        method(4, {"information_type": "answer",
                   "answer_q1" :10,
                   "answer_q2": 3,
                   "answer_q3": 1,
                   "answer_q4": 1,
                   "answer_q5": 3,
                   },
               )
        # # Task Trial
        # method(2, {"information_type": "estimate",
        #            "estimate": 20,
        #            },
        #        )
        # method(3, {"information_type": "estimate",
        #            "estimate": 30,
        #            },
        #        )
        # method(4, {"information_type": "estimate",
        #            "estimate": 40,
        #            },
        #        )
        # method(2, {"information_type": "reasoning",
        #            "reasoning": "I am Player 2",
        #            },
        #        )
        # method(3, {"information_type": "reasoning",
        #            "reasoning": "I am Player 3",
        #            },
        #        )
        # method(4, {"information_type": "reasoning",
        #            "reasoning": "I am Player 4",
        #            },
        #        )
