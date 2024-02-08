#!/usr/bin/env python3

import customtkinter
from PIL import Image

from GameBrowserFrame import GameBrowserFrame


        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x800")
        self.minsize(600,600)
        self.grid_rowconfigure(0, weight=10) 
        self.grid_rowconfigure(1, weight=1) 
        self.grid_columnconfigure((0), weight=1)

        self.gamebrowserframe = GameBrowserFrame(master=self)


        self.gamebrowserframe.append_button.configure(command=self.append_image_button)

        self.gamebrowserframe.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.containerFrame = customtkinter.CTkFrame(master=self)
        self.containerFrame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        for i in range(5):
            self.append_image(self.containerFrame,'book.jpg', row=0, column=i)


    def append_image(self, frame, image_path, row, column):
        # Load the image
        img = Image.open(image_path)

        main_image = customtkinter.CTkImage(light_image=img, size=(100,100))

        label = customtkinter.CTkLabel(frame, image=main_image, text='')
        
        label.grid(row=row, column=column, padx=2, pady=2)

    def append_image_button(self):
        print("hello from gui_search.py!")


app = App()
app.mainloop()