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
	game_data, image_path = game_parser2.search_game_title('Sonic Unleashed')

	img = (Image.open(image_path))
	#Resize the Image using resize method
	resized_image= img.resize((500,650), Image.LANCZOS)

	main_image.configure(light_image=resized_image,size=(500,650))

def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)
    
def on_combobox_text_changed(index, value, op):
	#print(f"on_combobox_text_changed {combobox.get()}")
		
	if len(combobox.get())==0:
		return
		
	titles = game_parser2.search_game_inDB(combobox.get())
	combobox.configure(values=titles)
	#combobox.event_generate("<Button-1>") doesnt work

def on_entry_text_changed(index, value, op):
	#print(f"on_combobox_text_changed {combobox.get()}")
		
	if len(entry.get())==0:
		return
		
	titles = game_parser2.search_game_inDB(entry.get())
	listbox.delete(0, customtkinter.END)
	for index, t in enumerate(titles):
		listbox.insert(index,t)


# Use CTkButton instead of tkinter Button
# button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
# button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


# main_image = customtkinter.CTkImage(light_image=Image.open('Python.svg.png'),size=(300,300))

# my_label = customtkinter.CTkLabel(app, text="", image=main_image)
# my_label.pack(pady=10)

app.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
app.grid_columnconfigure(0, weight=1)


v = customtkinter.StringVar()
v.trace_add(["write"],on_combobox_text_changed)

combobox = customtkinter.CTkComboBox(master=app,values=[],
                                     variable=v,
                                     command=combobox_callback)
combobox.grid(row=0, column=0, padx=10, pady=10, sticky="wne")

main_image = customtkinter.CTkImage(light_image=Image.open('Python.svg.png'),size=(300,300))
main_image_label = customtkinter.CTkLabel(app, text="", image=main_image)
main_image_label.grid(row=1, column=0, padx=10, pady=10)

button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
button.grid(row=2, column=0, padx=10, pady=10)


entryString = customtkinter.StringVar()
entryString.trace_add(["write"],on_entry_text_changed)

entry = customtkinter.CTkEntry(master=app, 
							   placeholder_text="Type a game title here",
							   textvariable=entryString)
entry.grid(row=3, column=0, sticky="wes")

listbox = CTkListbox(master=app)




listbox.grid(row=4, column=0, sticky="wne")

app.mainloop()