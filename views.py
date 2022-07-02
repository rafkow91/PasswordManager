from tkinter import END, IntVar, StringVar, Tk
from tkinter.font import BOLD
from tkinter.ttk import Button, Entry, Notebook, Frame, Treeview, Label, Radiobutton

from controllers import Database


class Application:
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug
        self.database = Database(debug)
        self.root = Tk()
        self.filter_choice = IntVar()
        self.filter_phrase = StringVar()

    def run(self) -> None:
        self.root.geometry('620x500')
        self.root.title('Password manager by rafkow91')
        for i in range(0, 6):
            self.root.rowconfigure(i, minsize=30)
            self.root.columnconfigure(i, minsize=30)

        # Tabs
        tabsystem = Notebook(self.root)
        self.saved_passwords_tab = Frame(tabsystem)
        self.add_password_tab = Frame(tabsystem)

        tabsystem.add(self.saved_passwords_tab, text='Saved passwords')
        tabsystem.add(self.add_password_tab, text='Add new password')
        tabsystem.pack(expand=1, fill='both')

        self._render_saved_passwords_tab()

        # Draw the window
        self.root.mainloop()

    def on_click_add_button(self, event):
        print('on_click_add_button')

    def _search_in_websites(self):
        pass

    def _search_in_users(self):
        pass

    def _search_in_categories(self):
        pass

    def _render_saved_passwords_tab(self):
        self.passwords_list = self.database.get_all_accounts()

        # Function used in method
        def on_treeview_select(event):
            try:
                item = self.saved_passwords_tree.selection()[0]
                print(self.saved_passwords_tree.item(item, 'values'))
            except IndexError:
                pass

        def on_click_filter_button(event):
            def search_in_all_columns():
                to_return = []
                for i in range(1, 4):
                    accounts = choice[i](filter_entry.get())
                    for account in accounts:
                        to_return.append(account)

                return to_return

            choice = {
                0: search_in_all_columns,
                1: self.database.search_in_website_name,
                2: self.database.search_in_username,
                3: self.database.search_in_category_name,
            }

            passwords_list = choice[self.filter_choice.get()](filter_entry.get())

            generate_tree(passwords_list)

        def on_click_reset_button(event):
            filter_entry.delete(0, END)
            self.passwords_list = self.database.get_all_accounts()
            generate_tree(self.passwords_list)

        def generate_tree(passwords):
            for i in self.saved_passwords_tree.get_children():
                self.saved_passwords_tree.delete(i)
            for password in passwords:
                self.saved_passwords_tree.insert(
                    '', 'end',
                    values=(
                        password[1],
                        password[2],
                        password[3],
                    ))

        # Frames
        top_frame = Frame(self.saved_passwords_tab)
        top_frame.pack()

        botton_frame = Frame(self.saved_passwords_tab)
        botton_frame.pack()

        # Tables with saved passwords
        saved_passwords_label = Label(top_frame, text='Saved passwords', font=('', 15, BOLD))
        saved_passwords_label.grid(column=0, row=0)

        self.saved_passwords_tree = Treeview(
            top_frame,
            columns=('website', 'user', 'category'),
            show='headings',
            height=15
        )
        self.saved_passwords_tree.heading('website', text='Website')
        self.saved_passwords_tree.heading('user', text='User')
        self.saved_passwords_tree.heading('category', text='Category')

        generate_tree(self.passwords_list)

        self.saved_passwords_tree.bind('<<TreeviewSelect>>', on_treeview_select)
        self.saved_passwords_tree.grid(column=0, row=1)

        # Filter phrase
        filter_entry_label = Label(botton_frame, text='Searched phrase: ')
        filter_entry_label.grid(column=0, row=0, padx=2)

        filter_entry = Entry(botton_frame)
        filter_entry.grid(column=1, row=0, columnspan=3)

        # Filter options
        filter_label = Label(botton_frame, text='Search in: ')
        filter_label.grid(column=0, row=1, padx=2)

        all_columns = Radiobutton(
            botton_frame,
            text='all columns',
            variable=self.filter_choice,
            value=0
        )
        all_columns.grid(column=1, row=1, padx=5)

        website = Radiobutton(
            botton_frame,
            text='websites',
            variable=self.filter_choice,
            value=1
        )
        website.grid(column=2, row=1, padx=5)

        user = Radiobutton(
            botton_frame,
            text='users name',
            variable=self.filter_choice,
            value=2,
        )
        user.grid(column=3, row=1, padx=5)

        category = Radiobutton(
            botton_frame,
            text='category names',
            variable=self.filter_choice,
            value=3
        )
        category.grid(column=4, row=1, padx=5)

        # Reset filter button
        reset_button = Button(botton_frame, text='Reset filtering')
        reset_button.bind('<Button-1>', on_click_reset_button)
        reset_button.grid(column=4, row=2, pady=10)

        # Filter button
        filter_button = Button(botton_frame, text='Filter')
        filter_button.bind('<Button-1>', on_click_filter_button)
        filter_button.grid(column=5, row=2, pady=10)

    def _render_add_password_tab(self, tab):

        # Add button
        button = Button(tab, text='Add new password')
        button.bind('<Button-1>', self.on_click_add_button)
        button.grid(column=4, row=1, padx=5)
