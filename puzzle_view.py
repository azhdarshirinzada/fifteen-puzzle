from tkinter import *
import ttk
from puzzle_controller import PuzzleController


class PuzzleView:

    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.controller = PuzzleController(self.model, self)

        self.login_frame = Frame(self.root, bg="white")
        self.login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.create_login_ui(self.login_frame)

        self.register_frame = Frame(self.root, bg="white")
        self.create_register_ui(self.register_frame)

        self.main_menu = Menu(self.root)
        self.menu(self.main_menu)

        self.game_frame = Frame(self.root, bg="black")

        self.tool_bar = Frame(self.root, bg="white")

        self.create_toolbar(self.tool_bar)

        self.congrats = Label(self.root, text="Congratulations!", font=100, bg="white", fg="green")

        self.hs_frame = Frame(self.root, bg="white")
        self.high_score_tree = ttk.Treeview(self.hs_frame, columns=('Steps', 'Time'), selectmode=NONE)
        self.return_btn = Button(self.hs_frame, text="Return", font=15, command=self.controller.return_was_clicked)
        self.high_score_tree.heading('#0', text="User's email")
        self.high_score_tree.heading('#1', text='Steps')
        self.high_score_tree.heading('#2', text='Time (in sec.)')
        self.high_score_tree.pack(side=TOP, fill=BOTH)

        self.return_btn.pack(side=BOTTOM, fill=X)

    def create_register_ui(self, frame):
        self.username_r = Label(frame, bg="white", fg="black", text="*Username: ", font=15)
        self.username_r.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.username_r_entry = Entry(frame, font=15)
        self.username_r_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        self.name_r = Label(frame, bg="white", fg="black", text="Name: ", font=15)
        self.name_r.grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.name_r_entry = Entry(frame, font=15)
        self.name_r_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        self.surname_r = Label(frame, bg="white", fg="black", text="Surname: ", font=15)
        self.surname_r.grid(row=2, column=0, padx=5, pady=5, sticky=E)
        self.surname_r_entry = Entry(frame, font=15)
        self.surname_r_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        self.email_r = Label(frame, bg="white", fg="black", text="*Email: ", font=15)
        self.email_r.grid(row=3, column=0, padx=5, pady=5, sticky=E)
        self.email_r_entry = Entry(frame, font=15)
        self.email_r_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        self.password_r = Label(frame, bg="white", fg="black", text="*Password: ", font=15)
        self.password_r.grid(row=4, column=0, padx=5, pady=5, sticky=E)
        self.password_r_entry = Entry(frame, font=15, show='*')
        self.password_r_entry.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        self.register_btn = Button(frame, text="Register", font=15, command=self.controller.register)
        self.register_btn.grid(row=5, column=1, padx=5, pady=5, sticky=EW)

    def create_login_ui(self, frame):
        self.email_label = Label(frame, bg="white", fg="black", text="Email: ", font=15)
        self.email_label.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.email_entry = Entry(frame)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        self.password_label = Label(frame, bg="white", fg="black", text="Password: ", font=15)
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.password_entry = Entry(frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        self.login_btn = Button(frame, text="Log in", command=self.controller.login)
        self.login_btn.grid(row=2, column=1, padx=5, pady=5, sticky=EW)

        self.signup_btn = Button(frame, text="Sign up", command=self.controller.sign_up)
        self.signup_btn.grid(row=2, column=0, padx=5, pady=5, sticky=EW)

    def create_toolbar(self, toolbar):
        self.start = Button(toolbar, text="Start", font=15, command=self.controller.start_was_clicked)
        self.start.grid(row=0, column=0, padx=5, pady=5, sticky=EW)
        self.reset = Button(toolbar, text="Reset", font=15, state=DISABLED, command=self.controller.reset_was_clicked)
        self.reset.grid(row=0, column=1, padx=5, pady=5, sticky=EW)
        self.pause = Button(toolbar, text="Pause", font=15, state=DISABLED, command=self.controller.pause_was_clicked)
        self.pause.grid(row=0, column=2, padx=5, pady=5, sticky=EW)
        self.continuebtn = Button(toolbar, text="Continue", font=15, command=self.controller.continue_was_clicked)
        self.stopwatch = Label(toolbar, width=5, font=15, text="00:00")
        self.stopwatch.grid(row=0, column=3, padx=5, pady=5, sticky=EW)
        self.count_of_steps = Label(toolbar, font=15, bg="white", fg="black",
                                    text="Steps: " + str(self.model.counts))
        self.count_of_steps.grid(row=1, column=0, padx=5, pady=5)

    def menu(self, menu):
        self.root.configure(menu=menu)
        file = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file)
        file.add_command(label="High scores", command=self.controller.high_scores)
        file.add_separator()
        file.add_command(label="Log out", command=self.controller.logout)
        file.add_separator()
        file.add_command(label="Exit", command=lambda: quit())
