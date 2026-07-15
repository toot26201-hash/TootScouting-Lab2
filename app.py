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
st.markdown("<p style='text-align: center; color: #888;'>ارفع ملف البيانات الخاص بالمباراة للبدء في تحلیل الأداء التکتیکي</p>", unsafe_allow_html=True)
st.write("---")

# 1. منطقة رفع الملف في منتصف الصفحة
st.subheader("📁 خطوة 1: تحميل ملف البيانات")
uploaded_file = st.file_uploader("اختر ملف الإكسيل أو الـ CSV المستخرج من برنامج التحليل", type=["csv", "xlsx"])

if uploaded_file is not None:
    st.success("تم تحميل الملف بنجاح! جاري معالجة البيانات...")
    
    # قراءة الملف بمرونة مع تحديد اسم الشيت الافتراضي للإكسيل
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        try:
            # محاولة قراءة شيت All Actions المخصص أولاً
            df = pd.read_excel(uploaded_file, sheet_name='All Actions', engine='openpyxl')
        except:
            # كخطة بديلة لو الاسم اختلف يقرا أول شيت متاح
            df = pd.read_excel(uploaded_file, engine='openpyxl')
    
    # تنظيف الأعمدة وتوحيد الـ Action
    df.columns = df.columns.astype(str).str.strip()
    
    # خريطة مرنة لربط المسميات المكتوبة في ملفك بالمتغيرات
    rename_dict = {
        'X Start': 'x1', 'Y Start': 'y1', 
        'X End': 'x2', 'Y End': 'y2',
        'Player': 'Player', 'Action': 'Action'
    }
    df = df.rename(columns=rename_dict)
    
    # التأكيد على وجود عمود Action ومعالجة الفراغات
    if 'Action' in df.columns:
        df['Action'] = df['Action'].fillna('None').astype(str).str.strip()
    else:
        df['Action'] = 'None'
        
    # التأكد من وجود الإحداثيات الأساسية للبدء في الرسم
    if 'x1' in df.columns and 'y1' in df.columns:
        # معالجة ذكية للأبعاد (تحويل النسب من 0-1 إلى أبعاد الملعب 120x80)
        df['x1'] = pd.to_numeric(df['x1'], errors='coerce')
        df['y1'] = pd.to_numeric(df['y1'], errors='coerce')
        df['x2'] = pd.to_numeric(df['x2'], errors='coerce')
        df['y2'] = pd.to_numeric(df['y2'], errors='coerce')
        
        if df['x1'].max() <= 1.0 and df['y1'].max() <= 1.0:
            df['x_scaled'], df['y_scaled'] = df['x1'] * 120, df['y1'] * 80
            df['x2_scaled'], df['y2_scaled'] = df['x2'] * 120, df['y2'] * 80
        else:
            df['x_scaled'], df['y_scaled'] = df['x1'], df['y1']
            df['x2_scaled'], df['y2_scaled'] = df['x2'], df['y2']
        
        # تصنيف الأكشن بناءً على الكلمات المفتاحية في ملفك
        def classify(val):
            val = val.lower()
            if 'pass' in val or 'تمرير' in val: return "Pass"
            if 'shot' in val or 'sh/a' in val or 'تسديد' in val: return "Shot"
            if 'tackle' in val or 'تدخل' in val or 'pressing' in val or 'ضغط' in val: return "Tackle"
            if 'clearance' in val or 'تشتيت' in val or 'تخليص' in val: return "Clearance"
            if 'interception' in val or 'extraction' in val or 'قطع' in val: return "Interception"
            if 'aerial' in val or 'هوائي' in val: return "Aerial Duel"
            if 'ground' in val or 'أرضي' in val: return "Ground Duel"
            if 'foul' in val or 'خطأ' in val: return "Foul"
            return "Other"

        df['Type'] = df['Action'].apply(classify)

        st.write("---")
        st.subheader("📊 خطوة 2: الفلترة والتحليل التكتيكي")

        # تقسيم الشاشة
        col_filter, col_pitch = st.columns([1, 2])

        with col_filter:
            st.markdown("### 🔍 أدوات التحكم")
            
            # فلتر اللاعبين المستخرجين تلقائياً من عمود Player
            players_list = ["All Players"] + sorted(df['Player'].dropna().astype(str).unique().tolist())
            selected_player = st.selectbox("👤 اختر اللاعب:", players_list)
            
            # فلتر الأكشنز
            all_types = sorted(df['Type'].unique().tolist())
            selected_actions = st.multiselect("اختر الأحداث المراد رسمها:", options=all_types, default=all_types)
            
            temp_df = df if selected_player == "All Players" else df[df['Player'].astype(str) == selected_player]
            filtered_df = temp_df[temp_df['Type'].isin(selected_actions)]
            
            st.markdown("---")
            st.markdown("### 📈 ملخص سريع")
            st.metric(label="عدد الأحداث المفلترة للملعب", value=len(filtered_df))

        with col_pitch:
            # رسم الملعب
            fig, ax = plt.subplots(figsize=(10, 7))
            pitch = Pitch(pitch_type='statsbomb', pitch_color='#1a1a1a', line_color='#7c7c7c')
            pitch.draw(ax=ax)
            fig.patch.set_facecolor('#1a1a1a')
            
            # اسم اللاعب خلفية مائية في الملعب
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
                "Interception": {"color": "#FFFF00", "marker": "o"} 
            }

            legend_elements = []
            for act in selected_actions:
                if act not in configs: continue
                cfg = configs[act]
                subset = filtered_df[filtered_df['Type'] == act]
                if subset.empty: continue
                
                # إزالة أي قيم فارغة في إحداثيات الرسم الحالي
                subset = subset.dropna(subset=['x_scaled', 'y_scaled'])
                if subset.empty: continue
                
                if cfg.get("is_arrow"):
                    # تصفية تمريرات لضمان وجود نقطة النهاية x2 و y2
                    arrow_df = subset.dropna(subset=['x2_scaled', 'y2_scaled'])
                    if not arrow_df.empty:
                        pitch.arrows(arrow_df['x_scaled'], arrow_df['y_scaled'], arrow_df['x2_scaled'], arrow_df['y2_scaled'], color=cfg['color'], width=2, ax=ax)
                        legend_elements.append(Line2D([0], [0], color=cfg['color'], lw=2, label=act))
                else:
                    pitch.scatter(subset['x_scaled'], subset['y_scaled'], color=cfg['color'], marker=cfg['marker'], s=150, ax=ax)
                    legend_elements.append(Line2D([0], [0], marker=cfg['marker'], color='none', markeredgecolor=cfg['color'], markerfacecolor=cfg['color'], label=act, markersize=10))

            if legend_elements:
                ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, facecolor='#222222', labelcolor='white')
            
            st.pyplot(fig)
            plt.close(fig)
    else:
        st.error("⚠️ لم نتمكن من العثور على أعمدة الإحداثيات (X Start, Y Start). يرجى التأكد من أن الهيدر مكتوب في السطر الأول.")
else:
    st.info("💡 في انتظار رفع ملف البيانات لعرض لوحة التحليل التفاعلية والملعب.")
