import streamlit as st
import requests
from deep_translator import GoogleTranslator

# 1. إعدادات الصفحة
st.set_page_config(page_title="مفسر الأحلام النفسي", page_icon="🌙", layout="centered")

# 2. جلب المفتاح
try:
    api_token = st.secrets["HUGGINGFACE_TOKEN"]
except:
    st.error("⚠️ لم يتم العثور على المفتاح! تأكد من إضافته في Secrets.")
    st.stop()

# 3. دالة الاتصال (تم التغيير لموديل Zephyr السريع)
def query_ai(payload):
    headers = {"Authorization": f"Bearer {api_token}"}
    # هنا استخدمنا موديل Zephyr بدلاً من Mistral لأنه أسرع
    api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

# 4. التنسيق
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stTextArea textarea { font-size: 18px !important; text-align: right; direction: rtl; }
    .stButton>button { background-color: #6C63FF; color: white; width: 100%; border-radius: 10px; padding: 10px; font-weight: bold;}
    .result-box { background-color: #1f2937; padding: 20px; border-radius: 10px; border-right: 5px solid #6C63FF; text-align: right; direction: rtl; margin-top: 20px; font-size: 18px; line-height: 1.8; }
</style>
""", unsafe_allow_html=True)

st.title("🌙 مفسر الأحلام النفسي")
st.markdown("### اكتب حلمك وسأحلله لك نفسياً")

dream_text = st.text_area("اكتب تفاصيل الحلم:", height=150)

if st.button("فسّر الحلم الآن ✨"):
    if dream_text:
        with st.spinner('جاري التحليل... 🧠'):
            try:
                # ترجمة
                translator = GoogleTranslator(source='auto', target='en')
                dream_en = translator.translate(dream_text)

                # تجهيز الطلب
                prompt = f"<|system|>You are a helpful psychologist assistant. Interpret the dream briefly.<|user|>{dream_en}<|assistant|>"

                # إرسال
                response = query_ai({"inputs": prompt, "parameters": {"max_new_tokens": 300, "return_full_text": False}})
                
                if isinstance(response, list) and 'generated_text' in response[0]:
                    ai_reply = response[0]['generated_text']
                    # تعريب الجواب
                    translator_ar = GoogleTranslator(source='en', target='ar')
                    final_reply = translator_ar.translate(ai_reply)
                    
                    st.success("تم التفسير!")
                    st.markdown(f'<div class="result-box">{final_reply}</div>', unsafe_allow_html=True)
                else:
                    st.error("الموديل مشغول جداً حالياً، حاول الضغط مرة أخرى بعد ثواني.")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
                
