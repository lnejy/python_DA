import streamlit as st
import bikes
import naverNews

# 사이드바 화면
st.sidebar.title('Side Bar')
user_id = st.sidebar.text_input('User ID', value='Your ID')
user_password = st.sidebar.text_input('Password', value='', type='password')

if user_password == '1234':
    st.sidebar.header('===포트폴리오===')
    select_data = ['메뉴선택', '따릉이 분석', '뉴스분석']
    menu = st.sidebar.selectbox('메뉴선택', select_data, index=0)

    if menu == '따릉이 분석':
        st.write('따릉이 분석')
        bikes.bike_main()
    elif menu == '뉴스분석':
        st.write('뉴스 분석')
        df = naverNews.data_create()
        st.dataframe(df)
        naverNews.text_visualizaiton(df)
    else:
        st.title('환영')
