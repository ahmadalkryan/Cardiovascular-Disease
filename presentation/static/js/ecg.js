// static/js/ecg.js
// ============================================
// كود تحليل تخطيط القلب (ECG) - منفصل عن HTML
// ============================================

(function () {
  "use strict";

  // ============================================
  // كلاس ECG Analyzer
  // ============================================
  class ECGAnalyzer {
    constructor(modelInfo) {
      this.modelInfo = modelInfo || {};
      this.currentModel = this._getDefaultModel();
      this.currentImage = null;
      this.isAnalyzing = false;

      this.elements = {
        uploadArea: document.getElementById("uploadArea"),
        imageInput: document.getElementById("imageInput"),
        previewContainer: document.getElementById("previewContainer"),
        imagePreview: document.getElementById("imagePreview"),
        predictBtn: document.getElementById("predictBtn"),
        loading: document.getElementById("loading"),
        resultDiv: document.getElementById("result"),
        modelSelector: document.getElementById("modelSelector"),
      };

      this.init();
    }

    // ============================================
    // الحصول على النموذج الافتراضي
    // ============================================
    _getDefaultModel() {
      const firstModel = document.querySelector(".model-option-card");
      return firstModel?.dataset?.model || "densenet_binary";
    }

    // ============================================
    // تهيئة الصفحة
    // ============================================
    init() {
      this._bindEvents();
      this._setupModelSelector();
      console.log("📊 ECG Analyzer initialized");
      console.log(`🎯 Current model: ${this.currentModel}`);

      if (Object.keys(this.modelInfo).length === 0) {
        showNotification("⚠️ لا توجد نماذج ECG متاحة", "warning");
      }
    }

    // ============================================
    // ربط الأحداث
    // ============================================
    _bindEvents() {
      const { uploadArea, imageInput, predictBtn } = this.elements;

      // رفع الصورة
      uploadArea.addEventListener("click", () => imageInput.click());
      uploadArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        uploadArea.classList.add("dragover");
      });
      uploadArea.addEventListener("dragleave", () =>
        uploadArea.classList.remove("dragover"),
      );
      uploadArea.addEventListener("drop", (e) => {
        e.preventDefault();
        uploadArea.classList.remove("dragover");
        this._handleFileDrop(e);
      });
      imageInput.addEventListener("change", (e) => {
        if (e.target.files[0]) this._handleFile(e.target.files[0]);
      });

      // تحليل الصورة
      predictBtn.addEventListener("click", () => this._analyze());
    }

    // ============================================
    // إعداد محدد النموذج
    // ============================================
    _setupModelSelector() {
      const cards = document.querySelectorAll(".model-option-card");
      cards.forEach((card) => {
        card.addEventListener("click", () => {
          const model = card.dataset.model;
          if (model) {
            this._selectModel(model);
          }
        });
      });
    }

    // ============================================
    // اختيار النموذج
    // ============================================
    _selectModel(model) {
      this.currentModel = model;
      document.querySelectorAll(".model-option-card").forEach((card) => {
        card.classList.toggle("active", card.dataset.model === model);
      });
      this.elements.resultDiv.style.display = "none";

      const info = this.modelInfo[model];
      showNotification(
        `تم اختيار نموذج ${info?.display_name || model}`,
        "info",
      );
    }

    // ============================================
    // معالجة الملف
    // ============================================
    _handleFile(file) {
      // التحقق من نوع الملف
      if (!file.type.startsWith("image/")) {
        showNotification("الرجاء رفع ملف صورة صالح", "error");
        return;
      }

      // التحقق من الحجم (16MB)
      if (file.size > 16 * 1024 * 1024) {
        showNotification("الملف كبير جداً. الحد الأقصى 16MB", "error");
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        this.currentImage = file;
        this.elements.imagePreview.src = e.target.result;
        this.elements.previewContainer.style.display = "block";
        this.elements.uploadArea.style.display = "none";
        this.elements.predictBtn.disabled = false;
        this.elements.resultDiv.style.display = "none";
        showNotification("تم رفع الصورة بنجاح", "success");
      };
      reader.onerror = () => showNotification("فشل قراءة الصورة", "error");
      reader.readAsDataURL(file);
    }

    // ============================================
    // معالجة إسقاط الملف
    // ============================================
    _handleFileDrop(e) {
      const file = e.dataTransfer.files[0];
      if (file) this._handleFile(file);
    }

    // ============================================
    // إعادة تعيين الصورة
    // ============================================
    resetImage() {
      this.currentImage = null;
      this.elements.imageInput.value = "";
      this.elements.previewContainer.style.display = "none";
      this.elements.uploadArea.style.display = "block";
      this.elements.predictBtn.disabled = true;
      this.elements.resultDiv.style.display = "none";
    }

    // ============================================
    // تحليل الصورة
    // ============================================
    async _analyze() {
      if (!this.currentImage || this.isAnalyzing) return;

      this.isAnalyzing = true;
      const formData = new FormData();
      formData.append("image", this.currentImage);
      formData.append("model", this.currentModel);

      this.elements.predictBtn.disabled = true;
      this.elements.predictBtn.innerHTML =
        '<span class="spinner-border spinner-border-sm me-2"></span> جاري التحليل...';
      this.elements.loading.style.display = "block";
      this.elements.resultDiv.style.display = "none";

      try {
        const response = await fetch("/api/predict/ecg", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();

        if (data.success) {
          this._displayResult(data);
          showNotification("تم تحليل الصورة بنجاح", "success");
        } else {
          showNotification(data.error || "حدث خطأ في التحليل", "error");
          this._showError(data.error || "حدث خطأ غير متوقع");
        }
      } catch (error) {
        showNotification("فشل الاتصال بالخادم", "error");
        console.error("Error:", error);
        this._showError("تأكد من تشغيل الخادم وحاول مرة أخرى");
      } finally {
        this.isAnalyzing = false;
        this.elements.predictBtn.disabled = false;
        this.elements.predictBtn.innerHTML =
          '<i class="fas fa-microscope me-2"></i> تحليل الصورة';
        this.elements.loading.style.display = "none";
      }
    }

    // ============================================
    // عرض النتائج
    // ============================================
    _displayResult(data) {
      const info = this.modelInfo[this.currentModel] || {};
      const classes_ar = data.classes_ar || info.classes_ar || [];
      const isNormal =
        data.predicted_class === "Normal" ||
        data.predicted_class_ar === "طبيعي";
      const cardBg = isNormal ? "#d4edda" : "#f8d7da";

      let html = `
        <div class="card border-0 shadow-sm result-card" style="background: ${cardBg};">
          <div class="card-body">
            <h5 class="text-center mb-3">
              <i class="fas fa-chart-bar me-2"></i>تفاصيل التشخيص
            </h5>
            <div class="mb-3">
      `;

      // عرض الاحتمالات
      if (data.all_probabilities_ar) {
        const sortedProbs = Object.entries(data.all_probabilities_ar).sort(
          (a, b) => b[1] - a[1],
        );

        for (const [cls_ar, prob] of sortedProbs) {
          const isPredicted = cls_ar === data.predicted_class_ar;
          const color = isPredicted ? data.class_color : "#6c757d";
          const probPercent = (prob * 100).toFixed(1);

          html += `
            <div class="prob-item" style="${isPredicted ? "background: rgba(102,126,234,0.1); border-right: 4px solid " + data.class_color : ""}">
              <div class="prob-label">
                <span style="${isPredicted ? "font-weight: bold; color: " + data.class_color : ""}">
                  ${isPredicted ? "▶ " : ""}${cls_ar} ${isPredicted ? " ✅" : ""}
                </span>
                <span class="prob-percent" style="color: ${color}">${probPercent}%</span>
              </div>
              <div class="progress-bar-custom" style="height: 8px; background: #e9ecef;">
                <div class="progress-fill" style="width: ${probPercent}%; background: ${color}; height: 8px; border-radius: 4px;"></div>
              </div>
            </div>
          `;
        }
      } else {
        html += '<p class="text-muted text-center">لا توجد بيانات احتمالية</p>';
      }

      html += `
            </div>
            <div class="text-center pt-3 border-top">
              <div class="result-class" style="color: ${data.class_color || "#667eea"}">
                ${data.predicted_class_ar || data.predicted_class || "غير معروف"}
              </div>
              <div class="display-4 my-2" style="color: ${data.class_color || "#667eea"}; font-size: 2.5rem; font-weight: bold;">
                ${data.confidence_percent || "0%"}
              </div>
              <div class="progress-bar-custom" style="height: 25px; background: #e9ecef;">
                <div class="progress-fill" style="width: ${(data.confidence || 0) * 100}%; background: ${data.class_color || "#667eea"};">
                  ${data.confidence_percent || "0%"}
                </div>
              </div>
              ${
                data.description
                  ? `
                <div class="description-box mt-3">
                  <i class="fas fa-info-circle me-2" style="color: ${data.class_color || "#667eea"};"></i>
                  ${data.description}
                </div>
              `
                  : ""
              }
              <div class="mt-3">
                <small class="text-muted">
                  <i class="fas fa-microchip me-1"></i>
                  النموذج: ${data.model_display || this.currentModel}
                  ${data.model_accuracy ? `<span class="badge bg-info ms-2">دقة: ${data.model_accuracy}</span>` : ""}
                  ${data.model_used ? `<span class="badge bg-secondary ms-1">${data.model_used}</span>` : ""}
                </small>
              </div>
            </div>
          </div>
        </div>
      `;

      this.elements.resultDiv.innerHTML = html;
      this.elements.resultDiv.style.display = "block";
      this.elements.resultDiv.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
      });
    }

    // ============================================
    // عرض الخطأ
    // ============================================
    _showError(message) {
      this.elements.resultDiv.innerHTML = `
        <div class="alert alert-danger">
          <i class="fas fa-exclamation-triangle me-2"></i>
          <strong>فشل التحليل</strong>
          <p class="mb-0 mt-1">${message}</p>
        </div>
      `;
      this.elements.resultDiv.style.display = "block";
    }
  }

  // ============================================
  // تهيئة الصفحة
  // ============================================
  document.addEventListener("DOMContentLoaded", function () {
    // معلومات النماذج من الخادم (محقونة من Flask)
    const modelInfo = window.ECG_MODELS || {};
    window.ecgAnalyzer = new ECGAnalyzer(modelInfo);
    console.log("📊 ECG page loaded successfully");
  });
})();
