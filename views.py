from tkinter import END, IntVar, Tk
from tkinter.font import BOLD, ITALIC
from tkinter.ttk import Button, Entry, Notebook, Frame, Treeview, Label, Radiobutton

from controllers import Database


class Application:
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug
        self.database = Database(debug)
        self.root = Tk()
        self.filter_choice = IntVar()

    def run(self) -> None:
        self.root.geometry('620x550')
        self.root.title('Password manager by rafkow91')
        # for i in range(0, 6):
        #     self.root.rowconfigure(i, minsize=30)
        #     self.root.columnconfigure(i, minsize=30)

        # Tabs
        tabsystem = Notebook(self.root)
        self.saved_passwords_tab = Frame(tabsystem)
        self.add_password_tab = Frame(tabsystem)
        self.categories_tab = Frame(tabsystem)

        tabsystem.add(self.saved_passwords_tab, text='Saved passwords')
        tabsystem.add(self.add_password_tab, text='Add new password')
        tabsystem.add(self.categories_tab, text='Categories')
        tabsystem.pack(expand=1, fill='both')

        self._render_saved_passwords_tab()
        self._render_add_password_tab()
        self._render_categories_tab()

        # Draw the window
        self.root.mainloop()

    def _render_saved_passwords_tab(self):
        self.passwords_list = self.database.get_all_accounts()

        # Function used in method
        def on_treeview_select(event):
            try:
                item = self.saved_passwords_tree.selection()[0]
                selected_account_id = self.saved_passwords_tree.item(item, 'values')[3]
            except IndexError:
                pass
            password = self.database.get_password(selected_account_id)
            self.root.clipboard_clear()
            self.root.clipboard_append(password)

        def on_click_filter_button(event):
            def search_in_all_columns(event):
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
                        password.website,
                        password.login,
                        password.category.name,
                        password.id,
                    ))

        # Frames
        header = Frame(self.saved_passwords_tab)
        header.pack()

        main_content = Frame(self.saved_passwords_tab)
        main_content.pack()

        filter_frame = Frame(self.saved_passwords_tab)
        filter_frame.pack()

        # Header
        saved_passwords_label = Label(header, text='Saved passwords', font=('', 15, BOLD))
        saved_passwords_label.grid(pady=10)

        # Refresh button
        refresh_button = Button(main_content, text='Refresh table')
        refresh_button.bind('<Button-1>', on_click_reset_button)
        refresh_button.grid(column=10, row=0, pady=2)

        self.saved_passwords_tree = Treeview(
            main_content,
            columns=('website', 'user', 'category', 'account_id'),
            show='headings',
            height=15
        )

        self.saved_passwords_tree.heading('website', text='Website')
        self.saved_passwords_tree.heading('user', text='User')
        self.saved_passwords_tree.heading('category', text='Category')
        self.saved_passwords_tree['displaycolumns'] = ('website', 'user', 'category')

        generate_tree(self.passwords_list)

        self.saved_passwords_tree.bind('<<TreeviewSelect>>', on_treeview_select)
        self.saved_passwords_tree.grid(column=0, row=1, columnspan=11)

        # Filter phrase
        filter_entry_label = Label(filter_frame, text='Searched phrase: ')
        filter_entry_label.grid(column=0, row=0, padx=2)

        filter_entry = Entry(filter_frame)
        filter_entry.grid(column=1, row=0, columnspan=3)

        # Filter options
        filter_label = Label(filter_frame, text='Search in: ')
        filter_label.grid(column=0, row=1, padx=2)

        all_columns = Radiobutton(
            filter_frame,
            text='all columns',
            variable=self.filter_choice,
            value=0
        )
        all_columns.grid(column=1, row=1, padx=5)

        website = Radiobutton(
            filter_frame,
            text='websites',
            variable=self.filter_choice,
            value=1
        )
        website.grid(column=2, row=1, padx=5)

        user = Radiobutton(
            filter_frame,
            text='users name',
            variable=self.filter_choice,
            value=2,
        )
        user.grid(column=3, row=1, padx=5)

        category = Radiobutton(
            filter_frame,
            text='category names',
            variable=self.filter_choice,
            value=3
        )
        category.grid(column=4, row=1, padx=5)

        # Reset filter button
        reset_button = Button(filter_frame, text='Reset filtering')
        reset_button.bind('<Button-1>', on_click_reset_button)
        reset_button.grid(column=4, row=2, pady=10)

        # Filter button
        filter_button = Button(filter_frame, text='Filter')
        filter_button.bind('<Button-1>', on_click_filter_button)
        filter_button.grid(column=5, row=2, pady=10)

    def _render_add_password_tab(self):
        def on_click_add_button(event):
            result = self.database.add_account(
                login=login_entry.get(),
                password=password_entry.get(),
                website=website_entry.get(),
                category_name=category_entry.get()
            )

            if not result:
                error_label['text'] = 'THIS ACCOUNT EXIST IN DATABASE'
            else:
                error_label['text'] = ''
                login_entry.delete(0, END)
                password_entry.delete(0, END)
                website_entry.delete(0, END)
                category_entry.delete(0, END)

        # Frames
        header = Frame(self.add_password_tab)
        header.pack()

        main_content = Frame(self.add_password_tab)
        main_content.pack()

        add_button_frame = Frame(self.add_password_tab)
        add_button_frame.pack()

        # Header
        add_password_label = Label(header, text='Add new password', font=('', 15, BOLD))
        add_password_label.grid(row=0, pady=10)

        error_label = Label(header, text='', font=('', 8, ITALIC, BOLD), foreground='red')
        error_label.grid(row=1, pady=10)

        # Form
        login_label = Label(main_content, text='Login:')
        login_label.grid(column=0, row=0, pady=2, padx=5, sticky='e')
        login_entry = Entry(main_content)
        login_entry.grid(column=1, row=0, pady=2)

        password_label = Label(main_content, text='Password:')
        password_label.grid(column=0, row=1, pady=2, padx=5, sticky='e')
        password_entry = Entry(main_content, show='*')
        password_entry.grid(column=1, row=1, pady=2)

        website_label = Label(main_content, text='Website:')
        website_label.grid(column=0, row=2, pady=2, padx=5, sticky='e')
        website_entry = Entry(main_content)
        website_entry.grid(column=1, row=2, pady=2)

        category_label = Label(main_content, text='Category:')
        category_label.grid(column=0, row=3, pady=2, padx=5, sticky='e')
        category_entry = Entry(main_content)
        category_entry.grid(column=1, row=3, pady=2)

        # Add button
        button = Button(add_button_frame, text='Add new password')
        button.bind('<Button-1>', on_click_add_button)
        button.grid(column=4, row=1, pady=15)

    def _render_categories_tab(self):
        self.categories_list = self.database.get_all_categories()

        # Function used in method
        def on_treeview_select(event):
            try:
                item = self.saved_passwords_tree.selection()[0]
                category_name = self.saved_passwords_tree.item(item, 'values')[0]
            except IndexError:
                pass
            self.root.clipboard_clear()
            self.root.clipboard_append(category_name)

        def on_click_refresh_button(event):
            self.categories_list = self.database.get_all_categories()
            generate_tree(self.categories_list)

        def on_click_add_button(event):
            result = self.database.add_category(
                name=add_category_entry.get()
            )

            if not result:
                error_label['text'] = 'THIS CATEGORY EXIST IN DATABASE'
            else:
                error_label['text'] = ''
                add_category_entry.delete(0, END)

        def generate_tree(categories):
            for i in self.categories_tree.get_children():
                self.categories_tree.delete(i)
            for category in categories:
                self.categories_tree.insert(
                    '', 'end',
                    values=(category.name))

        # Frames
        header = Frame(self.categories_tab)
        header.pack()

        header2 = Frame(self.categories_tab)
        header2.pack()

        main_content = Frame(self.categories_tab)
        main_content.pack()

        add_category_frame = Frame(self.categories_tab)
        add_category_frame.pack()

        # Header
        categories_label = Label(header, text='Categories', font=('', 15, BOLD))
        categories_label.grid(pady=10)

        error_label = Label(header, text='', font=('', 8, ITALIC, BOLD), foreground='red')
        error_label.grid(row=1, pady=10)

        # Refresh button
        refresh_button = Button(header2, text='Refresh table')
        refresh_button.bind('<Button-1>', on_click_refresh_button)
        refresh_button.grid(column=10, row=1, pady=2, padx=130)

        self.categories_tree = Treeview(
            main_content,
            columns=('name'),
            show='headings',
            height=15
        )

        self.categories_tree.heading('name', text='Category name')

        generate_tree(self.categories_list)

        self.categories_tree.bind('<<TreeviewSelect>>', on_treeview_select)
        self.categories_tree.grid(column=0, row=1, columnspan=11)

        # Filter phrase
        add_category_entry_label = Label(add_category_frame, text='Add new category: ')
        add_category_entry_label.grid(column=0, row=0, padx=2)

        add_category_entry = Entry(add_category_frame)
        add_category_entry.grid(column=1, row=0, columnspan=3)

        # Add button
        button = Button(add_category_frame, text='Add')
        button.bind('<Button-1>', on_click_add_button)
        button.grid(column=4, row=1, pady=15)
