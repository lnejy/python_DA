import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
import streamlit.components.v1 as components
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def data_preprocessing():
    bikes_tmp={}

    # 데이터 불러오기
    for i in range(1, 4):
        bikes_tmp[i] = pd.read_csv(f'day9_data\서울특별시 공공자전거 대여이력 정보_240{i}.csv', encoding='cp949')
    bikes = pd.concat(bikes_tmp, ignore_index=True)

    # 데이터 전처리
    bikes['대여일'] = pd.to_datetime(bikes['대여일시'])
    bikes['월'] = bikes['대여일'].dt.month
    bikes['일자'] = bikes['대여일'].dt.day
    bikes['시간대'] = bikes['대여일'].dt.hour

    weekdays={0:'월', 1:'화', 2:'수', 3:'목', 4:'금', 5:'토', 6:'일'}
    bikes['요일'] = bikes['대여일'].dt.weekday.map(weekdays)

    bikes['주말구분'] = bikes['대여일'].dt.weekday.map(lambda x : '평일' if x < 5 else '주말')

    return bikes


def top50(bikes):
    bikes_weekend = bikes.groupby(['대여 대여소번호', '대여 대여소명', '주말구분'])['자전거번호'].count().unstack()
    weekend50 = bikes_weekend.sort_values('주말', ascending=False).head(50).reset_index()
    bike_shop = pd.read_csv('day9_data\공공자전거 대여소 정보.csv', encoding='cp949')
    weekend50_total = pd.merge(weekend50, bike_shop, left_on ='대여 대여소번호', right_on='대여소번호')

    map = folium.Map(location=[weekend50_total['위도'].mean(), weekend50_total['경도'].mean()], zoom_start=12)

    for i in weekend50_total.index:
        markerC = MarkerCluster().add_to(map)
        sub_lat = weekend50_total.loc[i, '위도']
        sub_long = weekend50_total.loc[i, '경도']
        shop = [sub_lat, sub_long]
        sub_name = weekend50_total.loc[i, '대여 대여소명']

        folium.Marker(location=shop, popup=sub_name, icon=folium.Icon(color='red', icon='star')).add_to(markerC)
    
    components.html(map._repr_html_(), height=500)

def time_analysis(bikes):
    hourly_ride = bikes.groupby('시간대', as_index=False)['자전거번호'].count()
    weekday_ride = bikes.groupby('요일', as_index=False)['자전거번호'].count()

    fig, axes = plt.subplots(2, 1, figsize=(21, 6))

    sns.barplot(data=hourly_ride, x='시간대', y='자전거번호', ax=axes[0])
    sns.lineplot(data=weekday_ride, x='요일', y='자전거번호', ax=axes[1])

    st.pyplot(fig)


def bike_main():
    tab1, tab2, tab3 = st.tabs(["데이터 보기", "인기대여소50", "시간대별 분석"])

    with tab1:
        data = data_preprocessing()
        st.dataframe(data.head(20)) 
    with tab2:
        top50(data)
    with tab3:
        time_analysis(data)


if __name__ == '__main__':
    bike_main()