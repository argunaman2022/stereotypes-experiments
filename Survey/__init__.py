from otree.api import *
import itertools
import random
import math
import time

doc = """
Survey for Mturk for the stereotypes project. Michael Hilweg, Argun Aman 2023
"""
#TODO: when running small session adjust quota size.

#%%
class C(BaseConstants):
    NAME_IN_URL = 'Survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10 + 2  # 10  tasks  and 2 attention checks
    Tasks_path = 'Survey/tasks/'
    Instruction_path = '_templates/global/Instructions.html'
    Participation_fee = 0.5
    Max_bonus_payment = 2
    Bonus_multiplier = 4
    Quota_size = 100 #quota size #TODO: change it to 500/4
    Max_time_allowed = 3600 #1 hour
    Attention_Check_1_Place = 1  # on which page should the attention 1 check appear
    Attention_Check_2_Place = 5  # on which page should the attention 2 check appear


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    'initialize the quotas to 0'
    subsession.session.quota = {
    'quota_Male_Creative':0,
    'quota_Male_MRT':0,
    'quota_Female_Creative':0,
     'quota_Female_MRT':0
    }
    
    for p in subsession.get_players():
        #initialize the comprehension and attention checks to 1 i.e. True, theyll be set to 0 if participant fails them.
        p.participant.comprehension_check_1, p.participant.comprehension_check_2 = 1, 1
        p.participant.attention_2, p.participant.attention_1 = 1, 1
        
        p.gender = 'default' #need to set the gender to default so i can access and edit it later...
        p.participant.expiry = 0 #set the expiry to 0 so i can access and edit it later...


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    age = models.IntegerField(min=18, max=99)
    gender = models.StringField(choices=['Male', 'Female', 'Transgender female', 'Transgender male', 'Non binary'])
    race = models.StringField(
        choices=['White', 'Black or African American', 'American Indian or Alaska Native', 'Asian',
                 'Native Hawaiian or Other Pacific Islander', 'Other'])
    state = models.StringField(
        choices=["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut",
                 "District of Columbia", "Delaware",
                 "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky",
                 "Louisiana", "Massachusetts", "Maryland",
                 "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina",
                 "North Dakota", "Nebraska", "New Hampshire", "New Jersey",
                 "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico",
                 "Rhode Island", "South Carolina", "South Dakota",
                 "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin",
                 "West Virginia", "Wyoming"])
    education = models.StringField(label="Educational Attainment",
                                   choices=["Less than High School", "High School Graduate",
                                            "Some College/Associate Degree", "Bachelor's Degree", "Advanced Degree"])
    
    # whether they clicked on the detailed payment explanation
    payment_checked = models.StringField(choices=['Read', 'NotRead'], initial='NotRead')
    # SURVEY - 11 questions = 10 + 1 Attention_Check
    ComprehensionCheck_task = models.IntegerField(initial=1) #1==True
    # set initially to true, will turn to false if player fails the attention check, make sure to create the same field in the participant level.
    Attention_Check_1 = models.IntegerField(initial=1) #1==True
    Attention_Check_2 = models.IntegerField(initial=1)

    @staticmethod
    def defined_min():
        return -math.inf
    # 10 survey questions (remember: 10 survey questions, 2 attention checks in the choice Page.)
    NV_task = models.FloatField(min=defined_min())
    Maze_task = models.FloatField(min=defined_min())
    Count_letters_task = models.FloatField(min=defined_min())
    Word_puzzle_task = models.FloatField(min=defined_min())
    Word_order_task = models.FloatField(min=defined_min())
    Count_numbers_task = models.FloatField(min=defined_min())
    Ball_bucket_task = models.FloatField(min=defined_min())
    Word_in_word_task = models.FloatField(min=defined_min())
    Numbers_in_numbers_task = models.FloatField(min=defined_min())
    MRT_task = models.FloatField(min=defined_min())
    MRT_task_creative = models.FloatField(min=defined_min())

#%% FUNCTIONS AND VARIABLES
def every_day(player: Player, treatment):

    '''
    in this function to each participant i assign a random task order depending on his treatment 
                        as well as chosing the payoff relevant task
    1. make sure to create the "shuffled_tasks_incl_Attention_Check" in the settings.py participant field
    2. shuffle the tasks before assigning the participant
    3. Insert the attention check page in the C.Attention_Check - 1 place (3rd page for C.Attention_Check=3)
    4. make sure this code is only run in the first round. alternatively one can set a seed for shuffling.
    5. IMPORTANT! MAKE SURE TO USE player.participant.shuffled_tasks_incl_Attention_Check instead of tasks
    '''

    if treatment == 'MRT':
        shuffled_tasks = tasks_excl_attention
    else:
        shuffled_tasks = tasks_excl_attention_creative
    random.shuffle(shuffled_tasks)

    # randomly choose a task to be payment relevant and assign to the participant field from the list of 10 tasks.
    player.participant.payment_relevant_task = random.choice(shuffled_tasks)  
    
    player.participant.shuffled_tasks_incl_Attention_Check = (shuffled_tasks[0:C.Attention_Check_1_Place - 1]+ ['Attention_Check_1'] +
                                                             shuffled_tasks[C.Attention_Check_1_Place - 1:C.Attention_Check_2_Place - 1] + 
                                                             ['Attention_Check_2'] + shuffled_tasks[C.Attention_Check_2_Place - 1:])

def assign_quota(gender, player):
    '''
    here we assign the participant to a proper treatment: 
    1. we have 4 treatments: (creative, mrt) x (male, female)
    2. non binaries and transgendas are assigned to one of the 4 treatments randomly given quota is empty
    3. binaries are assigned to one of the two treatments randomly given both quotas are below C.quota_size 
        and these quotas are incremented.
        3.1 if the C.quota_size is full for both, they are kicked
        3.1 if C.quota_size is full for one but not the other s/he is assigned to the quota.
    '''
    if gender in ['Female', 'Male']:
        # this if statement checks whether both quotas are not full
        if (player.session.quota[f"quota_{gender}_Creative"] < C.Quota_size 
            and player.session.quota[f"quota_{gender}_MRT"] < C.Quota_size):
            assigned_treatment = random.choice(['MRT', 'Creative'])
        elif  player.session.quota[f"quota_{gender}_Creative"] < C.Quota_size:
            assigned_treatment = 'Creative'
        elif  player.session.quota[f"quota_{gender}_MRT"] < C.Quota_size:
            assigned_treatment = 'MRT'
        else: 
            assigned_treatment = 'QUOTA_FULL'
        
        if assigned_treatment is not 'QUOTA_FULL':
            'increment the quotas if the participant is assigned to a quota and is binary'
            player.session.quota[f"quota_{gender}_{assigned_treatment}"] += 1
    else:
        #i.e. if they're non-binary
        assigned_treatment = random.choice(['MRT', 'Creative'])       
    #store this in the participant level
    player.participant.treatment = assigned_treatment

def decrement_quota(player):
    '''
    decrements quota the participant belonged to in case he fails a comprehension or attention check
    '''
    gender = player.participant.gender
    assigned_treatment = player.participant.treatment
    if gender in ['Male', 'Female']:
        player.session.quota[f"quota_{gender}_{assigned_treatment}"] -= 1

# This is the list of tasks excluding the attention check. Note that in settings.py on the participant level shuffled_tasks_incl_Attention_Check is stored.
tasks_excl_attention = ['NV_task', 'Maze_task', 'Count_letters_task', 'Word_puzzle_task', 'Word_order_task',
                        'Count_numbers_task', 'Ball_bucket_task', 'Word_in_word_task', 'Numbers_in_numbers_task',
                        'MRT_task']

tasks_excl_attention_creative = tasks_excl_attention + ['MRT_task_creative']
tasks_excl_attention_creative.remove('MRT_task')

# Dictionary of true score differences between men and women to be used to calculate payoffs. Positive x implies men answered x percentage points more. Manually coded
true_difference_list = {
    'ComprehensionCheck_task': 0.5,
    'NV_task': 0.05,
    'Maze_task': 0.11,
    'Count_letters_task': -0.07,
    'Word_puzzle_task': 0,
    'Word_order_task': 0.12,
    'Count_numbers_task': 0,
    'Ball_bucket_task': 0,
    'Word_in_word_task': 0,
    'Numbers_in_numbers_task': 0,
    'MRT_task': 0.15,
    'MRT_task_creative': 0.15
}
#%% Classes
class Demographics(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'race', 'education', 'state']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == 1:
            assign_quota(player.gender, player) #assigns the participant to a quota and treatment
            every_day(player, player.participant.treatment) # depending on treatment shuffle his tasks
            player.participant.gender = player.gender              

class Introduction(Page):
    form_model = 'player'
    form_fields = ['payment_checked']
       
    @staticmethod
    def is_displayed(player: Player):
        return (player.participant.comprehension_check_2 == 1 and player.round_number == 1 
                and player.participant.treatment != 'QUOTA_FULL')
        
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.expiry = time.time() + C.Max_time_allowed


class ComprehensionCheck_1(Page):
    '''
    1. first the participant goes through comprehension check 1 page. if he fails this page,
       then he is shown the same page again in comprehension check 2 page. if he fails this again he is out!
    '''
    form_model = 'player'
    form_fields = ['ComprehensionCheck_task']
    
    def get_timeout_seconds(player):
        return player.participant.expiry - time.time()

    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.participant.treatment is not 'QUOTA_FULL'

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'path_task': C.Tasks_path + 'ComprehensionCheck_task.html',
        }
    
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == 1:
            player.participant.comprehension_check_1 = player.ComprehensionCheck_task 

class ComprehensionCheck_2(Page):
    '''
    1. the second comprehension check in case the participant fails the first one i.e his second try
    '''
    form_model = 'player'
    form_fields = ['ComprehensionCheck_task']

    def get_timeout_seconds(player):
        return player.participant.expiry - time.time()
    
    @staticmethod
    def is_displayed(player: Player):
        participant=player.participant
        return (player.round_number == 1 and participant.comprehension_check_1 == 0 
                and participant.comprehension_check_2 == 1 and player.participant.treatment != 'QUOTA_FULL')
    
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'path_task': C.Tasks_path + 'ComprehensionCheck_task.html',
        }
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == 1:
            player.participant.comprehension_check_2 = player.ComprehensionCheck_task
        if player.ComprehensionCheck_task == 0:
            # print(f"before decrement{str(player.subsession.session.quota)}")
            decrement_quota(player)
            # print(f"after decrement{str(player.subsession.session.quota)}")
            

class Choice(Page):
    '''
    1. Show the question from the shuffled list and elicit an answer
    2. store the answer in a player level
    3. calculate payoffs from this question and update participant payoff
    '''
    form_model = 'player'

    def get_timeout_seconds(player):
        return player.participant.expiry - time.time()

    @staticmethod
    def get_form_fields(player: Player):
        'dynamically setting the formfield to depend on the round number.'
        current_task = player.participant.shuffled_tasks_incl_Attention_Check[player.round_number - 1]
        return [current_task]

    def is_displayed(player: Player):
        return (player.participant.attention_1 == 1 and player.participant.attention_2 == 1 
                and player.participant.comprehension_check_2 == 1
                and player.participant.treatment != 'QUOTA_FULL' and player.participant.expiry > time.time())

    @staticmethod
    def vars_for_template(player: Player, tasks_path=C.Tasks_path):
        '''
        1. need the path_task to display the html
        2. need round_number to select the current task using JS
        '''
        round_number = player.round_number
        task = player.participant.shuffled_tasks_incl_Attention_Check[round_number - 1]
        path_task = tasks_path + task + '.html'
        return dict(path_task=path_task,
                    round_number=round_number,
                    amount_questions=C.NUM_ROUNDS)

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
        participant = player.participant 
        
        
        
        #current task
        task = participant.shuffled_tasks_incl_Attention_Check[
            player.round_number - 1]  
        if task == "Attention_Check_1":
            players_attention = getattr(player, task)  # false if they failed the Attention_Check
            participant.attention_1 = players_attention
            if players_attention == 0:
                decrement_quota(player)
        elif task == "Attention_Check_2":
            players_attention = getattr(player, task)  # false if they failed the Attention_Check
            participant.attention_2 = players_attention
            if players_attention == 0:
                decrement_quota(player)
        elif task == participant.payment_relevant_task:
            players_answer = getattr(player, task)  # player's answer is stored in player.task field
            true_difference = true_difference_list[task]  # get the true difference from the trie_difference_list
            participant.payoff = C.Participation_fee + max(0, C.Max_bonus_payment - abs(
                true_difference - players_answer) * C.Bonus_multiplier)  # save the participant payoff in its field, note that payoff doesnt include the part. fee
            # print(
            #     f"{participant.payment_relevant_task} was chosen for payment. To the task {task} you answered {players_answer} since the true value is {true_difference} you earn {C.Participation_fee} + max(0,({C.Max_bonus_payment}-abs({true_difference} - {players_answer})*{C.Bonus_multiplier})={participant.payoff} USD in total.")

        if player.round_number == C.NUM_ROUNDS and (participant.attention_1 == 0 or participant.attention_2 == 0
                                                    or participant.comprehension_check_2 == 0):
            # set the participant payoff to 0 if he has failed any of the attention checks or comprehension check.
            participant.payoff = 0
            
class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number == C.NUM_ROUNDS and player.participant.comprehension_check_2 == 1 and 
                player.participant.attention_1 == 1 and player.participant.attention_2 == 1 and 
                player.participant.treatment is not 'QUOTA_FULL' and player.participant.expiry > time.time())

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        participation_fee = C.Participation_fee
        bonus_payment = participant.payoff - participation_fee

        return ({'participation_fee': participation_fee, 'bonus_payment': bonus_payment})

class Results_failed_comprehension(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and player.participant.comprehension_check_2 == 0 

class Results_failed_attention(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number == C.NUM_ROUNDS and  player.participant.expiry > time.time() and 
                player.participant.attention_1 == 0 or player.participant.attention_2 == 0)

class Quota_Full(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and player.participant.treatment == 'QUOTA_FULL'
    
class TimeOut(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and player.participant.treatment != 'QUOTA_FULL' and player.participant.expiry < time.time()


page_sequence = [ Demographics, Introduction, ComprehensionCheck_1, ComprehensionCheck_2,  
                  Choice, Results, Results_failed_attention,
                  Results_failed_comprehension, Quota_Full, TimeOut]