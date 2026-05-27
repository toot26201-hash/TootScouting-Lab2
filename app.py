import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="TootScouting Dashboard", layout="wide")

# دالة ذكية لقراءة الملف المتعدد الفئات
def load_and_clean_data(file_path):
    # قراءة الملف كـ نص (CSV)
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
            
    return pd.DataFrame(data)

st.title("📊 TootScouting Performance Dashboard")

# تحميل الداتا
try:
    df = load_and_clean_data("EPS-honka..csv")
    # تسمية الأعمدة (بناءً على شكل الملف)
    df.columns = ['Category', 'Event', 'Time', 'Start', 'Stop', 'Team', 'Player', 'Metric1', 'Metric2', 'Metric3', 'Metric4', 'Metric5', 'Metric6', 'Metric7', 'Metric8', 'Metric9', 'Metric10', 'Metric11']
    
    # فلتر اللاعبين
    players = df['Player'].dropna().unique()
    selected_player = st.sidebar.multiselect("اختر اللاعب:", players)
    
    if selected_player:
        df = df[df['Player'].isin(selected_player)]
    
    # عرض الأرقام فوق (Metrics)
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي الأحداث", len(df))
    col2.metric("عدد التمريرات", len(df[df['Category'] == 'Pass']))
    col3.metric("عدد التسديدات", len(df[df['Category'] == 'SH/A']))
    
    # الرسم البياني
    st.subheader("توزيع الأحداث")
    fig = px.bar(df['Category'].value_counts().reset_index(), x='index', y='Category')
    st.plotly_chart(fig, use_container_width=True)
    
except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف: {e}")