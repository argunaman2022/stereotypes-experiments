from os import environ

SESSION_CONFIGS = [
    dict(name='survey',app_sequence=['Survey'],num_demo_participants=100)
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    #NOTE: our participation fee is hardcoded into our bonus payment so we can exclude those who fail the comprehension check from receiving anything.
    real_world_currency_per_point=1.00, participation_fee=0, doc="",
    mturk_hit_settings=dict( #todo: where do i specify completion code?
        keywords='bonus, study',
        #todo: change title
        title='An academic survey', #todo: work on title if needbe
        #todo: work on study desc.
        description=''' 
        In this study you will be asked 10 survey questions. In each question your task is to guess performance of past study participants.
        You will be paid a completion fee as well as a bonus fee which depends on how close your answers are to the true values.
        ''',
        frame_height=500,
        template='global/mturk_template.html',
        minutes_allotted_per_assignment=60,
        expiration_hours=7 * 24,
        qualification_requirements=[
        # Only US
        {
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}]
        },
        # At least 500 HITs approved
        {
            'QualificationTypeId': "00000000000000000040",
            'Comparator': "GreaterThanOrEqualTo",
            'IntegerValues': [500]
        },
        # At least 95% of HITs approved
        {
            'QualificationTypeId': "000000000000000000L0",
            'Comparator': "GreaterThanOrEqualTo",
            'IntegerValues': [97]
        }
        ]
        # grant_qualification_id='YOUR_QUALIFICATION_ID_HERE', # to prevent retakes #todo: learn how to do this
    )
)

PARTICIPANT_FIELDS = ['shuffled_tasks_incl_Attention_Check', 'payment_relevant_task', 
                      'comprehension_check_1', 'comprehension_check_2', 'attention_1',
                       'attention_2', 'treatment']
SESSION_FIELDS = {
    'quota':{}
}

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False


ADMIN_USERNAME = 'admin'
OTREE_AUTH_LEVEL = 'DEMO'
# for security, best to set admin password in an environment variable
#ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
ADMIN_PASSWORD = 'Margun-2023TEST'

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9730735539450'
