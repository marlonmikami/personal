import os
import ctypes
import shutil
from os.path import isfile, exists

ignoreList = [".git", ".index", "assets", "indexer.py"]

def deleteAndCreateIndexFolder():
    if exists("Home.md"):
        os.remove("Home.md")
    if exists(".index"):
        shutil.rmtree(".index", True)
    os.makedirs(".index")
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ctypes.windll.kernel32.SetFileAttributesW(".index", FILE_ATTRIBUTE_HIDDEN)



def createIndexFileForFolder(folderName, folderPath):
    """Creates a markdown file that indexes the current folder"""

    # gets all the relevant folders and the markdown files in the current directory
    filesList = []
    foldersList = []
    filesAndFolders = os.listdir(folderName)
    for x in filesAndFolders:
        name = x
        path = folderPath + "/" + name
        if (x not in ignoreList):
            if isfile(folderName + "/" + x):
                filesList.append([name,path])
            else:
                foldersList.append([name, path])

    # the root folder gets special treatment
    folderName = folderName if (folderName != ".") else "home"

    # create the content that goes into the markdown file
    markdownFileContent = "# " + folderName + "\n"
    markdownFileContent += createMarkdownList(foldersList, True)
    markdownFileContent += createMarkdownList(filesList, False)

    # for each folder in the current folder, call this function
    for folder in foldersList:
        createIndexFileForFolder(folder[0], folder[1])

    # create the markdown file and append its contents
    with open(".index/" + folderName + ".md", "x") as markdownFile:
        markdownFile.write(markdownFileContent)

    #print (markdownFileContent)



def createMarkdownList(list, isFolderList):
    """Get a list of files or folder and builds a string with a markdown list"""
    fileMarkdownContent = ""
    for item in list:
        itemName = item[0].replace(".md", "")
        itemPath = item[1]
        if isFolderList:
            itemPath = itemPath.replace("./","./.index/") + ".md"
        fileMarkdownContent += "\n* [" + itemName + "](" + itemPath + ")"
        
    return fileMarkdownContent



deleteAndCreateIndexFolder()
createIndexFileForFolder(".", "..")