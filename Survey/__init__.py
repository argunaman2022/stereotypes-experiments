from otree.api import *
import itertools
import random
import math

doc = """
Survey for Mturk for the stereotypes project. Michael Hilweg, Argun Aman 2023
"""
#todo: think about attention checks
#todo: hide the debug menu before publishing
#todo : grant qualification id to avoid repeat takes.
#todo: remove the codes for comprehension check
#todo: add a noise measurement per participant: fix the second question and repeat it in the 10th place, the differeince in the difference is taken as noise in decision.
class C(BaseConstants):
    NAME_IN_URL = 'Survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10 + 1 # 10  tasks  and an attention check
    Tasks_path= 'Survey/tasks/'
    Instruction_path='_templates/global/Instructions.html'
    Participation_fee= 0.5
    Max_bonus_payment=2
    Bonus_multiplier=4
    Attention_Check_Place = 3 # on which page should the attention check appear

class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    #demographics
    age = models.IntegerField(min=18, max=99)
    gender = models.StringField(choices=['Male','Female','Other'], widget=widgets.RadioSelect)
    race = models.StringField(choices=['White','Black or African American', 'American Indian or Alaska Native','Asian','Native Hawaiian or Other Pacific Islander','Other'])
    state = models.StringField(choices=["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware",
                                        "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland",
                                        "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey",
                                        "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota",
                                        "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"])
    education = models.StringField(label = "Educational Attainment", choices=["Less than High School","High School Graduate","Some College/Associate Degree","Bachelor's Degree","Advanced Degree"])
    #comprehension check
    attempts=models.IntegerField(min=-1000, initial=3)
    payment_checked=models.StringField( choices=['Read', 'NotRead'], initial='NotRead')
    #SURVEY - 11 questions = 10 + 1 Attention_Check
    ComprehensionCheck_task=models.FloatField(min=-1)
    # set initially to true, will turn to false if player fails the attention check, make sure to create the same field in the participant level.
    Attention_Check= models.IntegerField(initial = 1)

    @staticmethod
    def defined_min():
        return -math.inf
    NV_task=models.FloatField(min=defined_min())
    Maze_task=models.FloatField(min=defined_min())
    Count_letters_task=models.FloatField(min=defined_min())
    Word_puzzle_task=models.FloatField( min=defined_min())
    Word_order_task=models.FloatField(min=defined_min())
    Count_numbers_task=models.FloatField( min=defined_min())
    Ball_bucket_task=models.FloatField(min=defined_min())
    Word_in_word_task=models.FloatField(min=defined_min())
    Numbers_in_numbers_task=models.FloatField(min=defined_min())
    MRT_task=models.FloatField(min=defined_min())

#Functions and variables go here
#This is the list of tasks excluding the attention check. Note that in settings.py on the participant level shuffled_tasks_incl_Attention_Check is stored.
tasks_excl_attention = ['NV_task', 'Maze_task', 'Count_letters_task', 'Word_puzzle_task', 'Word_order_task',
                         'Count_numbers_task', 'Ball_bucket_task', 'Word_in_word_task', 'Numbers_in_numbers_task', 'MRT_task']

#Dictionary of true score differences between men and women to be used to calculate payoffs. Positive x implies men answered x percentage points more. Manually coded
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
#Pages
class Demographics(Page):
    '''
    1. ask for demographics
    2. assign the participant field 'attempts' an initial value of 3 only if it is round 1.
    '''
    form_model = 'player'
    form_fields = ['gender', 'age', 'race', 'education','state']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == 1:
            #this field must be created on the participant level in settings.py
            player.participant.attempts = 3
            player.participant.attention = 1

class ComprehensionCheck(Page):
    '''
    1. Participant starts with 3 attempts.
    2. Ask the participant to submit an answer to the comprehension check, store how many attempts they needed to solve.
    3. Store this number in the participant field. Participants can only proceed if this value is greater than 0 i.e. if they did not fail.
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
            player.participant.attempts= player.attempts #initialize the participant.attempts field with player.attempts.

class Introduction(Page):
    '''
    1. Show introduction as well as description of what's to follow
    2. Shuffle tasks and assign it to the participant field
    3. Check if participant clicks on the exact payment description.
    '''

    form_model = 'player'
    form_fields = ['payment_checked']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.participant.attempts >= 1

    def before_next_page(player: Player, timeout_happened):
        '''in this function to each participant i assign a random task order:
        1. make sure to create the "shuffled_tasks_incl_Attention_Check" in the settings.py participant field
        2. shuffle the tasks before assigning the participant
        3. Insert the attention check page in the C.Attention_Check - 1 place (3rd page for C.Attention_Check=3)
        4. make sure this code is only run in the first round. alternatively one can set a seed for shuffling.
        5. IMPORTANT! MAKE SURE TO USE player.participant.shuffled_tasks_incl_Attention_Check instead of tasks
        '''
        if player.round_number == 1:
            random.shuffle(tasks_excl_attention)
            player.participant.payment_relevant_task = random.choice(
                tasks_excl_attention)  # randomly choose a task to be payment relevant and assign to the participant field from the list of 10 tasks.
            # print(f"the randomly chosen task is {participant.payment_relevant_task}")
            tasks = tasks_excl_attention
            if 'Attention_Check' not in tasks:
                print(C.Attention_Check_Place)
                #tasks.insert(C.Attention_Check_Place-1,'Attention_Check') #insert the attention check in the page order
                tasks = tasks[0:C.Attention_Check_Place-1] + ['Attention_Check'] + tasks[C.Attention_Check_Place-1:]
            player.participant.shuffled_tasks_incl_Attention_Check = tasks
            print(player.participant.shuffled_tasks_incl_Attention_Check)

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
        current_task = player.participant.shuffled_tasks_incl_Attention_Check[player.round_number-1]
        return [current_task]
    def is_displayed(player: Player):
        # those who failed the comprehension check or the attention check won't see this page
        return player.participant.attempts >= 1 & player.participant.attention == 1

    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path):
        '''
        1. need the path_task to display the html
        2. need round_number to select the current task using JS
        '''
        round_number = player.round_number
        task = player.participant.shuffled_tasks_incl_Attention_Check[round_number-1]
        path_task = tasks_path + task + '.html'
        return dict(path_task=path_task,
                    round_number=round_number,
                    amount_questions= C.NUM_ROUNDS)

    @staticmethod
    def js_vars(player: Player):
        'i use the round_number and list of tasks to select the current task using JS, for this i need to pass these to JS in the page'
        dict = {'tasks': player.participant.shuffled_tasks_incl_Attention_Check, 'round_number': player.round_number}
        return dict

    def before_next_page(player: Player, timeout_happened):
        '''
        Updates participant payoff.
        1 out of 10 tasks is randomly chosen for payment.
        We randomly choose this task and store it on the participant field 'payment_relevant_task'.
        Then, we update the participant's payoff using the following function bonus payment = max(C.Max_bonus_payment - C.Bonus_multiplier* abs(true_value-participant's answer),0). total payment = bonus payment + completion fee
        '''
        participant = player.participant  # get the participant

        task = participant.shuffled_tasks_incl_Attention_Check[player.round_number - 1] # get the current task name depending on round number
        if task == "Attention_Check":
            players_attention = getattr(player, task)  # false if they failed the Attention_Check
            participant.attention = players_attention


        elif task == participant.payment_relevant_task:
            players_answer = getattr(player, task) #player's answer is stored in player.task field
            true_difference = true_difference_list[task] #get the true difference from the trie_difference_list
            participant.payoff = C.Participation_fee +  max(0,C.Max_bonus_payment-abs(true_difference - players_answer) * C.Bonus_multiplier) #save the participant payoff in its field, note that payoff doesnt include the part. fee
            print(f"{participant.payment_relevant_task} was chosen for payment. To the task {task} you answered {players_answer} since the true value is {true_difference} you earn {C.Participation_fee} + max(0,({C.Max_bonus_payment}-abs({true_difference} - {players_answer})*{C.Bonus_multiplier})={participant.payoff} USD in total.")

class Results(Page):
    @staticmethod
    def is_displayed(player:Player):
        return player.round_number==C.NUM_ROUNDS and player.participant.attempts >= 1 and player.participant.attention == 1

    @staticmethod
    def vars_for_template(player: Player):
        participant= player.participant
        participation_fee= C.Participation_fee
        bonus_payment = participant.payoff - participation_fee

        return ({'participation_fee':participation_fee, 'bonus_payment': bonus_payment})

class Results_failed_comprehension(Page):
    @staticmethod
    def is_displayed(player:Player):
        return player.round_number==C.NUM_ROUNDS and player.participant.attempts <= 1

    def before_next_page(player: Player, timeout_happened):
        '''
        Sets the participant completion fee to 0 if the participant failed the comprehension check
        '''
        participant = player.participant  # get the participant

        if player.round_number==C.NUM_ROUNDS and player.participant.attempts <= 1:
            participant.payoff = 0



class Results_failed_attention(Page):
    @staticmethod
    def is_displayed(player:Player):
        return player.round_number==C.NUM_ROUNDS and player.participant.attention == 0

    def before_next_page(player: Player, timeout_happened):
        '''
        Sets the participant completion fee to 0 if the participant failed the attention check
        '''
        participant = player.participant  # get the participant

        if player.round_number == C.NUM_ROUNDS and participant.attention == 0:
            participant.payoff = 0

page_sequence = [Demographics, Introduction,  Choice,  Results, Results_failed_attention]
