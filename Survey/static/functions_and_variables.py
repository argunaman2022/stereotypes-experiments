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