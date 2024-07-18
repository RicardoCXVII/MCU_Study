THRESHOLD = (5, 70, -23, 15, -57, 0) # Grayscale threshold for dark things...
import sensor, image, time, pyb
from pyb import Servo
#import car
from pyb import Pin, Timer
import time
inverse_left=False  #change it to True to inverse left wheel
inverse_right=False #change it to True to inverse right wheel
s1 = Servo(3) # servo on position 1 (P7)
s1.angle(42)

ain1 =  Pin('P0', Pin.OUT_PP)
ain2 =  Pin('P1', Pin.OUT_PP)
beep =  Pin('P2', Pin.OUT_PP)

ain1.low()
ain2.low()
beep.low()
beep.high()#开机蜂鸣器响一下
time.sleep_ms(500)
time.sleep_ms(500)
beep.low()

t1=260#前行
t2=700#打死后退
t3=300#进库后退

t4=100#出库前进
t5=700#出库打死
t6=360#前行

v1=-50



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
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
#sensor.set_windowing([0,20,80,40])
sensor.skip_frames(time = 2000)     # WARNING: If you use QQVGA it may take seconds
clock = time.clock()                # to process a frame sometimes.
ROI_L=(0,30,30,60)##左边界 侧方
ROI_R=(130,30,160,60)##右边界 侧方

ROI_L_2=(30,30,30,60)##左边界 倒车
ROI_R_2=(100,30,30,60)##右边界 倒车


ROI_F=(30,0,100,30)##前边界
ROI_B=(30,90,100,30)##后边界
ROI_C=(50,20,60,60)##车库中间
ROI_All=(0,0,160,120)
white_threshold=(54, 78, -11, 20, -12, -1)
daoche_flag,cefang_flag=(0,0)
while(True):
    clock.tick()
    #img = sensor.snapshot()
    img = sensor.snapshot().lens_corr(strength = 1.9, zoom = 1.0)
    l_1 = img.find_lines(x_stride = 1,y_stride=1 ,merge_distance=5000, max_theta_difference=30,roi=ROI_L)
    img.draw_rectangle(ROI_L[0],ROI_L[1],ROI_L[2],ROI_L[3],color=(255,0,0), thickness=1,fill=False)
    r_1 = img.find_lines(x_stride = 1,y_stride=1 ,merge_distance=5000, max_theta_difference=30,roi=ROI_R)
    img.draw_rectangle(ROI_R[0],ROI_R[1],ROI_R[2],ROI_R[3],color=(255,0,0), thickness=1,fill=False)


    l_2 = img.find_lines(x_stride = 1,y_stride=1 ,merge_distance=5000, max_theta_difference=30,roi=ROI_L_2)
    img.draw_rectangle(ROI_L_2[0],ROI_L_2[1],ROI_L_2[2],ROI_L_2[3],color=(0,255,0), thickness=1,fill=False)
    r_2 = img.find_lines(x_stride = 1,y_stride=1 ,merge_distance=5000, max_theta_difference=30,roi=ROI_R_2)
    img.draw_rectangle(ROI_R_2[0],ROI_R_2[1],ROI_R_2[2],ROI_R_2[3],color=(0,255,0), thickness=1,fill=False)


    #b = img.find_lines(merge_distance=5000, max_theta_difference=30,roi=ROI_B)
    #img.draw_rectangle(ROI_B[0],ROI_B[1],ROI_B[2],ROI_B[3],color=(255,0,0), thickness=1,fill=False)
    f = img.find_lines(x_stride = 2,y_stride=2 ,merge_distance=5000, max_theta_difference=30,roi=ROI_F)
    img.draw_rectangle(ROI_F[0],ROI_F[1],ROI_F[2],ROI_F[3],color=(255,0,0), thickness=1,fill=False)
    img.draw_rectangle(ROI_C[0],ROI_C[1],ROI_C[2],ROI_C[3],color=(255,0,0), thickness=1,fill=False)

    #单条边界线判断#
    if (l_1):
        img.draw_line((l_1[0][0],l_1[0][1],l_1[0][2],l_1[0][3]), color = (255, 0, 0))
    if (r_1):
        img.draw_line((r_1[0][0],r_1[0][1],r_1[0][2],r_1[0][3]), color = (255, 0, 0))
    if (l_2):
        img.draw_line((l_2[0][0],l_2[0][1],l_2[0][2],l_2[0][3]), color = (0, 255, 0))
    if (r_2):
        img.draw_line((r_2[0][0],r_2[0][1],r_2[0][2],r_2[0][3]), color = (0, 255, 0))
    #if (b):
        #img.draw_line((b[0][0],b[0][1],b[0][2],b[0][3]), color = (255, 0, 0))
    if (f):
        img.draw_line((f[0][0],f[0][1],f[0][2],f[0][3]), color = (255, 0, 0))
        if(80<f[0][6] and f[0][6] <110):
            print(f[0][6]) ## 返回 角度 PID控制角度为90
    #单条边界线判断#


    #车库判断
    if(l_1 and r_1 and f):##倒车
        car = img.find_blobs([white_threshold],roi = ROI_C,x_stride = 55 ,y_stride =55 ,merge = False)
        if(car):
            #print((l_1[0][0]+l_1[0][1])/2+(r_1[0][0]+r_1[0][1])/2) ##坐标
            daoche_flag=1;
            img.draw_rectangle((car[0][0],car[0][1],car[0][2],car[0][3]),color=(255,255,0), thickness=1,fill=False)
    if(l_2 and r_2 and f):##侧方
        car = img.find_blobs([white_threshold],roi = ROI_C,x_stride = 55 ,y_stride =55 ,merge = False)
        if(car):
            #print((l_2[0][0]+l_2[0][1])/2+(r_2[0][0]+r_2[0][1])/2) ##坐标
            cefang_flag=1;
            img.draw_rectangle((car[0][0],car[0][1],car[0][2],car[0][3]),color=(255,255,0), thickness=1,fill=False)
    if(daoche_flag==0 and cefang_flag==0):#无空车位置
        run(-50)
        if (f):
            if (f[0][6])>=90:
                print('>90')
                s1.angle(42+2*(f[0][6]-90))
                time.sleep_ms(5)
            else:
                print('<90')
                s1.angle(42-2*(90-f[0][6]))
                time.sleep_ms(5)
    if(daoche_flag==1):#发现倒车入库空位
        run(v1)
        print('1')
        time.sleep_ms(t1)#前行一会
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        run(0)
        s1.angle(98)#打死
        print('2')
        run(-v1)
        time.sleep_ms(t2)#向后倒一会
        time.sleep_ms(t2)
        time.sleep_ms(t2)
        s1.angle(42)#回正
        print('3')
        time.sleep_ms(t3)#再向后倒一会
        time.sleep_ms(t3)
        time.sleep_ms(t3)
        run(0)#停止
        print('4')
        #beep.high()#停车蜂鸣器响一下
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        #beep.low()
        run(v1)#向前走
        print('5')
        time.sleep_ms(t4)#向前走一会
        time.sleep_ms(t4)
        time.sleep_ms(t4)
        run(0)
        s1.angle(68)#打死
        print('6')
        run(v1)
        time.sleep_ms(t5)#再向前走一会
        time.sleep_ms(t5)
        time.sleep_ms(t5)
        s1.angle(42)#回正
        print('7')
        time.sleep_ms(t6)#再向前走一会
        time.sleep_ms(t6)
        time.sleep_ms(t6)
        run(0)
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        daoche_flag==0








    #print(clock.fps())
