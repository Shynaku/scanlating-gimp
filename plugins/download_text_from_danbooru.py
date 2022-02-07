#! /usr/bin/env python2
'''Downloads the text from notes on Danbooru and adds them to the image. Default values are based on what I use.'''

DEFAULT_TEXT_FONT = 'Wurper Regular,'
DEFAULT_TEXT_SIZE = 28

from gimpfu import *
import requests
import math
import re


class Note(object):
    '''Parser for a Danbooru note.'''

    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        text = self._parse_value('data-body')
        if text == '':
            return "Unable to parse note text!"
        text = text.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<').replace('&quot;', '"').replace('&#39;', "'").replace('&apos;', "'")
        text = re.sub('<[^>]*>', '', text)  # May be too aggressive if there's legitimate instance of this, but fine for now
        text = text.replace(' \n ', '\n').strip()  # Text tends to have spaces before and after, including between spans
        return text

    @property
    def x(self):
        return self._parse_int('data-x', default_value=0)

    @property
    def y(self):
        return self._parse_int('data-y', default_value=0)

    @property
    def height(self):
        return self._parse_int('data-height', default_value=30)

    @property
    def width(self):
        return self._parse_int('data-width', default_value=30)

    def _parse_int(self, property_name, default_value):
        try:
            return int(float(self._parse_value(property_name)))
        except Exception:
            return default_value

    def _parse_value(self, property_name):
        match = property_name + '="'
        index = self._text.find(match)
        if index == -1:
            return ''
        else:
            text = self._text[index + len(match):]
            out = ''
            for i in range(len(text)):
                if text[i] == '"':
                    break
                else:
                    out += text[i]
            return out


class NotesSection(object):
    '''Holds and parses the section of the html code with the notes.
    Could maybe be turned into an iterator function, but I'm keeping it around in case it's useful in the future.'''

    def __init__(self, html_text):
        self.raw = html_text
        self.text = self._parse_section()

    def has_notes(self):
        return bool(self.text)

    def __iter__(self):
        text = self.text
        article_index = text.find('<article')
        while article_index != -1:
            text = text[article_index:]
            end_index = text.find('</article')
            yield Note(text[:end_index])
            text = text[end_index:]
            article_index = text.find('<article')

    def notes(self):
        return list(self)

    def _parse_section(self):
        notes_index = self.raw.find('<section id="notes"')
        if notes_index == -1:
            return ''
        text = self.raw[notes_index:]
        return text[:text.find('</section')]


def download_text_from_danbooru(image, http, font_name, font_size):
    pdb.gimp_image_undo_group_start(image)
    resp = requests.get(http)
    if resp.status_code == 200:
        notes = NotesSection(resp.text)
        for note in notes:
            try:
                lyr = pdb.gimp_text_fontname(
                    image,
                    None,
                    note.x,
                    note.y,
                    note.text,
                    0,
                    True,
                    font_size,
                    PIXELS,
                    font_name
                )
                pdb.gimp_text_layer_set_justification(lyr, 2)
                pdb.gimp_text_layer_resize(lyr, note.width, note.height)
                if font_name == 'Wurper Regular,':
                    spacing = int(math.sqrt(font_size * .75))
                    pdb.gimp_text_layer_set_line_spacing(lyr, -1 * spacing)
            except Exception:
                pass
    pdb.gimp_image_undo_group_end(image)


register(
    'gimpfu-download-text-from-danbooru',
    'Download Text from Danbooru',
    'Downloads the text from a Danbooru page and attempts to add it to the correct location in the current image.',
    'Shynaku', 'Shynaku', '2022',
    'Download Text from Danbooru',
    '*',
    [
        (PF_IMAGE, 'image', 'takes current image', None),
        (PF_STRING, 'string', 'Link to Danbooru page', None),
        (PF_FONT, 'font', 'Font Name', DEFAULT_TEXT_FONT),
        (PF_SPINNER, 'size', 'Font Size', DEFAULT_TEXT_SIZE, (1, 3000, 1)),
    ],
    [],
    download_text_from_danbooru,
    menu='<Image>/Filters/Scanlating'
)

main()