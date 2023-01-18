from otree.api import *
import itertools

doc = """
Survey for Mturk for the stereotypes project. Michael Hilweg, Argun Aman 2023
"""


class C(BaseConstants):
    NAME_IN_URL = 'Survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 9
    Tasks_path= 'Survey/tasks/'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #demogragphics
    age=models.IntegerField()
    gender=models.StringField(choices=['Male','Female','Other'],optional=True)

    'The following are hidden fields which we will manually assign after the participant confirms the slider input.'
    #choices
    NV_task=models.StringField()
    Maze_task=models.StringField()
    Count_letters_task=models.StringField()
    Word_puzzle_task=models.StringField()
    Word_order_task=models.StringField()
    Count_numbers_task=models.StringField()
    Ball_bucket_task=models.StringField()
    Word_in_word_task=models.StringField()
    Numbers_in_numbers_task=models.StringField()
    MRT_task=models.StringField()

#### Functions and variables
#list of 9 unique tasks
tasks=['NV_task', 'Maze_task','Count_letters_task','Word_puzzle_task','Word_order_task',
        'Count_numbers_task','Ball_bucket_task','Word_in_word_task','Numbers_in_numbers_task','MRT_task']


class Introduction(Page):
    form_model = 'player'
    form_fields = ['gender', 'age']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Choice(Page):
    form_model = 'player'
    form_fields = tasks

    @staticmethod
    def vars_for_template(player: Player, form_fields=form_fields, tasks_path=C.Tasks_path):
        round_number = player.round_number
        task = tasks[round_number-1]

        path_task = tasks_path + task + '.html'
        return dict(
            path_task=path_task,
            task_name=task,
            round_number=round_number
        )

    @staticmethod
    def js_vars(player: Player):
        dict = {'tasks': tasks, 'round_number': player.round_number}
        return dict




class Results(Page):
    @staticmethod
    def is_displayed(player:Player):
        return player.round_number==C.NUM_ROUNDS


page_sequence = [Introduction, Choice, Results]
