import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename
from tkfontchooser import askfont
from PIL import ImageTk, Image, ImageDraw, ImageFont
from matplotlib import font_manager
from numpy import asarray

FONT = ('Courier', 18, 'bold')


def get_image(event):
    filename = filedialog.askopenfilename(title='Select an Image')
    upload_path.insert(0, filename)


def get_save_path(event):
    file_name = asksaveasfilename()
    name = upload_path.get().split(".")[1]
    ending = f".{name}"
    save_file_path_input.insert(0, f"{file_name}{ending}")


def add_image():
    with Image.open(upload_path.get()) as image:
        pic = ImageTk.PhotoImage(image)
        image_label.config(image=pic)
        image_label.image = pic
    # show editing buttons
    watermark_lettering.grid(column=4, row=3, columnspan=2, sticky='nw')
    watermark_lettering_input.grid(column=4, row=4, columnspan=2, sticky='nw')
    watermark_coloring.grid(column=4, row=5, sticky='nw')
    watermark_font.grid(column=5, row=5, sticky='nw')
    # show edits
    preview_label.grid(column=4, row=6, columnspan=2, sticky='nw', rowspan=2)
    preview_label2.grid(column=4, row=7, columnspan=2, sticky='nw')
    preview_button.grid(column=4, row=8, columnspan=2, sticky='nw')
    save_label.grid(column=4, row=9, columnspan=2, sticky='nw', rowspan=2)
    save_label2.grid(column=4, row=10, columnspan=2, sticky='nw')
    save_file_path_input.grid(column=4, row=11, columnspan=2, sticky='nw')
    save_button.grid(column=4, row=12, columnspan=2, sticky='nw')

# ALLOW EDITING OF IMAGE TO ADD DESIRED WATERMARK


def choose_color():
    text_color = askcolor(title='Watermark color chooser')[1]
    if text_color is not None:
        watermark_coloring.configure(fg=str(text_color))
        save_color_input.delete(0, END)
        save_color_input.insert(0, str(text_color))


def choose_font():
    text_font = askfont(title='Watermark font chooser')
    if text_font is not None:
        watermark_font.configure(font=(text_font['family'], 10))
        save_font_input.delete(0, END)
        save_font_input.insert(0, text_font['family'])
        save_fontsize_input.delete(0, END)
        save_fontsize_input.insert(0, text_font['size'])


def preview_image():
    open_and_edit()


def save_image():
    path = save_file_path_input.get()
    image = open_and_edit()
    # convert PhotoImage to rbg and save
    final_image = ImageTk.getimage(image)
    final_image2 = final_image.convert('RGB')
    final_final_image = final_image2.save(path)
    # reset entry default values
    upload_path.delete(0, END)
    watermark_lettering_input.delete(0, END)
    save_file_path_input.delete(0, END)
    xcor_input.delete(0, END)
    xcor_input.insert(0, '10')
    ycor_input.delete(0, END)
    ycor_input.insert(0, '10')
    save_color_input.delete(0, END)
    save_color_input.insert(0, 'black')
    save_font_input.delete(0, END)
    save_font_input.insert(0, 'Helvetica')
    image_label.config(image=default_image)
    watermark_coloring.configure(fg='black')
    watermark_font.configure(font='TkTextFont')


def get_xy(event):
    xcor_input.delete(0, END)
    xcor_input.insert(0, event.x)
    ycor_input.delete(0, END)
    ycor_input.insert(0, event.y)


def open_and_edit():
    font = save_font_input.get()
    fontsize = save_fontsize_input.get()
    color = save_color_input.get()
    x_coordinate = int(xcor_input.get())
    y_coordinate = int(ycor_input.get())
    with Image.open(upload_path.get()) as image:
        img1 = image.copy()
        img2 = Image.fromarray(asarray(img1))
        # CONFIGURE TEXT AND FONT REQUIREMENTS
        text = watermark_lettering_input.get()
        file = font_manager.findfont(font)
        ''' toggle between the 2 size options, 1st uses image width for bigger
        font size 2nd is true to the user selected font size '''
        # size = int(img1.width / 8)
        size = int(fontsize)
        fnt = ImageFont.truetype(file, size)
        # CREATE / DRAW WATERMARK
        draw = ImageDraw.Draw(img2, mode='RGB')
        draw.text((x_coordinate, y_coordinate), text, fill=color, font=fnt)
        img3 = ImageTk.PhotoImage(img2)
        image_label.config(image=img3)
        image_label.image = img3
        return img3


# CREATE APP WINDOW
window = tkinter.Tk()
window.title('EggZ watermarks')
window.config(width=800, height=800, padx=50, pady=50)

# upload image section
add_image_label = Label(text='Add image here: ', font=FONT)
add_image_label.grid(column=4, row=0, columnspan=2, sticky='nw')

upload_path = Entry(width=20)
upload_path.bind('<Button>', get_image)
upload_path.grid(column=4, row=1, columnspan=2, sticky='nw')

upload_button = Button(text='ADD', command=add_image, height=2)
upload_button.grid(column=4, row=2, sticky='nw')

default_image = PhotoImage(file='default.png')
image_label = Label(padx=20, pady=20, image=default_image)
image_label.grid(column=0, row=0, columnspan=3, rowspan=13, sticky='nw')
image_label.bind('<Double-Button-1>', get_xy)

# add watermark section
watermark_lettering = Label(text='Add your text: ', font=FONT)
watermark_lettering_input = Entry(width=20)
watermark_coloring = Button(window, text='COLOR', command=choose_color, height=2)
watermark_font = Button(text='FONT', command=choose_font, height=2)

# preview and save section
preview_label = Label(text='Double Click on Image', font=FONT)
preview_label2 = Label(text='to position watermark', font=FONT)
preview_button = Button(window, text='PREVIEW NEW IMAGE', command=preview_image, height=3)
save_label = Label(text='Save new image here: ', font=FONT)
save_label2 = Label(text='e.g. my_image', font=FONT)
save_file_path_input = Entry(width=20)
save_file_path_input.bind('<Button>', get_save_path)
save_button = Button(text='SAVE NEW IMAGE ', command=save_image, height=3, background='blue')

# invisible inputs
save_color_input = Entry()
save_color_input.insert(0, 'black')
save_font_input = Entry()
save_font_input.insert(0, 'Helvetica')
save_fontsize_input = Entry()
save_fontsize_input.insert(0, '10')
xcor_input = Entry()
xcor_input.insert(0, '10')
ycor_input = Entry()
ycor_input.insert(0, '10')
window.mainloop()
