#! /usr/bin/env python2
'''Downloads the text from notes on Danbooru and adds them to the image. Default values are based on what I use.'''

from gimpfu import *
import requests
import math

class Note(object):
    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        if '<span>' in self._text:
            text = self._text_from_spans()
        else:
            text = self._parse_value('data-body')
        return text.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<').replace('&quot;', '"').replace('&#39;', "'").replace('&apos;', "'")

    @property
    def x(self):
        return self._parse_int('data-x')

    @property
    def y(self):
        return self._parse_int('data-y')

    @property
    def height(self):
        return self._parse_int('data-height', default_value=30)

    @property
    def width(self):
        return self._parse_int('data-width', default_value=30)

    def _parse_int(self, property_name, default_value=0):
        try:
            return int(float(self._parse_value(property_name)))
        except Exception:
            return default_value

    def _text_from_spans(self):
        text = self._text
        spans = []
        span_start = text.find('<span')
        while span_start != -1:
            text = text[span_start:]
            build_text = False
            span_text = ''
            for i in range(len(text)):
                if text[i] == '>':
                    build_text = True
                    continue
                elif build_text:
                    if text[i] == '<':
                        spans.append(span_text.strip())
                        text = text[i:]
                        break
                    else:
                        span_text += text[i]
            span_start = text.find('<span')
        return '\n'.join(spans)

    def _parse_value(self, property_name):
        text = self._text
        value = ''
        match = property_name + '="'
        offset = len(match)
        for i in range(len(text)):
            if text[i:i+offset] == match:
                i += offset
                while text[i] != '"':
                    value += text[i]
                    i += 1
        return value

class NotesSection(object):
    def __init__(self, html_text):
        self.raw = html_text
        self.text = self._parse_section()

    def has_notes(self):
        return self.text is not None

    def notes(self):
        articles = self._parse_article_text([], self.text)
        for article_text in articles:
            yield Note(article_text)

    def _parse_article_text(self, articles, text):
        article = ''
        begin_write = False
        for i in range(len(text)):
            if text[i:i+9] == '<article ':
                begin_write = True
            if begin_write:
                if text[i:i+10] == '</article>':
                    article += '</article>'
                    articles.append(article)
                    return self._parse_article_text(articles, text.replace(article, ''))
                else:
                    article += text[i]
        return articles

    def _parse_section(self):
        notes_index = self.raw.find('<section id="notes"')
        if notes_index == -1:
            return
        text = self.raw[notes_index:]
        section = ''
        for i in range(len(text)):
            if text[i:i+10] == '</section>':
                text += '</section>'
                break
            else:
                section += text[i]
        return section


def download_text_from_danbooru(image, http, font_name, font_size):
    pdb.gimp_image_undo_group_start(image)
    resp = requests.get(http)
    if resp.status_code == 200:
        notes = NotesSection(resp.text)
        if notes.has_notes():
            for note in notes.notes():
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
        (PF_FONT, 'font', 'Font Name', 'Wurper Regular,'),
        (PF_SPINNER, 'size', 'Font Size', 28, (1, 3000, 1)),
    ],
    [],
    download_text_from_danbooru,
    menu='<Image>/Filters/Scanlating'
)

main()