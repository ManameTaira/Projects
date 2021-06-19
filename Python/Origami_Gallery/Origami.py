import webbrowser
import os
import sys
from os import listdir
from os.path import isfile, join
from yattag import Doc
from random import seed
from random import randint
seed(2)


def date_mask(date_raw, language):
    months = {'pt': ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                     'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro',
                      'Dezembro'),
              'en': ('January', 'February', 'March', 'April', 'May','June',
                     'July', 'August', 'September', 'October', 'November',
                     'December')}

    date = date_raw.split('-')
    month = months[language][int(date[1])-1]

    if language == 'pt':
        return f'{date[2]} de {month} de {date[0]}'
    else:
        return  f'{month} {date[2]}, {date[0]}'

def get_images():
    path = os.getcwd()+'\photos'

    name_list = (name for name in listdir(path) if isfile(join(path, name)))

    return name_list

def head(doc, tag, text):
    css = 'assets/css/main.css'
    js = 'assets/JavaScript/Script.js'
    page = 'Gallery'

    with tag('head'):
        doc.stag('meta', charset = 'utf-8', name = 'viewport', content = 'width=device-width, initial-scale=1.0')
        with tag('title'):
            text(page)
        doc.stag('link', rel = 'stylesheet', href = f'{css}')
        doc.stag('link', rel = 'stylesheet', href = 'https://fonts.googleapis.com/css2?family=Indie+Flower&display=swap')
        doc.stag('link', rel = 'stylesheet', href = 'https://fonts.googleapis.com/icon?family=Material+Icons')
        with tag('script'):
            doc.attr(src = 'https://code.jquery.com/jquery-1.9.1.js')
        with tag('script'):
            doc.attr(src = js)
        with tag('script'):
            doc.attr(src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js')

def header(doc, tag, text):
    with tag('div', klass = 'header'):
        text()
def about(doc, tag, text):
    with tag('div', klass = 'post-it'):

        with tag('p', klass = 'text-info pt'):
            text('O origami muitas vezes é a forma que uso para me distrair, principalmente '
            	 'quando tenho que encarar uma situação muito estressante, como as provas na '
            	 'faculdade. Além de me ajudar a distrair e extrair minha criatividade e talvez '
            	 'meu lado artístico, fazer origamis me ajuda a aumentar minha concentração e '
            	 'explorar novos materiais. Várias das composições criadas são compostas de '
            	 'materiais que junto ao longo do tempo, materiais simples, como fios de diversos '
            	 'materiais, rolha e garrafas de bebidas, e outros materiais não tão comuns, como '
            	 'tronco de bambu que havia sido podada do jardim de casa.')

        with tag('p', klass = 'text-info en'):
            text('O origami muitas vezes é a forma que uso para me distrair, principalmente '
            	 'quando tenho que encarar uma situação muito estressante, como as provas na '
            	 'faculdade. Além de me ajudar a distrair e extrair minha criatividade e talvez '
            	 'meu lado artístico, fazer origamis me ajuda a aumentar minha concentração e '
            	 'explorar novos materiais. Várias das composições criadas são compostas de '
            	 'materiais que junto ao longo do tempo, materiais simples, como fios de diversos '
            	 'materiais, rolha e garrafas de bebidas, e outros materiais não tão comuns, como '
            	 'tronco de bambu que havia sido podada do jardim de casa.')

        with tag('div', klass = 'instagram'):
            with tag('a', href='https://www.instagram.com/origami.mana/', klass='btn', target='_blank'):
                doc.stag('img', src = 'imagens/instagram-esbocado.svg', id = 'instagram-icon')

def photos(doc, tag, text):
    positions = {0:['left', '-10%'], 1:['right', '-75%']}
    index = 0
    for photo in get_images():
        info = photo.strip('.jpg').split('_')

        with tag('div', klass='position'):
            with tag('div', klass='sticker', style=f'right:{positions[index][1]}'):
                doc.stag('img', src = f'imagens/star_sticker.svg', style='width: 100%;')
            with tag('div', klass='photo_frame', style=f'float:{positions[index][0]}; rotate(0deg);'):
                index = 1 if index == 0 else 0
                doc.stag('img', src = f'photos/{photo}', klass = 'photo')
                with tag('p', klass = f'img_date pt {info[1]}'):
                    text(f'{date_mask(info[0], "pt")} - Coleção de {info[1]}')
                with tag('p', klass = 'img_date en'):
                    text(f'{date_mask(info[0], "en")} - {info[1]}\' Collection')

doc, tag, text = Doc().tagtext()
doc.asis('<!DOCTYPE html>')
with tag('html'):
        head(doc, tag, text)
        with tag('body'):
            header(doc, tag, text)
            about(doc, tag, text)
            with tag('section', klass = 'content_gallery'):
                photos(doc, tag, text)












f = open('index.html','w',encoding='utf8')
webbrowser.open_new_tab('index.html')
f.write(doc.getvalue())
f.close()
