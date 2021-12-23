# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 16:49:28 2021

@author: Playdata


pip install plotly
pip install cython

# anaconta prompt 에서 실행
conda install Cython pystan pymc3 arviz
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

import urllib.request
import datetime
import json
import glob
import sys
import os
# from fbprophet import Prophet

import warnings
warnings.filterwarnings(action='ignore')

# matplotlib inline
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.grid'] = False

pd.set_option('display.max_columns', 250)
pd.set_option('display.max_rows', 250)
pd.set_option('display.width', 100)

pd.options.display.float_format = '{:.2f}'.format



class NaverDataLabOpenAPI():
    """
    네이버 데이터랩 오픈 API 컨트롤러 클래스
    """

    """
    인증키 설정 및 검색어 그룹 초기화
    """
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.keywordGroups = []
        self.url = "https://openapi.naver.com/v1/datalab/search"
        
        
    """
    검색어 그룹 추가
    """
    def add_keyword_groups(self, group_dict):

        keyword_gorup = {
            'groupName': group_dict['groupName'],
            'keywords': group_dict['keywords']
        }
        
        self.keywordGroups.append(keyword_gorup)
        print(f">>> Num of keywordGroups: {len(self.keywordGroups)}")


    """
    요청 결과 반환
    """
    def get_data(self, startDate, endDate, timeUnit, device, ages, gender):
    
            # Request body
            body = json.dumps({
                "startDate": startDate,
                "endDate": endDate,
                "timeUnit": timeUnit,
                "keywordGroups": self.keywordGroups,
                "device": device,
                "ages": ages,
                "gender": gender
            }, ensure_ascii=False)
            
            # Results
            request = urllib.request.Request(self.url)
            request.add_header("X-Naver-Client-Id",self.client_id)
            request.add_header("X-Naver-Client-Secret",self.client_secret)
            request.add_header("Content-Type","application/json")
            response = urllib.request.urlopen(request, data=body.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                # Json Result
                result = json.loads(response.read())
                
                df = pd.DataFrame(result['results'][0]['data'])[['period']]
                for i in range(len(self.keywordGroups)):
                    tmp = pd.DataFrame(result['results'][i]['data'])
                    tmp = tmp.rename(columns={'ratio': result['results'][i]['title']})
                    df = pd.merge(df, tmp, how='left', on=['period'])
                self.df = df.rename(columns={'period': '날짜'})
                self.df['날짜'] = pd.to_datetime(self.df['날짜'])
                
            else:
                print("Error Code:" + rescode)
                
            return self.df
        
    """
    일 별 검색어 트렌드 그래프 출력
    """
    def plot_daily_trend(self):
            colList = self.df.columns[1:]
            n_col = len(colList)
    
            fig = plt.figure(figsize=(12,6))
            plt.title('일 별 검색어 트렌드', size=20, weight='bold')
            for i in range(n_col):
                sns.lineplot(x=self.df['날짜'], y=self.df[colList[i]], label=colList[i])
            plt.legend(loc='upper right')
            
            return fig

    """
    월 별 검색어 트렌드 그래프 출력
    """
    def plot_monthly_trend(self):
            df = self.df.copy()
            df_0 = df.groupby(by=[df['날짜'].dt.year, df['날짜'].dt.month]).mean().droplevel(0).reset_index().rename(columns={'날짜': '월'})
            df_1 = df.groupby(by=[df['날짜'].dt.year, df['날짜'].dt.month]).mean().droplevel(1).reset_index().rename(columns={'날짜': '년도'})
    
            df = pd.merge(df_1[['년도']], df_0, how='left', left_index=True, right_index=True)
            df['날짜'] = pd.to_datetime(df[['년도','월']].assign(일=1).rename(columns={"년도": "year", "월":'month','일':'day'}))
            
            colList = df.columns.drop(['날짜','년도','월'])
            n_col = len(colList)
                    
            fig = plt.figure(figsize=(12,6))
            plt.title('월 별 검색어 트렌드', size=20, weight='bold')
            for i in range(n_col):
                sns.lineplot(x=df['날짜'], y=df[colList[i]], label=colList[i])
            plt.legend(loc='upper right')
            
            return fig

    def plot_pred_trend(self, days):
        """
        검색어 그룹 별 시계열 트렌드 예측 그래프 출력
        days: 예측일수
        """
        colList = self.df.columns[1:]
        n_col = len(colList)
        
        fig_list = []
        for i in range(n_col):
            
            globals()[f"df_{str(i)}"] = self.df[['날짜', f'{colList[i]}']]
            globals()[f"df_{str(i)}"] = globals()[f"df_{str(i)}"].rename(columns={'날짜': 'ds', f'{colList[i]}': 'y'})

            m = Prophet()
            m.fit(globals()[f"df_{str(i)}"])

            future = m.make_future_dataframe(periods=days)
            forecast = m.predict(future)
            forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
            
            globals()[f"fig_{str(i)}"] = m.plot(forecast, figsize=(12,6))
            plt.title(colList[i], size=20, weight='bold')
            
            fig_list.append(globals()[f"fig_{str(i)}"])
            
        return fig_list

# 검색어 그룹 세트 정의
keyword_group_set = {
    'keyword_group_1': {'groupName': "삼겹살", 'keywords': ["삼겹살","돼지고기","삼겹살 맛집"]},
    'keyword_group_2': {'groupName': "파전&막걸리", 'keywords': ["파전","막걸리","김치전","파전 맛집"]},
    'keyword_group_3': {'groupName': "소고기", 'keywords': ["소고기","한우","소고기 맛집"]}
    }
#    'keyword_group_4': {'groupName': "테슬라", 'keywords': ["테슬라","Tesla","TSLA"]},
#    'keyword_group_5': {'groupName': "페이스북", 'keywords': ["페이스북","Facebook","FB"]}
# }

# API 인증 정보 설정
client_id = "bK6SRZLZNMahPGDdtfC0"
client_secret = "dfR3AdiO5w"

# 요청 파라미터 설정
startDate = "2020-01-01"
endDate = "2020-12-31"
timeUnit = 'date'
device = ''
ages = []
gender = ''

# 데이터 프레임 정의
naver = NaverDataLabOpenAPI(client_id=client_id, client_secret=client_secret)

naver.add_keyword_groups(keyword_group_set['keyword_group_1'])
naver.add_keyword_groups(keyword_group_set['keyword_group_2'])
naver.add_keyword_groups(keyword_group_set['keyword_group_3'])
# naver.add_keyword_groups(keyword_group_set['keyword_group_4'])
# naver.add_keyword_groups(keyword_group_set['keyword_group_5'])

df = naver.get_data(startDate, endDate, timeUnit, device, ages, gender)


# 일 별 트렌드 시각화 하기
fig_1 = naver.plot_daily_trend()

# 월 별 트렌드 시각화 하기
fig_2 = naver.plot_monthly_trend()

# 트렌드 예측하기
# fig_3 = naver.plot_pred_trend(days = 90)













