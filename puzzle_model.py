import sqlite3


class PuzzleModel:

    def __init__(self):

        self.conn = sqlite3.connect('fifteen_puzzle.db')
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS gameData(Username TEXT, Name TEXT, Surname TEXT,\
        Password TEXT, Email TEXT, Steps INTEGER, time INTEGER, date TEXT)')

        self.numbers = [i for i in range(1, 16)]
        self.my_labels = dict()
        self.sec, self.counts = 0, 0
        self.tick_id = ''
        self.EL_row, self.EL_column = 0, 0
        self.current_email = ''
        self.flag = True
        self.check_notice = False

        self.c.execute("SELECT Email, Steps, time FROM gameData")
        self.highScore_query = self.c.fetchall()

    def register_email_is_exist(self, email):
        self.c.execute("SELECT * FROM gameData WHERE Email = (?)", (email,))
        if self.c.fetchall():
            return True
        return False

    def login_email_is_exist(self, email, password):
        self.c.execute('SELECT * FROM gameData WHERE Password = (?) AND Email = (?)', (password, email))
        if self.c.fetchall():
            return True
        return False
