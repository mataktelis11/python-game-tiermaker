#!/usr/bin/env python3

import customtkinter
import tkinter
from PIL import Image
import tomllib
from GameBrowserFrame import GameBrowserFrame
import game_parser2



with open("config.toml", "rb") as f:
        config = tomllib.load(f)


class TierFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.guids = []
        self.labels = []


        
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
        self.tabview.set("Tier list")  # set currently visible tab

        self.gamebrowserframe = GameBrowserFrame(master=self.tabview.tab("Game Search"))
        self.gamebrowserframe.pack(fill=customtkinter.BOTH, expand=1)

        self.gamebrowserframe.append_button.configure(command=self.append_image_button)

        # creating tiers

        self.tiers = config['tiers']
        self.tiersColors = config['tiersColors']

        self.logo_n_container_tier = []
        self.logo_tier = []
        self.container_tier = []

        for i in range(len(self.tiers)):
            
            self.logo_n_container_tier.append(customtkinter.CTkFrame(master=self.tabview.tab("Tier list")))

            self.logo_tier.append(customtkinter.CTkLabel(master=self.logo_n_container_tier[i], 
                                              height=170,
                                              width=40,
                                              fg_color=self.tiersColors[i], 
                                              text=self.tiers[i])
            )
            self.logo_tier[i].pack(side=customtkinter.LEFT)

            self.container_tier.append(TierFrame(master=self.logo_n_container_tier[i], 
                                                 height=170, 
                                                 fg_color='#044536'))
            self.container_tier[i].pack(side=customtkinter.LEFT, fill=customtkinter.X, expand=1)

            self.logo_n_container_tier[i].pack(side=customtkinter.TOP, fill=customtkinter.X, expand=1)


        # self.label_a = customtkinter.CTkLabel(master=self.tabview.tab("Tier list"), 
        #                                 height=170,
        #                                 width=40,
        #                                 fg_color='blue', 
        #                                 text='A')
        
        # self.label_a.pack(side=customtkinter.LEFT)

        #self.gamebrowserframe.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.containerFrame = customtkinter.CTkScrollableFrame(master=self, orientation='horizontal', height=120)
        self.containerFrame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.contained_guids = []
        self.contained_labels = []
        self.choosen_guid = ''

        self.context_menu = tkinter.Menu(self, tearoff=0)

        for t in self.tiers:
            self.context_menu.add_command(label=f"Move to tier {t}",
                                      command= lambda arg=t: self.context_move_to_tier(arg))

        self.context_menu.add_separator()
        self.context_menu.add_command(label="Remove Game", command=self.context_menu_remove)
        self.context_menu.add_command(label="Close")



        self.tier_context_menu = tkinter.Menu(self, tearoff=0)
        self.tier_context_menu.add_command(label="Move to the right <", command=self.context_tier_move_right)
        self.tier_context_menu.add_command(label="Move to the left >", command=self.context_tier_move_left)
        self.tier_context_menu.add_command(label="Remove Game", command=self.context_tier_remove_game)
        self.tier_context_menu.add_command(label="Close")


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


    def append_game_to_tier(self, frame, guid):
        if guid in frame.guids:
            print('Game already in container')
            return
        
        frame.guids.append(guid)
        game_data, image_path = game_parser2.search_cache_data(guid)

        # Load the image
        pillow_image = Image.open(image_path)
        image_ratio = pillow_image.size[0] / pillow_image.size[1]
        container_ratio = 1.0

        if container_ratio > image_ratio:
            height = 150
            width = int(height * image_ratio)
        else:
            width = 150
            height = int(width / image_ratio)

        main_image = customtkinter.CTkImage(light_image=pillow_image, size=(width,height))
        label = customtkinter.CTkLabel(frame, image=main_image, text='')        
        #label.pack(side= customtkinter.LEFT, padx=5, pady=5)
        frame.labels.append(label)

        label.grid(row=0, column=len(frame.labels)-1, padx=5, pady=5)

        data = {"guid": guid}
        label.bind("<Button-3>", lambda event, arg=data: self.show_tier_context_menu(event, arg))

    def show_context_menu(self, event, arg):
        self.choosen_guid = arg["guid"]
        self.context_menu.post(event.x_root, event.y_root)

    def show_tier_context_menu(self, event, arg):
        self.choosen_guid = arg["guid"]
        self.tier_context_menu.post(event.x_root, event.y_root)

    def context_tier_remove_game(self):

        current_guid = self.choosen_guid
        
        for tierlist in self.container_tier:
            if current_guid in tierlist.guids:

                index = tierlist.guids.index(current_guid)
                tierlist.guids.pop(index)

                tierlist.labels[index].destroy()
                tierlist.labels.pop(index)

                # rearange grid
                for index,label in enumerate(tierlist.labels):
                    label.grid(row=0, column=index, padx=5, pady=5)

                self.append_game_to_container(current_guid)
                return
        print('guid not found in tierlists!')

    def context_tier_move_right(self):

        current_guid = self.choosen_guid
        
        for tierlist in self.container_tier:
            if current_guid in tierlist.guids:

                index = tierlist.guids.index(current_guid)
                if index == 0: return

                tierlist.guids[index-1], tierlist.guids[index] = tierlist.guids[index], tierlist.guids[index-1]
                tierlist.labels[index-1], tierlist.labels[index] = tierlist.labels[index], tierlist.labels[index-1]

                tierlist.labels[index].grid(row=0, column=index, padx=5, pady=5)
                tierlist.labels[index-1].grid(row=0, column=index-1, padx=5, pady=5)

                return
        print('guid not found in tierlists!')

    def context_tier_move_left(self):

        current_guid = self.choosen_guid
        
        for tierlist in self.container_tier:
            if current_guid in tierlist.guids:

                index = tierlist.guids.index(current_guid)
                if len(tierlist.guids) == 1: return
                if index == len(tierlist.guids)-1: return

                tierlist.guids[index+1], tierlist.guids[index] = tierlist.guids[index], tierlist.guids[index+1]
                tierlist.labels[index+1], tierlist.labels[index] = tierlist.labels[index], tierlist.labels[index+1]

                tierlist.labels[index].grid(row=0, column=index, padx=5, pady=5)
                tierlist.labels[index+1].grid(row=0, column=index+1, padx=5, pady=5)

                return
        print('guid not found in tierlists!')

    def context_menu_remove(self):
        self.remove_game_from_container(self.choosen_guid)

    def context_move_to_tier(self, arg):
        tier = arg
        index = config['tiers'].index(tier)
        self.append_game_to_tier(self.container_tier[index],self.choosen_guid)
        self.remove_game_from_container(self.choosen_guid)
        

    def clicked_image(self, event, arg):
        print(f'image was clicked with guid: {arg["guid"]}')
        #self.remove_game_from_container(arg["guid"])

        #label = self.get_label(arg["guid"])

        self.append_game_to_tier(self.container_tier[0],arg["guid"])
        
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