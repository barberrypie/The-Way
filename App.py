import tkinter as tk
import json
from datetime import datetime, timedelta

font_18 = ("Crystal", 18, "bold")
font_15 = ("Crystal", 15)
font_13 = ("Crystal", 13, "bold")
font_13_ = ("Crystal", 13)
font_10 = ("Crystal", 10)

def get_day_word(number):
    if number % 10 == 1 and number % 100 != 11:
        return "день"
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return "дня"
    else:
        return "дней"
    
def get_rating(false_counter, true_counter, check):
    if check == 0:
        return('Начни лучше сегодня')
    if false_counter > true_counter:
        return('Капец ты черт :с')
    elif false_counter == true_counter:
        return('Еще один раз и я на тебя обижусь.')
    else:
        return('<3')
    

class DailySurveyApp:
    def set_root(self, root_, title_, param = 0.4):
        root_.title(title_)
        root_.configure(bg="white")

        # 40% от размера экрана
        screen_w = root_.winfo_screenwidth() * param
        screen_h = root_.winfo_screenheight() * param

        # Размещение по центру
        x = (root_.winfo_screenwidth() - screen_w) / 2
        y = (root_.winfo_screenheight() - screen_h) / 2
        root_.wm_geometry("%dx%d+%d+%d" % (screen_w, screen_h, x, y ))
        root_.resizable(False, False)

        return root_

    def __init__(self, root):
        self.root = self.set_root(root, "The Way", 0.45)

        # Сегодняшняя дата
        self.today_date = datetime.now().date().strftime("%Y-%m-%d")
        self.day_of_start = datetime(2023, 12, 14)
        self.number_of_lines = 17

        # Список начальных дат для каждого лайна
        self.line_start_dates = [self.day_of_start + timedelta(days=i*10) for i in range(self.number_of_lines)]
        
        # Словарь для отслеживания денежных начислений в каждой линии
        self.money_data = {i: 0 for i in range(1, 18)}

        try:
            # Открываем JSON-файл
            with open("daily_data.json", "r") as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError:
            None
            # Если файл не найден, создаем пустой словарь
            #self.first()

        # Проверяем, есть ли запись для сегодняшней даты
        if self.today_date in self.data and self.data[self.today_date] != None:
            n = self.data[self.today_date]
            if n == "False":
               label_text = "Ты сегодня уже заполнял тупление.\nТы должен отправить на счет {} рублей.".format(self.calculate_money_for_line(1,self.get_current_line()))
            elif n == "True":
               label_text = ("Ты сегодня заполнял тупление.\nНа этот раз ты мне ничего не должен\nV●ᴥ●V")
            self.root.destroy()
            self.show_menu(None, None, label_text)
        else:
            self.show_survey() 

    # Штука для подсчета денег в лайне по его номеру
    def calculate_money_for_line(self, mode = 0, line_number = 0):
        money = 0
        prev_day_money = 0
        false_counter = 0

        # Список начальных дат для каждого лайна
        line_start_dates = [datetime(2023, 12, 14) + timedelta(days=i*10) for i in range(17)]

        # Начальная дата лайна
        line_start_date = line_start_dates[line_number - 1]

        # Проходим по дням лайна
        for i in range(10):
            day_date = (line_start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            value = self.data.get(day_date, None)

            # Проверяем значение текущего дня
            if value == "False":
                current_day_money = 200
            # Проверяем, повторяется ли предыдущий день
                if i > 0 and self.data.get((line_start_date + timedelta(days=i-1)).strftime("%Y-%m-%d")) == "False":
                    if prev_day_money >= 800:
                        prev_day_money = 400
                    current_day_money = prev_day_money * 2  # Умножаем только предыдущее начисление

                money += current_day_money
                prev_day_money = current_day_money

                false_counter += 1
            elif value == "True":
                current_day_money = 200

        # Штраф
        if false_counter >= 5:
            money += 500

        if mode == 1:
            return current_day_money
        else:
            return money
    
    def calculate_money_for_way(self):
        total_money = 0

        for line_number, start_date in enumerate(self.line_start_dates, start=1):
            line_money = self.calculate_money_for_line(0,line_number)
            total_money += line_money

        return total_money
    
    def show_survey(self):

        self.question_label = tk.Label(self.root, text="Как прошел твой день,\nСолнце? ʕ ᵔᴥᵔ ʔ", font=font_15, bg="#ECECEC", height= 5)
        self.question_label.pack(anchor=tk.N, fill=tk.X, padx=20, pady=(20, 0))

        self.frame_menu = tk.Frame(self.root, bg="white")
        self.frame_menu.pack(side=tk.TOP, fill=tk.BOTH, padx=20 ,pady=(20,0), expand=True)

        self.root.after(1, self.set_button_sizes)
        
        self.watch = tk.Button(self.frame_menu, text="Да я только посмотреть...", command=lambda: self.show_menu(None, None,"just_watch"), font=font_13_, bg="#ECECEC", height=4 , border=0)
        self.watch.pack(side=tk.BOTTOM, fill=tk.X, pady=20, expand=True)
        

    def set_button_sizes(self):
        self.frame_menu.update()

        self.stupid_button = tk.Button(self.frame_menu, text="Тупил...\n\n ┬┴┬┴┤(･_├┬┴┬┴", command=lambda: self.submit_survey("False"), font=font_13, bg="#FFCCE5", width=28, height=8, border=0)
        self.stupid_button.pack(side=tk.RIGHT)

        self.not_stupid_button = tk.Button(self.frame_menu, text="Не тупил!\n\n (˵◕ω◕˵)", command=lambda: self.submit_survey("True"), font=font_13, bg="#CCFFCC", width=28, height=8 , border=0)
        self.not_stupid_button.pack(side=tk.LEFT)



    def submit_survey(self, answer):
        # Записываем ответ пользователя в JSON-файл
        self.data[self.today_date] = answer
        with open("daily_data.json", "w") as json_file:
            json.dump(self.data, json_file, indent=4)
        self.root.destroy()
        self.show_menu(None, None, self.data[self.today_date])

    def show_menu(self, line_root = None, way_root = None, label_text = None):

        if line_root != None:
            line_root.destroy()
        elif way_root != None:
            way_root.destroy()

        menu_root = tk.Tk()
        menu_root = self.set_root(menu_root, "The Way. Menu")
        
        if label_text != None:
            if label_text == 'False':
                label_text = "Ты должен отправить на счет {} рублей.".format(self.calculate_money_for_line(1,self.get_current_line()))
            elif label_text == 'True':
                label_text =  "Ты сегодня уже заполнял Путь.\nНа этот раз ты мне ничего не должен\nV●ᴥ●V"
            elif label_text == "just_watch":
                label_text = "Ну смотри, раз пришел.\n Но я этого не одобряю.\nV-ᴥ-V"
            money_label = tk.Label(menu_root, text=label_text, font=font_15, bg="#ECECEC", height= 5)
            money_label.pack(anchor=tk.N, fill=tk.X, padx=20, pady=(20, 0))

        #if label_text != "just_watch":
        menu_label = tk.Label(menu_root, text="У меня есть для тебя вот это", font=font_13_, bg="white", height=2)
        menu_label.pack(pady=(20,0))

        self.frame_main_menu = tk.Frame(menu_root, bg="white")
        self.frame_main_menu.pack(side=tk.TOP, fill=tk.BOTH, padx=20 ,pady=(0,20), expand=True)
        self.root.after(1, self.set_main_button_sizes, menu_root, label_text)

        # Используйте frame_main_menu для установки размеров
        self.frame_main_menu = tk.Frame(menu_root, bg="white")
        self.frame_main_menu.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=(0, 20), expand=True)
        self.root.after(1, self.set_main_button_sizes, menu_root, label_text)

        #if label_text == "just_watch":
        #    self.stop_watch = tk.Button(self.frame_main_menu, text="Хочу отметить день", command=lambda: self.__init__(), font=font_13, bg="#CCFFCC", width=28, height=8, border=0)
        #    self.stop_watch.pack(side=tk.BOTTOM, padx=(0, 10), pady=(20))
            
    def set_main_button_sizes(self, menu_root, label_text):
        self.frame_main_menu.update()

        self.show_line_button = tk.Button(self.frame_main_menu, text="Line\n\n\n------------\n", command=lambda: self.show_line(menu_root, label_text), font=font_13, bg="#E5CCFF", width=28, height=8, border=0)
        self.show_line_button.pack(side=tk.RIGHT, padx=(10, 0))

        self.show_way_button = tk.Button(self.frame_main_menu, text="Way\n\n------------\n------------\n------------", command=lambda: self.show_way(menu_root, label_text), font=font_13, bg="#E5CCFF", width=28, height=8 , border=0)
        self.show_way_button.pack(side=tk.LEFT, padx=(0, 10))

        menu_root.mainloop()
 
    def get_current_line(self):
        # Определяем текущий лайн на основе сегодняшней даты
        for i, start_date in enumerate(self.line_start_dates):
            if datetime.strptime(self.today_date,"%Y-%m-%d") >= start_date and datetime.strptime(self.today_date,"%Y-%m-%d") < (start_date + timedelta(days=10)):
                return i + 1  # Возвращаем номер лайна

    def show_line(self, menu_root, label_text):
        menu_root.destroy()

        self.current_line = self.get_current_line()

        line_root = tk.Tk()
        line_root = self.set_root(line_root, "The Way. Line #{}".format(self.current_line) )

        money_for_line = self.calculate_money_for_line(0,self.current_line)

        money_label = tk.Label(line_root, text=f"Начислено за весь лайн: {money_for_line}",font = font_13_, bg="#ECECEC", height=2)
        money_label.pack(anchor=tk.N, fill=tk.X, padx=20, pady=(20,0))

        can_width = line_root.winfo_screenwidth()
        can_height = line_root.winfo_screenheight() * 0.1
        canvas = tk.Canvas(line_root, width=can_width, height=can_height, bg="white")
        canvas.pack(side=tk.TOP, padx=20, pady=(0,20))

        for i in range(1, 11):
            day_date = (self.line_start_dates[self.current_line - 1] + timedelta(days=i-1)).strftime("%Y-%m-%d")
           
            value = self.data.get(day_date, None)

            color = "#E0E0E0" if value is None else "#FF9999" if value == "False" else "#99FF99"

            center_x = i * (canvas.winfo_reqwidth() / (14*2.1))  # Равномерное распределение по оси x
            center_y = canvas.winfo_reqheight() // 2
            radius = min(center_x, center_y) * 0.5

            x1 = center_x - radius
            y1 = center_y - radius
            x2 = center_x + radius
            y2 = center_y + radius

            # Определяем текущий день и выделяем его
            if i == int((datetime.strptime(self.today_date,"%Y-%m-%d") - self.line_start_dates[self.current_line - 1]).days) + 1:
                if color == "#E0E0E0":
                    canvas.create_oval(x1,y1,x2,y2, fill=color, outline="#808080", width=2)
                elif color == "#FF9999":
                    canvas.create_oval(x1,y1,x2,y2, fill=color, outline="#FF0000", width=2)
                else:
                    canvas.create_oval(x1,y1,x2,y2, fill=color, outline="#33ff33", width=2)
                
                canvas.create_text(center_x, center_y, text="✡", fill="RED", font=font_18)
            else:
                if color == "#E0E0E0":
                    canvas.create_oval(x1,y1,x2,y2, fill=color, width=2, outline="#C0C0C0")
                elif color == "#FF9999":
                    canvas.create_oval(x1,y1,x2,y2, fill=color, width=2, outline="#FF6666")
                else:
                    canvas.create_oval(x1,y1,x2,y2, fill=color, width=2, outline="#66FF66")

        date_start_label = tk.Label(line_root, text=f"Начало лайна \nᐅ{(self.line_start_dates[self.current_line - 1]).strftime('%d.%m.%Y')}ᐊ", font = font_13_, bg="white", height=2)
        date_end_label = tk.Label(line_root, text=f"Окончание лайна \nᐅ{(self.line_start_dates[self.current_line - 1] + timedelta(days=10)).strftime('%d.%m.%Y')}ᐊ", font = font_13_, bg="white", height=2)

        date_start_label.pack(pady=(0, 20), side="left", padx=20)
        date_end_label.pack(pady=(0, 20), side="right", padx=20)

        # Добавляем кнопку для возврата
        return_button = tk.Button(line_root, text="Вернуться в меню", command=lambda: self.show_menu(line_root, None, label_text), font = font_13, bg="#E5CCFF", width=28, height=8, border=0)
        return_button.pack(side=tk.RIGHT, padx=(0, 0), pady=(0,20))

        line_root.mainloop()

    def show_way(self, menu_root, label_text):
        menu_root.destroy()

        way_root = tk.Tk()
        way_root = self.set_root(way_root, "The Way", 0.6)

        self.current_line = self.get_current_line()

        money_for_way = self.calculate_money_for_way()

        money_label = tk.Label(way_root, text=f"Начислено за весь путь: {money_for_way}",font = font_13_, bg="#ECECEC", height=2)
        money_label.pack(anchor=tk.N, fill=tk.X, padx=20, pady=(20,0))

        can_width = way_root.winfo_screenwidth()
        can_height = way_root.winfo_screenheight() * 0.2
        canvas = tk.Canvas(way_root, width=can_width, height=can_height, bg="white", )
        canvas.pack(expand=tk.YES, side=tk.TOP, padx=20, pady=(0,20), fill=tk.Y)

        offset_y = 0  # Начальное смещение по оси y
        line_number = 0
        for _ in enumerate(self.line_start_dates):

            for i in range(1, 11):
                day_date = (self.line_start_dates[line_number] + timedelta(days=i-1)).strftime("%Y-%m-%d")
            
                value = self.data.get(day_date, None)

                color = "#E0E0E0" if value is None else "#FF9999" if value == "False" else "#99FF99"

                center_x = i * (canvas.winfo_reqwidth() / (14*1.3))  # Равномерное распределение по оси x
                center_y = canvas.winfo_reqheight() // 6 + offset_y  # Смещение по оси y
                radius = canvas.winfo_reqheight() * 0.07

                x1 = center_x - radius
                y1 = center_y - radius
                x2 = center_x + radius
                y2 = center_y + radius

                if i == 1:
                    canvas.create_text(center_x - center_x/2, center_y, text=line_number+1, fill="black", font=font_10)

                # Определяем текущий день и выделяем его
                if i == int((datetime.strptime(self.today_date,"%Y-%m-%d") - self.line_start_dates[line_number]).days) + 1:
                    if color == "#E0E0E0":
                        canvas.create_oval(x1,y1,x2,y2, fill=color, outline="#808080", width=2)
                    elif color == "#FF9999":
                        canvas.create_oval(x1,y1,x2,y2, fill=color, outline="#FF0000", width=2)
                    else:
                        canvas.create_oval(x1,y1,x2,y2, fill=color, outline="#33ff33", width=2)

                    canvas.create_text(center_x, center_y, text="✡", fill="RED", font=font_18)

                else:
                    if color == "#E0E0E0":
                        canvas.create_oval(x1,y1,x2,y2, fill=color, width=2, outline="#C0C0C0")
                    elif color == "#FF9999":
                        canvas.create_oval(x1,y1,x2,y2, fill=color, width=2, outline="#FF6666")
                    else:
                        canvas.create_oval(x1,y1,x2,y2, fill=color, width=2, outline="#66FF66")
                
            offset_y += 15  # Увеличиваем смещение по оси y для следующей "линии"
            line_number+=1

        
        
        false_counter = 0
        true_counter = 0

        for value in self.data.values():
            if value == "False":
                false_counter += 1
            elif value == "True":
                true_counter += 1

        filled_counter = 0
    
        for value in reversed(self.data.values()):
            if value is None:
                filled_counter += 1
            elif value == "True" or value == "False":
                break

        # К-во дней от сегодня до даты начала
        check = (datetime.strptime(self.today_date,'%Y-%m-%d') - self.day_of_start).days + 1

        frame = tk.Frame(way_root, bg="white")
        frame.pack(side=tk.LEFT, anchor='w', fill=tk.Y, pady=(0,30), padx=(20,0), expand=True)

        good_label = tk.Label(frame, text=f"Хороших: \t\t{true_counter} {get_day_word(true_counter)}", font=font_13_, bg="WHITE", height=2)
        good_label.pack(side=tk.TOP, anchor="w")

        bad_label = tk.Label(frame, text=f"Плохих: \t\t{false_counter} {get_day_word(false_counter)}", font=font_13_, bg="WHITE", height=2)
        bad_label.pack(side=tk.TOP, anchor="w")

        non_label = tk.Label(frame, text=f"Учет не велся: \t{check - (false_counter + true_counter) } {get_day_word(check - (false_counter + true_counter))}", font=font_13_, bg="WHITE", height=2)
        non_label.pack(side=tk.TOP, anchor="w")
        
        frame = tk.Frame(way_root, bg="white")
        frame.pack(side=tk.LEFT, anchor='w', fill=tk.Y, pady=(0,30), padx=(20), expand=True)


        good_label = tk.Label(frame, text=f"Пройдено: \t\t{check} {get_day_word(check)}", font=font_13_, bg="WHITE", height=2)
        good_label.pack(side=tk.TOP, anchor="w")

        bad_label = tk.Label(frame, text=f"Осталось до конца пути: \t{filled_counter} {get_day_word(filled_counter)}", font=font_13_, bg="WHITE", height=2)
        bad_label.pack(side=tk.TOP, anchor="w")

        non_label = tk.Label(frame, text=f"Вердикт: \t{get_rating(false_counter, true_counter, check)}", font=font_13_, bg="WHITE", height=2)
        non_label.pack(side=tk.TOP, anchor="w")
        

        # Добавляем кнопку для возврата
        return_button = tk.Button(way_root, text="Вернуться в меню", command=lambda: self.show_menu(way_root, None, label_text), font=font_13, bg="#E5CCFF", width=28, height=5, border=0)
        return_button.pack(side=tk.LEFT, anchor='center', padx=(20, 20), pady=(0, 20))

        way_root.mainloop()




if __name__ == "__main__":
    root = tk.Tk()
    app = DailySurveyApp(root)
    root.mainloop()