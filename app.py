import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mplsoccer import Pitch

# إعداد الصفحة وتسميتها بشكل احترافي
st.set_page_config(
    page_title="TutScouting - Lab",
    page_icon="⚽",
    layout="wide"
)

# هيدر شيك للبرنامج
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>TootScouting - Advanced Match Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>ارفع ملف البيانات الخاص بالمباراة للبدء في تحليل الأداء التكتيكي</p>", unsafe_allow_html=True)
st.write("---")

# 1. منطقة رفع الملف في منتصف الصفحة (أول خطوة)
st.subheader("📁 خطوة 1: تحميل ملف البيانات")
uploaded_file = st.file_uploader("اختر ملف الإكسيل أو الـ CSV المستخرج من برنامج التحليل", type=["csv", "xlsx"])

if uploaded_file is not None:
    st.success("تم تحميل الملف بنجاح! جاري معالجة البيانات...")
    
    # قراءة الملف بمرونة
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    
    # تنظيف الأعمدة وتوحيد الـ Action
    df.columns = df.columns.str.strip()
    cols_lower = {col.lower(): col for col in df.columns}
    if 'action' in cols_lower:
        df = df.rename(columns={cols_lower['action']: 'Action'})
        df['Action'] = df['Action'].fillna('None').astype(str).str.strip()
    else:
        df['Action'] = 'None'
        
    df = df.rename(columns={'X Start': 'x1', 'Y Start': 'y1', 'X End': 'x2', 'Y End': 'y2'})
    
    # التأكد من وجود الإحداثيات
    if all(col in df.columns for col in ['x1', 'y1', 'x2', 'y2']):
        # معالجة ذكية للأبعاد
        if df['x1'].max() > 1.0 or df['y1'].max() > 1.0:
            df['x_scaled'], df['y_scaled'] = df['x1'], df['y1']
            df['x2_scaled'], df['y2_scaled'] = df['x2'], df['y2']
        else:
            df['x_scaled'], df['y_scaled'] = df['x1'] * 120, df['y1'] * 80
            df['x2_scaled'], df['y2_scaled'] = df['x2'] * 120, df['y2'] * 80
        
        # تصنيف الأكشن
        def classify(val):
            val = val.lower()
            if 'pass' in val or 'تمرير' in val: return "Pass"
            if 'shot' in val or 'تسديد' in val: return "Shot"
            if 'tackle' in val or 'تدخل' in val or 'extra' in val: return "Tackle"
            if 'clearance' in val or 'تشتيت' in val or 'تخلص' in val or 'تخليص' in val: return "Clearance"
            if 'interception' in val or 'قطع' in val or 'اعتراض' in val: return "Interception"
            if 'aerial' in val or 'هوائي' in val: return "Aerial Duel"
            if 'ground' in val or 'أرضي' in val: return "Ground Duel"
            if 'foul' in val or 'خطأ' in val: return "Foul"
            if 'counter' in val or 'ضغط' in val: return "Counterpress"
            return "Other"

        df['Type'] = df['Action'].apply(classify)

        st.write("---")
        st.subheader("📊 خطوة 2: الفلترة والتحليل")

        # تقسيم الشاشة لجزئين: جزء للفلترة وجزء للملعب
        col_filter, col_pitch = st.columns([1, 2])

        with col_filter:
            st.markdown("### 🔍 أدوات التحكم")
            
            # فلتر اللاعبين
            players_list = ["All Players"] + sorted(df['Player'].dropna().astype(str).unique().tolist())
            selected_player = st.selectbox("👤 اختر اللاعب:", players_list)
            
            # فلتر الأكشنز
            all_types = sorted(df['Type'].unique().tolist())
            selected_actions = st.multiselect("اختر الأحداث المراد رسمها:", options=all_types, default=all_types)
            
            temp_df = df if selected_player == "All Players" else df[df['Player'].astype(str) == selected_player]
            filtered_df = temp_df[temp_df['Type'].isin(selected_actions)]
            
            # إحصائية سريعة تظهر مع الفلترة
            st.markdown("---")
            st.markdown("### 📈 ملخص سريع")
            st.metric(label="عدد الأحداث المفلترة", value=len(filtered_df))

        with col_pitch:
            # رسم الملعب
            fig, ax = plt.subplots(figsize=(10, 7))
            pitch = Pitch(pitch_type='statsbomb', pitch_color='#1a1a1a', line_color='#7c7c7c')
            pitch.draw(ax=ax)
            fig.patch.set_facecolor('#1a1a1a')
            
            # كتابة اسم اللاعب بخلفية الملعب
            ax.text(60, 40, selected_player, color='#D4AF37', fontsize=45, fontweight='bold', 
                    ha='center', va='center', alpha=0.1, zorder=1)

            configs = {
                "Pass": {"color": "#00ffcc", "marker": None, "is_arrow": True},
                "Aerial Duel": {"color": "#3399ff", "marker": "^"},
                "Tackle": {"color": "#ff00ff", "marker": "X"},
                "Shot": {"color": "#00ff00", "marker": "*"},
                "Clearance": {"color": "#ffffff", "marker": "s"},
                "Ground Duel": {"color": "#8B4513", "marker": "v"},
                "Foul": {"color": "#ffcc00", "marker": "d"},
                "Counterpress": {"color": "#ff3300", "marker": "h"},
                "Interception": {"color": "#0000FF", "marker": "o"} 
            }

            legend_elements = []
            for act in selected_actions:
                if act not in configs: continue
                cfg = configs[act]
                subset = filtered_df[filtered_df['Type'] == act]
                if subset.empty: continue
                
                if cfg.get("is_arrow"):
                    pitch.arrows(subset['x_scaled'], subset['y_scaled'], subset['x2_scaled'], subset['y2_scaled'], color=cfg['color'], width=2, ax=ax)
                    legend_elements.append(Line2D([0], [0], color=cfg['color'], lw=2, label=act))
                else:
                    if act == "Interception":
                        pitch.scatter(subset['x_scaled'], subset['y_scaled'], facecolors='none', edgecolors=cfg['color'], marker=cfg['marker'], s=150, lw=2, ax=ax)
                    else:
                        pitch.scatter(subset['x_scaled'], subset['y_scaled'], color=cfg['color'], marker=cfg['marker'], s=150, ax=ax)
                    
                    legend_elements.append(Line2D([0], [0], marker=cfg['marker'], color='none', markeredgecolor=cfg['color'], markerfacecolor='none' if act=="Interception" else cfg['color'], label=act, markersize=10))

            if legend_elements:
                ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, facecolor='#222222', labelcolor='white')
            
            st.pyplot(fig)
            plt.close(fig)
    else:
        st.warning("الملف المرفوع لا يحتوي على أعمدة الإحداثيات المطلوبة (x1, y1, x2, y2) أو (X Start, Y Start...)")
else:
    # شاشة ترحيبية تظهر في البداية قبل رفع الملف
    st.info("💡 في انتظار رفع ملف البيانات لعرض لوحة التحليل التفاعلية والملعب.")
