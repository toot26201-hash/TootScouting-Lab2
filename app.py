import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="TootScouting Dashboard", layout="wide")

# تحميل ملف الـ CSV اللي فيه الأحداث
df = pd.read_csv("Untitled spreadsheet.xlsx - Sheet1.csv")
df.columns = df.columns.str.strip()

st.title("📊 TootScouting Performance Dashboard")

# 1. فلاتر جانبية احترافية
st.sidebar.header("الفلاتر")
selected_player = st.sidebar.multiselect("اختر اللاعبين:", df['Players'].dropna().unique())
if selected_player:
    df = df[df['Players'].isin(selected_player)]

# 2. كروت المؤشرات (Metrics) اللي في الصورة
col1, col2, col3, col4 = st.columns(4)
col1.metric("إجمالي الأحداث", len(df))
col2.metric("التمريرات", len(df[df['Event Type'] == 'Pass']))
col3.metric("الاستخلاصات", len(df[df['Event Type'] == 'extraction ']))
col4.metric("التسديدات", len(df[df['Event Type'] == 'Shot']))

# 3. الرسم البياني (Bar Chart) - تفاعلي
st.subheader("توزيع الأحداث حسب النوع")
event_counts = df['Event Type'].value_counts().reset_index()
event_counts.columns = ['Event', 'Count']
fig = px.bar(event_counts, x='Event', y='Count', color='Count', color_continuous_scale='Blues')
st.plotly_chart(fig, use_container_width=True)

# 4. جدول التفاصيل
st.subheader("تفاصيل اللقطات")
st.dataframe(df[['Event Time (mm:ss)', 'Event Type', 'Players', 'Tags']], use_container_width=True)