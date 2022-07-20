from datetime import *
from tkinter import *
from models.work_day import *
from tkinter import messagebox as mb
from .Table import *

"""
Класс EmployeesFrame является наследником tk.Frame, представляет собой экран, содержащий информацию о всех сотрудниках
с набором кнопок для определённых действий с записями таблицы.
"""


class EmployeesFrame(tk.Frame):
    """
    Конструктор инициализирует в себе стандартные параметры библиотеки tkinter. Параметр parent представляет собой
    экземпляр стандартного объекта tkinter, к которому будет привязан экран.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        headings = ['ID сотрудника', 'Фамилия', 'Имя', 'Отчество', 'Электронная почта', 'Номер телефона', 'Должность',
                    'Отдел']
        self._table = Table(self, headings=headings, rows=self.get_data())
        self._table.pack()

        self._frame_buttons = Frame(self)

        self._empty_label1 = tk.Label(self, text='')
        self._empty_label1.pack()

        start_btn = Button(self._frame_buttons, text='Открыть смену', font=('Arial', 20), command=self._check_in,
                           background='lightblue', pady=5, padx=5)
        start_btn.pack()

        self._empty_label2 = tk.Label(self._frame_buttons, text='')
        self._empty_label2.pack()

        end_btn = Button(self._frame_buttons, text='Закрыть смену', font=('Arial', 20), command=self._check_out,
                         background='lightblue', pady=5, padx=5)
        end_btn.pack()

        self._empty_label3 = tk.Label(self._frame_buttons, text='')
        self._empty_label3.pack()

        refresh_btn = Button(self._frame_buttons, text='Обновить', font=('Arial', 20), command=self._refresh,
                             background='lightblue', pady=5, padx=5)
        refresh_btn.pack()

        self._frame_buttons.pack()

    """
    Функция, делающая запрос данных из БД и возвращающая их в виде массива.
    """

    def get_data(self):
        data = []
        with db:
            for employee in Employee.select().order_by(Employee.surname, Employee.name, Employee.patronymic):
                content = [
                    employee.id,
                    employee.surname,
                    employee.name,
                    employee.patronymic,
                    employee.email,
                    employee.phone_number,
                    employee.position_id.title,
                    employee.department_id.address
                ]
                data.append(content)
        return data

    """
    Команда для кнопки, обеспечивающая открытие смены для выбранного сотрудника.
    """

    def _check_in(self):
        if self._table.get_table().selection():
            for selection in self._table.get_table().selection():
                employee_id = self._table.get_table().item(selection)['values'][0]
                with db:
                    if WorkDay.select().where(WorkDay.employee_id == employee_id, WorkDay.end_time.is_null()):
                        mb.showerror("Ошибка", "Смена уже открыта")
                    else:
                        WorkDay.insert(employee_id=employee_id, start_time=datetime.now()).execute()
                        mb.showinfo("Результат", "Смена открыта")
        else:
            mb.showerror('Ошибка', 'Выберите запись в таблице')

    """
    Команда для кнопки, обеспечивающая закрытие смены для выбранного сотрудника.
    """
    def _check_out(self):
        if self._table.get_table().selection():
            for selection in self._table.get_table().selection():
                employee_id = self._table.get_table().item(selection)['values'][0]
                with db:
                    if WorkDay.select().where(WorkDay.employee_id == employee_id, WorkDay.end_time.is_null()):
                        WorkDay.update(end_time=datetime.now()).where(WorkDay.employee_id == employee_id,
                                                                      WorkDay.end_time.is_null()).execute()
                        mb.showinfo("Результат", "Смена закрыта")
                    else:
                        mb.showerror("Ошибка", "Невозможно закрыть смену, так как она не была открыта")
        else:
            mb.showerror('Ошибка', 'Выберите запись в таблице')

    """
    Функция для обновления экрана.
    """
    def _refresh(self):
        parent = self.master
        self.destroy()
        parent.switch_frame(EmployeesFrame)
