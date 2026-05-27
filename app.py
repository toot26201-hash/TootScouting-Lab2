import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="TootScouting Pro", layout="wide")

# تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_csv("EPS-honka-actions.xlsx - All Actions.csv")
    return df

df = load_data()

st.title("📊 TootScouting: Professional Match Dashboard")

# 1. إحصائيات سريعة (Metrics)
col1, col2, col3, col4 = st.columns(4)
col1.metric("إجمالي الأحداث", len(df))
col2.metric("عدد التمريرات", len(df[df['Action'] == 'Pass']))
col3.metric("عدد التسديدات", len(df[df['Action'] == 'Shot']))
col4.metric("عدد اللاعبين", df['Player'].nunique())

st.markdown("---")

# 2. فلتر اللاعبين
selected_player = st.sidebar.multiselect("اختر اللاعبين:", df['Player'].dropna().unique())
if selected_player:
    df = df[df['Player'].isin(selected_player)]

# 3. رسم بياني (توزيع الأكشن)
st.subheader("توزيع أحداث المباراة")
fig = px.bar(df['Action'].value_counts().reset_index(), x='index', y='Action', 
             color='Action', text='Action')
st.plotly_chart(fig, use_container_width=True)

# 4. جدول اللقطات
st.subheader("سجل الأحداث")
st.dataframe(df[['Action', 'Player', 'Event Time (mm:ss)', 'Tags']], use_container_width=True)
