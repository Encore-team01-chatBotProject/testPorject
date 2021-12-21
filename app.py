# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 11:58:34 2021

@author: hunojung

chatterbot 설치 에러 발생시 1.0.4로 설치하면 됨
pip install chatterbot
pip install chatterbot==1.0.4
aa
"""
from flask import Flask, render_template, request
from django.shortcuts import render
from django import template
from folium.folium import Map

from pandas import Series, DataFrame

import cx_Oracle
import os

# 지도 표시를 위한 import
import webbrowser
import folium
import googlemaps
import pandas as pd
import platform

# matplotlib notebook
import matplotlib.pyplot as plt
import warnings
from matplotlib import font_manager, rc
# 지도 표시 import END

LOCATION = r"C:\instantclient_21_3"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"] #환경변수 등록

connection = cx_Oracle.connect("scott", "tiger", "127.0.0.1:1521/xe")
cursor = connection.cursor()

# chatbot 대답 코드
import pandas as pd
chat_dic = {}

cursor.execute("SELECT * FROM chatbot")

chatbot_data = DataFrame(cursor,columns=['request','rule','response'])
# chatbot_data = pd.read_excel("./data/chatbot_data.xlsx")

row = 0
for rule in chatbot_data['rule']:
    chat_dic[row] = rule.split('|')
    row += 1
     
def chat(requests):
    for k, v in chat_dic.items():
        chat_flag = False
        for word in v:
            if '맛집' in requests:
                print('맛집')
                maps=restaurant_list('서울특별시')
                return render(request,'./templates/index.html',{'map' : maps})

            if word in requests:
                chat_flag = True
            else:
                chat_flag = False
                break

                
        if chat_flag:
            
            res = chatbot_data['response'][k]
            # rule : 서울|맛집 / response : 서울 맛집 입니다.
            if (res == '서울 맛집 입니다.') :
                res = restaurant_list("서울특별시")
            
            return res
    return '무슨 말인지 모르겠어요'
# chatbot 대답코드 END

### ---  맛집 리스트 출력 코드 --- ###
def restaurant_list(region):
    # 주피터 에러 메시지 제거
    warnings.filterwarnings(action='ignore')

    # Plot 한글 지원
    plt.rcParams['axes.unicode_minus'] = False
    if platform.system() == 'Darwin':
        rc('font', family='AppleGothic')
    elif platform.system() == 'Windows':
        path = "c:/Windows/Fonts/malgun.ttf"
        font_name = font_manager.FontProperties(fname=path).get_name()
        rc('font', family=font_name)
    elif platform.system() == 'Linux':
        path = "/usr/share/fonts/NanumGothic.ttf"
        font_name = font_manager.FontProperties(fname=path).get_name()
        plt.rc('font', family=font_name)
    else:
        print('Unknown system... sorry~~~~')

    # Google map api key setting 강사님 key 씀
    gmaps_key = "AIzaSyC-ezB2J00Td105d4jqtdi2-JmZKuZ-5lY"
    gmaps = googlemaps.Client(key=gmaps_key)

    ## 음식점 엑셀데이터 다루기 ## 800개 데이터 다운로드 해놓음
    restaurant_df = pd.read_excel("./data/전국_맛집_취합종합본.xlsx", engine = 'openpyxl')
    
    map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
    for n in restaurant_df[restaurant_df['지역']==region].index:
        folium.Marker(
            [restaurant_df['lat'][n],restaurant_df['lng'][n]],
            radius = 10, 
            color='#3186cc',
            fill_color='#3186cc', 
            fill=True,
            tooltip=('<b>- 도시명</b>: ' + restaurant_df['도시명'][n] + '<br />'+
                     '<b>- 상호명</b>: ' + restaurant_df['식당상호'][n])
        ).add_to(map)
    map._repr_html_
    #지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환
    
    return map


    # webbrowser.open_new('restaurant_list.html')

### ---  맛집 리스트 출력 코드 END --- ###


# app 실행 시작 및 html 실행, 채팅 get하여 대답 return
app = Flask(__name__)
 
@app.route("/")
def home():
    print("home")
    return render_template("index.html")
 
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    ans = chat(userText)

    return ans
 
if __name__ == "__main__":
    app.run(port=9005)
# app END