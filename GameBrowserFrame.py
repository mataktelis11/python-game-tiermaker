
import customtkinter
from PIL import Image
from CTkListbox import *
import game_parser


class GameBrowserFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.current_guid = ''
        self.fetched_games = []


        self.grid_rowconfigure((0,1,2,3,4,5), weight=1) 
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
                                            command=self.fetch_button_function)
        self.fetch_button.grid(row=0, column=2, sticky="wesn")

        self.game_title_string = customtkinter.StringVar()
        self.game_entry = customtkinter.CTkEntry(master=self.resultFrame, 
                                                 state='readonly', 
                                                 textvariable=self.game_title_string)
        self.game_entry.grid(row=0, column=1, sticky="wesn", padx=5)

        self.resultFrame.grid(row=3, column=0, sticky='nwe', padx=20, pady=20)
        ##

        ## Game info frame
        self.game_info_frame = customtkinter.CTkFrame(master=self)
        

        self.game_info_frame.grid_rowconfigure((0, 1), weight=1)
        self.game_info_frame.grid_columnconfigure((0,1), weight=1)

        self.pillow_image = Image.open('Python.svg.png')
        self.main_image = customtkinter.CTkImage(light_image=self.pillow_image)
        self.main_image_ratio = self.pillow_image.size[0] / self.pillow_image.size[1]


        self.main_image_label = customtkinter.CTkLabel(self.game_info_frame, 
                                                       text="", 
                                                       image=self.main_image)
        self.main_image_label.bind("<Configure>", self.adjust_image)
        self.main_image_label.grid(row=0, column=0, padx=10, pady=10, sticky='wens')


        self.all_info_frame = customtkinter.CTkFrame(master=self.game_info_frame)
        self.all_info_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.all_info_frame.grid_columnconfigure((0,1), weight=1)

        labels = ['Title', 'Original release date', 'Platforms', 'Developers', 'Publishers', 'Genres']
        for i,l in enumerate(labels):
            templabel = customtkinter.CTkLabel(self.all_info_frame, 
                                                       text=l)
            templabel.grid(row=i, column=0)
        
        self.string_title = customtkinter.StringVar()
        self.rdate_title = customtkinter.StringVar()
        self.platforms_title = customtkinter.StringVar()
        self.devs_title = customtkinter.StringVar()
        self.pub_title = customtkinter.StringVar()
        self.genres_title = customtkinter.StringVar()

        #
        self.string_title_label = customtkinter.CTkLabel(self.all_info_frame, 
                                                  textvariable=self.string_title)
        self.string_title_label.grid(row=0, column=1)

        self.rdate_title_label = customtkinter.CTkLabel(self.all_info_frame, 
                                                  textvariable=self.rdate_title)
        self.rdate_title_label.grid(row=1, column=1)

        self.platforms_title_label = customtkinter.CTkLabel(self.all_info_frame, 
                                                  textvariable=self.platforms_title)
        self.platforms_title_label.grid(row=2, column=1)

        self.devs_title_label = customtkinter.CTkLabel(self.all_info_frame, 
                                                  textvariable=self.devs_title)
        self.devs_title_label.grid(row=3, column=1)

        self.pub_title_label = customtkinter.CTkLabel(self.all_info_frame, 
                                                  textvariable=self.pub_title)
        self.pub_title_label.grid(row=4, column=1)

        self.genres_title_label = customtkinter.CTkLabel(self.all_info_frame, 
                                                  textvariable=self.genres_title)
        self.genres_title_label.grid(row=5, column=1)
        #

        self.all_info_frame.grid(row=0, column=1)

        self.game_info_frame.grid(row=4, column=0, sticky='nwe', padx=20, pady=20)
        ##

        self.append_button = customtkinter.CTkButton(self, text='Append image to container')
        self.append_button.grid(row=5, column=0, sticky='swe', padx=20, pady=20)

        self.append_button_all = customtkinter.CTkButton(self, text='Append all cached images to container')
        self.append_button_all.grid(row=6, column=0, sticky='swe', padx=20, pady=20)

    def onselect(self, evt):

        #print(self.listbox.curselection())
        current_selection = self.listbox.get(self.listbox.curselection())
        #print(current_selection)
        self.game_title_string.set(current_selection)

    def search_button_function(self):
        if len(self.user_entry.get())==0:
            self.listbox.delete(0, customtkinter.END)
            return
		
        self.fetched_games = game_parser.search_game_with_API(self.user_entry.get())

        titles = [element['name'] for element in self.fetched_games]

        self.listbox.delete(0, customtkinter.END)
        for i, t in enumerate(titles):
            self.listbox.insert(i,t)

    def fetch_button_function(self):
        
        print(f'Fetch me guid {self.fetched_games[self.listbox.curselection()]}')
        game_parser.fetch_game_data(self.fetched_games[self.listbox.curselection()]['guid'])

        self.load_game_data(self.fetched_games[self.listbox.curselection()]['guid'])


    def load_game_data(self, guid):

        game_data, image_path = game_parser.search_cache_data(guid)

        self.string_title.set(game_data['title'])
        self.rdate_title.set(game_data['original_release_date'])
        self.platforms_title.set(', '.join(i['name'] for i in game_data['platforms']))
        self.devs_title.set(', '.join(i['name'] for i in game_data['developers']))
        self.pub_title.set(', '.join(i['name'] for i in game_data['publishers']))
        self.genres_title.set(', '.join(i['name'] for i in game_data['genres']))


        self.pillow_image = Image.open(image_path)
        self.main_image = customtkinter.CTkImage(light_image=self.pillow_image)
        self.main_image_ratio = self.pillow_image.size[0] / self.pillow_image.size[1]


        self.main_image_label.configure(image=self.main_image)

        self.current_guid = guid

    def adjust_image(self, event):
        # source: https://www.youtube.com/watch?v=VnwDPa9biwc

        event.height = 350

        container_ratio = event.width / event.height
        
        if container_ratio > self.main_image_ratio:
            height = int(event.height)
            width = int(height * self.main_image_ratio)
        else:
            width = int(event.width)
            height = int(width / self.main_image_ratio)

        self.main_image.configure(size=(width,height))