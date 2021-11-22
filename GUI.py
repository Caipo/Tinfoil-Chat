import tkinter as tk
from Client import *
import threading
from tkinter import *


gunmetal =  "#1B2432"
bone =  "#DDDBCB"
shiny_shamrock = "#61A886"
dark_liver = "#403F4C"
tea_green = "#D7EBBA"



class chat_app:

    def onselect(self, evt):
        try:

            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            self.str_label.set(value)
            print( "You selected item ", value)

        except:
            pass

    def update_chat_log(self):
        """Handles receiving of messages."""
        while True:
            
            new_msg = receive_data()
            if isinstance(new_msg, message):
                print(new_msg.content)
                self.message_box.insert(tk.END, f"{new_msg.author}: {new_msg.content}")



                

            



    def __init__(self, root):


        def update_users():
            from Client import clients
            print(clients , "in da update users")

            get_users()
            if isinstance( new_list := receive_data(), list):

                for idx, val in enumerate(new_list):
                    userbox.insert(idx + 1, val.name )

            '''
            for idx, val in enumerate(clients):
                print(val.name)
                userbox.insert(idx + 1, val.name )
                userbox.update()
            '''

            '''
            while True:
                if len(new_clients) != len(clients):
                    for idx, val in new_clients:
                        message_box.insert(idx + 1, val )  
    '''

        userbox = Listbox(root, background = gunmetal, fg = shiny_shamrock, selectbackground = tea_green, )






        message_frame = Frame(bg = "blue")
        message_frame.pack(side ="right", fill = "both",  expand = True, anchor = "w")


        self.str_label = StringVar()
        user_label = Label(message_frame, bd = 0,bg = dark_liver, textvariable = self.str_label, font=("Arial", 16), fg = shiny_shamrock)
        self.str_label.set("")
        user_label.pack(side = "top", fill = "both", anchor = "n", expand = False)



        message_box = Listbox(message_frame ,  bd = 0, background = dark_liver, fg = bone, width = 50)
        for idx, val in enumerate(["hello", "good bye"]):
            message_box.insert(idx + 1, val )  
        message_box.pack(  fill = "both" , expand= True , anchor = "w")



        self.message_box = message_box
        
        send_box = Entry(message_frame,  background = bone, fg = gunmetal)
        send_box.pack(side = "bottom", fill = "both", anchor = "s")


        gui_send = lambda event: send_to("nick", send_box.get())
        root.bind('<Return>',  gui_send)
        
        receive_thread = threading.Thread(target=self.update_chat_log)
        receive_thread.start()

        print(clients, "in the init")

        users_thread = threading.Thread(target=update_users)
        users_thread.start()


        
        
        userbox.pack(side = "left", fill = "y", anchor = "w")
        userbox.bind('<<ListboxSelect>>', self.onselect)
        receive_thread = threading.Thread(target= update_users)
        receive_thread.start()










    




class login_window():

    def __init__(self, root):
        self.root = root
        
    
        def submit():
            global root
         
            name=name_var.get()
            port=port_var.get()

            try:
                if login(port, name):
                    root.destroy()


            except Exception as e:
                print(e)
             
                name_var.set("")
                port_var.set("")



        
         
        # setting the windows size
        root.geometry("250x100")
          
        # declaring string variable
        # for storing name and portord
        name_var=tk.StringVar()
        port_var=tk.StringVar()
         
          
        # defining a function that will
        # get the name and portord and

            # print them on the screen

             
             
        # creating a label for
        # name using widget Label
        name_label = tk.Label(root, text = 'Username', font=('calibre',10, 'bold'))
          
        # creating a entry for input
        # name using widget Entry
        name_entry = tk.Entry(root,textvariable = name_var, font=('calibre',10,'normal'))
          
        # creating a label for portord
        port_label = tk.Label(root, text = 'Port', font = ('calibre',10,'bold'))
          
        # creating a entry for ord
        port_entry=tk.Entry(root, textvariable = port_var, font = ('calibre',10,'normal'))
          
        # creating a button using the widget
        # Button that will call the submit function
        sub_btn=tk.Button(root,text = 'Submit', command = submit)
          
        # placing the label and entry in
        # the required position using grid
        # method
        name_label.grid(row=0,column=0)
        name_entry.grid(row=0,column=1)
        port_label.grid(row=1,column=0)
        port_entry.grid(row=1,column=1)
        sub_btn.grid(row=2,column=1)
      

        def on_closing(event=None):
            """This function is to be called when the window is closed."""
            exit()




'''
class chat_window:

    def on_closing(event=None):
        """This function is to be called when the window is closed."""
        exit()
        my_msg.set("{quit}")


    def update_log(self):
        """Handles receiving of messages."""
        while True:
            
            new_msg = receive()
            self.msg_list.insert(tk.END, f"{new_msg.author}: {new_msg.content}")
            

    def __init__(self, root):

    

        
        top = root
        top.title("Chatter")

        messages_frame = tk.Frame(top)
        my_msg = tk.StringVar()  # For the messages to be sent.
        my_msg.set("Type your messages here.")
        scrollbar = tk.Scrollbar(messages_frame)  # To navigate through past messages.
        # Following will contain the messages.
        self.msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.msg_list.pack()
        messages_frame.pack()

        entry_field = tk.Entry(top, textvariable=my_msg)
        entry_field.bind("<Return>", get_users)
        entry_field.pack()
        send_button = tk.Button(top, text="Send", command=lambda:send_to("nick", my_msg.get() ))
        send_button.pack()


        #listbox = tk.Listbox(messages_frame, ["blap"], 10)

        
        receive_thread = threading.Thread(target=self.update_log)
        receive_thread.start()
'''


if __name__ == "__main__":
    login(input(), "nick")
    root = tk.Tk()
    root.title('Tin Foil Chat')
    chat_app(root)
    
    while True:
        tk.mainloop()
    top.protocol("WM_DELETE_WINDOW", on_closing)


    
