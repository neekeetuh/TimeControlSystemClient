from interface.client import *

"""
Главная функция, внутри которой происходит вызов клиентского приложения.
"""


def main():
    client = ClientInterface()
    client.start_app()


"""
Конструкция, запускающая главный скрипт.
"""
if __name__ == "__main__":
    main()
