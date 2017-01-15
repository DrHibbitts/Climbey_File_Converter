import json
import OBJ_Reader
import os, glob
import multiprocessing
from functools import partial

def OutputName(inFile):
    return inFile.rsplit('.', 1)[0] + ".txt"

def SaveLevel(level, outFile):
    with open(outFile, 'wb') as f:
        json.dump(level.toJSON(), f, indent=4, separators=(',', ': '))
    return True

def ConvertFile(inFile, isVerbose):
    print "Converting: {}".format(inFile)
    outFile = OutputName(inFile)
    extension = inFile.rsplit('.', 1)[-1]
    level = None
    if extension.lower() == "obj":
        print "OBJ File found"
        level = OBJ_Reader.OBJToLevel(inFile, isVerbose)

    if level is None:
        return False

    if isVerbose: json.dumps(level.toJSON(), indent=4, separators=(',', ': '))
    return SaveLevel(level, outFile)

def ConvertFolder(folderPath, doRecurse, doParallel, isVerbose):
    if doParallel:
        parpool = multiprocessing.Pool()
        map_func = lambda x, y: parpool.map(x, y)
    else:
        map_func = lambda x, y: map(x, y)

    if doRecurse:
        files = []
        for root, dirnames, filenames in os.walk(folderPath):
            files += map(lambda x: os.path.join(root, x), filenames)
    else:
        files = glob.glob(folderPath + "/*.*")

    map_func(partial(ConvertFile, isVerbose=isVerbose), files)

    if doParallel:
        parpool.close()

def Main():
    inFile = "Example Levels/Bare_minimum/Bare_minimum.obj"
    outFile = inFile.rsplit('.', 1)[0] + ".txt"
    print ConvertFile(inFile, outFile)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="Verbose mode. Whether to print additional processing details.",
                        action="store_true",
                        default=False)
    parser.add_argument("--parallel",
                        help="Parallel mode. Whether to use multiprocessing for handling multiple files.",
                        action="store_true",
                        default=False)
    parser.add_argument("-f", "--file",
                        help="File mode. It will convert a specified file",
                        type=str,
                        default="")
    parser.add_argument("-r", "--recursive",
                        help="Recursive mode. Directory mode will now walk through sub folders. Has no effect if in File mode",
                        action="store_true",
                        default=False)
    parser.add_argument("-p", "--path",
                        help="A valid path. A directory path by default or a filepath in File mode. Defaults to the script folder",
                        default=os.path.dirname(os.path.realpath(__file__)),
                        required=False)
    args = parser.parse_args()
    assert os.path.exists(args.path)
    if args.file:
        print "File Mode:\n"
        ConvertFile(args.path, args.verbose)
    else:
        ConvertFolder(args.path, args.recursive, args.parallel,args.verbose)
