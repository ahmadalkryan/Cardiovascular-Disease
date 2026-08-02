
# business/services/ai_service.py
"""AI Service - OpenRouter API for medical interpretation"""

import requests
from config import Config 
# from infrastructure.config import Config

class AIService:
    """AI Service for medical interpretation using OpenRouter API"""
    
    def __init__(self, api_key, api_url, model_name):
        self.api_key = api_key
        self.api_url = api_url
        self.model_name = model_name
        self.available = False
        self._check_connection()
    
    def _check_connection(self):
        """Test API connection"""
        try:
            headers = self._get_headers()
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": "Test"}],
                "max_tokens": 5
            }
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=15)
            self.available = response.status_code == 200
            if self.available:
                print(f"✅ AI model is working successfully!")
        except Exception as e:
            self.available = False
            print(f"⚠️ AI connection failed: {e}")
    
    def _get_headers(self):
        """Build HTTP headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://heart-diagnosis-system.com",
            "X-OpenRouter-Title": "Heart Disease Diagnosis System"
        }
    
    def call(self, messages, temperature=0.7):
        """Call AI model"""
        if not self.available:
            return None
        
        headers = self._get_headers()
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 2000,
            "top_p": 0.9
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"AI call error: {e}")
        return None
    
    # call remote AI Model 
    
    def get_interpretation(self, patient_data, prediction_result, probability, model_name):
        """Generate medical interpretation"""
        if not self.available:
            return None
        
        age = patient_data.get('age', 'غير محدد')
        sex = "ذكر" if patient_data.get('sex') == 1 else "أنثى"
        bp = patient_data.get('resting bp s', 'غير محدد')
        cholesterol = patient_data.get('cholesterol', 'غير محدد')
        max_hr = patient_data.get('max heart rate', 'غير محدد')
        exercise_angina = "نعم" if patient_data.get('exercise angina') == 1 else "لا"
        oldpeak = patient_data.get('oldpeak', 'غير محدد')
        st_slope = patient_data.get('ST slope', 'غير محدد')
        chest_pain = patient_data.get('chest pain type', 'غير محدد')
        fasting_sugar = "مرتفع" if patient_data.get('fasting blood sugar') == 1 else "طبيعي"
        resting_ecg = patient_data.get('resting ecg', 'غير محدد')
        
        if probability > 0.7:
            risk_level = "مرتفع 🔴"
            risk_desc = "خطر مرتفع للإصابة بأمراض القلب"
        elif probability > 0.3:
            risk_level = "متوسط 🟡"
            risk_desc = "خطر متوسط للإصابة بأمراض القلب"
        else:
            risk_level = "منخفض 🟢"
            risk_desc = "خطر منخفض للإصابة بأمراض القلب"
        
        model_display = Config.MODELS_INFO.get(model_name, {}).get('display_name', model_name)
        
        system_prompt = """أنت طبيب قلب متخصص. مهمتك تفسير نتائج نموذج التعلم الآلي وتقديم:
                1. تحليل أسباب النتيجة بناءً على بيانات المريض
                2. توصيات وقائية وعلاجية مخصصة
                3. تغييرات في نمط الحياة
                4. متى يجب مراجعة الطبيب

                كن دقيقاً ومهنياً، وتحدث باللغة العربية الفصحى الواضحة."""

        user_prompt = f"""تم تحليل بيانات مريض باستخدام {model_display} وكانت النتائج كالتالي:

                📊 **بيانات المريض:**
                - العمر: {age} سنة
                - الجنس: {sex}
                - ضغط الدم الانقباضي: {bp} مم زئبق
                - مستوى الكوليسترول: {cholesterol} ملغم/دل
                - سكر الدم الصائم: {fasting_sugar}
                - أقصى معدل لضربات القلب: {max_hr} نبضة/دقيقة
                - وجود ذبحة أثناء الجهد: {exercise_angina}
                - انخفاض مقطع ST: {oldpeak}
                - ميل مقطع ST: {st_slope}
                - نوع ألم الصدر: {chest_pain}
                - تخطيط القلب: {resting_ecg}

                📈 **نتائج النموذج الآلي:**
                - التشخيص: {risk_desc}
                - مستوى الخطر: {risk_level}
                - نسبة الاحتمالية: {probability*100:.1f}%

                📝 **المطلوب منك كطبيب:**
                1. **تحليل الأسباب:** ما العوامل في بيانات المريض التي أدت إلى هذا التشخيص؟
                2. **التوصيات الطبية:** ما الإجراءات التي يجب على المريض اتخاذها؟
                3. **نصائح الوقاية:** تغييرات في نمط الحياة والنظام الغذائي
                4. **متى يراجع الطبيب:** هل الحالة تستدعي مراجعة فورية؟"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self.call(messages)