from pyb import Servo
import time

while(1):
    s1 = Servo(3) # servo on position 1 (P7)
    s1.angle(35) # move to 45 degrees
    time.sleep_ms(500)
    s1.angle(35) # move to 45 degrees
    time.sleep_ms(500)
    s1.angle(35) # move to 45 degrees
    time.sleep_ms(500)
    print('yyrttu')
#s1.angle(-60, 1500) # move to -60 degrees in 1500ms

