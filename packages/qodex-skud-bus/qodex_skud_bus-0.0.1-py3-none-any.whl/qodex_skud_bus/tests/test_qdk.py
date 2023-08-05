from qdk.main import QDK
import threading

""" Тестируем подключение и работу с QBS. Здесь код клиента, работаем таким образом:
подключаемся, запускаем в параллельном потоке прослушивание и вывод в поток вывода информации (ответов) от QBS, а в другом
потоке мы отправляем команды на QBS в виде строки, после приглашения ввода "Input Command", если нужны аргументы, то оформляем их
в виде arg1=value1, arg2=value2"""


qdk = QDK('localhost', 5000)
qdk.make_connection()
qdk.subscribe()
response = qdk.get_response()


def listen_thread():
    while True:
        response = qdk.get_response()
        print("Response:", response)


def command_send_thread():
    while True:
        com = input('Input command: ')
        kwargs = input('kwargs(a-b,c-d): ')
        end_kwargs = {}
        if kwargs:
            kwargs_list = kwargs.split(',')
            for kwarg in kwargs_list:
                k,v = kwarg.split('-')
                end_kwargs[k] = v
        qdk.execute_method(com, get_response=False, **end_kwargs)


threading.Thread(target=listen_thread, args=()).start()
threading.Thread(target=command_send_thread(), args=()).start()
