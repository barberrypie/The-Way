from abc import ABC, abstractmethod
import tkinter as tk
import json
from datetime import datetime, timedelta
import random
import statements

class JSONLoader():
    def load_data(self):
        try:
            with open("daily_data.json", "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            return {}
    def save_data(self):
        with open("daily_data.json", "w") as json_file:
            json.dump(self.data, json_file, indent=4)

class Calculator():
    def calculate_money_for_line(self):
        pass
    def calculate_money_for_way(self):
        pass

class Dater():
    def get_today_date(self):
        self.today_date = datetime.now().date().strftime("%Y-%m-%d")
        return self.today_date
    def set_day_of_start(self):
        self.day_of_start = datetime(2023, 12, 14)
        return self.day_of_start
    def set_lines_count(self):
        return 17
    def set_day_of_end(self):
        self.day_of_end = self.day_of_start() + timedelta(self.set_lines_count*10)
        return self.day_of_end
    def get_day_word(self, number):
        if number % 10 == 1 and number % 100 != 11:
            return "день"
        elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
            return "дня"
        else:
            return "дней"
    
class Rater():
    def __init__(self, false_counter, true_counter, check):
        self.false_counter = false_counter
        self.true_counter = true_counter
        self.check = check
    
    def choose_random_value(list):
        if not list:
            return None
        return random.choice(list)
    
    def get_rating(self):
        if self.check == 0:
            return 'Начни лучше сегодня'
        if self.false_counter > self.true_counter:
            return self.choose_random_value(statements.negative_strings)
        elif self.false_counter == self.true_counter:
            return 'Еще один раз и я на тебя обижусь.'
        else:
            return '<3'


class AppData(JSONLoader, Calculator, Dater):
    def __init__(self, root):
        # Использование композиции для создания объектов других классов
        self.json_loader = JSONLoader()
        self.calculator = Calculator()
        self.dater = Dater()

        # Передача объекта корневого окна в класс
        self.root = root

        # Дополнительная инициализация атрибутов AppData
        self.data = self.json_loader.load_data()
        self.list_start_dates = [self.dater.set_day_of_start() + timedelta(days=i * 10) for i in range(self.dater.set_lines_count())]
        self.money_data = {i: 0 for i in range(1, self.dater.set_lines_count())}

    
class Drawable (ABC):
    @abstractmethod
    def draw_canwas():
        pass
    @abstractmethod
    def draw_circle():
        pass
    @abstractmethod
    def draw_button():
        pass
    @abstractmethod
    def draw_frame():
        pass
    @abstractmethod
    def draw_lable():
        pass
    @abstractmethod
    def draw_entry():
        pass

class Window(Drawable):
    def __init__(self, title_, percent = 0.4):
        self.root_ = tk.Tk()
        self.root_.title(title_)
        self.root_.configure(bg="white")

        # 40% от размера экрана
        screen_w = self.root_.winfo_screenwidth() * percent
        screen_h = self.root_.winfo_screenheight() * percent

        # Размещение по центру
        x = (self.root_.winfo_screenwidth() - screen_w) / 2
        y = (self.root_.winfo_screenheight() - screen_h) / 2
        self.root_.wm_geometry("%dx%d+%d+%d" % (screen_w, screen_h, x, y ))
        self.root_.resizable(False, False)

        return self.root_
    
    def draw_canvas(self, parameter = 0.1, side_ = tk.TOP, pady_= 0):
        canvas = tk.Canvas(self.root_, width=self.screen_w, height=self.screen_h * parameter, bg="white")
        canvas.pack(expand=tk.YES, side=side_, padx=20, pady=(pady_,20))
    
    def draw_circle(self, radius, x, y, height_parameter = 0.1, side = tk.TOP, pady = 0):
        canvas = self.draw_canvas(height_parameter, side, pady)
        canvas.create_oval(0, 0, 2*radius, 2*radius, outline="black", fill="white")
        canvas.pack()
        canvas.place(x=x, y=y)

    def draw_button(self, text, command, x, y):
        button = tk.Button(self.root, text=text, command=command)
        button.pack()
        button.place(x=x, y=y)

    def draw_frame(self, width, height, x, y):
        frame = tk.Frame(self.root, width=width, height=height, bg="white")
        frame.pack()
        frame.place(x=x, y=y)

    def draw_label(self, text, font, x, y):
        label = tk.Label(self.root, text=text, font=font)
        label.pack()
        label.place(x=x, y=y)

    def draw_entry(self, width, x, y):
        entry = tk.Entry(self.root, width=width)
        entry.pack()
        entry.place(x=x, y=y)

    def run(self):
        self.root.mainloop()




class AppGui(AppData, Window):
    def draw_window(self):
        # Рисование основного окна

    def draw_way(self, way_data):
        # Рисование пути на основе данных way_data


"""if __name__ == "__main__":
    root = tk.Tk()
    app = AppData(root)
    root.mainloop()"""


"""

    def get_data_for_date(self, date):
        return self.data.get(date, None)

    def get_current_line(self):
        for i, start_date in enumerate(self.line_start_dates):
            if datetime.strptime(self.today_date, "%Y-%m-%d") >= start_date and datetime.strptime(self.today_date, "%Y-%m-%d") < (start_date + timedelta(days=10)):
                return i + 1
class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass """

