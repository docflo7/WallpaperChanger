import random
import ctypes
import io, os, sys
from datetime import datetime

os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
random.seed()
i = 0
list = io.open('pathlist.txt', mode="r", encoding="utf-8")
filecount = int(list.readline())

rd = random.randint(1, filecount)
print(rd)
for line in list:
    i += 1
    if i > rd:
        break

output = io.open('used.txt', mode="r", encoding="utf-8")
outlist = []
for wall in output:
    outlist.append(wall)
output.close()

outlist.reverse()
output = io.open('used.txt', mode="w", encoding="utf-8")

SPI_SETDESKWALLPAPER = 20
ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, line[:-1], 0)
output.write(datetime.now().isoformat(' ') + ' ' + line)

for i in range(9):
    try:
        pop = outlist.pop()
    except:
        break
    output.write(pop)


