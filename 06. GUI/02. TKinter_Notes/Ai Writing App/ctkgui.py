from component import *
from customtkinter import *
import sqlite3
import base64
import shutil
from PIL import ImageTk
import os
import threading
import webbrowser

con = sqlite3.connect('postdb.db')
cur = con.cursor()
cur.execute('''
            CREATE TABLE IF NOT EXISTS Postdata (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Website_name CHAR(200),
                User_name CHAR(200),
                App_pass CHAR(200),
                Category_name CHAR(200),
                Openai_api CHAR(200),
                Openai_model CHAR(200), 
                Youtube_api CHAR(200), 
                Outline_generator TEXT,
                Intro_generator TEXT,
                PARA_generator TEXT,
                faq_generator TEXT,
                faq_ans TEXT,
                conclusion_generator  TEXT,
                excerpt_generator TEXT,     
                title_generator TEXT    
            )  
            ''')


data_check = cur.execute('''SELECT Website_name FROM Postdata WHERE ID=1''').fetchone()
print(data_check)

if data_check == None:
    cur.execute('''
                    INSERT INTO Postdata(
                        Website_name,
                        User_name,
                        App_pass,
                        Category_name,
                        Openai_api,
                        Openai_model,
                        Youtube_api,
                        Outline_generator,
                        Intro_generator,
                        PARA_generator,
                        faq_generator,
                        faq_ans,
                        conclusion_generator,
                        excerpt_generator,
                        title_generator)
                    VALUES(
                        'https://websitename.com/',
                        'wp username',
                        'app pass token',
                        'category name', 
                        'Openai Key',
                        'Openai_model',
                        'Youtube_api',
                        'Write outline on this topic ((keyword)) \nOutline must be H2 : format, not underscore, not symbol, not hyphen, not number and no indentation, under each H2 : will have 4 H3 : not need sub heading for H3 :\nAnd an important command is, outlines not answer \nAnd another important command is, do not give me me Introduction and Conclusion, each heading length must be less than 7 words\nH1: ((keyword))\n',
                        'Write a introduction on this keyword intro start with technical terms, not like are you and keyword must be include in output do not give me direct solution in intro section, intro last sentence must be interesting to read the full article, keyword: ((keyword))\nAnd length approx 100 words\n',
                        'Write paragraph section, interesting, and organized way like human writing but not unnecessary words and do not mention keyword and directly give answer without any similes \nPrompt Rember : ((previous_data))\nArticle title is : ((keyword)), heading is : ((heading)) \nYou are content writing expert output length will be 120 words and 12 to 15 words will have per sentence\n',
                        'Topic:((keyword))\nWrite 5 related questions on this topic\n1.',
                        'Write a short answer to this question within four sentence ((faq_question))',
                        'keyword: ((keyword))\nWrite an web article bottom summary\nAnd length approx 60 words\n',
                        'Write a short summary,\nKeyword: ((keyword)),\nMust be include keyword in output\nand length approx 25 words\n',                          
                        'Write an SEO title on this keyword within 55 characters and the keyword must be directly included in the title \nkeyword : ((keyword))\n'                           
                    )
                    
                    ''')
# TK part
window = CTk()
set_default_color_theme("green")
set_appearance_mode("light")
window.title("AI Writing App by Samrat Biswas")
window.geometry("1050x700")
iconpath = ImageTk.PhotoImage(file=os.path.join("logo.ico"))
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

category = CTkLabel(webinfo_frame, text="Category")
category.grid(row=0, column=3, padx=10, pady=3)

status = CTkLabel(webinfo_frame, text="Post Status")
status.grid(row=0, column=4, padx=10, pady=3)


# Input section
website_entry = CTkEntry(webinfo_frame, width=250, border_width=1)
website_entry.insert(0, str(cur.execute('''SELECT Website_name FROM Postdata WHERE ID=1''').fetchone()[0]))  # Default data
website_entry.grid(row=1, column=0, padx=10, pady=10)

username_entry = CTkEntry(webinfo_frame, width=150, border_width=1)
username_entry.insert(0, str(cur.execute('''SELECT User_name FROM Postdata WHERE ID=1''').fetchone()[0]))
username_entry.grid(row=1, column=1, padx=10, pady=10)

app_pass_entry = CTkEntry(webinfo_frame, width=250, border_width=1)
app_pass_entry.insert(0, str(cur.execute('''SELECT App_pass FROM Postdata WHERE ID=1''').fetchone()[0]))
app_pass_entry.grid(row=1, column=2, padx=10, pady=10)

category = CTkEntry(webinfo_frame, width=150, border_width=1)
category.insert(0, str(cur.execute('''SELECT Category_name FROM Postdata WHERE ID=1''').fetchone()[0]))
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

model_type_label = CTkLabel(apiinfo_frame, text="Mode")
model_type_label.grid(row=2, column=2, padx=5, pady=3)

youtube_api_label = CTkLabel(apiinfo_frame, text="YouTube API")
youtube_api_label.grid(row=2, column=3, padx=5, pady=3)

youtube_switch_label = CTkLabel(apiinfo_frame, text="YouTube")
youtube_switch_label.grid(row=2, column=4, padx=5, pady=3)

feature_img_switch_label = CTkLabel(apiinfo_frame, text="Feature Img")
feature_img_switch_label.grid(row=2, column=5, padx=5, pady=3)

body_img_switch_label = CTkLabel(apiinfo_frame, text="Body Img")
body_img_switch_label.grid(row=2, column=6, padx=5, pady=3)

# Input section
openai_api = CTkEntry(apiinfo_frame, width=250, border_width=1)
openai_api.insert(0, str(cur.execute('''SELECT Openai_api FROM Postdata WHERE ID=1''').fetchone()[0]))
openai_api.grid(row=3, column=0, padx=5, pady=10)

api_model = CTkEntry(apiinfo_frame, width=125, border_width=1)
api_model.insert(0, str(cur.execute('''SELECT Openai_model FROM Postdata WHERE ID=1''').fetchone()[0]))
api_model.grid(row=3, column=1, padx=5, pady=10)

model_type = CTkComboBox(apiinfo_frame, width=85, values=('Chat','Regular'), border_width=1, state='readonly')
model_type.set('Chat')
model_type.grid(row=3, column=2, padx=5, pady=10)

youtube_api = CTkEntry(apiinfo_frame, width=240, border_width=1)
youtube_api.insert(0, str(cur.execute('''SELECT Youtube_api FROM Postdata WHERE ID=1''').fetchone()[0]))
youtube_api.grid(row=3, column=3, padx=5, pady=10)

youtube_switch = CTkComboBox(apiinfo_frame, width=75, border_width=1, values=['Off', 'On'], state='readonly')
youtube_switch.set('Off')
youtube_switch.grid(row=3, column=4,pady=10, padx=5)

feature_img_switch = CTkComboBox(apiinfo_frame, width=75, border_width=1, values=['On', 'Off'], state='readonly')
feature_img_switch.set('On')
feature_img_switch.grid(row=3, column=5,pady=10, padx=5)

body_img_switch = CTkComboBox(apiinfo_frame, width=75, border_width=1, values=['On', 'Off'], state='readonly')
body_img_switch.set('On')
body_img_switch.grid(row=3, column=6,pady=10, padx=5)


# OpenAI Command Section
openai_section = CTkFrame(content_frame)
openai_section.grid(pady=10, padx=10)

outline_generator_label = CTkLabel(openai_section,width=155, text="Outline Generator : ")
outline_generator_label.grid(row=4, column=0, pady=10, padx=10, sticky='w')

outline_generator = CTkTextbox(openai_section, height=130, width=800, border_width=1)
outline_generator.insert(1.0, str(cur.execute('''SELECT Outline_generator FROM Postdata WHERE ID=1''').fetchone()[0]))
outline_generator.grid(row=4, column=1, pady=5, padx=10)

intro_generator_label = CTkLabel(openai_section, width=155, text="Intro Generator : ")
intro_generator_label.grid(row=5, column=0, pady=5, padx=10, sticky='w')

intro_generator = CTkTextbox(openai_section, height=80, width=800, border_width=1)
intro_generator.insert(1.0, str(cur.execute('''SELECT Intro_generator FROM Postdata WHERE ID=1''').fetchone()[0]))
intro_generator.grid(row=5, column=1, pady=5, padx=10)

para_generator_label = CTkLabel(openai_section, width=155, text="Para Generator : ")
para_generator_label.grid(row=6, column=0, pady=5, padx=10, sticky='w')

para_generator = CTkTextbox(openai_section, height=120, width=800, border_width=1)
para_generator.insert(1.0, str(cur.execute('''SELECT PARA_generator FROM Postdata WHERE ID=1''').fetchone()[0]))
para_generator.grid(row=6, column=1, pady=5, padx=10)

faq_generator_label = CTkLabel(openai_section, width=155, text="FAQ Generator : ")
faq_generator_label.grid(row=7, column=0, pady=5, padx=10, sticky='w')

faq_generator = CTkTextbox(openai_section, height=80, width=800, border_width=1)
faq_generator.insert(1.0, str(cur.execute('''SELECT faq_generator FROM Postdata WHERE ID=1''').fetchone()[0]))
faq_generator.grid(row=7, column=1, pady=5, padx=10)

faq_ans_generator_label = CTkLabel(openai_section, width=155, text="FAQ Ans Generator : ")
faq_ans_generator_label.grid(row=8, column=0, pady=5, padx=10, sticky='w')

faq_ans_generator = CTkTextbox(openai_section, height=2, width=800, border_width=1)
faq_ans_generator.insert(1.0, str(cur.execute('''SELECT faq_ans FROM Postdata WHERE ID=1''').fetchone()[0]))
faq_ans_generator.grid(row=8, column=1, pady=5, padx=10)

conclusion_generator_label = CTkLabel(openai_section, width=155, text="Conclusion Generator : ")
conclusion_generator_label.grid(row=9, column=0, pady=5, padx=10, sticky='w')

conclusion_generator = CTkTextbox(openai_section, height=90, width=800, border_width=1)
conclusion_generator.insert(1.0, str(cur.execute('''SELECT conclusion_generator FROM Postdata WHERE ID=1''').fetchone()[0]))
conclusion_generator.grid(row=9, column=1, pady=5, padx=10)

excerpt_generator_label= CTkLabel(openai_section, width=155, text="Excerpt Generator : ")
excerpt_generator_label.grid(row=10, column=0, pady=5, padx=10, sticky='w')

excerpt_generator = CTkTextbox(openai_section, height=100, width=800, border_width=1)
excerpt_generator.insert(1.0, str(cur.execute('''SELECT excerpt_generator FROM Postdata WHERE ID=1''').fetchone()[0]))
excerpt_generator.grid(row=10, column=1, pady=10, padx=10)

title_generator_label= CTkLabel(openai_section, width=155, text="Title Generator : ")
title_generator_label.grid(row=11, column=0, pady=5, padx=10, sticky='w')

title_generator = CTkTextbox(openai_section, height=70, width=800, border_width=1)
title_generator.insert(1.0, str(cur.execute('''SELECT title_generator FROM Postdata WHERE ID=1''').fetchone()[0]))
title_generator.grid(row=11, column=1, pady=10, padx=10)

# Terminal
terminal = CTkFrame(content_frame)
terminal.grid(row=11, column=0)

keyword_label = CTkLabel(terminal, text="Input Keywords")
keyword_label.grid(row=12, column=0, pady=5)

output_label = CTkLabel(terminal, text="Output")
output_label.grid(row=12, column=1, pady=5)

keyword_input = CTkTextbox(terminal, width=486, height=300)
keyword_input.insert('1.0', "Input keyword list here...")
keyword_input.grid(row=13, column=0, pady=0, ipadx=5)

output = CTkTextbox(terminal, fg_color=('black', 'white'), text_color=('white', 'black'), width=486, height=300)
output.grid(row=13, column=1, pady=0, ipadx=5)


# Command
command_label = CTkFrame(content_frame)
command_label.grid(row=14,column=0, padx=10, pady=(30, 30))

start = CTkButton(command_label, text=" ▶ Run", fg_color=('#2AA26F'), command=lambda:operation_start()) # Labda have to use when function is below
start.grid(row=15, column=0, padx=20, pady=10, ipadx=20)

Update = CTkButton(command_label, text=' ✔ Save Update', fg_color=("#2AA26F"), command=lambda:db_save())
Update.grid(row=15, column=1, padx=20, pady=10, ipadx=20)

Reset = CTkButton(command_label, text=' ↻ Reset Commands', fg_color=("#EB4C42"), command=lambda:reset_data())
Reset.grid(row=15, column=2, padx=20, pady=10, ipadx=20)

# Log
log_label = CTkLabel(content_frame, text="Logs", font=('',20), fg_color=("red"))
log_label.grid(row=16, column=0, pady=0, ipadx=20)

log = CTkTextbox(content_frame, fg_color=('black', 'white'), text_color=('white', 'black'), width=990, height=200)
log.grid(row=17, column=0, padx=5,  pady=(5, 10))

copyright = CTkLabel(content_frame, text="Need any help ?")
copyright.grid(row=18, column=0, padx=5,  pady=(5, 0))

copy_button = CTkButton(content_frame, text="Contact With Developer", fg_color=('#2374E1'), command=lambda : webbrowser.open_new('https://www.facebook.com/samratprobd/'))
copy_button.grid(row=19, column=0, padx=5,  pady=(5, 300))


def db_save():
    website_name = str(website_entry.get())
    username = str(username_entry.get())
    app_pass = str(app_pass_entry.get())
    category_name = str(category.get())
    openai_key = str(openai_api.get())
    model = str(api_model.get())
    youtube_key = str(youtube_api.get())
    outline_command = str(outline_generator.get('1.0', 'end-1c'))
    intro_command = str(intro_generator.get('1.0', 'end-1c'))
    para_command = str(para_generator.get('1.0', 'end-1c'))
    faq_command = str(faq_generator.get('1.0', 'end-1c'))
    faq_ans_command = str(faq_ans_generator.get('1.0', 'end-1c'))
    conclusion_command = str(conclusion_generator.get('1.0', 'end-1c'))
    except_command = str(excerpt_generator.get('1.0', 'end-1c'))
    title_command = str(title_generator.get('1.0', 'end-1c'))
cur.execute('''
    UPDATE Postdata
    SET
        Website_name = ?,
        User_name = ?,
        App_pass = ?,
        Category_name = ?,
        Openai_api = ?,
        Openai_model = ?,
        Youtube_api = ?,
        Outline_generator = ?,
        Intro_generator = ?,
        PARA_generator = ?,
        faq_generator = ?,
        faq_ans = ?,
        conclusion_generator = ?,
        excerpt_generator = ?,
        title_generator = ?
    WHERE ID = 1
''', (
    website_name,
    username,
    app_pass,
    category_name,
    openai_key,
    model,
    youtube_key,
    outline_command,
    intro_command,
    para_command,
    faq_command,
    faq_ans_command,
    conclusion_command,
    except_command,
    title_command
))


def reset_data():
    cur.execute('''
                    UPDATE Postdata
                    SET
                        Website_name = 'https://websitename.com/',
                        User_name = 'wp username',
                        App_pass = 'app pass token',
                        Category_name = 'category name', 
                        Openai_api = 'Openai Key',
                        Openai_model = 'Openai_model',
                        Youtube_api = 'Youtube_api',
                        Outline_generator = 'Write outline on this topic ((keyword)) \nOutline must be H2 : format, not underscore, not symbol, not hyphen, not number and no indentation, under each H2 : will have 4 H3 : not need sub heading for H3 :\nAnd an important command is, outlines not answer \nAnd another important command is, do not give me me Introduction and Conclusion, each heading length must be less than 7 words\nH1: ((keyword))\n',
                        Intro_generator = 'Write a introduction on this keyword intro start with technical terms, not like are you and keyword must be include in output do not give me direct solution in intro section, intro last sentence must be interesting to read the full article, keyword: ((keyword))\nAnd length approx 100 words\n',
                        PARA_generator = 'Write paragraph section, interesting, and organized way like human writing but not unnecessary words and do not mention keyword and directly give answer without any similes \nPrompt Rember : ((previous_data))\nArticle title is : ((keyword)), heading is : ((heading)) \nYou are content writing expert output length will be 120 words and 12 to 15 words will have per sentence\n',
                        faq_generator = 'Topic:((keyword))\nWrite 5 related questions on this topic\n1.',
                        faq_ans = 'write a short answer to this question within four sentence ((faq_question))',
                        conclusion_generator = 'keyword: ((keyword))\nWrite an web article bottom summary\nAnd length approx 60 words\n',
                        excerpt_generator = 'write a short summary,\nKeyword: ((keyword)),\nMust be include keyword in output\nand length approx 25 words\n',                          
                        title_generator = 'write an SEO title on this keyword within 55 characters and the keyword must be directly included in the title \nkeyword : ((keyword))\n'
                    WHERE ID = 1
                    
                    ''')
    window.destroy()

def operation_start():
    thread = threading.Thread(target=operation_start_thread)
    thread.start()

def operation_start_thread():
    website_url = website_entry.get()
    Username = username_entry.get()
    App_pass = app_pass_entry.get()
    category_name = category.get()
    status_value = status.get()
    openai_key = openai_api.get()
    engine = api_model.get()
    engine_type = model_type.get()
    youtube_key = youtube_api.get()
    youtube_status = youtube_switch.get()
    feature_img_status = feature_img_switch.get()
    body_img_status = body_img_switch.get()
    outline_command = outline_generator.get('1.0', 'end-1c')
    intro_command = intro_generator.get('1.0', 'end-1c')
    para_command = para_generator.get('1.0', 'end-1c')
    faq_command = faq_generator.get('1.0', 'end-1c')
    faq_ans_command = faq_ans_generator.get('1.0', 'end-1c')
    conclusion_command = conclusion_generator.get('1.0', 'end-1c')
    except_command = excerpt_generator.get('1.0', 'end-1c')
    title_command = title_generator.get('1.0', 'end-1c')


    # Wordpress posting code-----------------
    json_url = website_url + 'wp-json/wp/v2'
    token = base64.standard_b64encode((Username + ':' + App_pass).encode('utf-8'))  # we have to encode the usr and pw
    headers = {'Authorization': 'Basic ' + token.decode('utf-8')}

    i = 1
    keyword_list = keyword_input.get('1.0', 'end-1c')
    all_keywords = keyword_list.splitlines()
    output.delete('0.0', END)
    output.insert('0.0', '>>> Start Working...\n')
    for keyword in all_keywords:
        if len(keyword) > 0:
            print('Keyword : ', keyword)
            print(engine)
            print(engine_type)

            log.delete('0.0', END)
            log.insert(END, f'Keyword : {keyword}\n\n')
            log.insert(END, f'{engine}\n')
            log.insert(END, f'{engine_type}\n')

            openai_check = text_render('what is 1 + 1? Give me answer within 1 one character', openai_key, engine, engine_type, log, 0.3)
            if openai_check != 'openaierror':
                introduction = text_format(text_render(intro_command.replace('((keyword))', keyword), openai_key, engine, engine_type, log, 0.5), log)
                excerpt = text_render(except_command.replace('((keyword))',keyword), openai_key, engine, engine_type, log, 0.5)
                conclusion_para = text_format(text_render(conclusion_command.replace('((keyword))',keyword), openai_key, engine, engine_type, log, 0.5), log)

                # h2_title = text_render(f'Write an h2 heading on this keyword within 55 characters before starting the main article and the keyword must be directly included in the title \n keyword : {keyword}\n', keyword_model, 0.3).replace('"','').title()
                # summary = text_render(f'Write a short briefing before starting the main article after intro,\nKeyword: {keyword},\nMust be include keyword in output\nand length approx 70 words\n',keyword_model, 0.5)

                feature_img_raw = feature_image(keyword.strip(), json_url, headers, feature_img_status, log)
                image_id = feature_img_raw[0]
                print('Feature Image id ..........:', image_id)
                log.insert(END, f'Feature Image id ..........:{image_id}\n')
                img_source = feature_img_raw[1]
                print('Feature Image img_source ..........:', img_source)
                log.insert(END, f'Feature Image img_source ..........:{img_source}\n')


                post_body = introduction + img_source + content_body(keyword, para_command, outline_command, openai_key, engine,engine_type,json_url,headers, body_img_status, log) + youtubevid(keyword, youtube_key, youtube_status, log) + "<h2> FAQ's </h2>" + faq(keyword, faq_command, faq_ans_command, openai_key, engine, engine_type, log) + '<h2>Conclusion</h2>' + conclusion_para

                if post_body != 'contenbodyerror':
                    category_id = create_category(category_name, json_url, headers)
                    title = text_render(title_command.replace('((keyword))',keyword), openai_key, engine, engine_type, log, 0.3).replace('"','').title()
                    slug = keyword.replace(' ', '-')

                    # Post Data
                    if category_id == 0:
                        post = {'title': title,'slug': slug,'status': status_value,'content': post_body,'format': 'standard','excerpt': excerpt,'featured_media': int(image_id)}
                    else:
                        post = {'title': title,'slug': slug,'status': status_value,'content': post_body,'categories': [category_id],'format': 'standard','excerpt': excerpt,'featured_media': int(image_id)}


                    # Posting Request
                    r = requests.post(json_url + '/posts', headers=headers, json=post)
                    if r.status_code == 201:
                        output.insert(END, ''+str(i)+'. Keyword: ' + keyword + '\n')
                        print('completed, kw:', keyword)
                        log.insert(END, f'completed, kw: {keyword}')
                    else:
                        output.insert(END, str(f'{str(i)} . {keyword}, WP Error, Status Code is : {r.status_code}\n'))
                    sleep(10)
                    shutil.rmtree('bulkimg')
                else:
                    output.insert(END, str(f'{str(i)} . {keyword}, **OpenAI API error...\n'))


            else:
                output.insert(END, str(f'{str(i)} . {keyword}, **OpenAI API error...\n'))
        i += 1




def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")



if __name__== '__main__':
    window.mainloop()

con.commit()
cur.close()
