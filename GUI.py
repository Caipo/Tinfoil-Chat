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
            self.seleced_user = value
            print( "You selected item ", value)

        except:
            pass

    def update_chat_log(self):
        """Handles receiving of messages."""
        while True:
            
            new_msg = receive_data()
            if isinstance(new_msg, message):
                print(new_msg.content)
                self.message_box.insert(tk.END,  f"{new_msg.content}")



                
    def on_closing(event=None):
        """This function is to be called when the window is closed."""
        logout()
        exit()
            



    def __init__(self, root):


        def update_users():
            global clients




            get_users()
            if isinstance( new_list := receive_data(), set):
                for idx, val in enumerate(new_list):
                    userbox.insert(idx + 1, val.name )
                    clients = new_list
                    print("clients asdf")





        self.seleced_user = ""
        userbox = Listbox(root, background = gunmetal, fg = shiny_shamrock, selectbackground = tea_green, )



        message_frame = Frame(bg = "blue")
        message_frame.pack(side ="right", fill = "both",  expand = True, anchor = "w")


        self.str_label = StringVar()
        user_label = Label(message_frame, bd = 0,bg = dark_liver, textvariable = self.str_label, font=("Arial", 16), fg = shiny_shamrock)
        self.str_label.set("")
        user_label.pack(side = "top", fill = "both", anchor = "n", expand = False)



        message_box = Listbox(message_frame ,  bd = 0, background = dark_liver, fg = bone, width = 50)
        message_box.pack(  fill = "both" , expand= True , anchor = "w")



        self.message_box = message_box
        
        send_box = Entry(message_frame,  background = bone, fg = gunmetal)
        send_box.pack(side = "bottom", fill = "both", anchor = "s")
        self.send_box = send_box

        def gui_send(event, seleced_user):
            send_to(seleced_user, send_box.get())
            send_box.delete(0, END)

        root.bind('<Return>',  lambda e : gui_send( e,self.seleced_user))
        
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
         
            name = name_var.get()
            ip = ip_var.get()
            port=port_var.get()

            try:
                if login(port, name, ip ):
                    root.destroy()
                    root2 = Tk()
                    root2.title =  "Tin Foil Chat"
                    chat_app(root2)

                    while True:
                        root2.mainloop()

            except Exception as e:
                print(e)

                name_var.set("")
                ip_var.set("")
                port_var.set("")

        # setting the windows size
        root.geometry("250x100")
          
        # declaring string variable
        # for storing name and portord
        name_var=tk.StringVar()
        ip_var = tk.StringVar()
        port_var=tk.StringVar()
         


        # name using widget Label
        name_label = tk.Label(root, text = 'Username', font=('calibre',10, 'bold'))
        name_entry = tk.Entry(root,textvariable = name_var, font=('calibre',10,'normal'))

        ip_label = tk.Label(root, text='ip', font=('calibre', 10, 'bold'))
        ip_entry = tk.Entry(root, textvariable= ip_var, font=('calibre', 10, 'normal'))

        port_label = tk.Label(root, text = 'Port', font = ('calibre',10,'bold'))
        port_entry=tk.Entry(root, textvariable = port_var, font = ('calibre',10,'normal'))



        sub_btn=tk.Button(root,text = 'Submit', command = submit)
          
        #Placing
        name_label.grid(row=0,column=0)
        name_entry.grid(row=0,column=1)

        ip_label.grid(row=1,column=0)
        ip_entry.grid(row=1,column=1)

        port_label.grid(row=2,column=0)
        port_entry.grid(row=2,column=1)

        sub_btn.grid(row=3,column=1)

        def on_closing(event=None):
            """This function is to be called when the window is closed."""
            exit()



if __name__ == "__main__":

    root = tk.Tk()
    login_window(root)
    root.title('Tin Foil Chat')

    while True:
        root.mainloop()

    




    
