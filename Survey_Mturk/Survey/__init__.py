from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
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

    pass


class Introduction(Page):
    form_model = 'player'
    form_fields = ['gender', 'age']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1



class Choice1(Page):
    form_model= 'player'
    form_fields =  ['choice_NV_task', 'choice_Maze_task']
    
    @staticmethod
    def vars_for_template(player: Player, form_fields=form_fields,Tasks_path=C.Tasks_path):
        path_task = Tasks_path + str(form_fields[0]) + '.html'
        return dict(path_task=path_task)



class Choice2(Page):
    form_model = 'player'
    form_fields =  ['choice_NV_task', 'choice_Maze_task']

    @staticmethod
    def vars_for_template(player: Player, form_fields=form_fields,Tasks_path=C.Tasks_path):
        path_task = Tasks_path + str(form_fields[1]) + '.html'
        return dict(path_task=path_task)


class Results(Page):
    @staticmethod
    def is_displayed(player:Player):
        return player.round_number==C.NUM_ROUNDS


page_sequence = [Introduction, Choice1, Choice2, Results]
