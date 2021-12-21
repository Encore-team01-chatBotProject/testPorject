
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import folium
import webbrowser

def all_dust(keword):
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="+keword
    html_dust = requests.get(url).text
    soup_dust = bs(html_dust, 'lxml')
    
    
    dust_condition = soup_dust.select('div.detail_box tbody tr')
    dust_condition
    
    dust_condition_text = [title.get_text() for title in dust_condition]
    
    del dust_condition_text[18:]
    del dust_condition_text[0]
    
    
    dust_condition_table = []
    for i in dust_condition_text:
        i = i.split()
        dust_condition_table.append(i)
    
    columns_list = ['관측지점','현재','오전예보','오후예보']
    dust_condition_pd= pd.DataFrame(dust_condition_table, columns =columns_list)
    
    
    #엑셀 파일 읽기
    xlsx = pd.read_excel('./minidata/naver_dust_data.xlsx')
    #합치기
    dust_condition_last = pd.merge(dust_condition_pd,xlsx)
    #지도에 마크 표시
    m = folium.Map(location=[36.0198621404393, 127.88337017440863], tiles='cartodbpositron', zoom_start=7.2)

    for n in dust_condition_last.index:
        folium.Marker(
            [dust_condition_last['lat'][n],dust_condition_last['lng'][n]],
            radius=10,
            color='#3186cc',
            fill_color='#3186cc',
            fill=True,
            tooltip=dust_condition_last['관측지점'][n]+'<br/>'+
            '<b>-오전미세먼지</b>:'+dust_condition_last['오전예보'][n]+'<br/>'+
            '<b>-오후미세먼지</b>:'+dust_condition_last['오후예보'][n]).add_to(m)
    m.save('dust_map.html')

    return webbrowser.open_new('dust_map.html')

all_dust('미세먼지')
