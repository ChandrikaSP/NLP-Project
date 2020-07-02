from tkinter import *
import numpy as np
import time
import tkinter.messagebox
from app_console import chat
import pyttsx3
import threading
from tkinter.ttk import Combobox
from tkinter import Tk, Frame, Button
from tkinter import BOTH, LEFT

saved_username = ["You"]

window_size="400x400"

class ChatInterface(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        
        
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"
        self.font = "Verdana 10"

        menu = Menu(self.master)
        self.master.config(menu=menu, bd=5)

        file = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file)
       
        file.add_command(label="Clear Chat", command=self.clear_chat)
     
        file.add_command(label="Exit",command=self.chatexit)

    
        options = Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=options)

        # font
        font = Menu(options, tearoff=0)
        options.add_cascade(label="Font", menu=font)
        font.add_command(label="Default",command=self.font_change_default)
        font.add_command(label="Times",command=self.font_change_times)
        font.add_command(label="System",command=self.font_change_system)
        font.add_command(label="Helvetica",command=self.font_change_helvetica)
        font.add_command(label="Fixedsys",command=self.font_change_fixedsys)

        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_option)
       

        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill=BOTH)

        
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        
        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        
        self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)
        

        
        self.send_button_frame = Frame(self.master, bd=0)
        self.send_button_frame.pack(fill=BOTH)

        self.good_Radiobutton_frame = Frame(self.master, bd=0)
        self.good_Radiobutton_frame.pack()
        self.notgood_Radiobutton_frame = Frame(self.master, bd=1)
        self.notgood_Radiobutton_frame.pack()

        
        self.send_button = Button(self.send_button_frame, text="Send", width=5, relief=GROOVE, bg='white',
                                  bd=1, command=lambda: self.send_message_insert(None), activebackground="#FFFFFF",
                                  activeforeground="#000000")
        self.send_button.pack(side=LEFT, ipady=8)


        def positive_feedbacks():
            loaded_pos = np.load('positive_feedbacks.npy')
            loaded_neg = np.load('negative_feedbacks.npy') 
            selection = "accuracy based on user feedbacks : " + str((loaded_pos/(loaded_pos + loaded_neg)))
            label.config(text=selection)
            loaded = np.load('positive_feedbacks.npy') 
            np.save("positive_feedbacks", int(loaded) + 1)


        def negative_feedbacks():
            loaded_pos = np.load('positive_feedbacks.npy') 
            loaded_neg = np.load('negative_feedbacks.npy') 
            selection = "accuracy based on user feedbacks : " + str((loaded_pos/(loaded_pos + loaded_neg)))
            label.config(text=selection)
            loaded = np.load('negative_feedbacks.npy') 
            np.save("negative_feedbacks", int(loaded) + 1)


        var=IntVar()
        self.good_Radiobutton = Radiobutton(self.good_Radiobutton_frame, text="Good", variable=var, value=1, command = positive_feedbacks)
        self.good_Radiobutton.pack(side=LEFT, ipady=8)

        self.notgood_Radiobutton = Radiobutton(self.notgood_Radiobutton_frame, text="Not Good", variable=var, value=2, command = negative_feedbacks)
        self.notgood_Radiobutton.pack(side=LEFT, ipady=8)

        self.master.bind("<Return>", self.send_message_insert)
        
        self.last_sent_label(date="No messages sent.")
        #setting the background color to blue
        self.master.config(bg="#263b54")
        self.text_frame.config(bg="#263b54")
        self.text_box.config(bg="#1c2e44", fg="#FFFFFF")
        self.entry_frame.config(bg="#263b54")
        self.entry_field.config(bg="#1c2e44", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#263b54")
        self.send_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        self.good_Radiobutton_frame.config(bg="#263b54")
        self.good_Radiobutton.config(bg="#1c2e44", fg="#FFFFFF")
        self.notgood_Radiobutton_frame.config(bg="#263b54")
        self.notgood_Radiobutton.config(bg="#1c2e44", fg="#FFFFFF")

        self.sent_label.config(bg="#263b54", fg="#FFFFFF")


        # self.tl_bg = "#1c2e44"
        # self.tl_bg2 = "#263b54"
        # self.tl_fg = "#FFFFFF"
        #


        
        
    def last_sent_label(self, date):

        try:
            self.sent_label.destroy()
        except AttributeError:
            pass

        self.sent_label = Label(self.entry_frame, font="Verdana 7", text=date, bg=self.tl_bg2, fg=self.tl_fg)
        self.sent_label.pack(side=LEFT, fill=X, padx=3)

    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.last_sent_label(date="No messages sent.")
        self.text_box.delete(1.0, END)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)

    def chatexit(self):
        exit()

    def send_message_insert(self, message):
        user_input = self.entry_field.get()
        pr1 = "Me : " + user_input + "\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr1)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        
        ob=chat(user_input)
	#ob='yes'
        pr="WHO : " + ob + "\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        self.last_sent_label(str(time.strftime( "Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
        self.entry_field.delete(0,END)
        time.sleep(0)
        
        
        #return ob

        
    def font_change_default(self):
        self.text_box.config(font="Verdana 10")
        self.entry_field.config(font="Verdana 10")
        self.font = "Verdana 10"

    def font_change_times(self):
        self.text_box.config(font="Times")
        self.entry_field.config(font="Times")
        self.font = "Times"

    def font_change_system(self):
        self.text_box.config(font="System")
        self.entry_field.config(font="System")
        self.font = "System"

    def font_change_helvetica(self):
        self.text_box.config(font="helvetica 10")
        self.entry_field.config(font="helvetica 10")
        self.font = "helvetica 10"

    def font_change_fixedsys(self):
        self.text_box.config(font="fixedsys")
        self.entry_field.config(font="fixedsys")
        self.font = "fixedsys"

      

    # Blue
    def color_theme_dark_blue(self):
        self.master.config(bg="#263b54")
        self.text_frame.config(bg="#263b54")
        self.text_box.config(bg="#1c2e44", fg="#FFFFFF")
        self.entry_frame.config(bg="#263b54")
        self.entry_field.config(bg="#1c2e44", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#263b54")
        self.send_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        
        self.sent_label.config(bg="#263b54", fg="#FFFFFF")

        self.tl_bg = "#1c2e44"
        self.tl_bg2 = "#263b54"
        self.tl_fg = "#FFFFFF"

        # lb = Listbox(window, height=5, selectmode='multiple')
        # for num in data:
        #     lb.insert(END, num)
        # lb.place(x=250, y=150)

        ##########################################

    def default_format(self):
        self.font_change_default()
        self.color_theme_default()    

        
root=Tk()


a = ChatInterface(root)
label=Label(root)
label.pack()
root.geometry(window_size)
root.title("COVID-19 Chatbot")

root.mainloop()
