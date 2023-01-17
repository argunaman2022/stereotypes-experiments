from otree.api import *

doc = """
Survey for Mturk for the stereotypes project. Michael Hilweg, Argun Aman 2023
"""


class C(BaseConstants):
    NAME_IN_URL = 'Survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10
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
    choice_NV_task=models.StringField()
    choice_Maze_task=models.StringField()
    choice_Count_letters_task=models.StringField()
    choice_Word_puzzle_task=models.StringField()
    choice_Word_order_task=models.StringField()
    choice_Count_numbers_task=models.StringField()
    choice_Single_digit_calculus_task=models.StringField()
    choice_Ball_bucket_task=models.StringField()
    choice_Word_in_word_task=models.StringField()
    choice_Numbers_in_numbers_task=models.StringField()
    choice_MRT_task=models.StringField()

#### Functions and variables
#list of 10 unique tasks
tasks=['choice_NV_task','choice_Maze_task','choice_Count_letters_task','choice_Word_order_task','choice_Count_numbers_task',
       'choice_Single_digit_calculus_task','choice_Ball_bucket_task','choice_Word_in_word_task','choice_Numbers_in_numbers_task','choice_MRT_task']


def get_task():
    'this function cycles through tasks and returns the next task from tasks[]'
    import itertools
    task=itertools.cycle(tasks)
    return next(task)


class Introduction(Page):
    form_model = 'player'
    form_fields = ['gender', 'age']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1



class Choice(Page):
    form_model= 'player'

    form_fields =  [get_task()]
    
    @staticmethod
    def vars_for_template(player: Player, form_fields=form_fields,Tasks_path=C.Tasks_path):
        path_task = Tasks_path + str(form_fields[0]) + '.html'
        return dict(path_task=path_task, task_name=str(form_fields[0]))



# class Choice2(Page):
#     form_model = 'player'
#     form_fields =  ['choice_NV_task', 'choice_Maze_task']
#
#     @staticmethod
#     def vars_for_template(player: Player, form_fields=form_fields,Tasks_path=C.Tasks_path):
#         path_task = Tasks_path + str(form_fields[1]) + '.html'
#         return dict(path_task=path_task)
#

class Results(Page):
    @staticmethod
    def is_displayed(player:Player):
        return player.round_number==C.NUM_ROUNDS


page_sequence = [Introduction, Choice, Results]
