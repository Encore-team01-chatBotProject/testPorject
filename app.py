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
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# chatbot 대답 코드
import pandas as pd
chat_dic = {}
row = 0
chatbot_data = pd.read_excel("c:/work_py/project/data/chatbot_data.xlsx")

for rule in chatbot_data['rule']:
    chat_dic[row] = rule.split('|')
    row += 1
     
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
                return chatbot_data['response'][k]
    return '무슨 말인지 모르겠어요'
# chatbot 대답코드 END

# app 실행 시작 및 html 실행, 채팅 get하여 대답 return
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
    app.run(port=9005)
# app END