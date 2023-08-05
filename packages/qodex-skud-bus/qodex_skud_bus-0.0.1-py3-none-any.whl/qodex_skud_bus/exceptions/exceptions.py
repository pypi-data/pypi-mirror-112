class UnknownPoint(Exception):
    # Исключение, возникающее при неизвестном имени терминала
    def __init__(self):
        text = 'Неизвестная точка доступа'
        super().__init__(text)
