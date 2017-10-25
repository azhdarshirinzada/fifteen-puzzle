from tkinter import *
from random import random, shuffle
from tkinter.messagebox import showerror
from datetime import datetime
from time import time
from validation_rules import *


class PuzzleController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def game_is_begin(self):
        shuffle(self.model.numbers)
        shuffled = self.model.numbers.copy()
        self.model.EL_row, self.model.EL_column = int(random() * 4), int(random() * 4)
        for row in range(4):
            self.model.my_labels[row] = []
            for column in range(4):
                if row == self.model.EL_row and column == self.model.EL_column:
                    self.model.my_labels[row].append(Label(self.view.game_frame, width=8, height=4, text="", bg="black"))
                    self.model.my_labels[row][column]\
                        .grid(row=self.model.EL_row, column=self.model.EL_column, padx=2, pady=2)
                    self.model.my_labels[row][column].bind('<Button-1>', lambda event, r=row, c=column: self.move(r, c))
                    continue
                self.model.my_labels[row]\
                    .append(Label(self.view.game_frame, width=8, height=4, text=shuffled.pop(), bg="white", font=15,))
                self.model.my_labels[row][column].grid(row=row, column=column, padx=2, pady=2)
                self.model.my_labels[row][column].bind('<Button-1>', lambda event, r=row, c=column: self.move(r, c))

    def start_was_clicked(self):
        self.view.start.grid_forget()
        self.game_is_begin()
        self.view.game_frame.pack(side=BOTTOM)
        self.view.pause.configure(state=NORMAL)
        self.view.reset.configure(state=NORMAL)
        self.tick()
        self.model.check_notice = False

    def pause_was_clicked(self):
        self.model.flag = False
        self.view.root.after_cancel(self.model.tick_id)
        self.view.reset.configure(state=DISABLED)
        self.view.continuebtn.grid(row=0, column=2, padx=5, pady=5, sticky=EW)
        self.view.game_frame.pack_forget()

    def continue_was_clicked(self):
        self.model.flag = True
        self.view.continuebtn.grid_forget()
        self.view.reset.configure(state=NORMAL)
        self.view.pause.grid(row=0, column=2, padx=5, pady=5, sticky=EW)
        self.view.game_frame.pack(side=BOTTOM)
        self.tick()

    def reset_was_clicked(self):
        self.model.flag = True
        self.model.check_notice = False
        self.view.root.after_cancel(self.model.tick_id)
        self.model.counts = 0
        self.view.count_of_steps.configure(text="Steps: " + str(self.model.counts))
        self.model.sec = 0
        self.view.stopwatch.configure(text="00:00")
        self.game_is_begin()
        self.view.game_frame.pack(side=BOTTOM)
        self.view.pause.grid(row=0, column=2, padx=5, pady=5, sticky=EW)
        self.view.congrats.place_forget()
        self.tick()

    def return_was_clicked(self):
        self.view.hs_frame.place_forget()
        if self.model.current_email:
            self.view.tool_bar.pack(side=TOP, fill=Y)
            if self.model.flag:
                self.view.game_frame.pack(side=BOTTOM)
            if self.model.check_notice:
                self.view.congrats.place(relx=0.5, rely=0.5, anchor=CENTER)
                self.view.game_frame.pack_forget()
        else:
            self.view.login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def high_scores(self):
        for item in self.view.high_score_tree.get_children():
            self.view.high_score_tree.delete(item)
        if self.model.check_notice:
            self.view.congrats.place_forget()
        self.view.login_frame.place_forget()
        self.view.register_frame.place_forget()
        self.view.tool_bar.pack_forget()
        self.view.game_frame.pack_forget()
        for row in self.model.highScore_query:
            if row[1]:
                self.view.high_score_tree.insert('', 'end', text=row[0], values=(row[1], row[2]))
        self.view.hs_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def login(self):
        if self.model.login_email_is_exist(self.view.email_entry.get(), self.view.password_entry.get()):
            self.model.current_email = self.view.email_entry.get()
            self.view.login_frame.place_forget()
            self.view.tool_bar.pack(side=TOP, fill=Y)
        else:
            showerror("Error", "Invalid email or password\nPassword length must be minimum 8 characters")

    def logout(self):
        self.model.current_email = ''
        self.view.game_frame.pack_forget()
        self.view.tool_bar.pack_forget()
        self.view.register_frame.place_forget()
        self.view.hs_frame.place_forget()
        self.view.congrats.place_forget()
        self.view.login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.model.counts = 0
        self.model.sec = 0
        self.view.root.after_cancel(self.model.tick_id)
        self.view.stopwatch['text'] = "00:00"
        self.view.create_toolbar(self.view.tool_bar)

    def sign_up(self):
        self.view.login_frame.place_forget()
        self.view.register_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def register(self):
        date = datetime.fromtimestamp(time()).strftime('%Y-%m-%d, %H:%M:%S')
        if username_is_valid(self.view.username_r_entry.get()):
            if email_is_valid(self.view.email_r_entry.get()):
                if self.model.register_email_is_exist(self.view.email_r_entry.get()):
                    showerror("Error", "Enter another email")
                    return
                if password_is_valid(self.view.password_r_entry.get()):
                    if self.view.name_r_entry.get():
                        if name_is_valid(self.view.name_r_entry.get()):
                            if self.view.surname_r_entry.get():
                                if name_is_valid(self.view.surname_r_entry.get()):
                                    self.model.c.execute('INSERT INTO gameData(Name, Surname, Username, Email, Password, date) VALUES(?, ?, ?, ?, ?, ?)',
                                                         (self.view.name_r_entry.get(), self.view.surname_r_entry.get(), self.view.username_r_entry.get(),
                                                          self.view.email_r_entry.get(), self.view.password_r_entry.get(), date))
                                else:
                                    showerror("Error", "Invalid Surname")
                                    return
                            else:
                                self.model.c.execute('INSERT INTO gameData(Name, Username, Email, Password, date) VALUES(?, ?, ?, ?, ?)',
                                                     (self.view.name_r_entry.get(), self.view.username_r_entry.get(), self.view.email_r_entry.get(),
                                                      self.view.password_r_entry.get(), date))
                        else:
                            showerror("Error", "Invalid Name")
                            return
                    else:
                        self.model.c.execute('INSERT INTO gameData(Username, Email, Password, date) VALUES(?, ?, ?, ?)',
                                             (self.view.username_r_entry.get(), self.view.email_r_entry.get(), self.view.password_r_entry.get(), date))
                    self.model.current_email = self.view.email_r_entry.get()
                    self.view.register_frame.place_forget()
                    self.view.tool_bar.pack(side=TOP, fill=Y)
                    self.model.conn.commit()
                else:
                    showerror("Error", "Invalid password\nPassword length must be minimum 8 characters")
                    return
            else:
                showerror("Error", "Invalid email address")
                return
        else:
            showerror("Error", "Invalid username")
            return

    def move(self, row, column):
        if row == self.model.EL_row - 1 and column == self.model.EL_column:
            self.model.my_labels[self.model.EL_row][self.model.EL_column] \
                .configure(text=self.model.my_labels[self.model.EL_row - 1][self.model.EL_column]['text'], bg="white", font=20)
            self.model.my_labels[self.model.EL_row - 1][self.model.EL_column].configure(text="", bg="black")
            self.model.EL_row -= 1
            self.model.counts += 1
            self.view.count_of_steps['text'] = "Steps: " + str(self.model.counts)
        if row == self.model.EL_row + 1 and column == self.model.EL_column:
            self.model.my_labels[self.model.EL_row][self.model.EL_column] \
                .configure(text=self.model.my_labels[self.model.EL_row + 1][self.model.EL_column]['text'], bg="white", font=20)
            self.model.my_labels[self.model.EL_row + 1][self.model.EL_column].configure(text="", bg="black")
            self.model.EL_row += 1
            self.model.counts += 1
            self.view.count_of_steps['text'] = "Steps: " + str(self.model.counts)
        if row == self.model.EL_row and column == self.model.EL_column - 1:
            self.model.my_labels[self.model.EL_row][self.model.EL_column] \
                .configure(text=self.model.my_labels[self.model.EL_row][self.model.EL_column - 1]['text'], bg="white", font=20)
            self.model.my_labels[self.model.EL_row][self.model.EL_column - 1].configure(text="", bg="black")
            self.model.EL_column -= 1
            self.model.counts += 1
            self.view.count_of_steps['text'] = "Steps: " + str(self.model.counts)
        if row == self.model.EL_row and column == self.model.EL_column + 1:
            self.model.my_labels[self.model.EL_row][self.model.EL_column] \
                .configure(text=self.model.my_labels[self.model.EL_row][self.model.EL_column + 1]['text'], bg="white", font=20)
            self.model.my_labels[self.model.EL_row][self.model.EL_column + 1].configure(text="", bg="black")
            self.model.EL_column += 1
            self.model.counts += 1
            self.view.count_of_steps['text'] = "Steps: " + str(self.model.counts)
        self.check()

    def check(self):
        num = 1
        for row in range(4):
            for column in range(4):
                if self.model.my_labels[row][column].cget('text') == '':
                    return
                elif int(self.model.my_labels[row][column].cget('text')) == num:
                    num += 1
                    continue
                elif row == 3 and column == 1:
                    num = 0
                    self.model.check_notice = True
                    self.view.root.after_cancel(self.model.tick_id)
                    self.view.game_frame.pack_forget()
                    self.view.pause.grid_forget()
                    self.view.congrats.place(relx=0.5, rely=0.5, anchor=CENTER)
                    self.model.c.execute("SELECT time, Steps FROM gameData WHERE Email = ?", (self.model.current_email,))
                    result_from_data = self.model.c.fetchall()
                    try:
                        if result_from_data[0][0] > self.model.sec and result_from_data[0][1] > self.model.counts:
                            self.model.c.execute("UPDATE gameData SET time = (?), Steps = (?) WHERE Email = (?)",
                                                 (self.model.sec, self.model.counts, self.model.current_email))
                            self.model.conn.commit()
                            self.model.c.execute("SELECT Email, Steps, time FROM gameData")
                            self.model.highScore_query = self.model.c.fetchall()
                    except TypeError:
                        self.model.c.execute("UPDATE gameData SET time = (?), Steps = (?) WHERE Email = (?)",
                                             (self.model.sec, self.model.counts, self.model.current_email))
                        self.model.conn.commit()
                        self.model.c.execute("SELECT Email, Steps, time FROM gameData")
                        self.model.highScore_query = self.model.c.fetchall()
                else:
                    return

    def tick(self):
        self.model.tick_id = self.view.root.after(1000, self.tick)
        date = datetime.utcfromtimestamp(self.model.sec).strftime("%M:%S")
        self.view.stopwatch.configure(text=str(date))
        self.model.sec += 1
