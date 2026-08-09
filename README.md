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
</p>

يتبع المشروع **الهندسة ثلاثية الطبقات (3-Tier Architecture)** مع طبقة رابعة للبنية التحتية:
