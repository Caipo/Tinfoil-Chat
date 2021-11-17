import tkinter as tk
from Client import *
import threading, asyncio
'''
class login_window():

    def __init__(self, root):
        self.root = root
        
    
        def submit():
            global root
         
            name=name_var.get()
            port=port_var.get()

            try:
                login(port, name)
                print("Connected To Tinfoil Chat")
                #root.destroy()
                
                
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
      
'''





    


login(8, "nick")




def on_closing(event=None):
    """This function is to be called when the window is closed."""
    exit()
    my_msg.set("{quit}")


def r():
    global msg_list
    """Handles receiving of messages."""
    while True:
        
        print( "\n 1234123", s :=  recive())
        msg_list.insert(tk.END, s)

    



    
top = tk.Tk()
top.title("Chatter")

messages_frame = tk.Frame(top)
my_msg = tk.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tk.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tk.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send_to)
entry_field.pack()
send_button = tk.Button(top, text="Send", command=lambda:send_to("nick", my_msg.get() ))
send_button.pack()

receive_thread = threading.Thread(target=r)
receive_thread.start()

while True:

    tk.mainloop()




   
    

top.protocol("WM_DELETE_WINDOW", on_closing)
    


    
    



#chat()

    
