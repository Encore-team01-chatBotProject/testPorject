# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 14:19:37 2021

날씨 긁어와서 알려주는 
"""

import requests
from pandas import DataFrame as df
from bs4 import BeautifulSoup as bs
import pandas as pd
import folium
import webbrowser


# 날씨 크롤링
def for_all_clawer(keyword):
    html = requests.get('https://search.naver.com/search.naver?query='+'전국 날씨').text
    weather_data=bs(html,'lxml').find('div',class_='map _map_normal').findAll('span')
    weather_list_before=[title.get_text() for title in weather_data]

    weather_list=[weather_list_before[(i*3):((i*3)+3)] for i in range(12)]
    
    columns_list = ['지역','날씨','기온']
    weather_df=df(weather_list,columns=columns_list)
    weather_df.set_index('지역',inplace=True)
    # 위도 경도 획득
    position=pd.read_excel('./data/naver_data.xlsx')
    position.set_index('지역',inplace=True)
    
    # 날씨 + 위도 경도
    naver_weather_df = pd.merge(weather_df,position, how='left', right_index=True,left_index=True)
    
    # 지도 생성 + 답변 생성
    res = '# 날씨 정보 입니다. #<br>';
    maps = '';
    if '전국' in keyword:
        maps = folium.Map(location=[36.62675563, 127.4965159], zoom_start=7)
   
    for n in naver_weather_df.index:
        if n in keyword :
            maps = folium.Map(location=[naver_weather_df['lat'][n], naver_weather_df['lng'][n]],zoom_start=12)
        
        if ( '전국' in keyword  ) or ( n in keyword ):
            folium.Marker(
                [naver_weather_df['lat'][n],naver_weather_df['lng'][n]],
                radius=10,
                color='#3186cc',
                fill_color='#3186cc',
                fill=True,
                tooltip=('<b>'+n+' 날씨<b> : '+naver_weather_df['날씨'][n]+' 상태.<br />'+
                '<b>현재 기온</b> : '+naver_weather_df['기온'][n])+'℃').add_to(maps)
            res = res +( n +' : '+naver_weather_df['날씨'][n]+' 상태, '+
            '현재 온도 : '+naver_weather_df['기온'][n]+'℃<br />')

    if type(maps) == folium.folium.Map :
        maps.save('./templates/restaurant.html')
    else : 
        res = '날씨 확인할 지역을 제대로 입력해 주세요'
        
    return res



# 미세먼지 크롤링
def all_dust(keyword):
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=미세먼지"
    html_dust = requests.get(url).text
    soup_dust = bs(html_dust, 'lxml')
    
    dust_condition = soup_dust.select('div.detail_box tbody tr')
    
    dust_condition_text = [title.get_text() for title in dust_condition[:18]]    
    dust_condition_table = [line.split() for line in dust_condition_text]
    
    columns_list = ['지역','현재','오전예보','오후예보']
    dust_condition_pd= pd.DataFrame(dust_condition_table[1:], columns=['지역']+[words for words in dust_condition_table[0][1:]])
    dust_condition_pd.set_index('지역',inplace=True)
    
    # 위도 경도 획득
    position=pd.read_excel('./data/naver_data.xlsx')
    position.set_index('지역',inplace=True)
    
    # 미세먼지 + 위도 경도
    dust_condition_last = pd.merge(dust_condition_pd,position, how='left', right_index=True,left_index=True)
    

    # 지도 생성 + 답변 생성
    res = '# 미세먼지 정보 입니다. #<br>';
    maps = '';
    #지도에 마크 표시
    if '전국' in keyword:
        maps = folium.Map(location=[36.62675563, 127.4965159], tiles='cartodbpositron',zoom_start=7)

    for n in dust_condition_last.index:
        if n in keyword:
            maps = folium.Map(location=[dust_condition_last['lat'][n], dust_condition_last['lng'][n]], tiles='cartodbpositron',zoom_start=12)
        
        if ( '전국' in keyword ) or ( n in keyword ):
            folium.Marker(
                [dust_condition_last['lat'][n],dust_condition_last['lng'][n]],
                radius=10,
                color='#3186cc',
                fill_color='#3186cc',
                fill=True,
                tooltip='<b>'+n+'</b> 미세 먼지 현황<br/>'+
                '<b>오전</b> : '+dust_condition_last['오전예보'][n]+'<br/>'+
                '<b>오후</b> : '+dust_condition_last['오후예보'][n]).add_to(maps)
            
            res = res + n + ' 미세먼지 : 오전 - '+dust_condition_last['오전예보'][n]+ ' / 오후 - '+dust_condition_last['오후예보'][n]+'.<br />'
    
    if type(maps) == folium.folium.Map :
        maps.save('./templates/restaurant.html')
    else : 
        res = '미세먼지 확인할 지역을 제대로 입력해 주세요'
    
    return res


















