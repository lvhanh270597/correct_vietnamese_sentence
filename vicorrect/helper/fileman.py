import os
import shutil

def createPath(fpath):
    if not os.path.exists(fpath):
        try:
            os.makedirs(fpath)
            print("Created path '%s' successfully!" % fpath)
            return True
        except Exception as Error:
            print(Error)
            return False
    return True

def createFile(fpath):
    try:
        parentDir = os.path.dirname(fpath)
        createPath(parentDir)
        open(fpath, 'a').close()
    except Exception as Error:
        print(Error)
        return False
    return True

def searchReplace(fpath, rep, newfpath):
    try:
        text = open(fpath).read()
    except Exception as Error:
        print(Error)
        return False
    try:
        for _from, _to in rep.items():
            text = text.replace(_from, _to)    
        parentDir = os.path.dirname(newfpath)
        if not createPath(parentDir):
            return False
    except Exception as Error:
        print(Error)
        return False
    try:
        fdata = open(newfpath, "w")
        fdata.write(text)
    except Exception as Error:
        fdata.close()
        print(Error)
        return False
    return False

def removeFile(filePath):
    try:
        os.remove(filePath)
    except Exception as Error:
        print(Error)
        return False
    return True

def removePath(fpath):
    try:
        shutil.rmtree(fpath)
    except Exception as Error:
        print(Error)
        return False
    return True
