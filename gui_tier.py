#!/usr/bin/env python3

import customtkinter
from PIL import Image

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk() 
app.geometry("1500x1000")
app.minsize(600,600)

app.grid_rowconfigure(0, weight=10)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)





def button_function1():
    image = customtkinter.CTkImage(light_image=Image.open('book.jpg'))

    for label in imageLabelsS:
        label.configure(image=image)


def button_function2():
    pass

tierFrame = customtkinter.CTkFrame(master=app)

tierFrame.grid_rowconfigure((0,1,2,3,4), weight=1)
tierFrame.grid_columnconfigure((1,2,3,4,5,6,7,8,9), weight=3)
tierFrame.grid_columnconfigure(0, weight=1)

tierFrame.grid(row=0, column=0, sticky="wesn")

tiers = ['S', 'A', 'B', 'C', 'D']
tiersColors = ['#c42708', '#c47608', '#bec408', '#79c408', '#08c486']
for i in range(5):
    label = customtkinter.CTkLabel(tierFrame, 
                                   text=tiers[i], 
                                   fg_color=tiersColors[i],
                                   text_color='black')
    label.grid(row=i, column=0, sticky="wesn")


imageLabelsS = []

for i in range(1,10):
    image_label = customtkinter.CTkLabel(tierFrame, text="")
    imageLabelsS.append(image_label)
    image_label.grid(row=0, column=i, sticky="wesn")


containerFrame = customtkinter.CTkFrame(master=app)

containerFrame.grid_rowconfigure(0, weight=1)
containerFrame.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=2)

containerFrame.grid(row=1, column=0, sticky="wesn")


button1 = customtkinter.CTkButton(master=containerFrame, 
								 text="debug1",
								 command=button_function1)
button1.grid(row=0, column=0, sticky="wesn")

button2 = customtkinter.CTkButton(master=containerFrame, 
								 text="debug2",
								 command=button_function2)
button2.grid(row=0, column=1, sticky="wesn")

app.mainloop()