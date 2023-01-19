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
        task = tasks[player.round_number - 1] # get the current task name

        #print(getattr(player, task), player.NV_task)
        players_answer = getattr(player, task) #player's answer is stored in player.task field
        true_difference = true_difference_list[task] #get the true difference from the trie_difference_list
        earning_from_question = 1 - (true_difference - players_answer)**2 #calculate earnings of participant
        #print(f"players answer is {players_answer}")
        participant = player.participant #get the participant
        participant.payoff = participant.payoff + earning_from_question #edit the participants earning
        #print(f" to the task {task} you answered {players_answer} since the true value is {true_difference} you earn 1- ({true_difference} - {players_answer})^2")




class Results(Page):

    @staticmethod
    def is_displayed(player:Player):
        return player.round_number==C.NUM_ROUNDS


page_sequence = [Choice, Results]
