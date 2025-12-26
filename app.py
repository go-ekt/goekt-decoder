import streamlit as st
import google.generativeai as genai
import base64
import os

# --- 1. إعدادات الصفحة (Page Config) ---
st.set_page_config(
    page_title="GoEKT Paper Decoder",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. محرك الخطوط الذكي (Font Engine) ---
def load_font(font_path):
    """دالة لقراءة ملف الخط وتحويله لـ Base64 ليعمل على الويب"""
    try:
        with open(font_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# مسارات الخطوط (تأكد من رفعها في مجلد fonts على GitHub)
font_paths = {
    "KOLab-Bold": "fonts/KOLab-Bold.woff2",
    "KOSans-Bold": "fonts/KOSans-Bold.woff2",
    "KOSans-Regular": "fonts/KOSans-Regular.woff2",
    "KOSans-Light": "fonts/KOSans-Light.woff2"
}

# توليد CSS للخطوط
font_css = ""
# محاولة تحميل KO Lab
if font_b64 := load_font(font_paths["KOLab-Bold"]):
    font_css += f"""
    @font-face {{
        font-family: 'KO Lab';
        src: url(data:font/woff2;base64,{font_b64}) format('woff2');
        font-weight: 700;
    }}
    """
# محاولة تحميل KO Sans (Regular, Bold, Light)
if font_b64 := load_font(font_paths["KOSans-Regular"]):
    font_css += f"""
    @font-face {{
        font-family: 'KO Sans';
        src: url(data:font/woff2;base64,{font_b64}) format('woff2');
        font-weight: 400;
    }}
    """
if font_b64 := load_font(font_paths["KOSans-Bold"]):
    font_css += f"""
    @font-face {{
        font-family: 'KO Sans';
        src: url(data:font/woff2;base64,{font_b64}) format('woff2');
        font-weight: 700;
    }}
    """
if font_b64 := load_font(font_paths["KOSans-Light"]):
    font_css += f"""
    @font-face {{
        font-family: 'KO Sans';
        src: url(data:font/woff2;base64,{font_b64}) format('woff2');
        font-weight: 300;
    }}
    """

# fallback إذا لم يتم رفع الخطوط بعد
fallback_fonts = "sans-serif" if not font_css else "'KO Sans', sans-serif"
heading_fonts = "sans-serif" if not font_css else "'KO Lab', sans-serif"

# --- 3. نظام التصميم (Design System) ---
st.markdown(f"""
    <style>
    {font_css}

    :root {{
        /* ألوان GoEKT الصارمة */
        --goekt-primary: #E935C1;
        --goekt-secondary: #2AB7A9;
        --goekt-dark: #0B2B40;
        --goekt-text: #FFFFFF;
        
        --goekt-gradient: linear-gradient(135deg, #E935C1 0%, #2AB7A9 100%);
    }}

    .stApp {{
        background-color: var(--goekt-dark);
        font-family: {fallback_fonts};
    }}

    /* العناوين بـ KO Lab */
    h1, h2, h3 {{
        font-family: {heading_fonts} !important;
        background: var(--goekt-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        text-align: right;
    }}
    
    /* النصوص بـ KO Sans */
    p, li, .stMarkdown, label, .stTextArea textarea {{
        font-family: {fallback_fonts} !important;
        color: var(--goekt-text) !important;
        text-align: right;
        direction: rtl;
    }}

    /* تحسينات الواجهة */
    .stButton button {{
        background: var(--goekt-gradient) !important;
        color: white !important;
        font-family: {heading_fonts} !important;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 8px;
        transition: transform 0.2s;
        width: 100%;
    }}
    .stButton button:hover {{
        transform: scale(1.02);
    }}
    
    .stTextArea textarea {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--goekt-secondary) !important;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# --- 4. المنطق (API & Logic) ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.warning("⚠️ يرجى إضافة مفتاح API في Secrets")
    st.stop()

def goekt_translate(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    sys_prompt = """
    أنت 'GoEKT Paper Decoder'. مهمتك: ترجمة الأوراق العلمية للعربية بدقة.
    القواعد:
    1. اكتب المصطلح الإنجليزي بين قوسين بجوار العربي: الشبكات (Networks).
    2. حافظ على النغمة الأكاديمية الرصينة.
    3. استخدم Markdown للتنسيق.
    """
    try:
        return model.generate_content(f"{sys_prompt}\n\nالنص:\n{text}").text
    except Exception as e:
        return f"خطأ: {e}"

# --- 5. الواجهة (UI) ---
col1, col2 = st.columns([1, 4])
with col2:
    st.markdown("# 🧬 GoEKT Paper Decoder")
    st.markdown(f"**Empower. Knowledge. Transform.** | الإصدار v1.0 Pro")

st.markdown("---")

col_in, col_out = st.columns([1, 1])
with col_in:
    st.markdown("### 📥 النص الإنجليزي")
    src = st.text_area("Original Text", height=400, label_visibility="collapsed")
    btn = st.button("ترجمة علمية فورية ⚡")

with col_out:
    st.markdown("### 📤 الترجمة العربية")
    if btn and src:
        with st.spinner("جاري المعالجة..."):
            res = goekt_translate(src)
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; border-right:3px solid #2AB7A9;">
            {res}
            </div>
            """, unsafe_allow_html=True)
            st.success("تمت الترجمة بنجاح")
    elif btn:
        st.warning("أدخل النص أولاً")

st.markdown("---")
st.markdown("<div style='text-align:center; color:#2AB7A9; direction:ltr'>GoEKT Systems © 2026</div>", unsafe_allow_html=True)
