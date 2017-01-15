import json
import OBJ_Reader

def SaveLevel(level, outFile):
    with open(outFile, 'wb') as f:
        json.dump(level.toJSON(), f, indent=4, separators=(',', ': '))
    return True

def ConvertFile(inFile, outFile):
    extension = inFile.rsplit('.', 1)[-1]
    level = None
    if extension.lower() == "obj":
        print "OBJ File found"
        level = OBJ_Reader.OBJToLevel(inFile)

    if level is None:
        return False

    print json.dumps(level.toJSON(), indent=4, separators=(',', ': '))
    return SaveLevel(level, outFile)

def Main():
    inFile = "Example Levels/Bare_minimum/Bare_minimum.obj"
    outFile = inFile.rsplit('.', 1)[0] + ".txt"
    print ConvertFile(inFile, outFile)

if __name__ == '__main__':
    Main()