import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعداد الصفحة بشكل احترافي
st.set_page_config(page_title="TootScouting Dashboard", layout="wide")

# 2. تحميل البيانات
@st.cache_data
def load_data():
    # تأكد من رفع ملف "EPS-honka-actions.xlsx - All Actions.csv" على GitHub
    return pd.read_csv("EPS-honka-actions.xlsx - All Actions.csv")

df = load_data()

st.title("📊 TootScouting Performance Dashboard")

# 3. زرار التبديل بين الفيديو والإحصائيات
if 'show_stats' not in st.session_state:
    st.session_state.show_stats = True # البداية على الإحصائيات

if st.sidebar.button("🔄 تبديل الوضع"):
    st.session_state.show_stats = not st.session_state.show_stats

if st.session_state.show_stats:
    # --- وضع الإحصائيات (الداشبورد) ---
    st.subheader("إحصائيات الماتش الحية")
    
    # كروت الأرقام (Metrics) زي اللي في الصورة
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("إجمالي الأحداث", len(df))
    col2.metric("التمريرات", len(df[df['Action'] == 'Pass']))
    col3.metric("التسديدات", len(df[df['Action'] == 'Shot']))
    col4.metric("استخلاصات", len(df[df['Action'] == 'extraction ']))

    st.markdown("---")

    # الرسم البياني (Bar Chart)
    st.subheader("توزيع الأحداث")
    event_counts = df['Action'].value_counts().reset_index()
    event_counts.columns = ['Action', 'Count']
    fig = px.bar(event_counts, x='Action', y='Count', color='Count', 
                 color_continuous_scale='Blues', text='Count')
    st.plotly_chart(fig, use_container_width=True)

    # الجدول التفصيلي
    st.subheader("سجل اللقطات")
    st.dataframe(df[['Action', 'Player', 'Event Time (mm:ss)', 'Outcome']], use_container_width=True)

else:
    # --- وضع الفيديو ---
    st.subheader("وضع تحليل الفيديو")
    st.write("هنا سيتم عرض مشغل الفيديو الخاص بك.")
