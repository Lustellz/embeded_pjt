from kivy.core.window import Window
Window.size = (800, 480)

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger
from kivy.factory import Factory
import urllib
import time
import cv2

def recog(self):
    camera = self.ids['camera']
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    id = 0
    # img = cv2.flip('capture/temp.png', 1) # Flip vertically
    # img = camera.export_as_image()
    img = cv2.imread('capture/temp.png')
    img = cv2.flip(img, 1) # Flip vertically
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imwrite('capture/gray.jpg', gray)
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(0.1*360), int(0.1*600)),
       )
    Logger.info(faces)
    if len(faces):
        x, y, w, h = faces[0]
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        cv2.imwrite("capture/temp.jpg", gray[y:y+h,x:x+w])
        if (confidence < 100):
            return id
        else:
            return -2
    else:
        return -1

def newUser(self, pk):
    Logger.info(self)
    pass

class FirstScreen(Screen):
    def capture(self):
        names = ['진민재', 'EJ', 'MJ', 'HongJ', 'ProFe','JM','SM','YS','HJ','SiUn','j']
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        # camera.export_to_png("./capture/IMG_{}.png".format(timestr))
        camera.export_to_png("./capture/temp.png")
        Logger.info('captured')

        result = recog(self)
        Logger.info(result)
        if result >= 0:
            CheckPopup.id = result
            CheckPopup.title = '"' + str(names[result]) + '"님 본인이십니까?'
            Factory.CheckPopup().open()
        elif result == -1:
            Factory.FailPopup().open()
        elif result == -2:
            Factory.ManualPopup().open()

    def signUp(self, pk):
        Factory.SignPopup().open()
        Logger.info(pk)
        newUser(self, pk)

# class SecondScreen(Screen):
#     def leav(self):
#         params = '{"key":"value"}'
#         headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
#         req = UrlRequest('http://192.168.100.70:8000/students/2/', on_success=self.leavSuccess, method='POST')
    
#     def leavSuccess(req, result):
#         Logger.info('leav success')

class TheScreenManager(ScreenManager):
    pass

class CheckPopup(Popup):
    title = ''
    id = -1
    
    def yes(self):
        params = urllib.parse.urlencode({'pk': id})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        req = UrlRequest('http://192.168.100.70:8000/students/enter/', method='POST', req_body=params, req_headers=headers)
        self.dismiss()

    def no(self):
        Factory.ManualPopup().open()
        self.dismiss()
class ManualPopup(Popup):
    def confirm(self, id, password):
        params = urllib.parse.urlencode({'s_id': id, 'password':password})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        req = UrlRequest('http://192.168.100.70:8000/students/manual/enter/', method='POST', req_body=params, req_headers=headers)
        self.dismiss()

class SignPopup(Popup):
    def signUp(self, name, id, password, password2):
        if password == password2:
            params = urllib.parse.urlencode({'name': name, 's_id': id, 'password': password})
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            req = UrlRequest('http://192.168.100.70:8000/students/', on_success=self.success, method='POST', req_body=params, req_headers=headers)
        else:
            Factory.PasswordPopup().open()
            self.dismiss()
    
    def success(self, req, result):
        FirstScreen.signUp(self, result['pk'])
        self.dismisss()

root_widget = Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import Factory kivy.factory.Factory

TheScreenManager:
    transition: FadeTransition()
    FirstScreen:

<FirstScreen>:
    name: 'first'
    BoxLayout:
        Camera:
            id: camera
            pos: root.x, 200
            size: 600, 360
            resolution: 600, 360
            play: True
        BoxLayout:
            padding: 10
            size_hint: 0.5, 1
            size: 400, 480
            spacing: 10
            orientation: 'vertical'
            Button:
                text: '입실'
                font_size: 30
                font_name: './NanumBarunGothic.ttf'
                background_normal: ''
                background_color: 51/255.0,150/255.0,244/255.0,0.96
                on_release:
                    root.capture()
            Button:
                text: '퇴실'
                font_size: 30
                font_name: './NanumBarunGothic.ttf'
                background_normal: ''
                background_color: 51/255.0,150/255.0,244/255.0,0.96
                on_release:
                    Factory.CheckPopup().open()
            Button:
                text: '회원 등록'
                font_size: 30
                font_name: './NanumBarunGothic.ttf'
                background_normal: ''
                background_color: 230/255.0,206/255.0,73/255.0,0.9
                on_release:
                    root.signUp()

<SecondScreen>:
    name: 'second'
    GridLayout:
        cols: 2
        spacing: '8dp'
        row_force_default: True
        row_default_height: 40
        col_force_default: True
        col_default_width: 200

        Label:
            text: 'ID'
        TextInput:
            multiline: False
            text: ''
        Label:
            text: 'PASSWORD'
        TextInput:
            text: ''
            password: True
        Button:
            text: '로그인'
            font_size: 30
            font_name: './NanumBarunGothic.ttf'
            background_normal: ''
            background_color: 51/255.0,150/255.0,244/255.0,0.96
            on_release:
                root.leav()
                
        Button:
            text: '취소'
            font_size: 30
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

<SignPopup@Popup>:
    title: '정보를 입력해주세요'
    title_size: 28
    title_font: './NanumBarunGothic.ttf'
    size_hint: 0.5, 0.7
    auto_dismiss: False
    BoxLayout:
        padding: 10
        spacing: 10
        orientation: 'vertical'
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
        Button:
            text: '등록'
            font_size: 24
            font_name: './NanumBarunGothic.ttf'
            background_normal: ''
            background_color: 51/255.0,150/255.0,244/255.0,0.96
            on_release: 
                root.signUp(input_name.text, input_id.text, input_password.text, input_password2.text)

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
''')

# sm = ScreenManager()
# sm.add_widget(FirstScreen(name='first'))
# sm.add_widget(SecondScreen(name='second'))

class TestApp(App):
    def build(self):
        return root_widget

if __name__ == '__main__':
    TestApp().run()