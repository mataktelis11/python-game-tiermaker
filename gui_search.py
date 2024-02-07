#!/usr/bin/env python3

import customtkinter
from PIL import Image
from CTkListbox import *
import game_parser2


class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure((0,1,2,3), weight=1) 
        self.grid_columnconfigure((0), weight=1)

        self.logolabel = customtkinter.CTkLabel(master=self, text= 'Game Searh Engine')
        self.logolabel.grid(row=0, column=0, padx=20, sticky='swe')


        ## Search Frame
        self.searchFrame = customtkinter.CTkFrame(master=self)
        self.searchFrame.grid_rowconfigure(0, weight=1)
        self.searchFrame.grid_columnconfigure(0, weight=10)
        self.searchFrame.grid_columnconfigure(1, weight=1)

        self.user_entry = customtkinter.CTkEntry(master=self.searchFrame, 
                                                placeholder_text="Type a game title here")
        self.user_entry.grid(row=0, column=0, sticky="wesn", padx=5)

        self.search_button = customtkinter.CTkButton(master=self.searchFrame, 
                                            text="Search",
                                            command=self.search_button_function)
        self.search_button.grid(row=0, column=1, sticky="wesn")


        self.searchFrame.grid(row=1, column=0, sticky='nwe', padx=20)
        ##

        self.listbox = CTkListbox(master=self)
        self.listbox.grid(row=2, column=0, sticky="wnes", padx=20, pady=20)
        self.listbox.bind('<<ListboxSelect>>', self.onselect)

        ## Results Frame
        self.resultFrame = customtkinter.CTkFrame(master=self)
        self.resultFrame.grid_rowconfigure(0, weight=1)
        self.resultFrame.grid_columnconfigure(1, weight=10)
        self.resultFrame.grid_columnconfigure((0,2), weight=1)

        self.label = customtkinter.CTkLabel(master=self.resultFrame, text= 'Chosen game:')
        self.label.grid(row=0, column=0, padx=20, sticky='wesn')

        self.fetch_button = customtkinter.CTkButton(master=self.resultFrame, 
                                            text="Fetch game info",
                                            command=self.search_button_function)
        self.fetch_button.grid(row=0, column=2, sticky="wesn")

        self.game_entry = customtkinter.CTkEntry(master=self.resultFrame, state='readonly')

        self.game_entry.grid(row=0, column=1, sticky="wesn", padx=5)

        self.resultFrame.grid(row=3, column=0, sticky='nwe', padx=20, pady=20)
        ##



    def onselect(self, evt):
        # Note here that Tkinter passes an event object to onselect()

        print(f'You selected item {evt}')

        current_selection = self.listbox.get(self.listbox.curselection())

    def search_button_function(self):
        if len(self.user_entry.get())==0:
            self.listbox.delete(0, customtkinter.END)
            return
		
        titles = game_parser2.search_game_inDB(self.user_entry.get())
        self.listbox.delete(0, customtkinter.END)
        for i, t in enumerate(titles):
            self.listbox.insert(i,t)

    def fetch_button_function(self):
        pass



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x800")
        self.minsize(600,600)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure((0), weight=1)

        self.my_frame1 = MyFrame(master=self)
        self.my_frame1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


app = App()
app.mainloop()