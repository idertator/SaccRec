# Subject Parameters
from PyQt5.QtGui import QColor

DEBUG = True

DATE_FORMAT = '%d/%m/%Y'
DATETIME_FORMAT = '%d/%m/%Y %H:%M'

GENRES = (
    ('Unknown', 'Desconocido'),
    ('Male', 'Masculino'),
    ('Female', 'Femenino'),
)

SUBJECT_STATUSES = (
    ('Unknown', 'Desconocido'),
    ('Control', 'Control'),
    ('Presymptomatic', 'Presintomático'),
    ('SCA2', 'SCA2'),
)

OPENBCI_SAMPLE_RATES = (
    (250, '250'),
    (500, '500'),
    (1000, '1000'),
    (2000, '2000'),
    (4000, '4000'),
    (8000, '8000'),
    (16000, '16000'),
)

GENRES_DICT = {value: index for index, (value, _) in enumerate(GENRES)}
SUBJECT_STATUSES_DICT = {value: index for index, (value, _) in enumerate(SUBJECT_STATUSES)}
SUBJECT_STATUSES_LABELS = {value: label for value, label in SUBJECT_STATUSES}

SETTINGS_OPENBCI_DEFAULT_SAMPLE_RATE = 250

# Stimulus Parameters
STIMULUS_DEFAULT_ANGLE = 30
STIMULUS_MINIMUM_ANGLE = 10
STIMULUS_MAXIMUM_ANGLE = 60

DEFAULT_TESTS_COUNT = 1

STIMULUS_DEFAULT_DURATION = 3.0
STIMULUS_DEFAULT_VARIABILITY = 50.0

STIMULUS_DEFAULT_SACCADES = 10
STIMULUS_MINUMUM_SACCADES = 5
STIMULUS_MAXIMUM_SACCADES = 100

SETTINGS_STIMULUS_SCREEN_DEFAULT_WIDTH = 30.0
SETTINGS_STIMULUS_SCREEN_DEFAULT_WIDTH_MINIMUM = 10.0
SETTINGS_STIMULUS_SCREEN_DEFAULT_WIDTH_MAXIMUM = 200.0

SETTINGS_STIMULUS_SCREEN_DEFAULT_HEIGHT = 17.0
SETTINGS_STIMULUS_SCREEN_DEFAULT_HEIGHT_MINIMUM = 10.0
SETTINGS_STIMULUS_SCREEN_DEFAULT_HEIGHT_MAXIMUM = 200.0

SETTINGS_STIMULUS_SACCADIC_DISTANCE_MINIMUM = 5.0
SETTINGS_STIMULUS_SACCADIC_DISTANCE_MAXIMUM = SETTINGS_STIMULUS_SCREEN_DEFAULT_WIDTH_MAXIMUM - 2

SETTINGS_OPENBCI_DEFAULT_GAIN = 24
SETTINGS_OPENBCI_DEFAULT_CHANNEL_NUMBER = 8

SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS = 0.5
SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS_MINIMUM = 0.1
SETTINGS_DEFAULT_STIMULUS_BALL_RADIUS_MAXIMUM = 1.0

SETTINGS_DEFAULT_STIMULUS_BALL_COLOR = QColor(255, 255, 255)
SETTINGS_DEFAULT_STIMULUS_BACKGROUND_COLOR = QColor(0, 0, 0)

