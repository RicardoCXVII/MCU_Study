from pyb import Pin, Timer
from pyb import Servo
import time
inverse_left=False  #change it to True to inverse left wheel
inverse_right=False #change it to True to inverse right wheel

ain1 =  Pin('P0', Pin.OUT_PP)
ain2 =  Pin('P1', Pin.OUT_PP)
beep =  Pin('P2', Pin.OUT_PP)

ain1.low()
ain2.low()
s1 = Servo(3)
s1.angle(35)#回正
t1=250#前行
t2=550#打死后退
t3=0#后退
t4=370#反向打死后退

t5=570#反向打死出库
t6=360#回正前进
t7=300#打死前进
t8=200#前进+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

v1=-50

beep.low()
#beep.high()#开机蜂鸣器响一下
time.sleep_ms(500)
time.sleep_ms(500)
beep.low()


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


while True:
    if(1):
        #入库
        run(v1)
        print('1')
        time.sleep_ms(t1)#前行一会1
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        run(0)
        s1.angle(55)#先打死2
        print('2')
        run(-v1)
        time.sleep_ms(t2)#向后倒一会
        time.sleep_ms(t2)
        time.sleep_ms(t2)
        s1.angle(35)#回正3
        print('3')
        time.sleep_ms(t3)#再向后倒一会
        time.sleep_ms(t3)
        time.sleep_ms(t3)
        run(0)
        s1.angle(20)#反向打死4
        print('4')
        run(-v1)
        time.sleep_ms(t4)#向后倒一会
        time.sleep_ms(t4)
        time.sleep_ms(t4)
        run(0)#停止5
        print('5')
        #beep.high()#停车蜂鸣器响一下
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        beep.low()
        #
        #出库
        run(v1)#向前走6
        print('6')
        time.sleep_ms(t5)#向前走一会
        time.sleep_ms(t5)
        time.sleep_ms(t5)
        s1.angle(35)#回正7
        print('7')
        time.sleep_ms(t6)#再向前走一会
        time.sleep_ms(t6)
        time.sleep_ms(t6)
        run(0)
        s1.angle(60)#打死8
        print('8')
        run(v1)
        time.sleep_ms(t7)#再向前走一会
        time.sleep_ms(t7)
        time.sleep_ms(t7)
        s1.angle(35)#回正9
        print('9')
        time.sleep_ms(t8)#再向前走一会
        time.sleep_ms(t8)
        time.sleep_ms(t8)
        run(0)
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        time.sleep_ms(t1)
        time.sleep_ms(t1)

