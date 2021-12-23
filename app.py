# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 11:58:34 2021

@author: hunojung

chatterbot 설치 에러 발생시 1.0.4로 설치하면 됨
pip install chatterbot
pip install chatterbot==1.0.4

chatbot 테이블에 들어갈 내용
-----
REQUEST / RULE / RESPONSE
미세먼지	미세먼지|알려	미세먼지
너의 이름은?	너|이름	저는 천재 챗봇 천봇이라고 합니다
네 이름을 말해줘	네|이름|말해	저는 천재 챗봇 천봇이라고 합니다
네 이름이 뭐니?	네|이름|뭐	저는 천재 챗봇 천봇이라고 합니다
놀러가고 싶다	놀러|싶	가끔씩 휴식하는 것도 좋죠
느그 아부지 뭐하시노	느그|아부지|뭐하	우리 아부지 건달입니다
말귀좀 알아듣는다?	말귀|알아듣는다	다행이네요. 열심히 배우고 있어요
맛저해	맛저해	맛저하세요~
맛점해	맛점해	맛점하세요~
메리크리스마스	메리|크리	메리~ 크리스마스~
면접에서 떨어졌어	면접|떨어	다음엔 꼭 붙을 수 있을거에요
무슨 말인지 모르겠어	무슨|말|모르	죄송해요 학습이 덜 됐나봐요
뭐해?	뭐해	그냥 있어요
아 월요일이 다가온다	월요일|다가	월요병이 심한가봐요
안녕	안녕	안녕하세요
영화 추천해줘	영화|추천	아이언맨 시리즈와 어벤져스 시리즈를 보세요
1조 멤버 알려줘	1조|멤버|알려	1조원은 강재균,이성찬,정훈오,김기환 입니다
ㅋㅋㅋ	ㅋㅋㅋ	ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ
맛집 알려줘	맛집|알려	맛집
날씨	날씨|알려	날씨
-----
"""
### 모듈 import ###
from flask import Flask, render_template, request
from django.shortcuts import render
from folium.folium import Map
from pandas import Series, DataFrame

import pandas as pd
import cx_Oracle
import os
import flask
### 모듈 import END ###


### 직접 만들어놓은 모듈 불러오기 ###

# 전국 음식점 리스트 맵 만들기
import module.restaurant as rstr
import module.weather as wd

### 만들어놓은 모듈 불러오기 END ###


### DB 연결 - 데이터 끌어오기 ###
LOCATION = r"C:\instantclient_21_3"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"] #환경변수 등록

connection = cx_Oracle.connect("scott", "tiger", "127.0.0.1:1521/xe")
cursor = connection.cursor()

chat_dic = {} # rule 저장 dict

cursor.execute("SELECT * FROM chatbot")

chatbot_data = DataFrame(cursor,columns=['request','rule','response'])
# chatbot_data = pd.read_excel("./data/chatbot_data.xlsx")
row = 0
for rule in chatbot_data['rule']:
    chat_dic[row] = rule.split('|')
    row += 1
### DB 연결 - 데이터 끌어오기 ###


### chatbor 대답 ###
def chat(request):
    for k, v in chat_dic.items():
        chat_flag = False
        for word in v:
            if word in request:
                chat_flag = True
            else:
                chat_flag = False
                break
            
        if chat_flag:
            
            res = chatbot_data['response'][k]
            kinds = ''
            # rule : 서울|맛집 / response : 서울 맛집 입니다.
            if ( '맛집' in res ) :
                res = rstr.getList(request)
                if( '제대로' not in res):            
                    kinds = 'restaurant'
            
            elif( '날씨' in res ) :
                res = wd.for_all_clawer(request)
                if( '제대로' not in res):
                    kinds = 'weather'
            
            elif( '미세먼지' in res ):
                res = wd.all_dust(request)
                if( '제대로' not in res):
                    kinds = 'dust'
            
            return res, kinds
        
    return '무슨 말인지 모르겠어요', ''
### chatbot 대답 END ###


### app 실행 시작 및 html 실행, 채팅 get하여 대답 return ###
app = Flask(__name__)
 
@app.route("/")
def home():
    print("home")
    return render_template("index.html")
 
@app.route("/get")
def get_bot_response():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    userText = request.args.get('msg')
    ans , kinds= chat(userText)
    return ans+'|'+kinds

@app.route("/restaurant")
def restaurant():
    return flask.send_file("./templates/restaurant.html")

@app.route("/weather")
def weather():
    return render_template("weather.html")
    
@app.route("/dust")
def dust():
    return render_template("dust.html")

if __name__ == "__main__":
    app.run(port=9005)
### app END ###