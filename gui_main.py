#!/usr/bin/env python3

import customtkinter
from PIL import Image

import game_parser2
from CTkListbox import *


customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1500x1000")
app.minsize(600,600)




def button_function():


	current_selection = listbox.get(listbox.curselection())

	result = game_parser2.search_game_title(current_selection)

	if result is None: return

	game_data, image_path = result

	img = (Image.open(image_path))
	#Resize the Image using resize method
	resized_image= img.resize((500,650), Image.LANCZOS)

	main_image.configure(light_image=resized_image,size=(500,650))


def on_entry_text_changed(index, value, op):
		
	if len(entry.get())==0:
		listbox.delete(0, customtkinter.END)
		return
		
	titles = game_parser2.search_game_inDB(entry.get())
	listbox.delete(0, customtkinter.END)
	for i, t in enumerate(titles):
		listbox.insert(i,t)




	



app.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
app.grid_columnconfigure(0, weight=1)



main_image = customtkinter.CTkImage(light_image=Image.open('Python.svg.png'),size=(300,300))
main_image_label = customtkinter.CTkLabel(app, text="", image=main_image)
main_image_label.grid(row=2, column=0, padx=10, pady=10)




searchFrame = customtkinter.CTkFrame(master=app)


searchFrame.grid_rowconfigure(0, weight=1)
searchFrame.grid_columnconfigure(0, weight=10)
searchFrame.grid_columnconfigure(1, weight=1)

entryString = customtkinter.StringVar()
entryString.trace_add(["write"],on_entry_text_changed)


entry = customtkinter.CTkEntry(master=searchFrame, 
							   placeholder_text="Type a game title here",
							   textvariable=entryString)
entry.grid(row=0, column=0, sticky="wesn")

button = customtkinter.CTkButton(master=searchFrame, 
								 text="Search",
								 command=button_function)
button.grid(row=0, column=1, sticky="wesn")



searchFrame.grid(row=0, column=0, sticky="wes")

listbox = CTkListbox(master=app)




listbox.grid(row=1, column=0, sticky="wnes")

app.mainloop()