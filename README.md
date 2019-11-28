# Embeded

<!-- ABOUT THE PROJECT -->
## About The Project

Face recognition attendance system
등록된 회원의 얼굴을 구별하여 입, 퇴실을 할 수 있도록 하는 프로그램입니다.

사용할 수 있는 주소 목록은 다음과 같습니다.

### 요청 방식: GET
- /students/ : 등록된 전체 학생의 목록 조회
- /students/pk : pk에 해당하는 학생의 데이터 조회

### 요청 방식: POST
- /students/ : 새로운 학생 등록
- /sutdents/enter : 요청 받은 pk에 해당하는 학생 입실 후 pk 반환
- /students/exit : 요청 받은 pk에 해당하는 학생 퇴실 후 pk 반환
- /students/manual/enter : 요청 받은 정보로 입실 후 해당 학생 pk 반환
- /students/manual/exit : 요청 받은 정보로 퇴실 후 해당 학생 pk 반환

<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repo
```sh
git clone https://lab.ssafy.com/mjjin1214/embeded.git
```
2. Install NPM packages
```sh
npm install
```
3. Install Kivy

    https://kivy.org/doc/stable/gettingstarted/installation.html

### Run

1. Front-end
```sh
cd front
npm run serve
```
2. API Serve

    본 프로젝트는 django 웹 프레임워크를 사용하였기 때문에 python이 기본적으로 설치되어 있는 환경을 필요로 한다.
    
    2-1. repo 디렉토리로 이동하여 cli에서 가상환경을 설치한다. (python3는 `pip3` 명령어 사용)
    windows, unix 공통: `pip install virtualenv`
    
    2-2. 가상환경을 생성한다. 
    
    window, unix 공통: `virtualenv venv`
    
    2-3. 생성된 가상환경을 실행한다.
     window: `call venv/Scripts/activate`
     unix: `source venv/bin/activate` 
    
    (cf. 가상환경에서 벗어날 때: `deactivate`)
    
    2-4. pip를 최신 버전으로 업데이트 하고 django와 rest_framework를 설치한다.
    
    `python -m pip install --upgrade pip`
    
    `pip install django~=2.2.6`
    
    `pip install djangorestframework`
    
    3-1. 기능을 수행할 selenium과 chromedriver_binary, 암호화를 위한 pycryptodome을 설치한다.
    
    `pip install selenium`
    
    `pip install chromedriver_binary`
    
    `pip install pycryptodome`
    `pip install pycryptodomex`
    
    4-1.`python manage.py runserver`로 서버 실행
    
    주소창에 students로 등록된 학생의 목록에 접근할 수 있음

3. RaspberryPi UI(Kivy)
```sh
cd kivyRaspberry
python ui.py
```