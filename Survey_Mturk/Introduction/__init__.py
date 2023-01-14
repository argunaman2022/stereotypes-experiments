from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age=models.IntegerField()
    gender=models.StringField(choices=['Male','Female','Other'],optional=True)
    pass


# PAGES
class Introduction(Page):
    form_model = 'player'
    form_fields = ['gender', 'age']
    pass




page_sequence = [Introduction]
