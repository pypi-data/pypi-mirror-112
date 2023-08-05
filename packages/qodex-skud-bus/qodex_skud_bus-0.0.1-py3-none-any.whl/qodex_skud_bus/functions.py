from qodex_skud_bus.points_logic import points_description


def extract_message_type(message):
    """ Определить тип сообщения и вернуть ее название """
    if 'ERROR' in message:
        return 'ERROR'
    elif 'APINFO' in message:
        return 'APINFO'
    elif 'OK' in message:
        return 'OK'
    elif 'EVENT_CE' in message:
        return 'EVENT_CE'
    elif 'EVENT' in message:
        return 'EVENT'


def parse_event_ce_str(event_message_str: str):
    """ Получает событие EVENT_CE, извлекает номер точки доступа и возвращает ее """
    event_message_list = event_message_str.split(' ')
    point_num = event_message_list[4]
    point_status = event_message_list[3]
    date = event_message_list[1].replace('"', '')   # Поскольку в дате присутствует ", надо ее убрать
    time = event_message_list[2].replace('"', '')
    return point_num, point_status, date, time


def get_point_value(point_type_str: str, key:str):
    """ Получить значение ключа key из словаря с описанием логики всех точек доступов points_logic """
    return points_description[point_type_str][key]


def get_point_dict(points_list: list, key: str, value: str):
    """ Извлекает нужный словарь из списка по ключу """
    type_value = type(value)
    for item in points_list:
        if type_value(item[key]) == value:
            return item
