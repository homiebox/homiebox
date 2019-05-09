import os
import time

old = len(listdir('/home/pi/captures'))
inter = len(listdir('/home/pi/Desktop'))
new = len(listdir('/home/pi/captures'))

new = 0
i = 0

print(old)
print(inter)
print(new)
# while(i<10):
#    new =len(os.listdir('/home/pi/captures'))
#    if new > old:
#        old = new
#        print("Un mouvement a ete detecte")
#        time.sleep(30)
#        i= i+1
