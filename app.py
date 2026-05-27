import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="TootScouting Dashboard", layout="wide")

# دالة ذكية لقراءة الملف الجديد EPS-honka..csv
def load_and_clean_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    data = []
    current_category = None
    for line in lines:
        if line.startswith("CATEGORY:"):
            current_category = line.split(":")[1].strip()
        elif ";" in line and "Name" not in line and current_category:
            parts = line.strip().split(";")
            data.append([current_category] + parts)
            
    # تحويل البيانات لجدول (DataFrame)
    # ملاحظة: زودنا أعمدة لتغطية كل البيانات في ملفك
    df = pd.DataFrame(data)
    # تظبيط أسماء الأعمدة بناءً على الملف
    cols = ['Category', 'Name', 'Time', 'Start', 'Stop', 'Team', 'Player', 'Metric1', 'Metric2', 'Metric3', 'Metric4', 'Metric5', 'Metric6']
    df = df.iloc[:, :len(cols)] # قص الأعمدة الزيادة لو فيه
    df.columns = cols
    return df

st.title("📊 TootScouting Performance Dashboard")

# تحميل الداتا من الملف الجديد
try:
    # تأكد من أن اسم الملف في الكود هو نفس اسم الملف المرفوع على GitHub
    df = load_and_clean_data("EPS-honka..csv")
    
    # فلتر اللاعبين من القائمة الجانبية
    players = df['Player'].dropna().unique()
    selected_player = st.sidebar.multiselect("اختر اللاعب:", players)
    
    if selected_player:
        df = df[df['Player'].isin(selected_player)]
    
    # عرض الأرقام (Metrics)
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي الأحداث", len(df))
    # حساب التمريرات والتسديدات بناءً على الـ Category
    col2.metric("التمريرات", len(df[df['Category'] == 'Pass']))
    col3.metric("التسديدات", len(df[df['Category'] == 'SH/A']))
    
    # الرسم البياني
    st.subheader("توزيع الأحداث")
    fig = px.bar(df['Category'].value_counts().reset_index(), x='index', y='Category')
    st.plotly_chart(fig, use_container_width=True)
    
except Exception as e:
    st.error(f"⚠️ خطأ في قراءة الملف: {e}")
    st.info("تأكد أن الملف 'EPS-honka..csv' مرفوع في نفس فولدر 'app.py' على GitHub.")
