from gbarrier.main import GBarrier
from gphotocell.main import GPhotocell
from qodex_skud_bus import settings


points_description = {'EXTERNAL_GATE': {'superclass': GBarrier, 'description': 'Внешние ворота (с улицы)',
                                        'position': 'external'},
                      'INTERNAL_GATE': {'superclass': GBarrier, 'description': 'Внутренние ворота (с территории)',
                                        'position': 'internal'},
                      'EXTERNAL_PHOTOCELL': {'superclass': GPhotocell, 'description': 'Фотоэлементы на внешних воротах',
                                             'position': 'external'},
                      'INTERNAL_PHOTOCELL': {'superclass': GPhotocell, 'description': 'Фотоэлементы на внутренних воротах',
                                             'position': 'internal'},
                      }


state_descriptions = {'30': {'str_name': settings.normal_state},
                      '31': {'str_name': settings.lock_state},
                      '32': {'str_name': settings.unlock_state}}
