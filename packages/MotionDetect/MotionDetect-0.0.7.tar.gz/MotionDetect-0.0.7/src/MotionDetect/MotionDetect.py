# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 10:12:21 2021

@author: Administrator
"""

# pip install opencv-python

import cv2
import datetime
from WxToolsLujx import WxToolsLujx



class MotionDetect(object):
    def __init__(self, open_id = 'o47YY6x7s3tFyvbH0rpq-zAQXbAM',msg='hi,有人闯入你的家!!!!' ):  
        self.open_id = open_id
        self.msg = msg
        #ss = WxTools(msg='hi,breakoFF!',open_id='o47YY63sZ9FOFFRt3LSvc3iMf1eY')
        self.ss = WxToolsLujx.WxToolsLujx(msg=self.msg , open_id=self.open_id )


    def Detect(self):

        s = self.ss
        bg = None
        es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,4))
        is_send_msg = False

        camera = cv2.VideoCapture(0+ cv2.CAP_DSHOW)
        while True:
            ret , frame = camera.read()

            gray_f = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            gray_f = cv2.GaussianBlur(gray_f,(25,25),3)

            if bg is None :
                bg = gray_f
                continue

            diff = cv2.absdiff(bg,gray_f)
            diff = cv2.threshold(diff,50,255,cv2.THRESH_BINARY)[1]
            diff = cv2.dilate(diff,es,iterations = 3 )

            contours , hierarchy = cv2.findContours(diff.copy(),cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_SIMPLE)
            is_detected = False
            for c in contours:
                if cv2.contourArea(c) < 2000:
                    continue
                (x,y,w,h)=cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                is_detected = True
                if not is_send_msg :
                    is_send_msg = True
                    s.sendMsg()

                    

            if is_detected :
                show_text = "Motion :  Detected"
                show_color = (0,0,255)
            else:
                show_text = "Motion :  UnDetected"
                show_color = (0,255,0)        


            
            
            cv2.putText(frame,show_text,(10,20),
                        cv2.FONT_HERSHEY_SIMPLEX,0.5,show_color ,2)
            cv2.putText(frame,datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10,frame.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,255,0),1)
            
            cv2.imshow( 'video',frame )
            #cv2.imshow( 'diff', diff )
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        camera.release()
        cv2.destroyAllWindows()
        
        

if __name__ == '__main__':
    ss = MotionDetect(msg='hi,breakoff!',open_id='o47YY6x7s3tFyvbH0rpq-zAQXbAM')
    ss.Detect()

