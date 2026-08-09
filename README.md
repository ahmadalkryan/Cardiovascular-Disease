
#  نظام مساعد لتشخيص أمراض القلب باستخدام الذكاء الاصطناعي

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.0%2B-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/AI-Machine%20Learning-purple.svg" alt="AI">
  <img src="https://img.shields.io/badge/ECG-ONNX-red.svg" alt="ECG">
  <img src="https://img.shields.io/badge/Arabic-RTL-orange.svg" alt="Arabic">
</p>


## 📖 نظرة عامة

**  نظام مساعد لتشخيص أمراض القلب باستخدام الذكاء الاصطناعي
** هو نظام متكامل لتشخيص أمراض القلب باستخدام تقنيات الذكاء الاصطناعي وتعلم الآلة. يوفر النظام واجهة سهلة الاستخدام للأطباء لتشخيص أمراض القلب من خلال ثلاث نماذج تعلم آلي مختلفة، بالإضافة إلى تحليل صور تخطيط القلب (ECG) باستخدام نماذج ONNX العميقة.

### ✨ المميزات الرئيسية
```text
| الميزة | الوصف |

| 🧠 **ثلاثة نماذج تشخيص** | Minimal (4 ميزات)، Top8 (8 ميزات)، All11 (11 ميزة) |
| 📊 **تحليل ECG** | استخدام نماذج DenseNet و ONNX لتحليل صور تخطيط القلب |
| 📤 **معالجة مجمعة** | رفع ملفات CSV/Excel للتنبؤ الجماعي |
| 📋 **تقارير طبية** | إنشاء تقارير PDF مخصصة مع قوالب مرنة |
| 👨‍⚕️ **تعديل يدوي** | إمكانية تعديل التشخيص من قبل الطبيب |
| 🌐 **واجهة عربية** | دعم كامل للغة العربية مع تصميم متجاوب |
| 📊 **لوحة تحكم** | إحصائيات ورسوم بيانية لحالة المرضى |


```
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

## 🚀 البدء بالعمل (Getting Started)

### 1. المتطلبات الأساسية
تأكد من تثبيت بيئة عمل Python (الإصدار 3.8 أو أحدث).

### 2. تثبيت المشروع محلياً
قم بإنشاء بيئة افتراضية وتثبيت المكتبات المطلوبة عبر تشغيل الأوامر التالية:

```bash
# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة الافتراضية (Windows)
venv\Scripts\activate

# تفعيل البيئة الافتراضية (Mac/Linux)
source venv/bin/activate

# تثبيت المكتبات
pip install -r requirements.txt
```




### 4. تشغيل التطبيق
```bash
flask run
```


## 🚀 البدء السريع

### المتطلبات الأساسية
- Python 3.9+
- pip
- Git (اختياري)

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

# 4. تحميل النماذج
# قم بتحميل النماذج من Google Drive ووضعها في مجلد storage/models/

# 5. تشغيل التطبيق
python app.py
<p align="center">
  <img src="https://via.placeholder.com/800x400/667eea/ffffff?text=Architecture+Diagram" alt="Architecture">

  # 🫀 نظام مساعد طبيب القلب لتشخيص أمراض القلب

نظام ذكي لتشخيص أمراض القلب والأوعية الدموية يعتمد على تقنيات الذكاء الاصطناعي وتعلم الآلة.

---

## ✨ الميزات الرئيسية

| الميزة | الوصف |
| :--- | :--- |
| 🏥 **تشخيص فردي** | إدخال بيانات مريض واحد يدويًا والحصول على نتائج وتحليلات فورية. |
| 📊 **تشخيص جماعي** | رفع ملفات (CSV/Excel) وتنفيذ تنبؤات ذكية لعدد كبير من المرضى دفعة واحدة. |
| 🧠 **تحليل ECG** | رفع صور تخطيط القلب وتحليلها آلياً للكشف عن الاختلالات بواسطة نماذج الرؤية الحاسوبية. |
| 📋 **نظام التقارير** | بناء وتخصيص قوالب التقارير الطبية وتوليدها بصيغة PDF جاهزة للطباعة. |
| 👨‍⚕️ **إدارة المرضى** | سجل رقمي شامل لعرض، وتعديل، ومتابعة التاريخ الطبي للمرضى المسجلين. |

---

## 🧠 النماذج الذكية المستخدمة

### 1. نماذج تشخيص أمراض القلب (Tabular Data)

| النموذج | عدد الميزات | الخوارزمية المستخدمة | ميزة النموذج |
| :--- | :--- | :--- | :--- |
| **المبسط** | 4 ميزات | Logistic Regression | فحص مبدئي وتنبؤ فائق السرعة |
| **المتوسط** | 8 ميزات | Random Forest | توازن ممتاز بين الدقة وسرعة المعالجة |
| **الشامل** | 11 ميزة | KNN | تحليل عميق وأعلى دقة تشخيصية ممكنة |

### 2. نماذج تحليل تخطيط القلب (ECG ONNX Models)

| النموذج | نوع الشبكة | الوظيفة والتشخيص |
| :--- | :--- | :--- |
| **ECG Classifier** | ResNet / CNN | تصنيف الإشارات واكتشاف عدم انتظام ضربات القلب (Arrhythmia) |
| **Anomaly Detector** | Autoencoder | اكتشاف الأنماط غير الطبيعية والنادرة في رسم القلب |
| **Segmenter** | U-Net | تحديد وتفكيك الموجات الرئيسية (P, QRS, T) بدقة |

> 📥 **تحميل النماذج الطبية**: يمكنك تحميل جميع النماذج المدربة مسبقاً مباشرة من [Google Drive](https://drive.google.com/drive/folders/1Mgve4IwWW5iGVs87ZnW3bW6qm6Dt5L5X?usp=sharing) وضعها في مسارها المخصص.

---

## 🚀 البدء السريع بالتنبؤ والتشغيل

### المتطلبات الأساسية
- **Python 3.9+**
- **pip** (مدير حزم بايثون)

### خطوات التثبيت والتشغيل

1. **استنساخ المشروع ودخول المجلد:**
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

3. **تثبيت المكتبات المطلوبة:**
   ```bash
   pip install -r requirements.txt
   ```

4. **إعداد النماذج:**
   * قم بتحميل النماذج من رابط Google Drive أعلاه.
   * انقل الملفات المحملة إلى المجلد المخصص لها داخل المشروع: `storage/models/`.

5. **تشغيل خادم الويب (Flask):**
   ```bash
   python app.py
   ```


