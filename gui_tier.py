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




def adjust_image(event, arg):

    if imageLabels[arg['row']][arg['id']]._image=='':
        return
    
    if imageLabels[arg['row']][arg['id']]._image is None:
        return
    
    width = event.width
    height = event.height

    # if height > 50:
    #     height = 50

    imageObjects[arg['row']][arg['id']].configure(size=(width,height))
    


def button_function1():
    image = customtkinter.CTkImage(light_image=Image.open('book.jpg'))

    for row, labelrow in enumerate(imageLabels):
        for col, label in enumerate(labelrow):
            
            imageLabels[row][col].configure(image=image)
            imageObjects[row][col] = image

        


def button_function2():
    imageLabels[1][3].configure(image='')
    imageLabels[2][4].configure(image='')

tierFrame = customtkinter.CTkFrame(master=app)

tierFrame.grid_rowconfigure((0,1,2,3,4), weight=0, minsize=100)
tierFrame.grid_columnconfigure((1,2,3,4,5,6,7), weight=3)
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

    


imageLabels = []
imageObjects = []

for row in range(len(tiers)):

    currentRowLabels = []
    currentRowImages = []

    for i in range(1,7):
        image_label = customtkinter.CTkLabel(tierFrame, text="", fg_color='blue')
        currentRowLabels.append(image_label)
        image_label.grid(row=row, column=i, sticky="wesn")

        # source:   https://stackoverflow.com/questions/3296893/how-to-pass-an-argument-to-event-handler-in-tkinter
        #           https://www.youtube.com/watch?v=VnwDPa9biwc        
        data = {"row": row, "id": i-1}
        image_label.bind("<Configure>", lambda event, arg=data: adjust_image(event, arg))

        currentRowImages.append(0)

    imageLabels.append(currentRowLabels)
    imageObjects.append(currentRowImages)


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