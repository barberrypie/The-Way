from abc import ABC, abstractmethod
import tkinter as tk
import json
from datetime import datetime, timedelta

class JSONLoader(ABC):
    def load_data(self):
        try:
            with open("daily_data.json", "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            return {}
    def save_data(self):
        with open("daily_data.json", "w") as json_file:
            json.dump(self.data, json_file, indent=4)

class Calculator(ABC):
    def calculate_money_for_line(self):
        pass
    def calculate_money_for_way(self):
        pass

class Dater(ABC):
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

if __name__ == "__main__":
    root = tk.Tk()
    app = AppData(root)
    root.mainloop()

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

