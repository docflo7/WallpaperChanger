from os import listdir
from os.path import join, isfile, splitext
import io


def processWalls(folderpath, folder):
    global walls
    content = listdir(folderpath)
    for file in content:
        path = join(folderpath, file)
        if isfile(path):
            name, ext = splitext(path)
            if ext in acceptedExtensions:
                walls += [path]
        elif file not in ignoredFolders and folder not in maxDeepFolders:
            processWalls(path, file)


root = "D:\Pictures\Mangas-Animés"  # TODO: softcode
walls = []
maxDeepFolders = ['Kantoku', 'Pokemon', 'Kill la Kill', 'Love Live School Idol Project']  # Subfolders within these ones will be ignored
ignoredFolders = ['zJaquettes', 'zDualScreen', 'zOther', 'zPhone', '__seasons__', 'Transparents', 'osu',
                  'BRS Scans', 'The Idolm@ster - Civil War']  # Folders to ignore
acceptedExtensions = ['.jpg', '.png', '.jpeg']  

processWalls(root, '')
filecount = len(walls)
print('{} Wallpapers'.format(filecount))
print('--------')

list = io.open('pathlist.txt', mode="w", encoding="utf-8")
list.write(str(filecount) + '\n')
for path in walls:
    list.write(path + '\n')

list.close()
