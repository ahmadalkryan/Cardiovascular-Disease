Link To  Models https://drive.google.com/drive/folders/1Mgve4IwWW5iGVs87ZnW3bW6qm6Dt5L5X?usp=sharing
# 🫀 HEART_FLASK - نظام تشخيص أمراض القلب بالذكاء الاصطناعي

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.0%2B-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/AI-Machine%20Learning-purple.svg" alt="AI">
  <img src="https://img.shields.io/badge/ECG-ONNX-red.svg" alt="ECG">
  <img src="https://img.shields.io/badge/Arabic-RTL-orange.svg" alt="Arabic">
</p>

---

## 📖 نظرة عامة

**HEART_FLASK** هو نظام متكامل لتشخيص أمراض القلب باستخدام تقنيات الذكاء الاصطناعي وتعلم الآلة. يوفر النظام واجهة سهلة الاستخدام للأطباء لتشخيص أمراض القلب من خلال ثلاث نماذج تعلم آلي مختلفة، بالإضافة إلى تحليل صور تخطيط القلب (ECG) باستخدام نماذج ONNX العميقة.

### ✨ المميزات الرئيسية

| الميزة | الوصف |
|--------|-------|
| 🧠 **ثلاثة نماذج تشخيص** | Minimal (4 ميزات)، Top8 (8 ميزات)، All11 (11 ميزة) |
| 📊 **تحليل ECG** | استخدام نماذج DenseNet و ONNX لتحليل صور تخطيط القلب |
| 📤 **معالجة مجمعة** | رفع ملفات CSV/Excel للتنبؤ الجماعي |
| 📋 **تقارير طبية** | إنشاء تقارير PDF مخصصة مع قوالب مرنة |
| 👨‍⚕️ **تعديل يدوي** | إمكانية تعديل التشخيص من قبل الطبيب |
| 🌐 **واجهة عربية** | دعم كامل للغة العربية مع تصميم متجاوب |
| 📊 **لوحة تحكم** | إحصائيات ورسوم بيانية لحالة المرضى |

---

## 🏗️ الهندسة المعمارية

<p align="center">
  <img src="https://via.placeholder.com/800x400/667eea/ffffff?text=Architecture+Diagram" alt="Architecture">

  # 🫀 نظام مساعد طبيب القلب لتشخيص أمراض القلب

نظام ذكي لتشخيص أمراض القلب والأوعية الدموية يعتمد على تقنيات الذكاء الاصطناعي وتعلم الآلة.

---

## 📖 نظرة عامة

**مساعد طبيب قلبية** هو نظام ويب متكامل يساعد الأطباء في تشخيص أمراض القلب باستخدام:
- **3 نماذج تعلم آلي** للتنبؤ بأمراض القلب
- **3 نماذج ONNX** لتحليل صور تخطيط القلب (ECG)
- **نظام تقارير متكامل** مع توليد PDF
- **معالجة جماعية** لتحليل مجموعات بيانات كبيرة

---

## ✨ الميزات الرئيسية

| الميزة | الوصف |
|--------|-------|
| 🏥 **تشخيص فردي** | إدخال بيانات مريض واحد مع نتائج فورية |
| 📊 **تشخيص جماعي** | رفع ملف CSV/Excel وتنفيذ تنبؤات دفعة واحدة |
| 🧠 **تحليل ECG** | رفع صور تخطيط القلب وتحليلها باستخدام ONNX |
| 📋 **التقارير** | بناء قوالب مخصصة وتوليد تقارير PDF |
| 👨‍⚕️ **إدارة المرضى** | عرض وإدارة جميع المرضى المسجلين |

---

## 🧠 النماذج المستخدمة

### نماذج تشخيص أمراض القلب

| النموذج | الميزات | الخوارزمية | الاستخدام |
|---------|---------|------------|-----------|
| **المبسط** | 4 ميزات | Logistic Regression | تنبؤ سريع |
| **المتوسط** | 8 ميزات | Random Forest | توازن بين الدقة والسرعة |
| **الشامل** | 11 ميزة | KNN | أعلى دقة |

### نماذج تحليل ECG (ONNX)

| النموذج | التصنيف | الدقة | الملف |
|---------|---------|-------|-------|
| DenseNet Binary | طبيعي / غير طبيعي | ~95% | `binary.onnx` |
| DenseNet Multiclass | 3 فئات | ~94% | `3class.onnx` |
| ONNX Original | 4 فئات | 94.29% | `4class.onnx` |

> 📥 **تحميل النماذج**: [Google Drive](https://drive.google.com/drive/folders/1Mgve4IwWW5iGVs87ZnW3bW6qm6Dt5L5X?usp=sharing)

---

## 🚀 البدء السريع

### المتطلبات
- Python 3.9+
- pip

### خطوات التثبيت

```bash
# 1. استنساخ المشروع
git clone <repository-url>
cd HEART_FLASK

# 2. إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. تثبيت المتطلبات
pip install -r requirements.txt

# 4. تحميل النماذج ووضعها في storage/models/

# 5. تشغيل التطبيق
python app.py
</p>

يتبع المشروع **الهندسة ثلاثية الطبقات (3-Tier Architecture)** مع طبقة رابعة للبنية التحتية
