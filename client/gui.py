import tkinter as tk


def create_window() -> tk.Tk:
    window = tk.Tk()
    window.grid(2, 4, 1, 1)
    window.title('Pygeon')
    return window


def show_login_frame(window: tk.Tk):

    def _validate_login():
        print("username entered :", username.get())
        print("password entered :", password.get())
        logged_in = True
        if logged_in:
            login_frame.destroy()
            show_users_list_frame(window)
        else:
            error_msg.set("Bad credentials !")

    login_frame = tk.Frame(window)
    login_frame.grid(row=0, rowspan=3, column=0, columnspan=2, padx=20, pady=20)

    # username label and text entry box
    username = tk.StringVar()
    tk.Label(login_frame, text="User Name").grid(row=0, column=0, padx=5, sticky='e')
    tk.Entry(login_frame, textvariable=username).grid(row=0, column=1, pady=2)

    # password label and password entry box
    password = tk.StringVar()
    tk.Label(login_frame, text="Password").grid(row=1, column=0, padx=5, sticky='e')
    tk.Entry(login_frame, textvariable=password, show='*').grid(row=1, column=1, pady=2)

    # login button
    tk.Button(login_frame, text="Login", command=_validate_login).grid(row=2, column=1, pady=5, sticky='w')

    error_msg = tk.StringVar()
    tk.Label(login_frame, textvariable=error_msg).grid(row=3, column=0, columnspan=2)


def show_users_list_frame(window: tk.Tk):

    def _select_user():
        if users_list.curselection():
            user = users_list.get(users_list.curselection()[0])
            print("Selected", user)
            users_frame.destroy()
            show_chat_frame(window, user)

    window.grid(1, 2, 1, 1)

    users_frame = tk.Frame(window)
    users_frame.grid(row=0, rowspan=1, column=0, columnspan=2, padx=20, pady=20)

    users_list = tk.Listbox(users_frame)
    users_list.insert(0, "Toto")
    users_list.insert(1, "Toto1")
    users_list.insert(2, "Toto2")
    users_list.grid(row=0, column=0)

    tk.Button(users_frame, text="Select", command=_select_user).grid(row=1, column=0, pady=15)


def show_chat_frame(window: tk.Tk, user: str):

    def _send_msg():
        textbox.configure(state=tk.NORMAL)
        textbox.insert('end', message.get())
        textbox.insert('end', '\n')
        textbox.configure(state=tk.DISABLED)
        message.set("")

    window.grid(2, 3, 1, 1)

    chat_frame = tk.Frame(window, width=50)
    chat_frame.grid(row=0, rowspan=2, column=0, columnspan=3, padx=20, pady=20)

    tk.Label(chat_frame, text=user).grid(row=0, column=0, columnspan=2, pady=15)

    textbox = tk.Text(chat_frame, width=30, height=10)
    textbox.grid(row=2, column=0, columnspan=2)
    textbox.configure(state=tk.DISABLED)

    # password label and password entry box
    message = tk.StringVar()
    tk.Entry(chat_frame, textvariable=message).grid(row=3, column=0)
    tk.Button(chat_frame, text="Send", command=_send_msg).grid(row=3, column=1, padx=5, pady=10)
