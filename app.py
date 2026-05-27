import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="TootScouting Dashboard", layout="wide")

# دالة لقراءة ملف الـ EPS-honka..csv وتظبيطه
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    data = []
    category = "Unknown"
    for line in lines:
        if line.startswith("CATEGORY:"):
            category = line.split(":")[1].strip()
        elif ";" in line and "Name" not in line:
            parts = line.strip().split(";")
            data.append([category] + parts)
    
    # تحويل لجدول
    df = pd.DataFrame(data)
    # تظبيط الأعمدة (الأعمدة اللي تهمنا: Category, Player, Event)
    # بناءً على ملفك: العمود 0=Category, العمود 5=Player, العمود 0=Name
    df.columns = ['Category', 'Event', 'Time', 'Start', 'Stop', 'Team', 'Player'] + [f'M{i}' for i in range(len(df.columns)-7)]
    return df

st.title("📊 TootScouting Dashboard")

try:
    # قرائة الملف الجديد فقط
    df = load_data("EPS-honka..csv")
    
    # فلاتر
    players = df['Player'].dropna().unique()
    selected_player = st.sidebar.multiselect("اختر اللاعب:", players)
    
    if selected_player:
        df = df[df['Player'].isin(selected_player)]
    
    # عرض الإحصائيات
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الأحداث", len(df))
    c2.metric("التمريرات", len(df[df['Category'] == 'Pass']))
    c3.metric("التسديدات", len(df[df['Category'] == 'SH/A']))
    
    # رسم بياني
    fig = px.bar(df['Category'].value_counts().reset_index(), x='index', y='Category')
    st.plotly_chart(fig, use_container_width=True)
    
except Exception as e:
    st.error(f"⚠️ خطأ في الكود: {e}")
