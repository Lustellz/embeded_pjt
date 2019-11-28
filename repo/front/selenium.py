from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.options import Options

from django.http import HttpResponse, JsonResponse,QueryDict
from .models import Student
from .security import AESCipher

class Selenium():

    def __init__(self, s_id, password):
        self.s_id = s_id
        self.password = password

    def pk_action(self, action_type, pk):
        try:
            options = Options()
            options.add_argument('--start-fullscreen')

            browser = webdriver.Chrome(chrome_options=options)
            browser.get('http://edu.ssafy.com')
            # ID
            browser.find_element_by_id('userId').send_keys(self.s_id)
            # PWD
            browser.find_element_by_id('userPwd').send_keys(self.password)
            # 로그인 클릭
            browser.find_element_by_class_name('form-btn').click()
            # 출석 클릭
            if action_type == "enter":
                state = browser.find_element_by_class_name('state').click()
                browser.close()
                return JsonResponse({
                    'result': 'Student entered.',
                    'pk' : pk
                }, status=201)
            else:
                state2 = browser.find_element_by_class_name('state2').click()
                browser.close()
                return JsonResponse({
                        'result': 'Student exited.',
                        'pk' : pk
                    }, status=201)

        except:
            browser.close()
            return JsonResponse({
                        'result': 'Wrong student information.',
                        'pk' : pk
                    }, status=400)
    
