
#  نظام مساعد لتشخيص أمراض القلب باستخدام الذكاء الاصطناعي

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.0%2B-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/AI-Machine%20Learning-purple.svg" alt="AI">
  <img src="https://img.shields.io/badge/ECG-ONNX-red.svg" alt="ECG">
  <img src="https://img.shields.io/badge/Arabic-RTL-orange.svg" alt="Arabic">
</p>



# 🏥 مساعد طبيب القلب الذكي (CardioAssist Web System)

نظام ويب متكامل ومتطور ومصمم خصيصاً لمساعدة أطباء القلب في تشخيص الأمراض وتحليل البيانات الطبية بكفاءة عالية، بالاعتماد على تقنيات التعلم الآلي والذكاء الاصطناعي.

---

## 📖 نظرة عامة

**مساعد طبيب قلبية** هو نظام ويب متكامل يساعد الأطباء في تشخيص أمراض القلب باستخدام:
- **3 نماذج تعلم آلي** للتنبؤ بأمراض القلب بناءً على البيانات السريرية.
- **3 نماذج ONNX** لتحليل صور تخطيط القلب (ECG).
- **نظام تقارير متكامل** مع توليد PDF.
- **معالجة جماعية** لتحليل مجموعات بيانات كبيرة.

---

## ✨ الميزات الرئيسية

| الميزة | الوصف |
| :--- | :--- |
| 🏥 **تشخيص فردي** | إدخال بيانات مريض واحد مع نتائج فورية. |
| 📊 **تشخيص جماعي** | رفع ملف CSV/Excel وتنفيذ تنبؤات دفعة واحدة. |
| 🧠 **تحليل ECG** | رفع صور تخطيط القلب وتحليلها باستخدام ONNX. |
| 📋 **التقارير** | بناء قوالب مخصصة وتوليد تقارير PDF. |
| 👨‍⚕️ **إدارة المرضى** | عرض وإدارة جميع المرضى المسجلين. |

---

## 🧠 النماذج المستخدمة

### أولاً: نماذج تشخيص أمراض القلب (Tabular Models)

| النموذج | الميزات | الخوارزمية | الاستخدام |
| :--- | :--- | :--- | :--- |
| **المبسط** | 4 ميزات | Logistic Regression | تنبؤ سريع وفحص أولي. |
| **المتوسط** | 8 ميزات | Random Forest | توازن بين الدقة والسرعة. |
| **الشامل** | 11 ميزة | KNN | أعلى دقة وتجهيز تشخيص عميق. |

### ثانياً: نماذج تحليل تخطيط القلب (ECG ONNX Models)

| اسم ملف النموذج السحابي | نوع النموذج وتخصصه البرمجي | الدور التشخيصي في النظام |
| :--- | :--- | :--- |
| `binary.onnx` | **النموذج الخفيف** (Simple) | تصنيف أولي سريع لإشارات ورسوم التخطيط. |
| `3classes.onnx` | **النموذج المتوسط** (Medium) | تحليل متوازن للموجات الكهربائية الأساسية. |
| `4classes.onnx` | **النموذج الشامل** (Comprehensive) | كشف دقيق عن الاختلالات المعقدة في ضربات القلب. |

> 📥 **تحميل النماذج**: يمكنك تحميل ملفات النماذج الستة كاملة مباشرة عبر الرابط التالي وضبطها في مسارها المحدد أدناه: [Google Drive Folder](https://drive.google.com/drive/folders/1Mgve4IwWW5iGVs87ZnW3bW6qm6Dt5L5X?usp=sharing)

---

## 🚀 البدء السريع

### المتطلبات الأساسية
- Python 3.9+
- pip (مدير حزم بايثون)

### خطوات التثبيت والتشغيل

1. **استنساخ المشروع والدخول إلى مجلد العمل:**
   ```bash
   git clone <repository-url>
   cd HEART_FLASK
   ```

2. **إنشاء بيئة افتراضية وتفعيلها:**
   * **على أنظمة Linux/Mac:**
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   * **على نظام Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **تثبيت المكتبات والاعتماديات المطلوبة:**
   ```bash
   pip install -r requirements.txt
   ```

4. **تثبيت النماذج الذكية:**
   * قم بتحميل ملفات الامتداد (`.pkl`) و (`.onnx`) من رابط Google Drive.
   * انقل جميع الملفات الستة إلى المجلد التالي في مشروعك: `storage/models/`.

5. **تشغيل التطبيق:**
   ```bash
   python app.py
   ```
   * افتح متصفح الويب وانتقل إلى الرابط المحلي: `http://127.0.0.1:5000`

---
## 🏗️ الهندسة المعمارية
مشروع متكامل للتنبؤ بأمراض القلب وتحليل البيانات باستخدام إطار العمل **Flask** وبتصميم معماري يعتمد على فصل الطبقات (Layered Architecture).

## 📁 هيكلية المشروع (Project Architecture)

```text
HEART_FLASK/
│
├── 📄 app.py               # نقطة الدخول الرئيسية للتطبيق (Main Entry Point)
├── 📄 config.py            # إعدادات التطبيق العامة
├── 📄 requirements.txt     # المكتبات والمتطلبات اللازمة للتشغيل
├── 📄 .env                 # متغيرات البيئة السرية (Environment Variables)
├── 📄 .gitignore           # الملفات والمجلدات المتجاهلة في Git
│
├── 📁 application/         # 🎯 طبقة التطبيق (Controller Layer)
│   ├── 📁 dtos/            # كائنات نقل البيانات (Data Transfer Objects)
│   ├── 📁 exceptions/      # معالجة الاستثناءات والأخطاء المخصصة
│   └── 📁 routes/          # مسارات وإشارات التطبيق (API Endpoints)
│
├── 📁 business/            # 💼 طبقة الأعمال المنطقية (Business Logic Layer)
│   ├── 📁 config/          # إعدادات منطق الأعمال
│   ├── 📁 factories/       # مصانع إنشاء الكائنات (Factory Pattern)
│   ├── 📁 services/        # الخدمات البرمجية الأساسية
│   └── 📁 strategies/      # استراتيجيات وخوارزميات التنبؤ (Strategy Pattern)
│
├── 📁 infrastructure/      # 🏛️ طبقة البنية التحتية (Infrastructure Layer)
│   ├── 📁 models/          # نماذج وجداول قاعدة البيانات (ORM Models)
│   ├── 📁 repositories/    # مستودعات الوصول إلى البيانات (Repository Pattern)
│   └── 📁 logs/            # ملفات سجلات النظام والتتبع
│
├── 📁 presentation/        # 🎨 طبقة العرض والواجهات (Presentation Layer)
│   ├── 📁 static/          # الملفات الثابتة (CSS, JS, Images)
│   └── 📁 templates/       # قوالب العرض (HTML Templates / Jinja2)
│
├── 📁 storage/             # 💾 طبقة التخزين والبيانات (Storage & Data)
│   ├── 📁 data/            # ملفات البيانات الخام والمُعالجة (CSV Files)
│   ├── 📁 models/          # نماذج ذكاء الآلة المدربة وجاهزة للاستخدام (ML Models)
│   ├── 📁 uploads/         # الملفات والمستندات المرفوعة من قبل المستخدمين
│   └── 📁 reports/         # التقارير الطبية والإحصائية الصادرة (PDF Reports)
│
└── 📁 tests/               # 🧪 طبقة الاختبارات (Unit & Integration Tests)
```




