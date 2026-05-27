import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="TootScouting Analysis")

# تحميل البيانات (بدون تعقيدات)
@st.cache_data
def load_data():
    # تأكد من رفع الملف بالاسم ده على GitHub
    return pd.read_csv("EPS-honka-actions.xlsx - All Actions.csv")

df = load_data()

st.title("📊 TootScouting Dashboard")

# 1. كروت الإحصائيات (اللي في الصورة)
col1, col2, col3, col4 = st.columns(4)
col1.metric("إجمالي الأحداث", len(df))
col2.metric("عدد التمريرات", len(df[df['Action'] == 'Pass']))
col3.metric("عدد التسديدات", len(df[df['Action'] == 'Shot']))
col4.metric("الاستخلاصات", len(df[df['Action'] == 'extraction ']))

st.markdown("---")

# 2. الرسم البياني (اللي بيدي الشكل الاحترافي)
st.subheader("تحليل الأكشن")
fig = px.bar(df['Action'].value_counts().reset_index(), x='index', y='Action', 
             color='Action', text='Action')
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# 3. الجدول التفاعلي
st.subheader("التفاصيل")
st.dataframe(df[['Action', 'Player', 'Event Time (mm:ss)', 'Outcome']], use_container_width=True)
