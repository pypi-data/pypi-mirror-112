from sigur_interact.main import SigurSDK
from qodex_skud_bus import functions
from traceback import format_exc
from qpi.main import QPI
from qodex_skud_bus import points_logic
from qodex_skud_bus.exceptions import exceptions
from qodex_skud_bus import settings


class QodexSkudBus:
    def __init__(self, skud_ip, skud_port, points_list=None,
                 skud_test_mode=False, *args, **kwargs):
        """ Points_list - список словарей, описывающих все подключенные точки доступа, имеет вид, типа:
        [{'point_name': str, 'point_num':int, 'point_type': str}],
        где point_name - произвольное имя точки доступа,
        point_num - числовой идентификатор точки доступа,
        point_type - тип точки доступа (Фотоэлемент, Внешний шлагбаум и т.п(описание задано в файле points_logic)),
        linked_point - числовой идентификатор связанной точки доступа (например, фотоэелемента, если мы
        рассматриваем шлагбаум)"""
        if points_list is None:
            points_list = []
        self.points_list = points_list
        self.skud_sdk = SigurSDK(skud_ip, skud_port, 1, 2, 3, 4,
                                 test_mode=skud_test_mode)
        self.skud_sdk.set_external_react_function(self.message_operator)    # После каждого нового события вызывать заданую функцию
        self.skud_sdk.start_listen_thread()     # Запустить демона прослушки
        self.skud_sdk.subscribe_ce()            # Подписаться на все события
        self.init_points(points_list)
        self.qpi = QPI('localhost', 5000, self, without_auth=True, mark_disconnect=False)

    def get_api_support_methods(self):
        methods = {
            'get_point_state': {'method': self.get_point_state},
            'emulate_card_read': {'method': self.emulate_card_read},
            'lock_point': {'method': self.lock_point},
            'unlock_point': {'method': self.unlock_point},
            'normal_point': {'method': self.normal_point},
            'get_point_all_states_dict': {'method':
                                              self.get_point_all_states_dict},
            'get_points_info': {'method': self.get_points_info}
        }
        return methods

    def get_points_info(self, *args, **kwargs):
        points_list = [point['point_name'] for point in self.points_list]
        return points_list

    def init_points(self, pointlist):
        """ Инициировать экземпляры классов для всех точек доступов,
        заданных суперклассу атрибутом points_list"""
        for point_dict in pointlist:
            point_type = point_dict['point_type']
            point_superclass = functions.get_point_value(point_type,
                                                         'superclass')
            point_object = point_superclass(point_dict['point_num'],
                                            self.skud_sdk)
            point_dict['point_object'] = point_object
            point_dict['position'] = functions.get_point_value(point_type,
                                                               'position')


    def message_operator(self, message_bytes):
        """ Обрабытывает информацию, которая была получена от API СКУД """
        message_str = message_bytes.decode()
        message_list = message_str.split('\r\n')[:-1]
        for msg_str in message_list:
            msg_type = functions.extract_message_type(msg_str)
            #print("GOT", msg_str, '\n', msg_type)
            if msg_type == 'EVENT_CE':
                self.event_ce_operator(msg_str)
            elif msg_type == 'EVENT':
                pass

    def get_point_state(self, point_name_str: str, *args, **kwargs):
        point_dict = functions.get_point_dict(self.points_list, 'point_name', point_name_str)
        if not point_dict:
            raise exceptions.UnknownPoint
        point_state = point_dict['point_object'].get_current_state()
        return point_state

    def get_point_all_states_dict(self, point_name_str: str, *args, **kwargs):
        point_dict = functions.get_point_dict(self.points_list, 'point_name', point_name_str)
        point_state = point_dict['point_object'].get_states_dict()
        return point_state

    def lock_point(self, point_name_str: str, *args, **kwargs):
        point_dict = functions.get_point_dict(self.points_list, 'point_name', point_name_str)
        point_dict['point_object'].set_point_locked()
        return point_dict['point_name']

    def unlock_point(self, point_name_str: str, *args, **kwargs):
        point_dict = functions.get_point_dict(self.points_list, 'point_name', point_name_str)
        point_dict['point_object'].set_point_unlocked()
        return point_dict['point_name']

    def normal_point(self, point_name_str: str, *args, **kwargs):
        point_dict = functions.get_point_dict(self.points_list, 'point_name', point_name_str)
        point_dict['point_object'].set_point_normal()
        return point_dict['point_name']

    def event_ce_operator(self, event_message_str):
        """ Если произошло изменение состояния точек доступа """
        event_message_list = event_message_str.split(' ')
        # Произошло считывание метки по Wiegand 42
        if 'W42' in event_message_list and len(event_message_list) > 8:
            point_num = event_message_list[6]
            point_dict = functions.get_point_dict(self.points_list, 'point_num', point_num)
            info = {'command': 'new_card_detected', 'number': event_message_list[8], 'point_num': point_num,
                    'position': point_dict['position'], 'point_name': point_dict['point_name']}
            self.qpi.broadcast_sending(info)
        # Произошло изменение состояния точки доступа c другого клиента (при изменении с этого - сообщение не приходит)
        elif len(event_message_list) == 8:
            point_num, point_status, date, time = functions.parse_event_ce_str(event_message_str)
            point_dict = functions.get_point_dict(self.points_list, 'point_num', point_num)
            point_old_state = point_dict['point_object'].get_current_state()
            point_status_str = points_logic.state_descriptions[point_status]['str_name']
            point_dict['point_object'].set_state(point_status_str)
            info = {'command': 'point_state_changed', 'point_name': point_dict['point_name'],
                    'new_state': point_status_str,
                    'old_state': point_old_state}
            point_dict['point_object'].set_current_state(point_status_str)
            self.qpi.broadcast_sending(info)

    def set_point_state(self, point_num, state, *args, **kwargs):
        self.skud_sdk.set_point_state(point_num, state)

    def emulate_card_read(self, course: str, card_num: str, *args, **kwargs):
        try:
            if course == 'external':
                self.skud_sdk.sock.init_card_read_emulating_external(card_num)
            elif course == 'internal':
                self.skud_sdk.sock.init_card_read_emulating_inernal(card_num)
        except AttributeError:
            # Если не тестовый мод (sock - экземпляр объекта socket, а не SigurEmulator)
            return {'status': False, 'info': format_exc()}

    def get_unlock_state_str(self):
        return settings.unlock_state

    def get_lock_state_str(self):
        return settings.lock_state

    def get_normal_state_str(self):
        return settings.normal_state

    def get_last_lock_info(self, point_name):
        """ Вернуть массив, содержащий информацию о состоянии
        блокировки точки доступа"""
        # Получаем наименование состояний фотоэлементов в СКУД
        lock_state = self.get_lock_state_str()       # в SIGUR - ONLINE_LOCKED
        # Получаем состояние фотоэлементов
        point_states = self.get_point_all_states_dict(point_name)
        lock_state_info = point_states[lock_state]
        return lock_state_info

    def get_last_normal_info(self, point_name):
        """ Вернуть массив, содержащий информацию о состоянии
        блокировки точки доступа"""
        # Получаем наименование состояний фотоэлементов в СКУД
        normal_state = self.get_normal_state_str()    # в SIGUR - ONLINE_Normal
        # Получаем состояние фотоэлементов
        point_states = self.get_point_all_states_dict(point_name)
        normal_state = point_states[normal_state]
        return normal_state

    def get_last_unlocked_info(self, point_name):
        """ Вернуть массив, содержащий информацию о состоянии
        блокировки точки доступа"""
        # Получаем наименование состояний фотоэлементов в СКУД
        unlocked_state = self.get_normal_state_str() # в SIGUR - ONLINE_Normal
        # Получаем состояние фотоэлементов
        point_states = self.get_point_all_states_dict(point_name)
        unlocked_state = point_states[unlocked_state]
        return unlocked_state


if __name__ == '__main__':
    points_list = [
        {'point_name': 'EXTERNAL_GATE', 'point_num': 2,
         'point_type': 'EXTERNAL_GATE', 'position': 'external'},
        {'point_name': 'INTERNAL_GATE', 'point_num': 1,
            'point_type': 'INTERNAL_GATE', 'position': 'internal'},
        {'point_name': 'INTERNAL_PHOTOCELL', 'point_num': 3,
            'point_type': 'INTERNAL_PHOTOCELL', 'position': 'internal'},
        {'point_name': 'EXTERNAL_PHOTOCELL', 'point_num': 4,
            'point_type': 'EXTERNAL_PHOTOCELL', 'position': 'external'},
    ]
    qsb = QodexSkudBus('192.168.100.109', 3312, points_list=points_list,
                       skud_test_mode=False)
