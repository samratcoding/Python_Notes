# https://customtkinter.tomschimansky.com/documentation/

from customtkinter import *
from PIL import ImageTk
import os

window = CTk()
set_appearance_mode("System")
set_default_color_theme("green")
window.title("Automation App")
window.geometry("1050x700")
iconpath = ImageTk.PhotoImage(file=os.path.join("logo.png"))
window.wm_iconbitmap()
window.iconphoto(False, iconpath)

# Create a Frame + Content Frame with scrollbar
frame = CTkFrame(window)
frame.pack(fill=BOTH, expand=True)
canvas = CTkCanvas(frame)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
canvas.bind_all("<MouseWheel>", lambda event:on_mousewheel(event))  # Labda have to use when function is below
scrollbar = CTkScrollbar(frame, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
content_frame = CTkFrame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor=NW)



# website info widgets
webinfo_frame = CTkFrame(content_frame)
webinfo_frame.grid(pady=10, padx=20)

# label section
website_name = CTkLabel(webinfo_frame, text="Website Name")
website_name.grid(row=0, column=0, padx=10, pady=3)

user_name = CTkLabel(webinfo_frame, text="User Name")
user_name.grid(row=0, column=1, padx=10, pady=3)

app_pass = CTkLabel(webinfo_frame, text="Application Password")
app_pass.grid(row=0, column=2, padx=10, pady=3)

status = CTkLabel(webinfo_frame, text="Post Status")
status.grid(row=0, column=3, padx=10, pady=3)

category = CTkLabel(webinfo_frame, text="Category")
category.grid(row=0, column=4, padx=10, pady=3)

# Input section
website_entry = CTkEntry(webinfo_frame, width=250, border_width=1)
website_entry.insert(0, "edmontonranked.ca")  # Default data
website_entry.grid(row=1, column=0, padx=10, pady=10)

username_entry = CTkEntry(webinfo_frame, width=150, border_width=1)
username_entry.insert(0, "info@updigital.ca")
username_entry.grid(row=1, column=1, padx=10, pady=10)

app_pass_entry = CTkEntry(webinfo_frame, width=250, border_width=1)
app_pass_entry.insert(0, "pXHi KFT4 A7dm JUO5 JaXz r2gY")
app_pass_entry.grid(row=1, column=2, padx=10, pady=10)

category = CTkEntry(webinfo_frame, width=150, border_width=1)
category.insert(0, 'Category Name..')
category.grid(row=1, column=3, pady=10, padx=10)

status = CTkComboBox(webinfo_frame, width=100, border_width=1, values=['draft', 'publish'], state='readonly')
status.set('draft')
status.grid(row=1, column=4,pady=10, padx=10)




# API info widgets
apiinfo_frame = CTkFrame(content_frame)
apiinfo_frame.grid(pady=10, padx=20)

# label section
openai_api_label = CTkLabel(apiinfo_frame, text="OpenAI API")
openai_api_label.grid(row=2, column=0, padx=5, pady=3)

api_model_label = CTkLabel(apiinfo_frame, text="API Model")
api_model_label.grid(row=2, column=1, padx=5, pady=3)

youtube_api_label = CTkLabel(apiinfo_frame, text="YouTube API")
youtube_api_label.grid(row=2, column=2, padx=5, pady=3)

youtube_switch_label = CTkLabel(apiinfo_frame, text="Youtube ON/OFF")
youtube_switch_label.grid(row=2, column=3, padx=5, pady=3)

feature_img_switch_label = CTkLabel(apiinfo_frame, text="Feature Img ON/OFF")
feature_img_switch_label.grid(row=2, column=4, padx=5, pady=3)

body_img_switch_label = CTkLabel(apiinfo_frame, text="Body Img ON/OFF")
body_img_switch_label.grid(row=2, column=5, padx=5, pady=3)

# Input section
openai_api = CTkEntry(apiinfo_frame, width=250, border_width=1)
openai_api.insert(0, "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")
openai_api.grid(row=3, column=0, padx=5, pady=10)

api_model = CTkEntry(apiinfo_frame, width=125, border_width=1)
api_model.insert(0, "text-davinci-003")
api_model.grid(row=3, column=1, padx=5, pady=10)

youtube_api = CTkEntry(apiinfo_frame, width=250, border_width=1)
youtube_api.insert(0, "AIzaSyCd9r6YUMPcJk9wMxxg4spI6ATySesPXBo")
youtube_api.grid(row=3, column=2, padx=5, pady=10)

youtube_switch = CTkComboBox(apiinfo_frame, width=75, border_width=1, values=['Off', 'On'], state='readonly')
youtube_switch.set('Off')
youtube_switch.grid(row=3, column=3,pady=10, padx=5)

feature_img_switch = CTkComboBox(apiinfo_frame, width=75, border_width=1, values=['On', 'Off'], state='readonly')
feature_img_switch.set('On')
feature_img_switch.grid(row=3, column=4,pady=10, padx=5)

body_img_switch = CTkComboBox(apiinfo_frame, width=75, border_width=1, values=['On', 'Off'], state='readonly')
body_img_switch.set('On')
body_img_switch.grid(row=3, column=5,pady=10, padx=5)


# OpenAI Command Section
openai_section = CTkFrame(content_frame)
openai_section.grid(pady=10, padx=10)

outline_generator_label = CTkLabel(openai_section,width=155, text="Outline Generator : ")
outline_generator_label.grid(row=4, column=0, pady=10, padx=10, sticky='w')

outline_generator = CTkTextbox(openai_section, height=2, width=800, border_width=1)
outline_generator.grid(row=4, column=1, pady=5, padx=10)

intro_generator_label = CTkLabel(openai_section, width=155, text="Intro Generator : ")
intro_generator_label.grid(row=5, column=0, pady=5, padx=10, sticky='w')

intro_generator = CTkTextbox(openai_section, height=2, width=800, border_width=1)
intro_generator.grid(row=5, column=1, pady=5, padx=10)

para_generator_label = CTkLabel(openai_section, width=155, text="Para Generator : ")
para_generator_label.grid(row=6, column=0, pady=5, padx=10, sticky='w')

para_generator = CTkTextbox(openai_section, height=2, width=800, border_width=1)
para_generator.grid(row=6, column=1, pady=5, padx=10)

faq_generator_label = CTkLabel(openai_section, width=155, text="FAQ Generator : ")
faq_generator_label.grid(row=7, column=0, pady=5, padx=10, sticky='w')

faq_generator = CTkTextbox(openai_section, height=2, width=800, border_width=1)
faq_generator.grid(row=7, column=1, pady=5, padx=10)

faq_ans_generator_label = CTkLabel(openai_section, width=155, text="FAQ Ans Generator : ")
faq_ans_generator_label.grid(row=8, column=0, pady=5, padx=10, sticky='w')

faq_ans_generator = CTkTextbox(openai_section, height=2, width=800, border_width=1)
faq_ans_generator.grid(row=8, column=1, pady=5, padx=10)

conclusion_generator_label = CTkLabel(openai_section, width=155, text="Conclusion Generator : ")
conclusion_generator_label.grid(row=9, column=0, pady=5, padx=10, sticky='w')

conclusion_generator = CTkTextbox(openai_section, height=2, width=800, border_width=1)
conclusion_generator.grid(row=9, column=1, pady=5, padx=10)

excerpt_generator_label= CTkLabel(openai_section, width=155, text="Excerpt Generator : ")
excerpt_generator_label.grid(row=10, column=0, pady=5, padx=10, sticky='w')

excerpt_generator = CTkTextbox(openai_section, height=2, width=800, border_width=1)
excerpt_generator.grid(row=10, column=1, pady=10, padx=10)

# Terminal
terminal = CTkFrame(content_frame)
terminal.grid(row=11, column=0)

keyword_label = CTkLabel(terminal, text="Input Keywords")
keyword_label.grid(row=11, column=0, pady=5)

output_label = CTkLabel(terminal, text="Output")
output_label.grid(row=11, column=1, pady=5)

keyword_input = CTkTextbox(terminal, width=486, height=300)
keyword_input.insert('1.0', "Input keyword list here...")
keyword_input.grid(row=12, column=0, pady=0, ipadx=5)

output = CTkTextbox(terminal, fg_color=('black', 'white'), text_color=('white'), width=486, height=300)
output.grid(row=12, column=1, pady=0, ipadx=5)


# Command
command_label = CTkFrame(content_frame)
command_label.grid(row=13,column=0, padx=20, pady=(30, 200))

start = CTkButton(command_label, text="Run",  command=lambda:operation_start()) # Labda have to use when function is below
start.grid(row=14, column=0, padx=20, pady=20, ipadx=20)

stop = CTkButton(command_label, text='Stop', fg_color=("red"))
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


'''
from customtkinter import *
set_appearance_mode("dark")
set_default_color_theme("green")

window = CTk()
root.title("CustomTkinter Tabview")

tabview = CTkTabview(window)
tabview.pack(padx=20, pady=20)

tab1 = tabview.add("tab 1")
tabview.add("tab 2")
tabview.set("tab 2")

button_1 = CTkButton(tab1)
button_1.pack(padx=20, pady=20)

root.mainloop()
'''
