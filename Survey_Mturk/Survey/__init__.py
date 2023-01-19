from otree.api import *
import itertools

doc = """
Survey for Mturk for the stereotypes project. Michael Hilweg, Argun Aman 2023
"""
#todo write code for how long each question took to answer per participant.

class C(BaseConstants):
    NAME_IN_URL = 'Survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    Tasks_path= 'Survey/tasks/'
    Instruction_path='_templates/instructions.html'
    Completion_fee = cu(2)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #demogragphics
    age=models.IntegerField(min=16, max=99)
    gender=models.StringField(choices=['Male','Female','Other'],optional=True)

    'The following are hidden fields which we will manually assign after the participant confirms the slider input.'
    #choices
    NV_task=models.FloatField(blank=True, min=-1)
    Maze_task=models.FloatField(blank=True, min=-1)
    Count_letters_task=models.FloatField(blank=True, min=-1)
    Word_puzzle_task=models.FloatField(blank=True, min=-1)
    Word_order_task=models.FloatField(blank=True, min=-1)
    Count_numbers_task=models.FloatField(blank=True, min=-1)
    Ball_bucket_task=models.FloatField( blank=True, min=-1)
    Word_in_word_task=models.FloatField(blank=True, min=-1)
    Numbers_in_numbers_task=models.FloatField( blank=True, min=-1)
    MRT_task=models.FloatField(blank=True , min=-1)

#### Functions and variables
#list of 9 unique tasks
tasks=['NV_task', 'Maze_task','Count_letters_task','Word_puzzle_task','Word_order_task',
        'Count_numbers_task','Ball_bucket_task','Word_in_word_task','Numbers_in_numbers_task','MRT_task']

#Dictionary of true score differences between men and women to be used to calculate payoffs.
# Positive x implies men answered x percentage points more.
true_difference_list={
    'NV_task': 0.05,
    'Maze_task': 0.11,
    'Count_letters_task': -0.07,
    'Word_puzzle_task':0,
    'Word_order_task':0.12,
    'Count_numbers_task':0,
    'Ball_bucket_task':0,
    'Word_in_word_task':0,
    'Numbers_in_numbers_task':0,
    'MRT_task':0.15
}


def set_payoffs(player: Player):
    '''
    1. Payoff of the participant is the completion fee plus their earnings from each of the 9 questions.
    2. For the 9 questions they are paid based on accuracy using the following formula: 1- (a-b)^2 if a is the true value and b is the given answer.
    3. WORK ON THE SCORING RULE!!!!! #todo
    5. Convert the player field answers to decimal #todo
    '''

    player.payoff = C.Completion_fee
    for task, true_difference in true_difference_list.items():
        players_answer= player.f"{task}" #todo fix this problem
        print(players_answer)
        print(dir(player))

        player.payoff += 1 - (true_difference - players_answer)**2
        print(player.payoff, players_answer)



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

    def before_next_page(player: Player, timeout_happened):
        if player.round_number == C.NUM_ROUNDS:
            set_payoffs(Player)



class Results(Page):

    @staticmethod
    def is_displayed(player:Player):
        return player.round_number==C.NUM_ROUNDS


page_sequence = [Choice, Results]
