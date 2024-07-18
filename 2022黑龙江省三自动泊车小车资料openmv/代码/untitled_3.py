THRESHOLD = (5, 70, -23, 15, -57, 0) # Grayscale threshold for dark things...
import sensor, image, time, pyb

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
            print('ddddd')
            img.draw_rectangle((car[0][0],car[0][1],car[0][2],car[0][3]),color=(255,255,0), thickness=1,fill=False)
    if(l_2 and r_2 and f):##侧方
        car = img.find_blobs([white_threshold],roi = ROI_C,x_stride = 55 ,y_stride =55 ,merge = False)
        if(car):
            #print((l_2[0][0]+l_2[0][1])/2+(r_2[0][0]+r_2[0][1])/2) ##坐标
            print('cccccc')
            img.draw_rectangle((car[0][0],car[0][1],car[0][2],car[0][3]),color=(255,255,0), thickness=1,fill=False)

    #print(clock.fps())
