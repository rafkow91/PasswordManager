from tkinter import Tk
from tkinter.ttk import Button, Label

from pyparsing import col

from controllers import Database


class Application:
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug
        self.database = Database(debug)
        self.root = Tk()

    def run(self) -> None:
        self.root.geometry('500x500')
        self.root.title('Password manager by rafkow91')
        for i in range(0,6):
            self.root.rowconfigure(i, minsize=30)
            self.root.columnconfigure(i, minsize=30)


        # Main window label
        label = Label(self.root, text='Password Manager')
        label.grid(column=0, row=0, columnspan=4, )

        # Filter button
        button = Button(text='Filter')
        button.bind('<Button-1>', self.on_click_filter_button)
        button.grid(column=4, row=1)

        # Draw the window
        self.root.mainloop()

    def on_click_filter_button(self, event):
        print('on_click_filter_button')
