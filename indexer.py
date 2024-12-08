import os
import ctypes
import shutil
from os.path import isfile, exists

# files and folders to be ignored when indexing
ignoreList = ["index", "assets", "archive", "README.md", "indexer.py"]

def deleteAndCreateIndexFolder():
    if exists("Home.md"):
        os.remove("Home.md")
    if exists("index"):
        shutil.rmtree("index", True)
    os.makedirs("index")
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ctypes.windll.kernel32.SetFileAttributesW("index", FILE_ATTRIBUTE_HIDDEN)

def createIndexFileForFolder(folderName, folderPath, isRootFolder):
    """Creates a markdown file that indexes the current folder"""

    # gets all the relevant folders and the markdown files in the current directory
    filesList = []
    foldersList = []
    filesAndFolders = os.listdir(folderName)
    for x in filesAndFolders:
        name = x
        path = folderPath + "/" + name
        if (name not in ignoreList) and (not name.startswith(".")) and (not name.startswith("_")):
            if isfile(folderName + "/" + x):
                filesList.append([name,path])
            else:
                foldersList.append([name, path])

    # create the content that goes into the markdown file
    markdownFileContent = "# " + (folderName if (not isRootFolder) else "home") + "\n"
    markdownFileContent += createMarkdownList(foldersList, True, isRootFolder)
    markdownFileContent += createMarkdownList(filesList, False, isRootFolder)

    # for each folder in the current folder, call this function
    for folder in foldersList:
        createIndexFileForFolder(folder[0], folder[1], False)

    # create the markdown file and append its contents
    indexFilePath = "./index/" + folderName + ".md";
    if isRootFolder:
        indexFilePath = "./home.md"
    with open(indexFilePath, "x") as markdownFile:
        markdownFile.write(markdownFileContent)

    #print (markdownFileContent)



def createMarkdownList(list, isFolderList, isRootFolder):
    """Get a list of files or folder and builds a string with a markdown list"""
    fileMarkdownContent = ""
    for item in list:
        itemName = item[0].replace(".md", "")
        itemPath = item[1]
        if (not isRootFolder):
            itemPath = "." + itemPath
        if isFolderList:
            itemPath = itemPath.replace("./","./index/") + ".md"
        fileMarkdownContent += "\n* [" + itemName + "](" + itemPath + ")"
        
    return fileMarkdownContent



deleteAndCreateIndexFolder()
createIndexFileForFolder(".", ".", True)