from gbarrier.main import GBarrier
from gphotocell.main import GPhotocell

points_description = {'EXTERNAL_GATE': {'superclass': GBarrier, 'description': 'Внешние ворота (с улицы)',
                                        'position': 'external'},
                      'INTERNAL_GATE': {'superclass': GBarrier, 'description': 'Внутренние ворота (с территории)',
                                        'position': 'internal'},
                      'EXTERNAL_PHOTOCELL': {'superclass': GPhotocell, 'description': 'Фотоэлементы на внешних воротах',
                                             'position': 'external'},
                      'INTERNAL_PHOTOCELL': {'superclass': GPhotocell, 'description': 'Фотоэлементы на внутренних воротах',
                                             'position': 'internal'},
                      }


state_descriptions = {'30': {'str_name': 'ONLINE_NORMAL'},
                       '31': {'str_name': 'ONLINE_LOCKED'},
                       '32': {'str_name': 'ONLINE_UNLOCKED'}}
