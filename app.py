import streamlit as st
import requests
import time
from deep_translator import GoogleTranslator

# 1. إعدادات الصفحة
st.set_page_config(page_title="مفسر الأحلام", page_icon="🌙", layout="centered")

# 2. جلب المفتاح
try:
    api_token = st.secrets["HUGGINGFACE_TOKEN"]
except:
    st.error("⚠️ المفتاح غير موجود! تأكد من Secret.")
    st.stop()

# 3. دالة الاتصال (مع كود الإلحاح)
def query_with_retry(payload):
    headers = {"Authorization": f"Bearer {api_token}"}
    api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    
    # نحاول 5 مرات قبل ما نستسلم
    for i in range(5):
        response = requests.post(api_url, headers=headers, json=payload)
        data = response.json()
        
        # إذا نجحنا ورجعنا قائمة (يعني اكو جواب)
        if isinstance(data, list):
            return data
        
        # إذا قال السيرفر "Loading" (يعني نايم)
        if isinstance(data, dict) and "error" in data:
            wait_time = data.get("estimated_time", 10) # نشوف شكد يحتاج وقت
            st.toast(f"⏳ الموديل يجهز نفسه... انتظر {int(wait_time)} ثانية...")
            time.sleep(wait_time + 1) # ننتظر ونعيد المحاولة
            continue
            
    return {"error": "فشلت المحاولات، السيرفر مشغول جداً"}

# 4. التنسيق
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .stTextArea textarea { text-align: right; direction: rtl; font-size: 18px; }
    .stButton>button { background-color: #8A2BE2; color: white; width: 100%; font-size: 20px; }
    .result { background-color: #2b2d42; padding: 20px; border-radius: 10px; text-align: right; direction: rtl; }
</style>
""", unsafe_allow_html=True)

st.title("🌙 مفسر الأحلام الذكي")

dream = st.text_area("اكتب حلمك هنا:", height=150)

if st.button("فسّر حلمي ✨"):
    if dream:
        with st.spinner('جاري الاتصال بالطبيب النفسي... 🧠'):
            try:
                # ترجمة الحلم للإنجليزي
                trans_en = GoogleTranslator(source='auto', target='en').translate(dream)
                
                # إرسال الطلب
                prompt = f"<|system|>You are a psychologist. Interpret this dream briefly and positively.<|user|>{trans_en}<|assistant|>"
                result = query_with_retry({"inputs": prompt, "parameters": {"max_new_tokens": 250}})
                
                if isinstance(result, list):
                    ai_text = result[0]['generated_text']
                    # تنظيف النص (نحذف أي كلام إضافي من الموديل)
                    if "<|assistant|>" in ai_text:
                        ai_text = ai_text.split("<|assistant|>")[1]
                        
                    # ترجمة الجواب للعربي
                    reply_ar = GoogleTranslator(source='en', target='ar').translate(ai_text)
                    
                    st.success("تم التفسير!")
                    st.markdown(f'<div class="result">{reply_ar}</div>', unsafe_allow_html=True)
                else:
                    st.error("السيرفر عليه ضغط عالي.. حاول بعد دقيقة.")
                    
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
    else:
        st.warning("اكتب الحلم أولاً!")
