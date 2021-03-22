from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from bs4 import BeautifulSoup
import json, time, ssl
import urllib.parse
import urllib.request


#Window.size = (480, 720)

UI_DEFINE = """
<InfoScreen>:
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: 124/255, 39/255, 18/255, 255/255
            Rectangle:
                size: self.size
                pos: self.pos
        BoxLayout:
            size_hint: (1.0, 0.2)
            orientation: "vertical"
            Label:
                text: "Your Infomation"
                font_size: dp(50)
                markup: True
                size_hint: 1.0, 0.7
            Button:
                text: "확인"
                font_name: "basic.ttf"
                size_hint: 0.7, 0.3
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                background_normal: ""
                background_color: 100/255, 20/255, 0/255, 255/255
                on_release: app.call_unsel()
        BoxLayout:
            orientation: "vertical"
            size_hint: (1.0, 0.8)
            MDLabel:
                id: title
                text: ""
                font_name: "basic.ttf"
                markup: True
                size_hint: 0.9, 0.1
            MDLabel:
                id: result
                text: ""
                font_name: "basic.ttf"
                markup: True
                multiline: True
                size_hint: 0.9, 0.9
                color: 1, 1, 1, 1
                
"""

class InfoScreen(Screen):
    def __init__(self, name):
        super().__init__()
        self.name = name

class Main(MDApp):
    def __init__(self):
        super().__init__()
        self.theme_cls.theme_style = "Dark"
        Builder.load_string(UI_DEFINE)
        self.scrmng = ScreenManager()
        input_ui = InfoScreen("infoscreen")
        self.scrmng.add_widget(input_ui)
        self.scrmng.current = "infoscreen"

    def build(self):
        return self.scrmng

    def call_unsel(self):
        
        #sex: 성별은 M(남성), F(여성) 중 한개 선택
        #lunar: 생년월일이 음력인지 양력인지 구분 0 > 양력, 1 > 음력, 2 >음력의 윤달포함
        
        uri = "https://nh.sinbiun.co.kr/GoodLuck.asp"
        info = {
            "bType": "A104",
            "bSex": "M",
            "bLunar": '0',
            "bYear": "1982",
            "bMonth": '7', "bDay": "8", "bHour": "0"
        }
        '''
        encoded_body = json.dumps(info)

        http = urllib3.PoolManager()
        r = http.request('POST', url,
                 headers={'Content-Type': 'application/x-www-form-urlencoded'},
                 body=encoded_body)
        print(r)
        '''

        details = urllib.parse.urlencode(info)
        details = details.encode('UTF-8')
        
        
        url = urllib.request.Request(uri, details)
        
        url.add_header("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13")
        url.add_header("Content-Type", "application/x-www-form-urlencoded")
        url.add_header("Host", "nh.sinbiun.co.kr")
        url.add_header("Connection", "keep-alive")

        context = ssl._create_unverified_context()
        #response = urllib.request.urlopen(requests, data=data.encode('utf-8'), context=context)
        
        ResponseData = urllib.request.urlopen(url, context=context).read().decode("utf-8")
        soup = BeautifulSoup(ResponseData, 'html.parser')
        value  = soup.find_all('div', class_='result_cont mgt60')
        select = 1
        returnValue = ""
        returnTitle = None
        returnResult = None
        for i in value:
            title = i.find('span', class_='txt_bg_00').get_text()
            cont = i.find('div', class_='cont_txt mgt20').get_text().replace("\r\n", '').replace("\t","")
            if value.index(i) == select:
                if select < 5: 
                    if '고객' in cont: cont = cont.replace("고객", "%%s"%name)
                    returnTitle = title
                    returnResult = cont
                    break
                else:
                    arr = cont.split("\n\n\n\n\n")
                    for j in range(len(arr)):
                        temp = arr[j].replace("\n\n\n", '').split("\n")
                        returnValue += (temp[0]+":"+temp[1])
                        if j < len(arr) - 1: returnValue += ">"
                    returnTitle = title
                    returnResult = returnValue
                    break

        self.scrmng.current_screen.ids.title.text = returnTitle
        self.scrmng.current_screen.ids.result.text = returnResult

if __name__ == "__main__":
    Main().run()
