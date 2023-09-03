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
        elif whitelistFolders:
            if file in whitelistFolders:
                processWalls(path, file)
            elif folder in whitelistFolders and folder not in maxDeepFolders:
                processWalls(path, file)
        elif file not in ignoredFolders and folder not in maxDeepFolders:
            processWalls(path, file)


root = "D:\Pictures\Mangas-Animés"  # TODO: softcode
walls = []
maxDeepFolders = ['Pokemon', 'Evangelion', 'Kill la Kill', 'Love Live School Idol Project', 'The Idolm@ster']  # Subfolders within these ones will be ignored
ignoredFolders = ['zJaquettes', 'zDualScreen', 'zOther', 'zPhone', '__seasons__', 'Transparents', 'osu',
                  'BRS Scans', 'The Idolm@ster - Civil War']  # Folders to ignore
whitelistFolders = ['Azur Lane', 'Arknights', 'Bocchi The Rock', 'Date a Live', 'Fate Series', 'Girls Frontline', 'Genshin Impact', 
                    'Gotoubun no Hanayome', 'Honkai Impact', 'KanColle', 'Legion', 'Love Live Sunshine', 'Love Live! Nijigasaki Gakuen',  
                    'PlayStation', 'Pokemon', 'Seishun Buta Yarou', 'Summertime Rendering', 'Sword Art Online', 'The Idolm@ster', 
                    'Tensei Shitara Slime Datta Ken', 'Touhou', 'Tower of Fantasy', 'Vehicles', 'VTuber', 'Warship Girls']  # If set, only these folders will be processed
                    
whitelistFolders = ['_Artist_', 'Arknights', 'Azur Lane', 'Blue Archive', 'Bocchi The Rock', 'Evangelion', 'Fate Kaleid', 'Fate Series', 'Figure Story', 'Genshin Impact', 'Girls Frontline', 
'Gotoubun no Hanayome', 'Honkai Impact', 'Honkai Star Rail', 'KanColle', 'Legion', 'Love Live Sunshine', 'Love Live! Nijigasaki Gakuen', 'Lycoris Recoil', 'Oshi no Ko', 
'PlayStation', 'Pokemon', 'Project Sekai', 'Seishun Buta Yarou', 'Summertime Rendering', 'Sword Art Online', 'Tate no Yuusha no Nariagari', 'Tensei Shitara Slime Datta Ken', 'Tenten Kakumei', 
'The Idolm@ster', 'Touhou', 'Tower of Fantasy', 'Vehicles', 'VTuber', 'Warship Girls']

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
