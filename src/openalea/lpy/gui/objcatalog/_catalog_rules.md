# Rules to store obj files

I'll just write some rules to store the files
- files are stored as obj, mtl, jpg, png.
- each model is stored in a folder
- each folder holds all files related to a model
- the name is `file.obj`, `file.mtl`, `any_file_name.jpg` (referenced in `file.mtl`)

This folder should be transfered to the install folder (probably with setup.py)

Then we'll make a Python library that you can import, that will do this:

- read the folder content
- list all files availables
- load files on-demand (avoid loading all files at import)

3D files are previewed on [https://3dviewer.net/](https://3dviewer.net/) just to verify *how they should* be displayed.