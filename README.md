# scanlating-gimp
Gimp plugins to aid in scanlation processes. The tools will be in: Filters > Scanlating > \*

## Installation
Either copy the files in the "plugin" folder into your GIMP plug-ins folder or map the "plugins" folder in GIMP. To find the plugins folder or map to the repo's folder, open GIMP, then go to: Edit > Preference. Under "Folders", click on "Plug-ins" to find/add the locations GIMP will search for plugins. After copying/mapping, you may need to restart GIMP for the tools to show up.

## Plugins
### Download Text from Danbooru
Downloads the notes from a Danbooru page and positions them on the current image. It will likely work with other \*boorus (tested on Gelbooru once), but the code will be maintained for Danbooru.

### Download Pool from Danbooru
Downloads all of the images from a pool, saves them in a specified folder, and applies the text (using the same method as `Download Text from Danbooru`). Files will be saved with the number they appear by in the pool. Unlike `Download Text from Danbooru`, this will only work with Danbooru pools. XCF files with the text will be saved and loaded after the tool completes. Currently, it will download any file extension, but only JPEG, PNG, and GIF files will be loaded with notes attached.

### Add Text Halo to Halo Layer
Adds a halo to the currently-selected layer using the current background color. It will search for a layer named "halo" (case sensitive), and it will create one in the third position from the bottom if one does not exist.

## Other Resources
### Resynthesizer
Suite for "texture transfer". Incredibly useful for removing text on difficult background. You'll probably still need to do some cleanup, but having the machine do 90% of your work is a no brainer: https://github.com/bootchk/resynthesizer
