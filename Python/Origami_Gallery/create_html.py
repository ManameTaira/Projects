import os
from yattag import Doc
from yattag import indent

MONTHS = {'01':'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September',
          '10': 'October', '11': 'November', '12': 'December'}

def get_text_list(file_path):
    with open(file_path, 'r') as f:
        return [paragraph for paragraph in f.read().split('\n')]

def create_head(doc, tag, text):
    """Create the HTML head tag containing path to the source for the css file.

    Args:
        doc (yattag.Doc): An Yattag object containing the html file.
        tag (yattag method): An Yattag method to create the html tags and close itself.
        text (yattag method): An Yattag method to add the volue to the tag created by the method tag.
    """
    sources = {'css': 'assets/css/main.css'}

    with tag('head'):
        doc.stag('meta', charset='utf-8', name='viewport', content='width=device-width, initial-scale=1.0')
        with tag('title'):
            text('Gallery')                                                                                                                             # the page title

        for href in sources.values():
            doc.stag('link', rel='stylesheet', href=href)


def create_menu(tag, text, nav):
    """Creates the html code for the menu.

    Args:
        tag (yattag method): An Yattag method to create the html tags and close itself.
        text (yattag method): An Yattag method to add the volue to the tag created by the method tag.
        nav (dict): A dict containing the section name and the reference to add to the tag as an href.
    """
    with tag('nav', klass='menu'):
        for option, href in nav.items():
            with tag('a', href=href, klass='menu item'):
                text(option)


def create_title(doc, tag, text, title, path_images):
    """Create the section title, like in the About section, add the pin icon and the anchor.

    Args:
        doc (yattag.Doc): An Yattag object containing the html file.
        tag (yattag method): An Yattag method to create the html tags and close itself.
        text (yattag method): An Yattag method to add the volue to the tag created by the method tag.
        title (str): The section name.
        path_images (str): The path to images folder, containing the pin icon.
    """
    with tag('h1'):
        with tag('a', href=f'#{title}', klass='anchor'):
            doc.stag('img', src = f'{path_images}\pin.svg', klass = 'pin')
            text(title)


def write_about(doc, tag, text, about, path_images):
    """Write the text in the about section and add the instagram icon containing the link href.

    Args:
        doc (yattag.Doc): An Yattag object containing the html file.
        tag (yattag method): An Yattag method to create the html tags and close itself.
        text (yattag method): An Yattag method to add the volue to the tag created by the method tag.
        about (list): A list containing the text to writes, each element should be a paragraph.
        path_images (str): The path to images folder, containing the instagram icon.
    """
    with tag('section', klass='home'):
        with tag('p', klass='about'):
            for paragraph in about:
                text(paragraph)
                doc.stag('br')
                doc.stag('br')

        with tag('div', klass = 'instagram'):
            with tag('p', klass='instagram'):
                    text('Mana Tai')
            with tag('a', href='https://www.instagram.com/origami.mana/', target='_blank'):
                doc.stag('img', src = f'{path_images}/instagram.svg', id = 'instagram')


def date_mask(date):
    """Parse the date from YYYY-mm-dd to the format Month dd, YYYY

    Args:
        date (str): A date in the format YYYY-mm-dd

    Returns:
        str: The date in the format Month dd, YYYY
    """
    date = date.split('-')
    return  f'{MONTHS[date[1]]} {date[2]}, {date[0]}'


def photo_labels(filename):
    """Parse the filename in to the label name and the date.

    Args:
        filename (str): The filename in the format YYYY-mm-dd_name_optional.jpg

    Returns:
        tuple: A tuple containing the name to write the label (Name Optional) and the date in the format Month dd, YYYY.
    """
    name = ' '.join(filename.split('_')[1:]).split('.')[0].capitalize()
    date = filename.split('_')[0]

    return name, date_mask(date)


def create_photoframe(doc, tag, text, photo_path, filename):
    """Create the frame to add the photo and the photo label containing the photo name and the date.

    Args:
        doc (yattag.Doc): An Yattag object containing the html file.
        tag (yattag method): An Yattag method to create the html tags and close itself.
        text (yattag method): An Yattag method to add the volue to the tag created by the method tag.
        photo_path (str): The path to photo folder.
        filename (str): The filename to add to the html should be in the format YYYY-mm-dd_name_optional.jpg.
    """
    name, date = photo_labels(filename)

    with tag('div', klass='frame'):
        with tag('div', klass='image'):
            doc.stag('img', src = f'{photo_path}\{filename}', klass = 'photo')
        with tag('h2'):
            text(name)
        with tag('h2', klass='date'):
            text(date.replace('-', '/'))


path = f'{os.getcwd()}'
path_images = 'images'
path_photos = 'photos'

about = get_text_list(f'{path}\data\\about.txt')

doc, tag, text = Doc().tagtext()
doc.asis('<!DOCTYPE html>')
create_head(doc, tag, text)

nav_anchor = {'About': '#'}                                                                                                                             # About sectin has no folder directory
nav_anchor.update({folder.capitalize(): f'#{folder.capitalize()}' for folder in os.listdir(f'{path}\photos')})                                          # add the other sections acording to the folder source name

with tag('html'):
    with tag('body'):
        create_menu(tag, text, nav_anchor)
        for title in nav_anchor:
            with tag('div', id=title):                                                                                                                  # the anchor to the section will refer to the div that contain the section
                create_title(doc, tag, text, title, path_images)

                if title == 'About':
                    write_about(doc, tag, text, about, path_images)                                                                                     # about section just containg the text
                    continue

                with tag('section', klass='columns'):
                    path_photo = f'{path_photos}\{title.lower()}'                                                                                               # add the current section to the path
                    for filename in os.listdir(path_photo):
                        create_photoframe(doc, tag, text, path_photo, filename)


with open('index.html','w',encoding='utf8') as f:
    f.write(indent(doc.getvalue()))                                                                                                                     # add the in indentation to writes the html file
    f.close()
