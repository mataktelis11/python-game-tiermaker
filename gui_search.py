#!/usr/bin/env python3

import customtkinter
from PIL import Image

from GameBrowserFrame import GameBrowserFrame
import game_parser2


        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x1200")
        self.minsize(600,600)
        self.grid_rowconfigure(0, weight=10) 
        self.grid_rowconfigure(1, weight=1) 
        self.grid_columnconfigure((0), weight=1)


        self.tabview = customtkinter.CTkTabview(master=self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tabview.add("Tier list")  # add tab at the end
        self.tabview.add("Game Search")  # add tab at the end
        self.tabview.set("Game Search")  # set currently visible tab

        self.gamebrowserframe = GameBrowserFrame(master=self.tabview.tab("Game Search"))
        self.gamebrowserframe.pack(fill=customtkinter.BOTH, expand=1)

        self.gamebrowserframe.append_button.configure(command=self.append_image_button)

        #self.gamebrowserframe.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.containerFrame = customtkinter.CTkScrollableFrame(master=self, orientation='horizontal', height=120)
        self.containerFrame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.contained_guids = []


    def append_image(self, frame, image_path):
        # Load the image
        pillow_image = Image.open(image_path)


        image_ratio = pillow_image.size[0] / pillow_image.size[1]
        container_ratio = 1.0

        if container_ratio > image_ratio:
            height = 100
            width = int(height * image_ratio)
        else:
            width = 100
            height = int(width / image_ratio)

        main_image = customtkinter.CTkImage(light_image=pillow_image, size=(width,height))
        label = customtkinter.CTkLabel(frame, image=main_image, text='')        
        label.pack(side= customtkinter.RIGHT, padx=5, pady=5)
        

    def append_game_to_container(self, guid):
        
        if guid in self.contained_guids:
            print('Game already in container')
            return

        self.contained_guids.append(guid)
        game_data, image_path = game_parser2.search_cache_data(guid)

        # Load the image
        pillow_image = Image.open(image_path)
        image_ratio = pillow_image.size[0] / pillow_image.size[1]
        container_ratio = 1.0

        if container_ratio > image_ratio:
            height = 100
            width = int(height * image_ratio)
        else:
            width = 100
            height = int(width / image_ratio)

        main_image = customtkinter.CTkImage(light_image=pillow_image, size=(width,height))
        label = customtkinter.CTkLabel(self.containerFrame, image=main_image, text='')        
        label.pack(side= customtkinter.RIGHT, padx=5, pady=5)



    def append_image_button(self):
        guids = ['3030-20464', '3030-25305', '3030-45214', '3030-64883', '3030-20953', '3030-30196',
                 '3030-73838', '3030-21170', '3030-31463', '3030-59912']
        
        for g in guids:
            
            self.append_game_to_container(g)



app = App()
app.mainloop()