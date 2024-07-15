import openai
from random import choice
from PIL import Image
from PIL import ImageFile
import requests
import os
import json
from time import sleep
from googleapiclient.discovery import build
from bing_image_downloader import downloader
import people_also_ask
import re
ImageFile.LOAD_TRUNCATED_IMAGES = True
from tkinter import END


def image_operation_bing(command, log):
    print('Image operation ..............')
    log.insert(END,'Image operation ..............\n')
    try:
        os.mkdir('bulkimg')
    except FileExistsError:
        pass
    try:
        downloader.download(command, limit=1, output_dir='bulkimg', filter='.jpg', verbose=False)
        try:
            im = Image.open('bulkimg/' + command + '/Image_1.jpg')
        except:
            try:
                im = Image.open('bulkimg/' + command + '/Image_1.png')
            except:
                im = Image.open('bulkimg/' + command + '/Image_1.JPEG')

        # Define the desired size
        desired_size = (670, 330)
        # Calculate the cropping area based on the desired size
        width, height = im.size
        left = (width - desired_size[0]) / 2
        upper = (height - desired_size[1]) / 2
        right = (width + desired_size[0]) / 2
        lower = (height + desired_size[1]) / 2

        # Crop the image
        cropped_image = im.crop((left, upper, right, lower))
        cropped_image.save('bulkimg/' + command + '.jpg')
    except:
        pass


def body_img(command, json_url, headers, body_img_status, log):
    if body_img_status == 'On':
        image_operation_bing(command, log)
        try:
            media = {'file': open('bulkimg/' + command + '.jpg', 'rb')}
            image = requests.post(json_url + '/media', headers=headers, files=media)
            print(' Body IMG : --------- ', image)
            log.insert(END, f'Body IMG : --------- {image}\n')
            image_title = command.replace('-', ' ').split('.')[0]
            post_id = str(json.loads(image.content.decode('utf-8'))['id'])
            source = json.loads(image.content.decode('utf-8'))['guid']['rendered']
            image1 = '<!-- wp:image {"align":"center","id":' + post_id + ',"sizeSlug":"full","linkDestination":"none"} -->'
            image2 = '<div class="wp-block-image"><figure class="aligncenter size-full"><img src="' + source + '" alt="' + image_title + '" title="' + image_title + '" class="wp-image-' + post_id + '"/></figure></div>'
            image3 = '<!-- /wp:image -->'
            image_wp = image1 + image2 + image3
            print('Body Image:\n.......\n.........\n.........\n', image_wp, '...........\n.........\n.....\n')
            log.insert(END, f'Body Image:\n.......\n.........\n.........\n {image_wp} ...........\n.........\n.....\n')
            return image_wp
        except:
            return ''
    else:
        return ''

def feature_image(command, json_url, headers, feature_img_status, log):
    if feature_img_status == 'On':
        image_operation_bing(command, log)
        try:
            media = {'file': open('bulkimg/' + command + '.jpg', 'rb')}
            image = requests.post(json_url + '/media', headers=headers, files=media)
            print(' Body IMG : --------- ', image)
            log.insert(END, f'Body IMG : --------- {image}\n')
            image_title = command.replace('-', ' ').split('.')[0]
            post_id = str(json.loads(image.content.decode('utf-8'))['id'])
            source = json.loads(image.content.decode('utf-8'))['guid']['rendered']
            image1 = '<!-- wp:image {"align":"center","id":' + post_id + ',"sizeSlug":"full","linkDestination":"none"} -->'
            image2 = '<div class="wp-block-image"><figure class="aligncenter size-full"><img src="' + source + '" alt="' + image_title + '" title="' + image_title + '" class="wp-image-' + post_id + '"/></figure></div>'
            image3 = '<!-- /wp:image -->'
            image_wp = image1 + image2 + image3
            f_img = [post_id, image_wp]
            return f_img
        except:
            f_img = [0, '']
            return f_img
    else:
        f_img = [0, '']
        return f_img


def text_format(text, log):
    print('Text formating .................')
    log.insert(END, f'Text formating .................\n')
    if len(text) > 0:
        rc1 = choice([3, 4])
        rc2 = choice([10, 11])
        rc3 = choice([16, 17])
        p_format = text.replace('?', '?---').replace('.', '.---').replace('!', '!---').strip().split(sep='---')
        p = '<p>' + ''.join(p_format[:rc1]) + '</p>' + '<p>' + ''.join(p_format[rc1:7]) + '</p>' + '<p>' + ''.join(p_format[7:rc2]) + '</p>' + '<p>' + ''.join(p_format[rc2:13]) + '</p>' + '<p>' + ''.join(p_format[13:rc3]) + '</p>' + '<p>' + ''.join(p_format[rc3:20]) + '</p>' + '<p>' + ''.join(p_format[20:]) + '</p>'
        text = p.replace('  ', ' ').replace('<p></p>', '').replace('<p><p>', '<p>').replace('</p></p>', '</p>').replace('<p> ', '<p>').replace('\n', '').replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').replace('5.', '').replace('6.', '').replace('7.', '').replace('8.', '').replace('9.', '').replace('10.', '').replace('<p>  ','<p>').replace('<p> ','<p>').replace('.','. ').replace('.  ','. ').replace('!!','')
        return text
    else:
        return ''


def text_generate(prompt, engine, model_type, log, temp):
    if model_type == 'Regular':
        res = openai.Completion.create(model=engine.strip(), prompt=prompt, temperature=temp, max_tokens=2000,top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0,stop=['asdfasdf', 'asdasdf'])
        text = res['choices'][0]['text'].strip()
        print('Text render .................')
        log.insert(END, 'Text render .................\n')
        return text
    else:
        response = openai.ChatCompletion.create(model=engine, messages=[{"role": "system", "content": ''},{"role": "user", "content": prompt}])
        result = ''
        for choice in response.choices:
            result += choice.message.content
        return result

def text_render(prompt, openai_key, engine, model_type, log, temp=0.7):
    openai.api_key = openai_key
    sleep_sec = 0
    attempts = 1
    max_attempts = 4
    while attempts < max_attempts:
        try:
            text = text_generate(prompt, engine, model_type, log, temp)
            break
        except Exception as Opps:
            print(f"OpenAI Fail, trying {str(attempts + 1)} time...waiting time {str(sleep_sec)} seconds...")
            print(f'Error Message from OpenAI Server : {str(Opps)}')
            log.insert(END, f"OpenAI Fail, trying {str(attempts + 1)} time...waiting time {str(sleep_sec)} seconds...\n")
            log.insert(END, f'Error Message from OpenAI Server : {str(Opps)}\n')
            sleep(sleep_sec)
            sleep_sec += 30
            attempts += 1
    else:
        text = 'openaierror'
        print("Maximum number of attempts reached. Operation failed...")
        log.insert(END, "Maximum number of attempts reached. Operation failed...\n")
    return text


def formated_outline(keyword, outline_command, openai_key, engine_type, engine, log):
    while True:
        outline = text_render(outline_command.replace('((keyword))',keyword), openai_key,engine_type,engine, log)
        if 'h2' in outline or 'H2' in outline or outline == 'openaierror':
            break
    if outline != 'openaierror':
        outlines = list()
        for line in outline.splitlines():
            if len(line) > 1 and not 'introduction' in line.lower() and not 'objective' in line.lower() and not 'conclusion' in line.lower() and not 'overview' == line.lower():
                if 'h2' in line.lower():
                    line_format = line.replace('H2','').replace('h2','').replace(':','').replace('-','').strip()
                    if len(line_format) > 0:
                        outlines.append('<h2>'+line_format.capitalize()+'</h2>')
                else:
                    line_format = line.replace('H3','').replace('h3','').replace(':','').replace('-','').strip()
                    if len(line_format) > 0:
                        outlines.append('<h3>'+line_format.capitalize()+'</h3>')
        return outlines
    else:
        return 'outlineerror'


def content_body(keyword, para_command, outline_command, openai_key, engine, engine_type, json_url,headers, body_img_status, log):
    print('Content body .................')
    log.insert(END, f'Content body .................\n')
    outlines = formated_outline(keyword, outline_command, openai_key, engine, engine_type, log)
    print(outlines)
    log.insert(END, f'{outlines}\n')
    prompt_remember = ''
    content_body_data = ''
    if outlines != 'outlineerror':
        for heading in outlines:
            prompt_remember += heading
            if 'h2' in heading.lower():
                clean_heading = heading.replace('H2', '').replace('h2', '').replace(':', '').replace('-', '').replace('/','').replace('<', '').replace('>', '').replace('Step', '').strip()
                print(f'Para Section H2 : {heading} .................')
                log.insert(END, f'Para Section H2 : {heading} .................\n')

                body_img_src = body_img(clean_heading.strip() + ' of '+keyword.strip(),json_url,headers, body_img_status, log)
                section = text_format(text_render(para_command.replace('((previous_data))', prompt_remember).replace('((keyword))', keyword).replace('((heading))',clean_heading), openai_key, engine, engine_type, log), log)
                prompt_remember = section
                content_body_data += heading + body_img_src + section
            else:
                print(f'Para Section H3 : {heading}.................')
                log.insert(END, f'Para Section H3 : {heading}.................\n')
                clean_heading = heading.replace('H3', '').replace('h3', '').replace(':', '').replace('-', '').replace('/','').replace('<', '').replace('>', '').replace('H4','').replace('h4','').replace('Step','').strip()
                section = text_format(text_render(para_command.replace('((previous_data))', prompt_remember).replace('((keyword))', keyword).replace('((heading))',clean_heading), openai_key, engine, engine_type, log), log)
                prompt_remember = section
                content_body_data += heading + section
        print('Content body done .................')
        log.insert(END, f'Content body done .................\n')
        return content_body_data
    else:
        return 'contenbodyerror'

def create_category(cat_name, json_url, headers):
    id = 0
    if len(cat_name) > 0:
        data = {"name":cat_name}
        try:
            cat = requests.post(json_url + '/categories', headers=headers, json=data)
            id = str(json.loads(cat.content.decode('utf-8'))['id'])
        except KeyError:
            cat = requests.get(json_url + '/categories', headers=headers)
            cat_id = json.loads(cat.content.decode('utf-8'))
            for cat in cat_id:
                if cat_name.lower() == cat['name'].lower():
                    id = str(cat['id'])
    return id

def youtubevid(self, youtube_api, youtube_status, log):
    print('Youtube API .................')
    log.insert(END, 'Youtube API .................\n')
    if youtube_status == 'On':
        youtube = build('youtube', 'v3', developerKey=youtube_api.strip())
        try:
            request = youtube.search().list(q=self, part='snippet', type='video', maxResults=1)
            res = request.execute()
            id = res['items'][0]['id']['videoId']
            youtube_url = '<!-- wp:html --><figure  style="text-align: center"><iframe width="640" height="360" src="https://www.youtube.com/embed/' + id + '?rel=0&amp;enablejsapi=1"></iframe></figure><!-- /wp:html --><!-- wp:separator {"align":"center"} --><hr class="wp-block-separator aligncenter"/><!-- /wp:separator -->'
        except:
            youtube_url = ' *** Youtube API Has Been Finished or Invalid API*** '
        return youtube_url
    else:
        return ''

def faq(keyword, faq_command, faq_ans_command, openai_key, engine, enine_type, log):
    print('FAQ .................')
    log.insert(END, f'FAQ .................\n')
    try:
        questions = people_also_ask.get_related_questions(keyword, 5)
    except:
        outline = text_render(faq_command.replace('((keyword))',keyword), openai_key, engine, enine_type, log)
        questions = outline.splitlines()
    faq_body = ''
    schema = '<script type="application/ld+json">{"@context":"https://schema.org","@type": "FAQPage","mainEntity":['
    for q in questions:
        q_filter = re.sub(r'[0-9]. ','', q)
        q_h3 = '<strong>'+q_filter.title()+'</strong>'
        q_body_raw = text_render(faq_ans_command.replace('((faq_question))',q_filter.replace('"','')), openai_key, engine, enine_type, log)
        q_body = '<!-- wp:paragraph --><p>'+q_body_raw+'</p><!-- /wp:paragraph -->'
        faq_body += q_h3 + q_body
        question = '{"@type": "Question","name": "'+q_filter.replace('"','').title()+'",'
        ans = '"acceptedAnswer": {"@type": "Answer","text": "'+q_body_raw.replace('"','')+'"}},'
        schema += question + ans
    schema += ']}</script>'
    schema_final = schema.replace(',]}</script>',']}</script>')
    faq_final = faq_body + schema_final
    return faq_final
