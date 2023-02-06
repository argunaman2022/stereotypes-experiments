from otree.api import *
import itertools
import random

doc = """
Survey for Mturk for the stereotypes project. Michael Hilweg, Argun Aman 2023
"""
#todo: think about comprehension and attention checks
#todo write code for how long each question took to answer per participant.
#todo: it seems using multiple rounds creates multiple players
#todo: qualifiaction requirements for mturk
#todo: hide the debug menu before publishing
#todo: currently using psycopg2-binary because of an issue at render.com [see requirements.txt], one should best use no binary.
class C(BaseConstants):
    NAME_IN_URL = 'Survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10
    Tasks_path= 'Survey/tasks/'
    Instruction_path='_templates/global/Instructions.html'
    #note: participation fee is in the session configs #todo make sure this is completion fee not mere participation fee

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    age=models.IntegerField(min=16, max=99)
    gender=models.StringField(choices=['Male','Female','Other'], widget=widgets.RadioSelect)
    attempts=models.IntegerField(min=-1000, initial=3)

    'The following are hidden fields which we will manually assign after the participant confirms the slider input.'
    ComprehensionCheck_task=models.FloatField(min=-1)
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

#Functions and variables

#This is the list of tasks. Note that in settings.py on the participant level shuffled_tasks is stored.
tasks = ['NV_task', 'Maze_task', 'Count_letters_task', 'Word_puzzle_task', 'Word_order_task',
             'Count_numbers_task', 'Ball_bucket_task', 'Word_in_word_task', 'Numbers_in_numbers_task', 'MRT_task']

#Dictionary of true score differences between men and women to be used to calculate payoffs. Positive x implies men answered x percentage points more.
true_difference_list={
    'ComprehensionCheck_task':0.5,
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

class Demographics(Page):
    '''
    1. ask for gender and age
    2. assign the participant field 'attempts' an initial value of 3 only if it is round 1.
    '''
    form_model = 'player'
    form_fields = ['gender', 'age']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == 1:
            # make sure to create this participant field in the settings file
            player.participant.attempts = 3

class ComprehensionCheck(Page):
    '''
    1. Participant starts with 3 attempts.
    2. Ask the participant to submit an answer to the comprehension check, store how many attempts they needed to solve.
    3. Store this number in the partiicpant field. Participant can only proceed if this value is greater than 0 i.e. if they did not fail
    '''
    form_model = 'player'
    form_fields = ['ComprehensionCheck_task', 'attempts']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'path_task': C.Tasks_path + 'ComprehensionCheck_task.html',
            'Allowed_number_attempts': player.attempts
        }
    def js_vars(player: Player):
        return {'Allowed_number_attempts': player.participant.attempts}
    def before_next_page(player: Player, timeout_happened):
        if player.round_number==1:
            player.participant.attempts= player.attempts

class Introduction(Page):
    '''
    1. Show introduction as well as description of whats to follow
    2. Shuffle tasks and assign it to the participant field
    '''
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.participant.attempts>=0

    def before_next_page(player: Player, timeout_happened):
        '''in this function to each participant i assign a random task order:
        1. make sure to create the "shuffled_tasks" in the settings.py participant field
        2. shuffle the tasks before assigning the participant
        3. make sure this code is only run in the first round. alternatively one can set a seed for shuffling.
        4. IMPORTANT! MAKE SURE TO USE player.participant.shuffled_tasks instead of tasks
        '''
        if player.round_number==1:
            random.shuffle(tasks)
            print(tasks)
            player.participant.shuffled_tasks= tasks


class Choice(Page):
    '''
    1. Show the question from the shuffled list and elicit an answer
    2. store the answer in a player level
    3. calculate payoffs from this question and update participant payoff
    '''
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        'dynamically setting the formfield to depend on the round number.'
        current_task = player.participant.shuffled_tasks[player.round_number-1]
        return [current_task]
    def is_displayed(player: Player):
        return player.participant.attempts >= 1 #those who failed the comprehension check wont see this page

    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path):
        '''
        1. need the path_task to display the html
        2. need round_number to select the current task using JS
        '''
        round_number = player.round_number
        task = player.participant.shuffled_tasks[round_number-1]
        path_task = tasks_path + task + '.html'
        return dict(path_task=path_task,
                    round_number=round_number,
                    amount_questions= C.NUM_ROUNDS)

    @staticmethod
    def js_vars(player: Player):
        'i use the round_number and list of tasks to select the current task using JS, for this i need to pass these to JS in the page'
        dict = {'tasks': player.participant.shuffled_tasks, 'round_number': player.round_number}
        return dict

    def before_next_page(player: Player, timeout_happened):
        'updates the participant\'s payoff'
        task = player.participant.shuffled_tasks[player.round_number - 1] # get the current task name
        # todo: fix the payoff function
        players_answer = getattr(player, task) #player's answer is stored in player.task field
        true_difference = true_difference_list[task] #get the true difference from the trie_difference_list
        value = 0.5 - (true_difference - players_answer) ** 2
        earning_from_question = max(0,value) #calculate earnings of participant, min 0
        participant = player.participant #get the participant
        participant.payoff = participant.payoff + earning_from_question #edit the participants earning
        print(f" to the task {task} you answered {players_answer} since the true value is {true_difference} you earn 0.5- ({true_difference} - {players_answer})^2={value}")

class Results(Page):
    @staticmethod
    def is_displayed(player:Player):
        return player.round_number==C.NUM_ROUNDS and player.participant.attempts >= 0

    @staticmethod
    def vars_for_template(player: Player):
        participant= player.participant
        participation_fee= participant.payoff_plus_participation_fee() - participant.payoff

        return ({'participation_fee':participation_fee})


page_sequence = [Demographics, ComprehensionCheck, Introduction,  Choice,  Results]
