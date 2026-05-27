import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

st.title("📊 TootScouting Dashboard")

# الإحصائيات (Metrics)
col1, col2, col3, col4 = st.columns(4)
col1.metric("إجمالي الأحداث", len(df))
col2.metric("التمريرات", len(df[df['Action'] == 'Pass']))
col3.metric("التسديدات", len(df[df['Action'] == 'Shot']))
col4.metric("استخلاصات", len(df[df['Action'] == 'extraction ']))

# الرسم البياني
st.subheader("تحليل الأكشن")
fig = px.bar(df['Action'].value_counts().reset_index(), x='index', y='Action')
st.plotly_chart(fig, use_container_width=True)

# الجدول
st.dataframe(df, use_container_width=True)
