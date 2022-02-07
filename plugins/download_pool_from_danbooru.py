#! /usr/bin/env python2
DEFAULT_TEXT_FONT = 'Wurper Regular,'
DEFAULT_TEXT_SIZE = 28

from gimpfu import *
import requests
import os
import shutil
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from download_utils import download_text_from_danbooru, DEFAULT_TEXT_FONT, DEFAULT_TEXT_SIZE


def find_href_link(html_text, link_text=''):
    href_index = html_text.find('href="')
    if href_index != -1:
        href_text = html_text[href_index + 6:]
        for i in range(len(href_text)):
            if href_text[i] == '"':
                break
            else:
                link_text += href_text[i]
    return link_text


def find_pool_links(url=None, response=None):
    pool_links = []
    if response is None:
        response = requests.get(url)
    if response.status_code == 200:
        text = response.text
        posts_index = text.find('<div class="posts-container')
        if posts_index != -1:
            text = text[posts_index:]
            article_index = text.find('<article')
            while article_index != -1:
                text = text[article_index:]
                link = find_href_link(text, 'https://danbooru.donmai.us')
                if link != 'https://danbooru.donmai.us':
                    pool_links.append(link)
                text = text[1:]
                article_index = text.find('<article')
    return pool_links


def find_page_count(response):
    html = response.text
    pages_div_index = html.find('<div class="paginator ')
    if pages_div_index == -1:
        return 0
    text = html[pages_div_index:]
    count = 1
    page_link_index = text.find('<a class="paginator-page ')
    while page_link_index != -1:
        count += 1
        text = text[page_link_index + 1:]
        page_link_index = text.find('<a class="paginator-page ')
    return count


def download_and_load(link, link_num, folder, font_name, font_size):
    image_path_base = os.path.join(folder, str(link_num).zfill(3))
    response = requests.get(link)
    if response.status_code == 200:
        text = response.text
        image_link_index = text.find('<li id="post-info-size')
        if image_link_index != -1:
            text = text[image_link_index:]
            image_link = find_href_link(text)
            extension = os.path.splitext(image_link)[1].lower()
            stream = requests.get(image_link, stream=True)
            if stream.status_code == 200:
                image_path = image_path_base + extension
                stream.raw.decode_content = True
                with open(image_path, 'wb') as f:
                    shutil.copyfileobj(stream.raw, f)
                if extension in ['.jpg', '.jpeg']:
                    image = pdb.file_jpeg_load(image_path, image_path)
                elif extension == '.png':
                    image = pdb.file_png_load(image_path, image_path)
                elif extension == '.gif':
                    image = pdb.file_gif_load(image_path, image_path)
                else:
                    return
                download_text_from_danbooru(image, link, font_name, font_size)
                xcf_path = image_path_base + '.xcf'
                pdb.gimp_xcf_save(0, image, None, xcf_path, xcf_path)
                return xcf_path


def download_pool_from_danbooru(folder, url, font_name, font_size, open_files):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    url = url.split('?')[0]  # remove queries
    response = requests.get(url)
    files_to_open = []
    if response.status_code == 200:
        page_count = find_page_count(response)
        if page_count:
            links = []
            for i in range(1, page_count + 1):
                if i == 1:
                    links += find_pool_links(response=response)
                else:
                    links += find_pool_links(url='{0}?page={1}'.format(url, i))
            for link_num, link in enumerate(links, start=1):
                xcf_file = download_and_load(link, link_num, folder, font_name, font_size)
                if xcf_file is not None:
                    files_to_open.append(xcf_file)
    if open_files:
        for xcf_file in files_to_open:
            gimp.Display(pdb.gimp_file_load(xcf_file, xcf_file))


register(
    'gimpfu-download-pool-from-danbooru',
    'Download Pool from Danbooru',
    'Downloads all of the images in a Danbooru pool, then applies any available notes to it.',
    'Shynaku', 'Shynaku', '2022',
    'Download Pool from Danbooru',
    '',
    [
        (PF_STRING, 'folder', 'Output folder', None),
        (PF_STRING, 'pool', 'Link to Danbooru pool', None),
        (PF_FONT, 'font', 'Font Name', DEFAULT_TEXT_FONT),
        (PF_SPINNER, 'size', 'Font Size', DEFAULT_TEXT_SIZE, (1, 3000, 1)),
        (PF_BOOL, 'load', 'Load Files after download', True, None)
    ],
    [],
    download_pool_from_danbooru,
    menu='<Image>/Filters/Scanlating'
)

main()