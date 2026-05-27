import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="TootScouting Dashboard", layout="wide")

# دالة لقراءة الملف بذكاء (لأن ملفك مقسم لـ Categories)
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    data = []
    category = "Unknown"
    for line in lines:
        if line.startswith("CATEGORY:"):
            category = line.split(":")[1].strip()
        elif ";" in line and "Name" not in line and not line.startswith("Summary"):
            parts = line.strip().split(";")
            data.append([category] + parts)
    
    # تحويل البيانات لجدول
    df = pd.DataFrame(data)
    # تسمية الأعمدة (العمود الأول هو Category، والعمود السادس هو Player)
    # ملاحظة: زودنا أعمدة لتغطية بياناتك
    columns = ['Category', 'Event', 'Time', 'Start', 'Stop', 'Team', 'Player'] + [f'Extra_{i}' for i in range(df.shape[1]-7)]
    df.columns = columns
    return df

st.title("📊 TootScouting Performance Dashboard")

try:
    # 1. تحديد مكان الملف (شغال أونلاين وأوفلاين)
    file_path = "EPS-honka..csv"
    
    # 2. تحميل البيانات
    df = load_data(file_path)
    
    # 3. فلتر اللاعبين
    players = df['Player'].dropna().unique()
    selected_player = st.sidebar.multiselect("اختر اللاعب:", players)
    
    if selected_player:
        df = df[df['Player'].isin(selected_player)]
    
    # 4. كروت المؤشرات (Metrics)
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي الأحداث", len(df))
    # حساب الفئات بناءً على الـ Category اللي في الملف
    col2.metric("التمريرات", len(df[df['Category'] == 'Pass']))
    col3.metric("التسديدات", len(df[df['Category'] == 'SH/A']))
    
    # 5. رسم بياني تفاعلي
    st.subheader("توزيع الأحداث حسب النوع")
    fig = px.bar(df['Category'].value_counts().reset_index(), x='index', y='Category', color='index')
    st.plotly_chart(fig, use_container_width=True)
    
    # 6. الجدول التفصيلي
    st.subheader("تفاصيل اللقطات")
    st.dataframe(df[['Category', 'Event', 'Player', 'Time']], use_container_width=True)

except Exception as e:
    st.error(f"⚠️ حدث خطأ أثناء تشغيل الداشبورد: {e}")
    st.write("تأكد أن الملف 'EPS-honka..csv' موجود في نفس مسار ملف 'app.py' على GitHub.")
