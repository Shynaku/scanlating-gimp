# scanlating-gimp
Gimp plugins to aid in scanlation processes

## Plugins
### Download Text from Danbooru
Downloads the notes from a Danbooru page and positions them on the current image. It will likely work with other \*boorus (tested on Gelbooru once), but the code will be maintained for Danbooru.

### Add Text Halo to Halo Layer
Adds a halo to the currently-selected layer using the current background color. It will search for a layer named "halo" (case sensitive), and it will create one in the third position from the bottom if one does not exist. (Warning: if it makes a new layer that ends up being above the selected layer, it will throw an error. I'm too lazy right now to add error handling for it.)
