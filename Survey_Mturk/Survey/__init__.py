from otree.api import *
import itertools
import random

doc = """
Survey for Mturk for the stereotypes project. Michael Hilweg, Argun Aman 2023
"""
#todo: think about comprehension and attention checks
#todo write code for how long each question took to answer per participant.
#todo: it seems using multiple rounds creates multiple players
class C(BaseConstants):
    NAME_IN_URL = 'Survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 9
    Tasks_path= 'Survey/tasks/'
    Instruction_path='_templates/instructions.html'
    #note: participation fee is in the session configs #todo make sure this is completion fee not mere participation fee

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
    NV_task=models.FloatField(min=-1)
    Maze_task=models.FloatField(min=-1)
    Count_letters_task=models.FloatField(min=-1)
    Word_puzzle_task=models.FloatField( min=-1)
    Word_order_task=models.FloatField(min=-1)
    Count_numbers_task=models.FloatField( min=-1)
    Ball_bucket_task=models.FloatField(min=-1)
    Word_in_word_task=models.FloatField(min=-1)
    Numbers_in_numbers_task=models.FloatField(min=-1)
    MRT_task=models.FloatField(min=-1)


#### Functions and variables

# list of 9 unique tasks, defined on the participant level to to allow shuffling is in the settings menu
tasks = ['NV_task', 'Maze_task', 'Count_letters_task', 'Word_puzzle_task', 'Word_order_task',
             'Count_numbers_task', 'Ball_bucket_task', 'Word_in_word_task', 'Numbers_in_numbers_task', 'MRT_task']
#todo: make randomize the order make it balanced
#todo: make sure the participant can only move to next page after moving the slider.

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


class Introduction(Page):
    form_model = 'player'
    form_fields = ['gender', 'age']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Choice(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player: Player):
        'dynamically setting the formfield to depend on the round number.'
        current_task = tasks[player.round_number-1]
        # if player.round_number>1: #if we are in round 2 then current player has access to player 1 (who's the same participant) fields
        #     prev_player = player.in_round(player.round_number - 1)
        # else:
        #     prev_player = player
        #
        # if player.round_number>1:
        #     for task in tasks[0:player.round_number-2]:
        #         player.task= getattr(prev_player, task)
        return [current_task]


    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path):
        '''
        1. need the path_task to display the html
        2. need round_number to select the current task using JS
        '''
        round_number = player.round_number
        task = tasks[round_number-1]
        path_task = tasks_path + task + '.html'
        return dict(
            path_task=path_task,
            round_number=round_number,
        )

    @staticmethod
    def js_vars(player: Player):
        'i use the round_number and list of tasks to select the current task using JS, for this i need to pass these to JS in the page'
        dict = {'tasks': tasks, 'round_number': player.round_number}
        return dict

    def before_next_page(player: Player, timeout_happened):
        'updates the participant\'s payoff'
        task = tasks[player.round_number - 1] # get the current task name
        # todo: fix the payoff function
        players_answer = getattr(player, task) #player's answer is stored in player.task field
        true_difference = true_difference_list[task] #get the true difference from the trie_difference_list
        earning_from_question = 1 - (true_difference - players_answer)**2 #calculate earnings of participant
        participant = player.participant #get the participant
        participant.payoff = participant.payoff + earning_from_question #edit the participants earning
        print(f" to the task {task} you answered {players_answer} since the true value is {true_difference} you earn 1- ({true_difference} - {players_answer})^2")




class Results(Page):
    @staticmethod
    def is_displayed(player:Player):
        return player.round_number==C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        participant= player.participant
        participation_fee= participant.payoff_plus_participation_fee() - participant.payoff

        return ({'participation_fee':participation_fee})


page_sequence = [Introduction, Choice,  Results]
