#!/usr/bin/env python3

import customtkinter
import tkinter
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
        self.contained_labels = []
        self.choosen_guid = ''

        self.context_menu = tkinter.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Remove Game", command=self.context_menu_remove)
        self.context_menu.add_command(label="Close")
        


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


        # source:   https://stackoverflow.com/questions/3296893/how-to-pass-an-argument-to-event-handler-in-tkinter
        #           https://www.youtube.com/watch?v=VnwDPa9biwc        
        data = {"guid": guid}
        label.bind("<Button-1>", lambda event, arg=data: self.clicked_image(event, arg))
        label.bind("<Button-3>", lambda event, arg=data: self.show_context_menu(event, arg))

        self.contained_labels.append(label)

    def show_context_menu(self, event, arg):
        self.choosen_guid = arg["guid"]
        self.context_menu.post(event.x_root, event.y_root)

    def context_menu_remove(self):
        self.remove_game_from_container(self.choosen_guid)

    def clicked_image(self, event, arg):
        print(f'image was clicked with guid: {arg["guid"]}')
        #self.remove_game_from_container(arg["guid"])

        #label = self.get_label(arg["guid"])
        
    def get_label(self, guid):
        index = self.contained_guids.index(guid)
        return self.contained_labels[index]
    
    def remove_game_from_container(self, guid):
        
        if guid not in self.contained_guids:
            print('Game is not in container')
            return
        
        index = self.contained_guids.index(guid)
        self.contained_guids.pop(index)

        self.contained_labels[index].destroy()
        self.contained_labels.pop(index)


    def append_image_button(self):
        guids = ['3030-20464', '3030-25305', '3030-45214', '3030-64883', '3030-20953', '3030-30196',
                 '3030-73838', '3030-21170', '3030-31463', '3030-59912']
        
        for g in guids:
            
            self.append_game_to_container(g)

        print(self.contained_guids)


app = App()
app.mainloop()