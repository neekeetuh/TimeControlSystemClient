from tkinter import *
from .frames.EmployeesFrame import EmployeesFrame

"""
Класс ClientInterface является наследником класса Tk, представляет собой интерфейс клиентского приложения.
"""


class ClientInterface(Tk):
    """
    Конструктор не принимает в себя никаких параметров и инициализирует в себе стандартные параметры библиотеки tkinter.
    """

    def __init__(self):
        super().__init__()
        self.title("TimeControlSystem")
        self.geometry("1920x1080")
        self.minsize(width=800, height=500)
        self._frame = None
        self.switch_frame(EmployeesFrame)

    """
    Функция, запускающая клиентское приложение.
    """

    def start_app(self):
        self.mainloop()

    """
    Функция, меняющая экраны. Параметр frame_class представляет собой класс экрана, который приложение должно 
    отобразить по команде.
    """

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
