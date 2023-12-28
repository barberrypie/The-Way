import tkinter as tk
import json
from datetime import datetime, timedelta


class AppData:
    def __init__(self):
        self.today_date = datetime.now().date().strftime("%Y-%m-%d")
        self.day_of_start = datetime(2023, 12, 14)
        self.number_of_lines = 17
        self.line_start_dates = [self.day_of_start + timedelta(days=i*10) for i in range(self.number_of_lines)]
        self.money_data = {i: 0 for i in range(1, 18)}
        self.data = self.load_data()
    
    def load_data_from_json(self):
        try:
            with open("daily_data.json", "r") as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError:
            pass

    def save_data_to_json(self):
        with open("daily_data.json", "w") as json_file:
            json.dump(self.data, json_file, indent=4)


    def get_current_line(self):
        for i, start_date in enumerate(self.line_start_dates):
            if datetime.strptime(self.today_date, "%Y-%m-%d") >= start_date and datetime.strptime(self.today_date, "%Y-%m-%d") < (start_date + timedelta(days=10)):
                return i + 1

    def calculate_money_for_line(self, line_number):
        # Реализация подсчета денег для линии
        pass

    def calculate_money_for_way(self):
        # Реализация подсчета денег для всего пути
        pass

class AppGUI:
    def __init__(self, root, app_data):
        self.root = root
        self.app_data = app_data
        self.root.title("The Way")
        self.root.configure(bg="white")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.show_survey()

    def show_survey(self):
        # Реализация отображения опроса
        pass

    def show_menu(self, label_text):
        # Реализация отображения меню согласно переданному тексту
        pass

    def show_line(self):
        # Реализация отображения информации о линии
        pass

    def show_way(self):
        # Реализация отображения информации о пути
        pass

    def draw_circles_on_line(self, line_number):
        line = self.app_data.lines[line_number - 1]
        frame = tk.Frame(self.root, bg="white")
        frame.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=(0, 20), expand=True)
        canvas = tk.Canvas(frame, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight() * 0.2, bg="white")
        canvas.pack(expand=tk.YES, side=tk.TOP, padx=20, pady=(0, 20), fill=tk.Y)
        line.draw_circles(canvas, self.app_data.today_date)

    def run(self):
        self.root.mainloop()

class MenuGUI(AppGUI):
    def __init__(self, app_data):
        super().__init__(app_data)

   

class Line(AppData, AppGUI):
    def __init__(self, line_number, start_date, data):
        self.line_number = line_number
        self.start_date = start_date
        self.data = data

    def draw_circles(self, canvas, today_date):
        for i in range(1, 11):
            day_date = (self.start_date + timedelta(days=i - 1)).strftime("%Y-%m-%d")
            value = self.data.get(day_date, None)
            
            color = "#E0E0E0" if value is None else "#FF9999" if value == "False" else "#99FF99"

            center_x = i * (canvas.winfo_reqwidth() / (14 * 1.3))
            center_y = canvas.winfo_reqheight() // 6
            radius = canvas.winfo_reqheight() * 0.07

            x1 = center_x - radius
            y1 = center_y - radius
            x2 = center_x + radius
            y2 = center_y + radius

            canvas.create_oval(x1, y1, x2, y2, fill=color, width=2, outline="#C0C0C0")
            if i == int((datetime.strptime(today_date, "%Y-%m-%d") - self.start_date).days) + 1:
                canvas.create_text(center_x, center_y, text="✡", fill="RED", font=("Crystal", 18, "bold"))


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Way(metaclass=SingletonMeta):
    def __init__(self, app_data):
        self.app_data = app_data
        self.lines = [Line(app_data, i) for i in range(1, app_data.number_of_lines + 1)]

    def show_way_info(self):
        # Реализация отображения информации о пути
        pass

class Line:
    def __init__(self, app_data, line_number):
        self.app_data = app_data
        self.line_number = line_number

    def show_line_info(self):
        # Реализация отображения информации о линии
        pass



class MainApplication:
    def __init__(self, root):
        self.app_data = AppData()
        self.app_gui = AppGUI(root, self.app_data)

    def run(self):
        self.app_gui.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    app.run()