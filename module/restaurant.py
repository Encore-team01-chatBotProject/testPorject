# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 11:52:15 2021

맛집 마크된 지도 만드는 파
"""

# 지도 표시를 위한 import
import folium
import googlemaps
import pandas as pd
import platform
import webbrowser
# matplotlib notebook
import matplotlib.pyplot as plt
import warnings
from matplotlib import font_manager, rc
# 지도 표시 import END

### ---  맛집 리스트 출력 코드 --- ###
def getList(keyword):
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
    # Plot 한글지원 END
    
    # Google map api key setting 강사님 key 씀
    gmaps_key = "AIzaSyC-ezB2J00Td105d4jqtdi2-JmZKuZ-5lY"
    gmaps = googlemaps.Client(key=gmaps_key)

    ## 음식점 엑셀데이터 다루기 ## 800개 데이터 다운로드 해놓음
    restaurant_df = pd.read_excel("./data/전국_맛집_취합종합본.xlsx", engine = 'openpyxl')

    for n in restaurant_df.index:
        if(restaurant_df['지역'][n][-3:] == '광역시' ):
            restaurant_df['지역'][n] = restaurant_df['지역'][n][:-3]
        elif(restaurant_df['지역'][n] == '서울특별시'):
            restaurant_df['지역'][n] = '서울'
    
    res = '# 맛집 정보 입니다. #<br>';
    maps = '';
    for n in restaurant_df.index:
        if (( restaurant_df['지역'][n] in keyword ) or ( restaurant_df['도시명'][n] in keyword )) and type(maps) != folium.folium.Map:
            maps = folium.Map(location=[restaurant_df['lat'][n], restaurant_df['lng'][n]],zoom_start=10)
        
        if ( restaurant_df['지역'][n] in keyword ) or ( restaurant_df['도시명'][n] in keyword ):
            folium.Marker(
                [restaurant_df['lat'][n],restaurant_df['lng'][n]],
                radius = 10, 
                color='#3186cc',
                fill_color='#3186cc', 
                fill=True,
                tooltip=('<b>도시명</b>: ' + restaurant_df['도시명'][n] + '<br />'+
                         '<b>상호명</b>: ' + restaurant_df['식당상호'][n])
            ).add_to(maps)
    
    if type(maps) == folium.folium.Map :
        maps.save('./templates/restaurant.html')
    else : 
        res = '맛집 확인할 지역을 제대로 입력해 주세요'
    #지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환
    
    return res
### ---  맛집 리스트 출력 코드 END --- ###