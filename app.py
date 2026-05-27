import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الصفحة
st.set_page_config(page_title="TootScouting Analysis", layout="wide")

# 2. دالة تنظيف الداتا (بتاخد الـ CSV وتقسمه)
def load_and_process_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    data = []
    cat = "Unknown"
    for line in lines:
        if line.startswith("CATEGORY:"):
            cat = line.split(":")[1].strip()
        elif ";" in line and "Name" not in line and not line.startswith("Summary"):
            data.append([cat] + line.strip().split(";"))
    
    df = pd.DataFrame(data)
    # تسمية الأعمدة
    cols = ['Category', 'Name', 'Time', 'Start', 'Stop', 'Team', 'Player']
    df = df.iloc[:, :7]
    df.columns = cols
    return df

# 3. تحميل الداتا
df = load_and_process_data("EPS-honka..csv")

# 4. زرار التبديل (الريموت كنترول)
if 'show_stats' not in st.session_state: st.session_state.show_stats = False
if st.sidebar.button("📊 عرض إحصائيات الماتش"):
    st.session_state.show_stats = not st.session_state.show_stats

# 5. عرض الإحصائيات (المطابقة للصورة)
if st.session_state.show_stats:
    st.subheader("تقرير أداء الماتش")
    
    # الكروت (Metrics)
    c1, c2, c3, c4 = st.columns(4)
    # بنعد الأحداث بناءً على الـ Category
    c1.metric("إجمالي الأحداث", len(df))
    c2.metric("التمريرات", len(df[df['Category'] == 'Pass']))
    c3.metric("التسديدات", len(df[df['Category'] == 'SH/A']))
    c4.metric("إجمالي اللاعبين", df['Player'].nunique())
    
    st.markdown("---")
    
    # الرسم البياني التفاعلي
    fig = px.bar(df['Category'].value_counts().reset_index(), x='index', y='Category', 
                 title="توزيع الأحداث حسب النوع",
                 color='Category', color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df, use_container_width=True)
else:
    st.write("أنت في وضع الفيديو.. اضغط على الزرار الجانبي لعرض الإحصائيات")
