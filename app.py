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
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

def forClawer(keword):
    html = requests.get('https://search.naver.com/search.naver?query='+keword)
    soup=bs(html.text,'html.parser')
    data1=soup.find('div',class_='temperature_text').find('strong').text
    print(data1)
    if data1 :
        return data1
    else : 
        return '지역을 다시 입력 하세요' 

chat_dic = {}
row = 0
chatbot_data = pd.read_excel("C:/workspace_flask/testPorject/data/chatbot_data.xlsx")

for rule in chatbot_data['rule']:
    chat_dic[row] = rule.split('|')
    row += 1
     
def chat(request):
    for k, v in chat_dic.items():
        chat_flag = False
        for word in v:
            if word in request:
                chat_flag = True
                
                if word in '날씨':
                    return forClawer(request)
            else:
                chat_flag = False
                break
        if chat_flag:
                return chatbot_data['response'][k]
    return '무슨 말인지 모르겠어요'

app = Flask(__name__)

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")
 
@app.route("/")
def home():
    print("home")
    return render_template("index.html")
 
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chat(userText))
 
if __name__ == "__main__":
    app.run(host='192.168.1.233',port=9006)