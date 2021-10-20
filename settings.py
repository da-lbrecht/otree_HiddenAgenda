from os import environ

SESSION_CONFIGS = [
    dict(
        name='delphi',
        app_sequence=['delphi'],
        num_demo_participants=4,
        participation_fee=5,
        use_browser_bots=False, # Play experiment with bots, as long as programmed bots are available
    ),
    dict(
        name='delphi_hiddenagenda',
        app_sequence=['delphi_hiddenagenda'],
        num_demo_participants=4,
        participation_fee=5,
        use_browser_bots=False,  # Play experiment with bots, as long as programmed bots are available
    ),
    dict(
        name='vc_ftf',
        app_sequence=['vc_ftf'],
        num_demo_participants=4,
        participation_fee=5,
        use_browser_bots=False,  # Play experiment with bots, as long as programmed bots are available
    ),
    dict(
        name='vc_ftf_hiddenagenda',
        app_sequence=['vc_ftf_hiddenagenda'],
        num_demo_participants=4,
        participation_fee=5,
        use_browser_bots=False,  # Play experiment with bots, as long as programmed bots are available
    ),
]

ROOMS = [
    dict(
        name='demo',
        display_name='Demo',
        participant_label_file='_rooms/demo.txt',
        use_secure_urls=True
    ),
    dict(
        name='econ_lab',
        display_name='BEElab',
        participant_label_file='_rooms/beelab.txt',
        use_secure_urls=True
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '3970727780349'

# Environment variables
DATABASE_URL = 'postgres://postgres@localhost/hiddenagenda_db'
OTREE_PRODUCTION = 1  # uncomment this line to enable production mode
OTREE_AUTH_LEVEL = 'DEMO'
