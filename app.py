import streamlit as st
import google.generativeai as genai

# --- 1. إعدادات الصفحة والهوية ---
st.set_page_config(
    page_title="GoEKT Paper Decoder",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. سحب مفتاح API من المخزن السري (Secrets) ---
# هذا يجعل الأداة تعمل فوراً للعميل دون إدخال مفاتيح
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except FileNotFoundError:
    st.error("⚠️ لم يتم العثور على مفتاح API. يرجى إضافته في إعدادات Streamlit Secrets.")
    st.stop()

# --- 3. تصميم GoEKT (CSS Injection) ---
st.markdown("""
    <style>
    /* استيراد خط تجريبي يشبه Changa/Cairo */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

    /* الألوان الأساسية */
    :root {
        --primary: #0A192F;
        --secondary: #172a45;
        --accent: #64FFDA;
        --text: #CCD6F6;
        --cta: #C026D3;
    }

    /* تطبيق الخلفية والخطوط */
    .stApp {
        background-color: var(--primary);
        font-family: 'Cairo', sans-serif;
    }

    /* العناوين */
    h1, h2, h3, h4 {
        color: var(--accent) !important;
        font-family: 'Cairo', sans-serif;
        font-weight: 700;
    }

    /* النصوص العادية */
    p, label, .stMarkdown {
        color: var(--text) !important;
    }

    /* حقول الإدخال */
    .stTextArea textarea {
        background-color: var(--secondary) !important;
        color: white !important;
        border: 1px solid var(--accent) !important;
        border-radius: 8px;
    }

    /* الأزرار (CTA) */
    .stButton button {
        background: linear-gradient(90deg, var(--accent), var(--cta)) !important;
        color: var(--primary) !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 2rem !important;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        opacity: 0.9;
        transform: scale(1.02);
    }
    
    /* إخفاء القوائم الافتراضية لستريم ليت لتبدو كأنها تطبيق خاص */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 4. العقل المدبر (The Brain Logic) ---
def goekt_translate(text):
    # إعدادات الموديل
    model = genai.GenerativeModel('gemini-1.5-flash') # نستخدم Flash لسرعة ورخص التكلفة
    
    # الـ System Prompt الصارم
    system_instruction = """
    You are the 'GoEKT Scientific Decoder'. Translate the following English academic text to Arabic.
    
    STRICT RULES:
    1. Keep scientific terms in English brackets: e.g., الشبكات العصبية (Neural Networks).
    2. Tone: Academic, professional, objective.
    3. Format: Use Markdown with bold headings.
    4. Output Structure:
       - **العنوان بالعربية**
       - **المصطلحات المفتاحية:** (List key terms translated)
       - **الترجمة:** (The full translation)
    """
    
    try:
        response = model.generate_content(f"{system_instruction}\n\nTEXT TO TRANSLATE:\n{text}")
        return response.text
    except Exception as e:
        return f"حدث خطأ في الاتصال: {str(e)}"

# --- 5. واجهة المستخدم (UI Layout) ---

# الهيدر والشعار
col_logo, col_title = st.columns([1, 6])
with col_title:
    st.markdown("# GoEKT Paper Decoder")
    st.markdown("**Empower. Knowledge. Transform.** | المترجم الأكاديمي الذكي")

st.markdown("---")

# منطقة العمل
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📄 النص الأصلي (English)")
    source_text = st.text_area("ألصق النص أو فقرة من الورقة البحثية هنا...", height=400, label_visibility="collapsed")
    
    # زر الترجمة
    translate_click = st.button("ترجمة علمية فورية ⚡")

with col2:
    st.markdown("### 🧬 الترجمة (Arabic)")
    
    # حاوية النتائج
    result_container = st.container()
    
    if translate_click and source_text:
        with result_container:
            with st.spinner('جاري تحليل المصطلحات وتفكيك النص...'):
                translation = goekt_translate(source_text)
                st.markdown(translation)
                st.success("✅ تمت الترجمة بدقة GoEKT")
    elif not source_text and translate_click:
        st.warning("يرجى إدخال نص أولاً!")
    else:
        with result_container:
            st.info("النتائج ستظهر هنا...")

# الفوتر
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64FFDA; font-size: 0.8rem;'>
    GoEKT Systems v1.0 © 2026 | Built for the Future
</div>
""", unsafe_allow_html=True)
