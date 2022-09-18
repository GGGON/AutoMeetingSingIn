# author: skywoodsz

import os
import pandas as pd
import pyautogui
import time
from datetime import datetime
import cv2
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED,as_completed

'''
	利用opencv模板匹配进行入会像素坐标获取，执行鼠标相应动作与密码验证存在判断
	@param tempFile: 模板匹配图像
		   whatDo：鼠标执行动作
		   debug： debug
'''
def ImgAutoClick(tempFile,k='',x=''):
    pyautogui.screenshot('screen.png')
    gray = cv2.imread('screen.png', 0)
    #载入截图
    img_templete = cv2.imread(tempFile, 0)
    #print(tempFile)

    y1, x1 = img_templete.shape
    #print('y1,x1', y1, x1)
    # 模板琵琶
    res = cv2.matchTemplate(gray, img_templete, cv2.TM_SQDIFF)
    #  #解析左上角下标
    #  upper_left=cv2.minMaxLoc(res)[2]
    #  #计算右下角下标
    #  upper_right=(upper_left[0]+width,upper_left[1]+height)
    #  #计算中心区域下标
    #  avg=((upper_left[0]+upper_right[0])/2,(upper_left[1]+upper_right[1])/2)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    x = min_loc[0]
    y = min_loc[1]
    #if(tempFile=='CloseMeeting.png'):
    # print('x,y', x, y)
    # print(x + x1 / 2, y + y1 / 2)

    top_left = min_loc

   # pyautogui.moveTo(int(x + x1 / 2), int(y + y1 / 2))
    pyautogui.click(int(x + x1 / 2), int(y + y1 / 2))
   # if(min_val < 1000):
    # print( top + h / 2, left + w / 2)
     #whatDo(top+h/2,left+w/2)
    #else:
    #    return False


    os.remove("screen.png")
    
    return True

'''
	会议自动登录
	@param meeting_id: 会议号
		   password：密码，若则保持默认NULL
'''
def SignIn(meeting_id, password=''):
    os.startfile("D:\腾讯会议\WeMeet\wemeetapp.exe")
    time.sleep(4)

    ImgAutoClick("JoinMeeting.png", pyautogui.click(), False)
    time.sleep(2)

    ImgAutoClick("meeting_id.png", pyautogui.click(), False)
    time.sleep(1)
    print("write")
    pyautogui.write(meeting_id)
    time.sleep(2)
    ImgAutoClick("right.png",pyautogui.click())
    time.sleep(2)
    ImgAutoClick("final.png", False)
    time.sleep(3)
    #print("password")
    res = ImgAutoClick("password.png")

    if res and( password != ''):
        time.sleep(1)
        pyautogui.write(password)
        time.sleep(1)
       # print("passwordJoin")
        ImgAutoClick("passwordJoin.png", pyautogui.click(), False)
        time.sleep(1)



    return True

def CloseMeeeting():
    print("Close!!!")
    ImgAutoClick("CloseMeeting.png")
    time.sleep(2)

    ImgAutoClick("LeaveMeeting.png")


def beginLesson(lesson):

 startTime = datetime.strptime(lesson['startTime'], "%H:%M")-datetime.strptime('0:4', "%H:%M")






 while True:
    now = datetime.now()
    print(startTime)
    hour = now.strftime("%H")
    # print(type(hour))
    Time = now.strftime("%H:%M:%S")
    print(Time)
    Time = datetime.strptime(Time, "%H:%M:%S") - datetime.strptime('0:0', "%H:%M")
    print((Time - startTime).seconds)
    # print((startTime-Time).seconds)
    print((Time - startTime).days)
    if ((Time - startTime).days == -1):  # 现在时间比开始时间小 无效课程
         time.sleep(60)
         continue;
    if((Time - startTime).seconds>10*60):#15*60
         return f"{lesson}过时课程"

    #%W:
   # print(now)
    #现在时间比开始时间大:
    meeting_id = lesson['meetingId'] # meeting id
    password = lesson['password'] # meeting password
    try:
     if ((Time - startTime).seconds<60*6): # sign in time
       #60
        SignIn(meeting_id, password)
        print("Sign In!")
        num=int(lesson['num'])
        lessongap=num-1
        time.sleep(num*40*60+lessongap*10*60+4*60)
        #time.sleep(0.5*60)
        CloseMeeeting()

        return f"OK{lesson}";
    except:
     raise Exception(f"{lesson}出现60s内未执行异常"+now.strftime("%H:%M:%S"))


futures=[]
pool=ThreadPoolExecutor(max_workers=12)
with open('lessons.csv',mode='r',encoding='utf-8') as f:
    Lesson = {
        'weekday': '',
        'startTime': '',
        'num': '',  # 课程节数
        'cycle': '',  # 单双周 1单 2双
        'meetingId': '',
        'password': '',
        'name':''

    }
    print(f.readline())
    for line in f:

       lesson=Lesson
       if(line.strip()==''):
           continue;
       items=line.strip().split(',')
       #筛除不符合本day(1,2,3,4,5)的课程
       if(items[0]!=str(datetime.now().isoweekday())):
           continue;
       #筛除不符合本周的课程(本周是单周or双周)

       if(items[3]=='1'and datetime.now().isocalendar().week%2==0):
           print(f'不符合本周:{items[6]}')
           continue;
       if(items[3] =='2' and datetime.now().isocalendar().week % 2 == 1):
           print(f'不符合本周:{items[6]}')
           continue;

       #print(line.strip())
       lesson['weekday']=items[0]
       lesson['startTime']=items[1]
       lesson['num']=items[2]
       lesson['cycle']=items[3]
       lesson['meetingId']=items[4]
       lesson['password']=items[5]
       lesson['name']=items[6]
       futures.append(pool.submit(beginLesson,lesson))
wait(futures,return_when=ALL_COMPLETED)
i=0
for res in as_completed(futures):
    i=i+1
    print(i)
    print(res.result())
print("ALL OVER")