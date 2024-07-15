from tkinter import *
from tkinter import ttk, Label
from PIL import ImageTk
import os

window = Tk()
window.title("Automation App")
window.geometry("1100x700")
iconpath = ImageTk.PhotoImage(file=os.path.join("logo.png"))
window.wm_iconbitmap()
window.iconphoto(False, iconpath)


# >>> Create a Frame + Content Frame with scrollbar .............
frame = Frame(window, bg='white')
frame.pack(fill=BOTH, expand=True)
canvas = Canvas(frame)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
canvas.bind_all("<MouseWheel>", lambda event:on_mousewheel(event))  # Labda have to use when function is below
scrollbar = Scrollbar(frame, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
content_frame = Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor=NW)



# >>> website info widgets ......................
webinfo_frame = LabelFrame(content_frame, text="Input your website information")
webinfo_frame.grid(pady=10, padx=20)

# >>> label section ......
website_name = Label(webinfo_frame, text="Website Name", width=25)
website_name.grid(row=0, column=0, padx=10, pady=3)

user_name = Label(webinfo_frame, text="User Name", width=25)
user_name.grid(row=0, column=1, padx=10, pady=3)

app_pass = Label(webinfo_frame, text="Application Password",width=25)
app_pass.grid(row=0, column=2, padx=10, pady=3)

status = Label(webinfo_frame, text="Post Status", width=25)
status.grid(row=0, column=3, padx=10, pady=3)

category = Label(webinfo_frame, text="Category", width=25)
category.grid(row=0, column=4, padx=10, pady=3)

# >>> Input section .....
website_entry = Entry(webinfo_frame, width=25)
website_entry.insert(0, "edmontonranked.ca")  # Default data
website_entry.grid(row=1, column=0, padx=10, pady=10)

username_entry = Entry(webinfo_frame, width=20)
username_entry.insert(0, "info@updigital.ca")
username_entry.grid(row=1, column=1, padx=10, pady=10)

app_pass_entry = Entry(webinfo_frame, width=20)
app_pass_entry.insert(0, "pXHi KFT4 A7dm JUO5 JaXz r2gY")
app_pass_entry.grid(row=1, column=2, padx=10, pady=10)

category = Entry(webinfo_frame, width=20)
category.insert(0, 'Category Name..')
category.grid(row=1, column=3, pady=10, padx=10)

status = ttk.Combobox(webinfo_frame, width=20, values=['draft', 'publish'], state='readonly')
status.set('draft')
status.grid(row=1, column=4,pady=10, padx=10)



# >>> API info widgets ...............................
apiinfo_frame = LabelFrame(content_frame, text="API Section")
apiinfo_frame.grid(pady=10, padx=20)

# >>> label section .............
openai_api_label = Label(apiinfo_frame, text="OpenAI API", width=20)
openai_api_label.grid(row=2, column=0, padx=5, pady=3)

api_model_label = Label(apiinfo_frame, text="API Model", width=20)
api_model_label.grid(row=2, column=1, padx=5, pady=3)

youtube_api_label = Label(apiinfo_frame, text="YouTube API",width=20)
youtube_api_label.grid(row=2, column=2, padx=5, pady=3)

youtube_switch_label = Label(apiinfo_frame, text="Youtube ON/OFF")
youtube_switch_label.grid(row=2, column=3, padx=5, pady=3)

feature_img_switch_label = Label(apiinfo_frame, text="Feature Img ON/OFF")
feature_img_switch_label.grid(row=2, column=4, padx=5, pady=3)

body_img_switch_label = Label(apiinfo_frame, text="Body Img ON/OFF")
body_img_switch_label.grid(row=2, column=5, padx=5, pady=3)

# >>> Input section  ................
openai_api = Entry(apiinfo_frame, width=40)
openai_api.insert(0, "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")
openai_api.grid(row=3, column=0, padx=5, pady=10)

api_model = Entry(apiinfo_frame, width=15)
api_model.insert(0, "text-davinci-003")
api_model.grid(row=3, column=1, padx=5, pady=10)

youtube_api = Entry(apiinfo_frame, width=40)
youtube_api.insert(0, "AIzaSyCd9r6YUMPcJk9wMxxg4spI6ATySesPXBo")
youtube_api.grid(row=3, column=2, padx=5, pady=10)

youtube_switch = ttk.Combobox(apiinfo_frame, width=10,values=['Off', 'On'], state='readonly')
youtube_switch.set('Off')
youtube_switch.grid(row=3, column=3,pady=10, padx=5)

feature_img_switch = ttk.Combobox(apiinfo_frame, width=10, values=['On', 'Off'], state='readonly')
feature_img_switch.set('On')
feature_img_switch.grid(row=3, column=4,pady=10, padx=5)

body_img_switch = ttk.Combobox(apiinfo_frame, width=10, values=['On', 'Off'], state='readonly')
body_img_switch.set('On')
body_img_switch.grid(row=3, column=5,pady=10, padx=5)


# >>> OpenAI Command Section .................
openai_section = LabelFrame(content_frame, text="OpenAI Command Section")
openai_section.grid(pady=10, padx=10)

# >>>> Label Section..........
outline_generator_label = Label(openai_section, text="Outline Generator : ")
outline_generator_label.grid(row=4, column=0, pady=5, padx=10, sticky='w')

outline_generator = Text(openai_section, height=2, width=106)
outline_generator.grid(row=4, column=1, pady=5, padx=10)

intro_generator_label = Label(openai_section, text="Intro Generator : ")
intro_generator_label.grid(row=5, column=0, pady=5, padx=10, sticky='w')

# >>>> Input Section..........
intro_generator = Text(openai_section, height=2, width=106)
intro_generator.grid(row=5, column=1, pady=5, padx=10)

para_generator_label = Label(openai_section, text="Para Generator : ")
para_generator_label.grid(row=6, column=0, pady=5, padx=10, sticky='w')

para_generator = Text(openai_section, height=2, width=106)
para_generator.grid(row=6, column=1, pady=5, padx=10)

faq_generator_label: Label = Label(openai_section, text="FAQ Generator : ")
faq_generator_label.grid(row=7, column=0, pady=5, padx=10, sticky='w')

faq_generator = Text(openai_section, height=2, width=106)
faq_generator.grid(row=7, column=1, pady=5, padx=10)

faq_ans_generator_label: Label = Label(openai_section, text="FAQ Ans Generator : ")
faq_ans_generator_label.grid(row=8, column=0, pady=5, padx=10, sticky='w')

faq_ans_generator = Text(openai_section, height=2, width=106)
faq_ans_generator.grid(row=8, column=1, pady=5, padx=10)

conclusion_generator_label: Label = Label(openai_section, text="Conclusion Generator : ")
conclusion_generator_label.grid(row=9, column=0, pady=5, padx=10, sticky='w')

conclusion_generator = Text(openai_section, height=2, width=106)
conclusion_generator.grid(row=9, column=1, pady=5, padx=10)

excerpt_generator_label: Label = Label(openai_section, text="Excerpt Generator : ")
excerpt_generator_label.grid(row=10, column=0, pady=5, padx=10, sticky='w')

excerpt_generator = Text(openai_section, height=2, width=106)
excerpt_generator.grid(row=10, column=1, pady=5, padx=10)

# >>> Terminal .........................
terminal = LabelFrame(content_frame, text="Terminal")
terminal.grid(row=11, column=0, )

# >>> Label  .................
keyword_label = Label(terminal, text="Input Keywords")
keyword_label.grid(row=11, column=0, pady=5)

output_label = Label(terminal, text="Output")
output_label.grid(row=11, column=1, pady=5)

# >>> Input .............
keyword_input = Text(terminal, width=62)
keyword_input.insert('1.0', "Input keyword list here...")
keyword_input.grid(row=12, column=0, pady=0, ipadx=5)

output = Text(terminal, bg='#3F4247', fg='white', width=62)
output.grid(row=12, column=1, pady=0, ipadx=5)


# >>> Command ................
command_label = Frame(content_frame)
command_label.grid(row=13,column=0)

start = Button(command_label, text="Run", font=15, bg='#20B2AA', fg='white', command=lambda:operation_start()) # Labda have to use when function is below
start.grid(row=14, column=0, padx=20, pady=20, ipadx=20)

stop = Button(command_label, text='Stop', font=15, bg='#CC397B', fg='white')
stop.grid(row=14, column=1, padx=20, pady=20, ipadx=20)


def operation_start():
    website_name = website_entry.get()
    username = username_entry.get()
    app_pass = app_pass_entry.get()
    category_name = category.get()
    status_value = status.get()
    keyword_list = keyword_input.get('1.0', 'end-1c')

    output.insert(1.0, 'Website Name: ' + website_name + '\n')
    output.insert(1.0, 'User Name: ' + username + '\n')
    output.insert(1.0, 'App Password: ' + app_pass + '\n')
    output.insert(1.0, 'Category Name: ' + category_name + '\n')
    output.insert(1.0, 'Status: ' + status_value + '\n')
    output.insert(1.0, 'Keyword: ' + keyword_list + '\n')

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

if __name__== '__main__':
    window.mainloop()
