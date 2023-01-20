from otree.api import *
import itertools
import random

doc = """
Survey for Mturk for the stereotypes project. Michael Hilweg, Argun Aman 2023
"""
#todo: think about comprehension and attention checks
#todo write code for how long each question took to answer per participant.
#todo: it seems using multiple rounds creates multiple players
#note: participation fee is in the session configs #todo make sure this is completion fee not mere participation fee

class C(BaseConstants):
    NAME_IN_URL = 'Survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    Tasks_path= 'Survey/tasks/'
    Instruction_path='_templates/instructions.html'
    #list of questions that will be used in the survey
    Tasks= ['NV_task', 'Maze_task', 'Count_letters_task', 'Word_puzzle_task', 'Word_order_task',
             'Count_numbers_task', 'Ball_bucket_task', 'Word_in_word_task', 'Numbers_in_numbers_task', 'MRT_task']

    # Dictionary of true score differences between men and women to be used to calculate payoffs.
    # Positive x implies men answered x percentage points more.
    true_difference_list = {
        'NV_task': 0.05,
        'Maze_task': 0.11,
        'Count_letters_task': -0.07,
        'Word_puzzle_task': 0,
        'Word_order_task': 0.12,
        'Count_numbers_task': 0,
        'Ball_bucket_task': 0,
        'Word_in_word_task': 0,
        'Numbers_in_numbers_task': 0,
        'MRT_task': 0.15
    }

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

#todo: make randomize the order make it balanced
#todo: make sure the participant can only move to next page after moving the slider.





class Introduction(Page):
    form_model = 'player'
    form_fields = ['gender', 'age']




class Ball_bucket_page(Page):
    task= 'Ball_bucket_task'
    form_model = 'player'
    form_fields = [task]

    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path, task=task):
        path_task = tasks_path + task + '.html'
        return dict(path_task=path_task)

    

class Count_letters_page(Page):
    task= 'Count_letters_task'
    form_model = 'player'
    form_fields = [task]

    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path, task=task):
        path_task = tasks_path + task + '.html'
        return dict(path_task=path_task)

    

class Count_numbers_page(Page):
    task= 'Count_numbers_task'
    form_model = 'player'
    form_fields = [task]

    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path, task=task):
        path_task = tasks_path + task + '.html'
        return dict(path_task=path_task)

    

class Maze_page(Page):
    task= 'Maze_task'
    form_model = 'player'
    form_fields = [task]

    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path, task=task):
        path_task = tasks_path + task + '.html'
        return dict(path_task=path_task)

    

class MRT_page(Page):
    task= 'MRT_task'
    form_model = 'player'
    form_fields = [task]

    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path, task=task):
        path_task = tasks_path + task + '.html'
        return dict(path_task=path_task)

    

class Numbers_in_numbers_page(Page):
    task= 'Numbers_in_numbers_task'
    form_model = 'player'
    form_fields = [task]

    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path, task=task):
        path_task = tasks_path + task + '.html'
        return dict(path_task=path_task)

    

class NV_page(Page):
    task= 'NV_task'
    form_model = 'player'
    form_fields = ['NV_task']

    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path, task=task):
        path_task = tasks_path + task + '.html'
        return dict(path_task=path_task)


class Word_in_word_page(Page):
    task= 'Word_in_word_task'
    form_model = 'player'
    form_fields = [task]

    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path, task=task):
        path_task = tasks_path + task + '.html'
        return dict(path_task=path_task)

    

class Word_order_page(Page):
    task= 'Word_order_task'
    form_model = 'player'
    form_fields = [task]

    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path, task=task):
        path_task = tasks_path + task + '.html'
        return dict(path_task=path_task)

    


class Word_puzzle_page(Page):
    task= 'Word_puzzle_task'
    form_model = 'player'
    form_fields = [task]

    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path, task=task):
        path_task = tasks_path + task + '.html'
        return dict(path_task=path_task)

    


class ResultsWaitPage(Page):
    def before_next_page(player: Player, timeout_happened):
        '''
        updates the participant\'s payoff:
        1. loop through the tasks in the C.Tasks list
        2. Get players answer to this task
        3. Compare players answer to the true difference and assign payoff
        '''
        # todo: fix the payoff function
        for task in C.Tasks:
            players_answer = getattr(player, task) #player's answer is stored in player.task field
            true_difference = C.true_difference_list[task] #get the true difference from the trie_difference_list
            earning_from_question = 1 - (true_difference - players_answer)**2 #calculate earnings of participant
            participant = player.participant #get the participant
            participant.payoff = participant.payoff + earning_from_question #edit the participants earning
            print(f" to the task {task} you answered {players_answer} since the true value is {true_difference} you earn 1- ({true_difference} - {players_answer})^2")


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant= player.participant
        participation_fee= participant.payoff_plus_participation_fee() - participant.payoff

        return ({'participation_fee':participation_fee})


page_sequence = [Introduction, NV_page, Maze_page, Count_letters_page, Word_puzzle_page, Word_order_page,
             Count_numbers_page, Ball_bucket_page, Word_in_word_page, Numbers_in_numbers_page, MRT_page, ResultsWaitPage,  Results]
