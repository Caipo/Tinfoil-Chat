from client import *
from threading import Thread
from datetime import datetime
from time import sleep
import tkinter as tk
from dotenv import load_dotenv 

# Color Scheme for chat app
gunmetal = "#1B2432"
bone = "#DDDBCB"
shiny_shamrock = "#61A886"
dark_liver = "#403F4C"
tea_green = "#D7EBBA"

def main():
    root = tk.Tk()
    LoginWindow(root)
    root.title('Login')


    print("Generating RSA")
    generate_RSA()
    print("Done Generation")

    while True:
        root.mainloop()

class ChatApp:
    @staticmethod
    def ask_for_users():
        while True:
            # We want to ask for a list of users
            get_users()
            sleep(5)

    def update_users(self, new_list):
        global clients
        if isinstance(new_list, set):
            if new_list != clients:
                self.user_box.delete(0, tk.END)
                for idx, val in enumerate(new_list):
                    self.user_box.insert(idx + 1, val)
                    clients = new_list

    def update_chat_log(self, new_msg):
        if isinstance(new_msg, message):
            self.message_box.insert(tk.END,
                                    f"{new_msg.author} : {str(datetime.fromtimestamp(new_msg.time).time())[0:5]}")
            self.message_box.insert(tk.END, f"{new_msg.content}")
            self.message_box.insert(tk.END, "")

    # Sorts the user list form the messages
    def handle_data(self):
        while True:
            data = receive_data()

            # If data is a message sent it to update chat log
            if isinstance(data, message):
                self.update_chat_log(data)

            # If its a set of userse we want to add all of them to the side bar
            if isinstance(data, set):
                self.update_users(data)

    @staticmethod
    def on_closing():
        root.destroy()

    def __init__(self, root):

        # root.protocol("WM_DELETE_WINDOW",  lambda e : self.on_closing() )
        # root.bind('<Escape>', lambda e : self.on_closing(e) )
        root.title("Tinfoil Chat")

        # Update the server users
        self.selected_user = ""  # Will be changed as soon as a user is clicked
        user_box = tk.Listbox(root, background=gunmetal, fg=shiny_shamrock, selectbackground=tea_green, )
        user_box.pack(side="left", fill="y", anchor="w")
        self.user_box = user_box

        message_frame = tk.Frame(bg="blue")
        message_frame.pack(side="right", fill="both", expand=True, anchor="w")

        # All the messages
        message_box = tk.Listbox(message_frame, bd=0, background=dark_liver, fg=bone, width=50)
        message_box.pack(fill="both", expand=True, anchor="w")

        self.message_box = message_box

        # Send box in the chat app
        send_box = tk.Entry(message_frame, background=bone, fg=gunmetal)
        send_box.pack(side="bottom", fill="both", anchor="s")
        self.send_box = send_box

        def gui_send(event):
            send_to(send_box.get())
            send_box.delete(0, tk.END)

        root.bind('<Return>', lambda e: gui_send(e))

        # Asks the server whom online
        ask_users_thread = Thread(target=self.handle_data)
        ask_users_thread.start()

        # Keeps getting the data from the server and handles it
        handle_data = Thread(target=self.ask_for_users)
        handle_data.start()
        
# This is the initial log in window
class LoginWindow():
    def __init__(self, root):
        self.root = root
        root.resizable(False, False)
        root.bind('<Escape>', lambda e: self.submit())

        def submit():
            password = password_var.get()
            ip = ip_var.get()
            port = port_var.get()


            if secure_login(ip, port, password):
                root.destroy()
                root2 = tk.Tk()
                root2.title("Tin Foil Chat")
                ChatApp(root2)

                while True:
                    root2.mainloop()

            #except Exception as e:
            #    print(e)

                password_var.set("")

        # setting the windows size
        root.geometry("250x100")

        # Strings for labels
        password_var = tk.StringVar()
        ip_var = tk.StringVar()
        port_var = tk.StringVar()

        # IP box
        ip_label = tk.Label(root, text='ip', font=('calibre', 10, 'bold'))
        ip_entry = tk.Entry(root, textvariable=ip_var, font=('calibre', 10, 'normal'), )
        ip_entry.insert(0, "192.168.1.68")

        # Port Box
        port_label = tk.Label(root, text='Port', font=('calibre', 10, 'bold'))
        port_entry = tk.Entry(root, textvariable=port_var, font=('calibre', 10, 'normal'))
        port_entry.insert(0, "1234")

        # Password box
        password_label = tk.Label(root, text='Password', font=('calibre', 10, 'bold'))
        password_entry = tk.Entry(root, textvariable=password_var, font=('calibre', 10, 'normal'), show="*")
        password_entry.insert(0, "blap")

        # Enter Button
        sub_btn = tk.Button(root, text='Submit', command=submit)

        # Placing
        ip_label.grid(row=0, column=0)
        ip_entry.grid(row=0, column=1)

        port_label.grid(row=1, column=0)
        port_entry.grid(row=1, column=1)

        password_label.grid(row=2, column=0)
        password_entry.grid(row=2, column=1)

        sub_btn.grid(row=3, column=1)

        def on_closing(event=None):
            exit() 

if __name__ == "__main__":
    main()
