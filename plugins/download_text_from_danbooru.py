#! /usr/bin/env python2
'''Downloads the text from notes on Danbooru and adds them to the image. Default values are based on what I use.'''

from gimpfu import *
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from download_utils import download_text_from_danbooru, DEFAULT_TEXT_FONT, DEFAULT_TEXT_SIZE


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