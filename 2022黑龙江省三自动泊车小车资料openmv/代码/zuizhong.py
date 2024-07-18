THRESHOLD = (0, 25, -21, 12, -23, 21) # Grayscale threshold for dark things...
from pyb import Servo
import sensor, image, time,ustruct
#import car
from pyb import Pin, Timer
import time
inverse_left=False  #change it to True to inverse left wheel
inverse_right=False #change it to True to inverse right wheel
s1 = Servo(3) # servo on position 1 (P7)
s1.angle(48)

ain1 =  Pin('P0', Pin.OUT_PP)
ain2 =  Pin('P1', Pin.OUT_PP)

ain1.low()
ain2.low()


pwma = Pin('P6')
tim = Timer(2, freq=1000)
ch1 = tim.channel(1, Timer.PWM, pin=pwma)
ch1.pulse_width_percent(0)

def run(left_speed):
    if inverse_left==True:
        left_speed=(-left_speed)

    if left_speed < 0:
        ain1.low()
        ain2.high()
    else:
        ain1.high()
        ain2.low()
    ch1.pulse_width_percent(int(abs(left_speed)))


sensor.reset()
#sensor.set_vflip(True)
#sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA) # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
#sensor.set_windowing([0,20,80,40])
sensor.skip_frames(time = 2000)     # WARNING: If you use QQVGA it may take seconds
clock = time.clock()                # to process a frame sometimes.


#识别区域
roi1 =     [(0, 17, 15, 25),        #  左  x y w h
            (65,17,15,25),# 右
            (30,0,20,15),#上
            (32,22,13,13)]#中

while(True):
    #s1 = Servo(3) # servo on position 1 (P7)
    #s1.angle(78) # move to 45 degrees
    #time.sleep_ms(500)
    #s1.angle(48) # move to 45 degrees
    #time.sleep_ms(500)
    #s1.angle(20) # move to 45 degrees
    #time.sleep_ms(500)
    #print('yyrttu')
    clock.tick()
    img = sensor.snapshot().binary([THRESHOLD])
    left_flag,right_flag,up_flag,mid_flag=(0,0,0,0)
    for rec in roi1:
        img.draw_rectangle(rec, color=(255,0,0))#绘制出roi区域
    if img.find_blobs([(96, 100, -13, 5, -11, 18)],roi=roi1[0]):  #left
        print('left')
        left_flag=1
    if img.find_blobs([(96, 100, -13, 5, -11, 18)],roi=roi1[1]):  #right
        print('right')
        right_flag=1
    if img.find_blobs([(96, 100, -13, 5, -11, 18)],roi=roi1[2]):  #right
        print('up')
        up_flag=1
    if img.find_blobs([(96, 100, -13, 5, -11, 18)],roi=roi1[3]):  #mid
        print('mid')
        mid_flag=1
    #if img.find_blobs([(96, 100, -13, 5, -11, 18)],roi=roi1[2]):  #up
        #up_flag=1
        #print('up')
    if left_flag==1 and right_flag==1 and up_flag==1 and mid_flag==1:#打死
        print('daodian,dasi')
        run(45)
        time.sleep_ms(400)
        s1.angle(78) # move to 45 degrees
        #time.sleep_ms(500)
        print('daodian,dasi111')
        run(47)
        time.sleep_ms(500)
        time.sleep_ms(500)
        continue
    if left_flag==1 and right_flag==1 and mid_flag==1:#前进
        #outuart(0,0,2)
        print('qianjin')
        s1.angle(48) # move to 45 degrees
        run(-40)
        continue
    if right_flag==1 and up_flag== and mid_flag==1:#车垂直车库了
        #outuart(0,0,3)
        print('chuizhi')
        run(0)
        s1.angle(48) # move to 45 degrees
        #time.sleep_ms(500)
        run(40)
        continue
    if left_flag==1 and up_flag==1 and mid_flag==1:#停止
        run(0)
        print('stop')
        continue



