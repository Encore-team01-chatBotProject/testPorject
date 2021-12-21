# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 11:58:34 2021

@author: Playdata

chatterbot 설치시 에러 발생시 1.0.4로 설치하면 됨
pip install chatterbot
pip install chatterbot==1.0.4
123123

"""
from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from pandas import DataFrame as df
import folium
import webbrowser



naver_excel=pd.read_excel('C:/workspace/work_py/mini/testPorject/data/naver_data.xlsx')


def for_one_clawer(keyword):
    html = requests.get('https://search.naver.com/search.naver?query='+keyword)
    soup=bs(html.text,'html.parser')
    data1=soup.find('div',class_='temperature_text').find('strong').text
    data2=soup.find('p',class_='summary').text
    data3=soup.find('dl',class_='summary_list').find('dt',class_='term').text
    data4=soup.find('dl',class_='summary_list').find('dd',class_='desc').text
    if data1 :
        return data1[0:5]+' '+data1[5:]+'<br>'+'   '+data2+'<br>'+'   '+data3+'   '+data4
    else : 
        return '지역을 다시 입력 하세요' 

def for_all_clawer(keyword):
    html = requests.get('https://search.naver.com/search.naver?query='+keyword+'날씨').text
    soup=bs(html,'lxml')
    data5=soup.find('div',class_='map _map_normal').findAll('span')
    data5_text=[title.get_text() for title in data5]
    data5_text2=[]
    for i in range(12):
        data5_text2.append(data5_text[(i*3):((i*3)+3)])

    data1_df=df(data5_text2)

    columns_list = ['지역','날씨','기온']
    data1_fix=pd.DataFrame(data5_text2,columns=columns_list)
    data1_fix.set_index('지역',inplace=True)

    columns_list=['지역','lat','lng']
    naver=pd.DataFrame(naver_excel,columns=columns_list)
    naver.set_index('지역',inplace=True)

    naver_weather = pd.merge(data1_fix,naver,left_on='지역',right_on='지역')
    map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
    for n in naver_weather.index:
        folium.Marker(
            [naver_weather['lat'][n],naver_weather['lng'][n]],
            radius=10,
            color='#3186cc',
            fill_color='#3186cc',
            fill=True,
            tooltip='<b>-날씨</b>:'+naver_weather['날씨'][n]+'<br/>'+
            '<b>-기온</b>:'+naver_weather['기온'][n]).add_to(map)
    # map.save('test2.html')
    print('sssss')
    return data5_text2


chat_dic = {}
row = 0
chatbot_data = pd.read_excel("C:/workspace/work_py/mini/testPorject/data/chatbot_data.xlsx")

for rule in chatbot_data['rule']:
    chat_dic[row] = rule.split('|')
    row += 1
     
def chat(request):
    for k, v in chat_dic.items():
        chat_flag = False
        for word in v:
            if word in request:
                chat_flag = True
                
            if request in '날씨':
                return for_one_clawer(request)
            if request in '전국':
                print("전국")
                return for_all_clawer(request)

            else:
                chat_flag = False
                break
        if chat_flag:
                return chatbot_data['response'][k]
    return '무슨 말인지 모르겠어요'

app = Flask(__name__)


@app.route("/")
def home():
    print("home")
    return render_template("index.html")
 
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chat(userText))
 
if __name__ == "__main__":
    app.run(port=9006)