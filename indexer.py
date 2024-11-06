import os
import ctypes
import shutil
from os.path import isfile, exists

def deleteAndCreateIndexFolder():
    if exists("Home.md"):
        os.remove("Home.md")
    if exists(".index"):
        shutil.rmtree(".index", True)
    os.makedirs(".index")
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ctypes.windll.kernel32.SetFileAttributesW(".index", FILE_ATTRIBUTE_HIDDEN)

def createIndexFileForFolder(folderName):
    """Creates a markdown file that indexes the current folder"""

    # gets all the folders and files in the current directory
    files = []
    folders = []
    filesAndFolders = os.listdir(folderName)
    for x in filesAndFolders:
        if isfile(x):
            if x.endswith(".md"):
                files.append(x.split(".")[0])
        else:
            folders.append(x)

    # the root folder gets special treatment
    folderName = folderName.lower() if folderName != "." else "home"

    # for the current folder, build a string with the markdown contents
    markdownFileContent = buildMarkdownString(folderName, files)

    # create the markdown file and append its contents
    with open(folderName + ".md", "x") as markdownFile:
        markdownFile.write(markdownFileContent)

    print (markdownFileContent)

def buildMarkdownString(folderName, files):
    """For the current folder, build a string with the markdown contents"""

    fileMarkdownContent = "# " + folderName + "\n"
    for file in files:
        fileName = file.replace(".md", "")
        fileMarkdownContent += "\n* [" + fileName + "](" + fileName + ".md)"
        
    return fileMarkdownContent

deleteAndCreateIndexFolder()
createIndexFileForFolder(".")