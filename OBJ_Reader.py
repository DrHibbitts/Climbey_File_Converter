from Level import Level
import Blocks
import numpy as np
import Core

def OBJToLevel(inFile, isVerbose=False):
    return ParseOBJ(inFile, isVerbose)


def ParseOBJ(inFile, verbose=False):
    with open(inFile, 'rb') as f:
        objLines = f.readlines()
    material = None
    verts = []
    static_blocks = []
    for line in objLines:
        lineType, data = line.split(" ", 1)
        lineType = lineType.lower()
        if lineType == "usemtl":
            material = str.strip(data).split(".", 1)[0]
            if verbose: print "Using Material: {}".format(material)
        elif lineType == "o":
            if len(verts) == 8:
                if verbose: print "Block Found."
                if material in Blocks.STATIC_BLOCKS:
                    pointList = np.array(verts, dtype=float)
                    size, position, rotation = Core.CalculateBlockProperties(pointList)
                    static_blocks.append(Blocks.Block(material, size, position, rotation, False, False, False))
            if verbose: print "\n----------\n"

            if verbose: print "{} found".format(data)
            verts = []
        elif lineType == "v":
            verts.append(np.array(data.split(), dtype=float))
    if len(verts) == 8:
        if verbose: print "Block Found."
        if material in Blocks.STATIC_BLOCKS:
            pointList = np.array(verts, dtype=float)
            size, position, rotation = Core.CalculateBlockProperties(pointList)
            static_blocks.append(Blocks.Block(material, size, position, rotation, False, False, False))

    return Level(static_blocks, [], Blocks.SettingsBlock(Blocks.Block("LevelSign", [1,1,1], [0,0,0], [0,0,0,1], False, False, False)), [], [])