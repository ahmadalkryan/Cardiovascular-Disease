// // script.js - Professional Heart Disease Prediction

// // تعريف الميزات لكل نموذج
// const FEATURES = {
//   top3: ["ST slope", "exercise angina", "chest pain type"],
//   top5: [
//     "ST slope",
//     "exercise angina",
//     "chest pain type",
//     "oldpeak",
//     "max heart rate",
//   ],
//   all11: [
//     "age",
//     "sex",
//     "chest pain type",
//     "resting bp s",
//     "cholesterol",
//     "fasting blood sugar",
//     "resting ecg",
//     "max heart rate",
//     "exercise angina",
//     "oldpeak",
//     "ST slope",
//   ],
// };

// // الأسماء العربية للميزات
// const FEATURES_AR = {
//   "ST slope": "ميل مقطع ST",
//   "exercise angina": "ذبحة أثناء الجهد",
//   "chest pain type": "نوع ألم الصدر",
//   oldpeak: "انخفاض ST (oldpeak)",
//   "max heart rate": "أقصى معدل لضربات القلب",
//   age: "العمر",
//   sex: "الجنس",
//   "resting bp s": "ضغط الدم الانقباضي",
//   cholesterol: "الكوليسترول",
//   "fasting blood sugar": "سكر الدم الصائم",
//   "resting ecg": "تخطيط القلب",
// };

// // أوصاف الميزات
// const FEATURES_DESC = {
//   "ST slope":
//     "1 = مائل للأعلى (طبيعي), 2 = مسطح (مشبوه), 3 = مائل للأسفل (خطير)",
//   "exercise angina": "هل يعاني المريض من ألم في الصدر عند بذل مجهود؟",
//   "chest pain type":
//     "1=ذبحة نموذجية, 2=ذبحة غير نموذجية, 3=ألم غير ذبحي, 4=بدون أعراض",
//   oldpeak: "انخفاض مقطع ST (بالملليمتر) - القيم الأعلى تشير إلى خطر أكبر",
//   "max heart rate":
//     "أقصى معدل لضربات القلب (نبضة/دقيقة) - القيم الأقل تشير إلى خطر أكبر",
//   age: "العمر بالسنوات",
//   sex: "0=أنثى, 1=ذكر",
//   "resting bp s": "ضغط الدم الانقباضي (mmHg) - القيم الطبيعية 90-120",
//   cholesterol: "الكوليسترول (mg/dL) - القيم الطبيعية أقل من 200",
//   "fasting blood sugar": "0=طبيعي, 1=مرتفع",
//   "resting ecg": "0=طبيعي, 1=اضطراب, 2=تضخم",
// };

// // القيم الافتراضية
// const DEFAULT_VALUES = {
//   "ST slope": 2,
//   "exercise angina": 0,
//   "chest pain type": 4,
//   oldpeak: 0.6,
//   "max heart rate": 150,
//   age: 55,
//   sex: 1,
//   "resting bp s": 120,
//   cholesterol: 200,
//   "fasting blood sugar": 0,
//   "resting ecg": 0,
// };

// // خيارات القيم للميزات الفئوية
// const OPTIONS = {
//   "ST slope": [1, 2, 3],
//   "exercise angina": [0, 1],
//   "chest pain type": [1, 2, 3, 4],
//   sex: [0, 1],
//   "fasting blood sugar": [0, 1],
//   "resting ecg": [0, 1, 2],
// };

// let currentModel = "top5";

// // تحديث حقول الإدخال حسب النموذج المختار
// function updateInputs() {
//   const container = document.getElementById("inputs-container");
//   const features = FEATURES[currentModel];

//   let html = '<div class="inputs-grid">';

//   features.forEach((feature) => {
//     html += `
//             <div class="input-group-custom">
//                 <label>
//                     <i class="fas fa-chart-line"></i>
//                     ${FEATURES_AR[feature] || feature}
//                 </label>
//         `;

//     if (OPTIONS[feature]) {
//       html += `<select class="form-select" id="input_${feature}" data-feature="${feature}">`;
//       OPTIONS[feature].forEach((opt) => {
//         const selected = opt === DEFAULT_VALUES[feature] ? "selected" : "";
//         html += `<option value="${opt}" ${selected}>${opt}</option>`;
//       });
//       html += `</select>`;
//     } else {
//       let value = DEFAULT_VALUES[feature] || "";
//       html += `<input type="number" class="form-control" id="input_${feature}"
//                            data-feature="${feature}" value="${value}" step="any">`;
//     }

//     html += `<small class="text-muted"><i class="fas fa-info-circle me-1"></i>${FEATURES_DESC[feature] || ""}</small>`;
//     html += `</div>`;
//   });

//   html += "</div>";
//   container.innerHTML = html;
// }

// // جمع البيانات من حقول الإدخال
// function collectData() {
//   const features = FEATURES[currentModel];
//   const data = {};

//   features.forEach((feature) => {
//     const input = document.getElementById(`input_${feature}`);
//     if (input) {
//       let value = parseFloat(input.value);
//       if (isNaN(value)) value = 0;
//       data[feature] = value;
//     }
//   });

//   return data;
// }

// // عرض نتيجة التنبؤ مع تأثير حركي
// function displayResult(result) {
//   const container = document.getElementById("result-container");
//   const isHealthy = result.result === "HEALTHY";

//   let riskBadge = "";
//   if (result.risk_level === "HIGH") {
//     riskBadge = '<span class="badge bg-danger">عالي 🔴</span>';
//   } else if (result.risk_level === "MEDIUM") {
//     riskBadge = '<span class="badge bg-warning">متوسط 🟡</span>';
//   } else {
//     riskBadge = '<span class="badge bg-success">منخفض 🟢</span>';
//   }

//   container.innerHTML = `
//         <div class="result-card ${isHealthy ? "result-healthy" : "result-disease"}">
//             <div class="result-icon">
//                 ${isHealthy ? '<i class="fas fa-heartbeat"></i>' : '<i class="fas fa-exclamation-triangle"></i>'}
//             </div>
//             <div class="result-title">
//                 ${isHealthy ? '<i class="fas fa-check-circle"></i> نتيجة مطمئنة' : '<i class="fas fa-exclamation-circle"></i> تنبيه هام'}
//             </div>
//             <div class="result-probability">
//                 ${result.probability_percent}
//             </div>
//             <div class="result-risk">
//                 مستوى الخطر: ${riskBadge}
//             </div>
//             <div class="result-recommendation">
//                 <i class="fas fa-stethoscope me-2"></i>
//                 <strong>التوصية الطبية:</strong> ${result.recommendation_ar}<br>
//                 <small class="text-muted mt-2 d-flex align-items-center justify-content-center gap-3">
//                     <span><i class="fas fa-microchip"></i> النموذج: ${result.model_used}</span>
//                     <span><i class="fas fa-chart-line"></i> دقة النموذج: ${result.model_accuracy}%</span>
//                 </small>
//             </div>
//         </div>
//     `;

//   container.style.display = "block";
//   container.scrollIntoView({ behavior: "smooth", block: "nearest" });

//   // إضافة تأثير صوتي وهمي (تغيير بسيط في UI)
//   const btn = document.getElementById("predictBtn");
//   btn.style.background = isHealthy
//     ? "linear-gradient(135deg, #2ecc71, #27ae60)"
//     : "linear-gradient(135deg, #e74c3c, #c0392b)";
//   setTimeout(() => {
//     btn.style.background = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)";
//   }, 1000);
// }

// // إجراء التنبؤ مع تحسينات UI
// async function predict() {
//   // التحقق من صحة البيانات
//   const data = collectData();

//   // التحقق من الميزات المطلوبة
//   const requiredFeatures = FEATURES[currentModel];
//   const missingFeatures = requiredFeatures.filter(
//     (f) => data[f] === undefined || data[f] === null,
//   );

//   if (missingFeatures.length > 0) {
//     alert(
//       `يرجى إدخال جميع البيانات المطلوبة: ${missingFeatures.map((f) => FEATURES_AR[f] || f).join(", ")}`,
//     );
//     return;
//   }

//   const btn = document.getElementById("predictBtn");
//   const originalHTML = btn.innerHTML;
//   btn.innerHTML =
//     '<span class="spinner-border spinner-border-sm me-2"></span> جاري التحليل...';
//   btn.disabled = true;

//   document.getElementById("result-container").style.display = "none";

//   try {
//     const response = await fetch(`/predict/${currentModel}`, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(data),
//     });

//     const result = await response.json();

//     if (result.success) {
//       displayResult(result);
//     } else {
//       showError(result.error || "حدث خطأ غير متوقع");
//     }
//   } catch (error) {
//     showError("خطأ في الاتصال بالخادم. تأكد من تشغيل الخادم.");
//     console.error("Error:", error);
//   } finally {
//     btn.innerHTML = originalHTML;
//     btn.disabled = false;
//   }
// }

// // عرض رسالة خطأ
// function showError(message) {
//   const container = document.getElementById("result-container");
//   container.innerHTML = `
//         <div class="alert alert-danger">
//             <i class="fas fa-exclamation-triangle me-2"></i>
//             <strong>خطأ:</strong> ${message}
//         </div>
//     `;
//   container.style.display = "block";
//   setTimeout(() => {
//     container.style.opacity = "0";
//     setTimeout(() => {
//       container.style.display = "none";
//       container.style.opacity = "1";
//     }, 3000);
//   }, 5000);
// }

// // تغيير النموذج مع تأثير حركي
// function changeModel(model) {
//   currentModel = model;

//   document.querySelectorAll(".model-option").forEach((opt) => {
//     opt.classList.remove("active");
//     if (opt.dataset.model === model) {
//       opt.classList.add("active");
//     }
//   });

//   // تأثير انتقالي
//   const container = document.getElementById("inputs-container");
//   container.style.opacity = "0.5";

//   updateInputs();

//   setTimeout(() => {
//     container.style.opacity = "1";
//   }, 200);

//   // إخفاء النتيجة السابقة
//   document.getElementById("result-container").style.display = "none";
// }

// // تهيئة الصفحة
// document.addEventListener("DOMContentLoaded", () => {
//   // إضافة مستمعات الأحداث للنماذج
//   document.querySelectorAll(".model-option").forEach((opt) => {
//     opt.addEventListener("click", () => {
//       changeModel(opt.dataset.model);
//     });
//   });

//   // إضافة مستمع لزر التنبؤ
//   document.getElementById("predictBtn").addEventListener("click", predict);

//   // إضافة تأثير Enter للتنبؤ
//   document.addEventListener("keypress", (e) => {
//     if (e.key === "Enter" && document.activeElement.tagName !== "BUTTON") {
//       document.getElementById("predictBtn").click();
//     }
//   });

//   // تهيئة حقول الإدخال
//   updateInputs();

//   // تحميل النموذج الافتراضي
//   console.log("✅ التطبيق جاهز للاستخدام - النموذج الافتراضي: top5");
// });

// static/js/script.js - Professional Heart Disease Prediction

/**
 * ================================================
 * نظام تشخيص أمراض القلب - السكربت الرئيسي
 * ================================================
 *
 * هذا الملف يحتوي على الدوال المشتركة بين جميع الصفحات.
 * الدوال الخاصة بصفحة معينة يتم التحقق من وجود العناصر قبل تنفيذها.
 */

// ================================================
// تعريف الميزات لكل نموذج
// ================================================
const FEATURES = {
  minimal: ["ST slope", "exercise angina", "chest pain type", "oldpeak"],
  top8: [
    "ST slope",
    "chest pain type",
    "exercise angina",
    "oldpeak",
    "max heart rate",
    "sex",
    "fasting blood sugar",
    "cholesterol",
  ],
  all11: [
    "age",
    "sex",
    "chest pain type",
    "resting bp s",
    "cholesterol",
    "fasting blood sugar",
    "resting ecg",
    "max heart rate",
    "exercise angina",
    "oldpeak",
    "ST slope",
  ],
};

// الأسماء العربية للميزات
const FEATURES_AR = {
  "ST slope": "ميل مقطع ST",
  "exercise angina": "ذبحة أثناء الجهد",
  "chest pain type": "نوع ألم الصدر",
  oldpeak: "انخفاض ST (oldpeak)",
  "max heart rate": "أقصى معدل لضربات القلب",
  age: "العمر",
  sex: "الجنس",
  "resting bp s": "ضغط الدم الانقباضي",
  cholesterol: "الكوليسترول",
  "fasting blood sugar": "سكر الدم الصائم",
  "resting ecg": "تخطيط القلب",
};

// أوصاف الميزات
const FEATURES_DESC = {
  "ST slope":
    "1 = مائل للأعلى (طبيعي), 2 = مسطح (مشبوه), 3 = مائل للأسفل (خطير)",
  "exercise angina":
    "هل يعاني المريض من ألم في الصدر عند بذل مجهود؟ (0=لا, 1=نعم)",
  "chest pain type":
    "1=ذبحة نموذجية, 2=ذبحة غير نموذجية, 3=ألم غير ذبحي, 4=بدون أعراض",
  oldpeak: "انخفاض مقطع ST (بالملليمتر) - القيم الأعلى تشير إلى خطر أكبر",
  "max heart rate":
    "أقصى معدل لضربات القلب (نبضة/دقيقة) - القيم الأقل تشير إلى خطر أكبر",
  age: "العمر بالسنوات",
  sex: "0=أنثى, 1=ذكر",
  "resting bp s": "ضغط الدم الانقباضي (mmHg) - القيم الطبيعية 90-120",
  cholesterol: "الكوليسترول (mg/dL) - القيم الطبيعية أقل من 200",
  "fasting blood sugar": "0=طبيعي, 1=مرتفع",
  "resting ecg": "0=طبيعي, 1=اضطراب, 2=تضخم",
};

// القيم الافتراضية
const DEFAULT_VALUES = {
  "ST slope": 2,
  "exercise angina": 0,
  "chest pain type": 4,
  oldpeak: 0.6,
  "max heart rate": 150,
  age: 55,
  sex: 1,
  "resting bp s": 120,
  cholesterol: 200,
  "fasting blood sugar": 0,
  "resting ecg": 0,
};

// خيارات القيم للميزات الفئوية
const OPTIONS = {
  "ST slope": [1, 2, 3],
  "exercise angina": [0, 1],
  "chest pain type": [1, 2, 3, 4],
  sex: [0, 1],
  "fasting blood sugar": [0, 1],
  "resting ecg": [0, 1, 2],
};

let currentModel = "top8";

// ================================================
// دوال مشتركة لجميع الصفحات
// ================================================

/**
 * تحديث حقول الإدخال حسب النموذج المختار
 * تعمل فقط في صفحة التشخيص الفردي (index.html)
 */
function updateInputs() {
  const container = document.getElementById("inputs-container");

  // الخروج إذا كان العنصر غير موجود (الصفحة الحالية ليست صفحة التشخيص)
  if (!container) {
    return;
  }

  const features = FEATURES[currentModel];

  if (!features) {
    container.innerHTML =
      '<div class="text-center text-danger">خطأ في تحميل الميزات</div>';
    return;
  }

  let html = '<div class="inputs-grid">';

  features.forEach((feature) => {
    html += `
            <div class="input-group-custom">
                <label>
                    <i class="fas fa-chart-line"></i>
                    ${FEATURES_AR[feature] || feature}
                </label>
        `;

    if (OPTIONS[feature]) {
      html += `<select class="form-select" id="input_${feature}" data-feature="${feature}">`;
      OPTIONS[feature].forEach((opt) => {
        const selected = opt === DEFAULT_VALUES[feature] ? "selected" : "";
        html += `<option value="${opt}" ${selected}>${opt}</option>`;
      });
      html += `</select>`;
    } else {
      let value = DEFAULT_VALUES[feature] || "";
      html += `<input type="number" class="form-control" id="input_${feature}" 
                           data-feature="${feature}" value="${value}" step="any">`;
    }

    html += `<small class="text-muted"><i class="fas fa-info-circle me-1"></i>${FEATURES_DESC[feature] || ""}</small>`;
    html += `</div>`;
  });

  html += "</div>";
  container.innerHTML = html;
}

/**
 * جمع البيانات من حقول الإدخال
 */
function collectData() {
  const features = FEATURES[currentModel];
  const data = {};

  features.forEach((feature) => {
    const input = document.getElementById(`input_${feature}`);
    if (input) {
      let value = parseFloat(input.value);
      if (isNaN(value)) value = 0;
      data[feature] = value;
    } else {
      data[feature] = DEFAULT_VALUES[feature] || 0;
    }
  });

  return data;
}

/**
 * عرض نتيجة التنبؤ مع تأثير حركي
 */
function displayResult(result) {
  const container = document.getElementById("result-container");

  // الخروج إذا كان العنصر غير موجود
  if (!container) {
    return;
  }

  const isHealthy = result.result === "HEALTHY";

  let riskBadge = "";
  if (result.risk_level === "HIGH") {
    riskBadge = '<span class="badge bg-danger">عالي 🔴</span>';
  } else if (result.risk_level === "MEDIUM") {
    riskBadge = '<span class="badge bg-warning">متوسط 🟡</span>';
  } else {
    riskBadge = '<span class="badge bg-success">منخفض 🟢</span>';
  }

  container.innerHTML = `
        <div class="result-card ${isHealthy ? "result-healthy" : "result-disease"}">
            <div class="result-icon">
                ${isHealthy ? '<i class="fas fa-heartbeat"></i>' : '<i class="fas fa-exclamation-triangle"></i>'}
            </div>
            <div class="result-title">
                ${isHealthy ? '<i class="fas fa-check-circle"></i> نتيجة مطمئنة' : '<i class="fas fa-exclamation-circle"></i> تنبيه هام'}
            </div>
            <div class="result-probability">
                ${result.probability_percent}
            </div>
            <div class="result-risk">
                مستوى الخطر: ${riskBadge}
            </div>
            <div class="result-recommendation">
                <i class="fas fa-stethoscope me-2"></i>
                <strong>التوصية الطبية:</strong> ${result.recommendation_ar}<br>
                <small class="text-muted mt-2 d-flex align-items-center justify-content-center gap-3">
                    <span><i class="fas fa-microchip"></i> النموذج: ${result.model_used}</span>
                    <span><i class="fas fa-chart-line"></i> دقة النموذج: ${result.model_accuracy || "غير محددة"}%</span>
                </small>
            </div>
        </div>
    `;

  container.style.display = "block";
  container.scrollIntoView({ behavior: "smooth", block: "nearest" });

  // تغيير لون الزر مؤقتاً
  const btn = document.getElementById("predictBtn");
  if (btn) {
    btn.style.background = isHealthy
      ? "linear-gradient(135deg, #2ecc71, #27ae60)"
      : "linear-gradient(135deg, #e74c3c, #c0392b)";
    setTimeout(() => {
      btn.style.background =
        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)";
    }, 1000);
  }
}

/**
 * إجراء التنبؤ
 */
async function predict() {
  const data = collectData();

  const btn = document.getElementById("predictBtn");
  if (!btn) return;

  const originalHTML = btn.innerHTML;
  btn.innerHTML =
    '<span class="spinner-border spinner-border-sm me-2"></span> جاري التحليل...';
  btn.disabled = true;

  const resultContainer = document.getElementById("result-container");
  if (resultContainer) {
    resultContainer.style.display = "none";
  }

  try {
    const response = await fetch(`/predict/${currentModel}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (result.success) {
      displayResult(result);
    } else {
      showError(result.error || "حدث خطأ غير متوقع");
    }
  } catch (error) {
    showError("خطأ في الاتصال بالخادم. تأكد من تشغيل الخادم.");
    console.error("Error:", error);
  } finally {
    btn.innerHTML = originalHTML;
    btn.disabled = false;
  }
}

/**
 * عرض رسالة خطأ
 */
function showError(message) {
  const container = document.getElementById("result-container");
  if (!container) {
    console.error(message);
    return;
  }

  container.innerHTML = `
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle me-2"></i>
            <strong>خطأ:</strong> ${message}
        </div>
    `;
  container.style.display = "block";
  setTimeout(() => {
    container.style.opacity = "0";
    setTimeout(() => {
      container.style.display = "none";
      container.style.opacity = "1";
    }, 500);
  }, 5000);
}

/**
 * تغيير النموذج مع تأثير حركي
 */
function changeModel(model) {
  currentModel = model;

  document.querySelectorAll(".model-option").forEach((opt) => {
    opt.classList.remove("active");
    if (opt.dataset.model === model) {
      opt.classList.add("active");
    }
  });

  const container = document.getElementById("inputs-container");
  if (!container) return;

  container.style.opacity = "0.5";
  updateInputs();
  setTimeout(() => {
    container.style.opacity = "1";
  }, 200);

  const resultContainer = document.getElementById("result-container");
  if (resultContainer) {
    resultContainer.style.display = "none";
  }
}

/**
 * عرض إشعار للمستخدم
 */
function showNotification(message, type = "info") {
  const toastElement = document.getElementById("notificationToast");
  if (!toastElement) {
    console.log(message);
    return;
  }

  const toastBody = document.getElementById("toastMessage");
  const toastHeader = toastElement.querySelector(".toast-header");

  if (toastBody) toastBody.textContent = message;

  if (toastHeader) {
    toastHeader.style.background = "";
    toastHeader.style.color = "";

    if (type === "success") {
      toastHeader.style.background = "#2ecc71";
      toastHeader.style.color = "white";
    } else if (type === "error") {
      toastHeader.style.background = "#e74c3c";
      toastHeader.style.color = "white";
    } else if (type === "warning") {
      toastHeader.style.background = "#f39c12";
      toastHeader.style.color = "white";
    } else {
      toastHeader.style.background = "#667eea";
      toastHeader.style.color = "white";
    }
  }

  try {
    const bsToast = new bootstrap.Toast(toastElement);
    bsToast.show();
  } catch (e) {
    console.log("Toast:", message);
  }
}

// ================================================
// التهيئة - تعمل فقط في صفحة التشخيص الفردي
// ================================================
document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ النظام جاهز - الصفحة:", window.location.pathname);

  // التحقق من وجود عناصر صفحة التشخيص
  const modelOptions = document.querySelectorAll(".model-option");
  const predictBtn = document.getElementById("predictBtn");
  const inputsContainer = document.getElementById("inputs-container");

  // تهيئة صفحة التشخيص فقط إذا كانت العناصر موجودة
  if (modelOptions.length > 0) {
    modelOptions.forEach((opt) => {
      opt.addEventListener("click", () => {
        changeModel(opt.dataset.model);
      });
    });
  }

  if (predictBtn) {
    predictBtn.addEventListener("click", predict);
  }

  if (inputsContainer) {
    updateInputs();
    console.log("✅ تم تحميل النموذج الافتراضي:", currentModel);
  }

  // إضافة تأثير Enter للتنبؤ (فقط في صفحة التشخيص)
  if (predictBtn) {
    document.addEventListener("keypress", (e) => {
      if (
        e.key === "Enter" &&
        document.activeElement &&
        document.activeElement.tagName !== "BUTTON" &&
        document.activeElement.tagName !== "TEXTAREA"
      ) {
        e.preventDefault();
        predictBtn.click();
      }
    });
  }
});
