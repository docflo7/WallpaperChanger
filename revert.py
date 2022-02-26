import ctypes
import io

output = io.open('used.txt', mode="r", encoding="utf-8")
outlist = []
for wall in output:
    outlist.append(wall)
output.close()

outlist.reverse()
outlist.pop()
output = io.open('used.txt', mode="w", encoding="utf-8")
path = outlist.pop()

SPI_SETDESKWALLPAPER = 20
print(path[27:-1])
ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path[27:-1], 0)

output.write(path)
while True:
    try:
        pop = outlist.pop()
    except:
        break
    output.write(pop)
