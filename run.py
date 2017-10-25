from tkinter import Tk
from puzzle_model import PuzzleModel
from puzzle_view import PuzzleView


if __name__ == '__main__':

    root = Tk()
    root.title("Fifteen Puzzle")
    root.configure(bg="white")
    root.minsize(width=610, height=450)

    model = PuzzleModel()
    view = PuzzleView(root, model)

    root.mainloop()
