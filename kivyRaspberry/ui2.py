from kivy.core.window import Window
Window.size = (800, 480)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.camera import Camera
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger
from kivy.factory import Factory

from PIL import Image as Image2
from security import AESCipher

import urllib
import time
import cv2
import os
import numpy as np

backend = '13.125.220.148:8000'
root_widget = BoxLayout()
sm = ScreenManager(size_hint=(0.5, 1))
cap = cv2.VideoCapture(0)
cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

def train():
    path = 'dataset'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image2.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = faceCascade.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    
    recognizer.train(faceSamples, np.array(ids))
    recognizer.write('trainer/trainer.yml')

class CheckPopup(Popup):
    title = ''
    id = -1
    
    def yes(self):
        params = urllib.parse.urlencode({'pk': CheckPopup.id})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        if FirstScreen.inout:
            req = UrlRequest('http://'+backend+'/students/exit/', on_success=self.success, method='POST', req_body=params, req_headers=headers)
        else:
            req = UrlRequest('http://'+backend+'/students/enter/', on_success=self.success, method='POST', req_body=params, req_headers=headers)
        img = cv2.imread('./capture/temp.jpg')
        timestr = time.strftime("%Y%m%d_%H%M%S")
        cv2.imwrite("dataset/User." + str(id) + '.' + timestr + ".jpg", img)
        self.dismiss()

    def no(self):
        Factory.ManualPopup().open()
        self.dismiss()

    def success(self, req, result):
        Factory.SignSuccessPopup().open()

class ManualPopup(Popup):
    def confirm(self, id, password):
        params = urllib.parse.urlencode({'s_id': id, 'password':password})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        if FirstScreen.inout:
            req = UrlRequest('http://'+backend+'/students/manual/exit/', on_success=self.success, on_failure=self.failure, method='POST', req_body=params, req_headers=headers)
        else:
            req = UrlRequest('http://'+backend+'/students/manual/enter/', on_success=self.success, on_failure=self.failure, method='POST', req_body=params, req_headers=headers)
        self.dismiss()

    def success(self, req, result):
        pk = result['pk']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        cv2.imwrite("dataset/User." + str(pk) + '.' + timestr + ".jpg", img)
        Factory.SignSuccessPopup().open()
    
    def failure(self, req, result):
        Factory.ManualFailPopup().open()

Builder.load_string('''
#:import Factory kivy.factory.Factory

<FirstScreen>:
    name: 'first'
    BoxLayout:
        padding: 10
        spacing: 10
        orientation: 'vertical'
        Button:
            text: '입실'
            font_size: 30
            font_name: './NanumBarunGothic.ttf'
            background_normal: ''
            background_color: 51/255.0,150/255.0,244/255.0,0.96
            on_release:
                root.capture(0)
        Button:
            text: '퇴실'
            font_size: 30
            font_name: './NanumBarunGothic.ttf'
            background_normal: ''
            background_color: 51/255.0,150/255.0,244/255.0,0.96
            on_release:
                root.capture(1)
        Button:
            text: '회원 등록'
            font_size: 30
            font_name: './NanumBarunGothic.ttf'
            background_normal: ''
            background_color: 230/255.0,206/255.0,73/255.0,0.9
            on_release:
                root.manager.current = 'second'

<SecondScreen>:
    name: 'second'
    BoxLayout:
        size: 200, 400
        padding: 10
        spacing: 10
        orientation: 'vertical'
        Label:
            id: sentence
            text: '정보 입력 후 등록 버튼을 누르면 사진 촬영이 시작됩니다!'
            text_size: root.width-10, None
            font_name: './NanumBarunGothic.ttf'
            font_size: 30
            size_hint: 1, 2
        TextInput:
            id: input_name
            text: ''
            multiline: False
            font_size: 20
            font_name: './NanumBarunGothic.ttf'
            hint_text: "Name"
        TextInput:
            id: input_id
            text: ''
            multiline: False
            font_size: 20
            hint_text: "ID"
        TextInput:
            id: input_password
            text: ''
            password: True
            font_size: 20
            hint_text: "PASSWORD"
        TextInput:
            id: input_password2
            text: ''
            password: True
            font_size: 20
            hint_text: "CONFIRM PASSWORD"
        BoxLayout:
            Button:
                text: '등록'
                font_size: 24
                font_name: './NanumBarunGothic.ttf'
                background_normal: ''
                background_color: 51/255.0,150/255.0,244/255.0,0.96
                on_release: 
                    root.signUp(input_name.text, input_id.text, input_password.text, input_password2.text)
            Button:
                text: '취소'
                font_size: 24
                font_name: './NanumBarunGothic.ttf'
                on_release: 
                    root.manager.current = 'first'

<CheckPopup@Popup>:
    title: root.title
    title_size: 28
    title_font: './NanumBarunGothic.ttf'
    size_hint: 0.5, 0.5
    auto_dismiss: False
    BoxLayout:
        padding: 10
        spacing: 10
        Button:
            text: '예'
            font_size: 24
            font_name: './NanumBarunGothic.ttf'
            background_normal: ''
            background_color: 51/255.0,150/255.0,244/255.0,0.96
            on_release: root.yes()
        Button:
            text: '아니오'
            font_size: 24
            font_name: './NanumBarunGothic.ttf'
            on_release: root.no()

<ManualPopup@Popup>:
    title: 'Id/Password 입력해주세요.'
    title_size: 28
    title_font: './NanumBarunGothic.ttf'
    size_hint: 0.5, 0.5
    auto_dismiss: False
    BoxLayout:
        padding: 10
        spacing: 10
        orientation: 'vertical'
        TextInput:
            id: input_id
            text: ''
            multiline: False
            font_size: 20
            hint_text: "ID"
        TextInput:
            id: input_password
            text: ''
            password: True
            font_size: 20
            hint_text: "PASSWORD"
        Button:
            text: '확인'
            font_size: 24
            font_name: './NanumBarunGothic.ttf'
            background_normal: ''
            background_color: 51/255.0,150/255.0,244/255.0,0.96
            on_release: root.confirm(input_id.text, input_password.text)

<FailPopup@Popup>:
    title: '다시 촬영해주세요.'
    title_size: 28
    title_font: './NanumBarunGothic.ttf'
    size_hint: 0.5, 0.3
    Button:
        text: '닫기'
        font_size: 24
        font_name: './NanumBarunGothic.ttf'
        background_normal: ''
        background_color: 51/255.0,150/255.0,244/255.0,0.96
        on_release: root.dismiss()
    
<PasswordPopup@Popup>:
    title: '비밀번호가 부정확합니다.'
    title_size: 28
    title_font: './NanumBarunGothic.ttf'
    size_hint: 0.5, 0.3
    Button:
        text: '닫기'
        font_size: 24
        font_name: './NanumBarunGothic.ttf'
        background_normal: ''
        background_color: 51/255.0,150/255.0,244/255.0,0.96
        on_release:
            root.dismiss()

<ManualFailPopup@Popup>:
    title: 'Id/Passwrod 부정확합니다.'
    title_size: 28
    title_font: './NanumBarunGothic.ttf'
    size_hint: 0.5, 0.3
    Button:
        text: '닫기'
        font_size: 24
        font_name: './NanumBarunGothic.ttf'
        background_normal: ''
        background_color: 51/255.0,150/255.0,244/255.0,0.96
        on_release: root.dismiss()

<SignupFailPopup@Popup>:
    title: '이미 존재하는 Id입니다.'
    title_size: 28
    title_font: './NanumBarunGothic.ttf'
    size_hint: 0.5, 0.3
    Button:
        text: '닫기'
        font_size: 24
        font_name: './NanumBarunGothic.ttf'
        background_normal: ''
        background_color: 51/255.0,150/255.0,244/255.0,0.96
        on_release: root.dismiss()

<SignSuccessPopup@Popup>:
    title: '정상적으로 처리 되었습니다.'
    title_size: 28
    title_font: './NanumBarunGothic.ttf'
    size_hint: 0.5, 0.3
    Button:
        text: '닫기'
        font_size: 24
        font_name: './NanumBarunGothic.ttf'
        background_normal: ''
        background_color: 51/255.0,150/255.0,244/255.0,0.96
        on_release: root.dismiss()

''')

class FirstScreen(Screen):
    def capture(self, inout):
        FirstScreen.inout = inout
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        ret, img =cap.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        if len(faces):
            x, y, w, h = faces[0]
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            cv2.imwrite("capture/temp.jpg", gray[y:y+h,x:x+w])
            if (confidence < 100):
                CheckPopup.id = id
                req = UrlRequest('http://'+backend+'/students/'+str(id)+'/', self.success)
            else:
                Factory.ManualPopup().open()
        else:
            Factory.FailPopup().open()
    
    def success(self, req, result):
        CheckPopup.title = '"' + result['name'] + '"님 본인이십니까?'
        Factory.CheckPopup().open()

class SecondScreen(Screen):
    label = '정보 입력 후 등록 버튼을 누르면 사진 촬영이 시작됩니다.'
    def signUp(self, name, id, password, password2):
        if password == password2:
            password = AESCipher(id).encrypt(password)
            params = urllib.parse.urlencode({'name': name, 's_id': id, 'password': password})
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            req = UrlRequest('http://'+backend+'/students/', on_success=self.success, on_failure=self.failure, method='POST', req_body=params, req_headers=headers)
        else:
            Factory.PasswordPopup().open()
    
    def success(self, req, result):
        t = 0
        pk = result['pk']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        while(t < 30):
            ret, img = cap.read()
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            for (x,y,w,h) in faces:
                t += 1
                cv2.imwrite("dataset/User." + str(pk) + '.' + timestr + str(t) + ".jpg", gray[y:y+h,x:x+w])
        
        train()
        sm.current = 'first'

    def failure(self, req, result):
        Factory.SignupFailPopup().open()

class TheScreenManager(ScreenManager):
    pass

class TestApp(App):

    def build(self):
        global root_widget, sm
        self.img1=Image()
        layout = BoxLayout()
        layout.add_widget(self.img1)
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        layout.add_widget(sm)
        cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/33.0)
        root_widget.add_widget(layout)
        return root_widget

    def update(self, dt):
        global cap
        ret, frame = cap.read()
        cv2.imshow("CV2 Image", frame)
        buf1 = cv2.flip(frame, -1)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img1.texture = texture1

if __name__ == '__main__':
    TestApp().run()
    cv2.destroyAllWindows()