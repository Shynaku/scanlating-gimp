#! /usr/bin/env python2
'''This plugin adds a halo to the selected text layer.
By default, it will add this to a layer named "halo" or create one if it does not already exist.
Uses the current background color for the fill color.'''

from gimpfu import *


def create_text_halo(image, drawable, buffer_size):
    pdb.gimp_image_undo_group_start(image)
    pdb.gimp_selection_clear(image)
    pdb.gimp_image_select_item(image, CHANNEL_OP_ADD, drawable)
    pdb.gimp_selection_grow(image, buffer_size)
    # Find or create layer named "halo"
    for halo_layer in image.layers:
        if halo_layer.name == 'halo':
            break
    else:
        halo_layer = pdb.gimp_layer_new(image,
                                image.width, image.height,
                                RGBA_IMAGE,
                                'halo',
                                100,
                                LAYER_MODE_NORMAL_LEGACY)
        # Assumes the last layer is the original, then one layer above for removing text, redraws, etc.
        index = len(image.layers) - 2
        if index < 0:
            index = 0
        image.add_layer(halo_layer, index)
    pdb.gimp_edit_fill(halo_layer, FILL_BACKGROUND)
    pdb.gimp_selection_clear(image)
    pdb.gimp_image_undo_group_end(image)


register(
    'gimpfu-add-text-halo-to-halo-layer',
    'Add Text Halo to Halo Layer',
    'Adds a halo to the selected text layer to a layer named "halo".',
    'Shynaku', 'Shynaku', '2022',
    'Add Text Halo to Halo Layer',
    '*',
    [
        (PF_IMAGE, 'image', 'takes current image', None),
        (PF_DRAWABLE, 'drawable', 'takes current selected layer', None),
        (PF_SPINNER, 'size', 'Buffer size', 2, (1, 3000, 1))
    ],
    [],
    create_text_halo,
    menu='<Image>/Filters/Scanlating'
)

main()