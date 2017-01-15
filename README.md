**Climbey File Converter**

A generic converter for transfering 3D model files to Climbey's Custom Level format. Currently supports OBJ with Basic Blocks only. Future work will allow other formats (FBX, etc.) and give access to non-basic blocks such as moving platforms and ziplines.

**Requirements**

* Python 2.7
* Numpy (Currently investigating the feasability of removing this dependency)

**Usage in 3D program**

When creating your level with your 3D program of choice you should currently only use cuboids, further shapes will be added as time goes one. These cuboids should have their Material set such that the material name matches one of Climbey's basic block types, you can find a full list of the currently supported types can be found at the top of Blocks.py with the global variable STATIC_BLOCKS. As of the time of writing the list is: ['Icy', 'Spikes', 'Metal', 'Glass', 'Lava', 'Grabbable', 'Spikes', 'Jumpy', 'GravityField', '[CameraRig]', 'Finishline']

If you have multiple instances of a material and it gives names like Metal.001, Metal.002, etc. this is fine as only the base name is used for comparison.

**Script Usage**

The script should be run from Main.py and takes various command line options. To see a full list of options run "python Main.py --help" in your terminal. 

For example, to recursively walk directories from the script location and convert them all in parallel you would do "python Main.py -r --parallel"

**Examples**

Three example levels and their original blender files are in the "Example Levels" folder
* Bare_minimum.obj - The minimum needed objects to make the level playable in climbey
* Base_custom_level.obj - A level with one of every kind of block in it
* Example_level - An example of a very simple level

**Thanks**

This work is based off qwanzaden's original OBJ convert which you can find here: https://github.com/qwanzaden/OBJ-to-Climbey-txt-converter
