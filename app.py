import streamlit as st
import requests
from deep_translator import GoogleTranslator

# 1. إعدادات الصفحة
st.set_page_config(page_title="مفسر الأحلام النفسي", page_icon="🌙", layout="centered")

# 2. جلب المفتاح من الخزنة
try:
    api_token = st.secrets["HUGGINGFACE_TOKEN"]
except:
    st.error("⚠️ لم يتم العثور على المفتاح! تأكد من إضافته في Secrets.")
    st.stop()

# 3. دالة الاتصال بالذكاء الاصطناعي (نستخدم موديل ذكي للنصوص)
def query_ai(payload):
    headers = {"Authorization": f"Bearer {api_token}"}
    # نستخدم موديل Mistral القوي والسريع للنصوص
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

# 4. تنسيق الواجهة (ستايل عربي أنيق)
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextArea textarea {
        font-size: 18px !important;
        text-align: right;
        direction: rtl;
    }
    .stButton>button {
        background-color: #6C63FF; 
        color: white; 
        width: 100%;
        border-radius: 10px;
        font-size: 20px;
        font-weight: bold;
        padding: 10px;
    }
    h1, h3, p { text-align: center; }
    .result-box {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-right: 5px solid #6C63FF;
        text-align: right;
        direction: rtl;
        margin-top: 20px;
        font-size: 18px;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# 5. واجهة التطبيق
st.title("🌙 مفسر الأحلام النفسي")
st.markdown("### حلل أحلامك من منظور نفسي وعلمي")
st.write("---")

# صندوق إدخال الحلم
dream_text = st.text_area("اكتب تفاصيل حلمك هنا:", height=150, placeholder="مثال: حلمت أنني أطير فوق البحر وكان الجو عاصفاً...")

if st.button("فسّر الحلم الآن ✨"):
    if dream_text:
        with st.spinner('جاري استشارة الذكاء الاصطناعي... 🧠'):
            try:
                # خطوة 1: ترجمة الحلم للإنجليزية ليفهمه الموديل بدقة
                translator_to_en = GoogleTranslator(source='auto', target='en')
                dream_en = translator_to_en.translate(dream_text)

                # خطوة 2: تجهيز السؤال للطبيب النفسي (Prompt)
                prompt = f"""
                Act as a professional and empathetic psychologist. 
                Interpret the following dream briefly. Focus on emotions, hidden anxieties, and give a positive psychological advice.
                Dream: "{dream_en}"
                Interpretation:
                """

                # خطوة 3: إرسال الطلب
                response = query_ai({"inputs": prompt, "parameters": {"max_new_tokens": 250, "return_full_text": False}})
                
                # استخراج النص الناتج
                if isinstance(response, list) and 'generated_text' in response[0]:
                    ai_reply_en = response[0]['generated_text']
                    
                    # خطوة 4: ترجمة التفسير للعربية
                    translator_to_ar = GoogleTranslator(source='en', target='ar')
                    ai_reply_ar = translator_to_ar.translate(ai_reply_en)

                    # عرض النتيجة
                    st.success("تم التحليل بنجاح!")
                    st.markdown(f'<div class="result-box"><b>🔮 التفسير النفسي:</b><br>{ai_reply_ar}</div>', unsafe_allow_html=True)
                
                else:
                    st.error("السيرفر مشغول قليلاً، حاول الضغط مرة أخرى!")
                    
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
    else:
        st.warning("الرجاء كتابة الحلم أولاً!")

# التذييل
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>© 2026 تم التطوير بواسطة <b>مقتدى سامي</b> (قسم علم النفس)</div>", unsafe_allow_html=True)
              
