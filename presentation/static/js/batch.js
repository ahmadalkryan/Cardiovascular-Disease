// static/js/batch.js
// ============================================
// كود التنبؤ المجمع - منفصل عن HTML
// ============================================

(function () {
  "use strict";

  // ============================================
  // ✅ تعريف النماذج (مركزي)
  // ============================================
  const MODEL_FEATURES = {
    minimal: {
      display: "النموذج المبسط (4 ميزات)",
      features: ["ST slope", "exercise angina", "chest pain type", "oldpeak"],
      features_ar: [
        "ميل مقطع ST",
        "ذبحة أثناء الجهد",
        "نوع ألم الصدر",
        "انخفاض ST",
      ],
    },
    top8: {
      display: "النموذج المتوسط (8 ميزات)",
      features: [
        "ST slope",
        "chest pain type",
        "exercise angina",
        "oldpeak",
        "max heart rate",
        "sex",
        "fasting blood sugar",
        "cholesterol",
      ],
      features_ar: [
        "ميل مقطع ST",
        "نوع ألم الصدر",
        "ذبحة أثناء الجهد",
        "انخفاض ST",
        "أقصى معدل لضربات القلب",
        "الجنس",
        "سكر الدم الصائم",
        "الكوليسترول",
      ],
    },
    all11: {
      display: "النموذج الشامل (11 ميزة)",
      features: [
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
      features_ar: [
        "العمر",
        "الجنس",
        "نوع ألم الصدر",
        "ضغط الدم الانقباضي",
        "الكوليسترول",
        "سكر الدم الصائم",
        "تخطيط القلب",
        "أقصى معدل لضربات القلب",
        "ذبحة أثناء الجهد",
        "انخفاض ST",
        "ميل مقطع ST",
      ],
    },
  };

  // ============================================
  // ✅ كلاس BatchPredictor
  // ============================================
  class BatchPredictor {
    constructor() {
      this.selectedFile = null;
      this.batchResults = null;
      this.currentModelKey = "top8";
      this.isPredicting = false;
      this.isSaving = false;

      this.elements = this._getElements();
      this._bindEvents();
      this._updateModelFeatures();

      console.log("📊 BatchPredictor initialized");
    }

    // ============================================
    // الحصول على عناصر DOM
    // ============================================
    _getElements() {
      return {
        uploadArea: document.getElementById("uploadArea"),
        fileInput: document.getElementById("fileInput"),
        fileInfo: document.getElementById("fileInfo"),
        fileName: document.getElementById("fileName"),
        fileSize: document.getElementById("fileSize"),
        filePreview: document.getElementById("filePreview"),
        fileColumns: document.getElementById("fileColumns"),
        fileValidation: document.getElementById("fileValidation"),
        fileValidationMessage: document.getElementById("fileValidationMessage"),
        predictBtn: document.getElementById("predictBtn"),
        modelSelect: document.getElementById("modelSelect"),
        modelFeaturesDisplay: document.getElementById("modelFeaturesDisplay"),
        resultsContainer: document.getElementById("resultsContainer"),
        loadingOverlay: document.getElementById("loadingOverlay"),
        loadingMessage: document.getElementById("loadingMessage"),
        editModal: document.getElementById("editModal"),
      };
    }

    // ============================================
    // ربط الأحداث
    // ============================================
    _bindEvents() {
      const { uploadArea, fileInput, modelSelect, predictBtn } = this.elements;

      // رفع الملف
      uploadArea.addEventListener("click", () => fileInput.click());
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
      fileInput.addEventListener("change", (e) => {
        if (e.target.files[0]) this._handleFile(e.target.files[0]);
      });

      // تغيير النموذج
      modelSelect.addEventListener("change", () => {
        this.currentModelKey = modelSelect.value;
        this._updateModelFeatures();
        if (this.selectedFile) {
          this._validateFile(this.selectedFile);
        }
      });

      // زر التنبؤ
      predictBtn.addEventListener("click", () => this._predictBatch());
    }

    // ============================================
    // تحديث ميزات النموذج
    // ============================================
    _updateModelFeatures() {
      const info = MODEL_FEATURES[this.currentModelKey];
      if (info && this.elements.modelFeaturesDisplay) {
        this.elements.modelFeaturesDisplay.textContent = `الميزات المطلوبة: ${info.features_ar.join("، ")}`;
      }
    }

    // ============================================
    // معالجة الملف
    // ============================================
    _handleFile(file) {
      // التحقق من نوع الملف
      const validExtensions = [".csv", ".xlsx", ".xls"];
      const ext = "." + file.name.split(".").pop().toLowerCase();
      if (!validExtensions.includes(ext)) {
        showNotification("الرجاء رفع ملف CSV أو Excel", "error");
        return;
      }

      // التحقق من الحجم (16MB)
      if (file.size > 16 * 1024 * 1024) {
        showNotification("حجم الملف يتجاوز الحد المسموح (16MB)", "error");
        return;
      }

      this.selectedFile = file;
      this.batchResults = null;

      // عرض معلومات الملف
      this.elements.fileName.textContent = file.name;
      this.elements.fileSize.textContent = `(${(file.size / 1024).toFixed(1)} KB)`;

      // قراءة الملف
      const reader = new FileReader();
      reader.onload = (e) => this._onFileRead(e, file);
      reader.onerror = () => {
        showNotification("فشل قراءة الملف", "error");
      };

      if (file.name.endsWith(".csv")) {
        reader.readAsText(file);
      } else {
        this.elements.filePreview.textContent = `📁 ${file.name}`;
        this.elements.fileColumns.textContent = "📊 ملف Excel";
        this.elements.fileValidation.style.display = "none";
        this.elements.predictBtn.disabled = false;
        this.elements.fileInfo.style.display = "block";
        this.elements.uploadArea.style.display = "none";
      }
    }

    // ============================================
    // معالجة قراءة الملف
    // ============================================
    _onFileRead(e, file) {
      const content = e.target.result;
      if (file.name.endsWith(".csv")) {
        const lines = content.split("\n").filter((l) => l.trim());
        this.elements.filePreview.textContent = `معاينة:\n${lines.slice(0, 4).join("\n").substring(0, 300)}...`;
        if (lines.length > 0) {
          const headers = lines[0].split(",").map((c) => c.trim());
          this.elements.fileColumns.textContent = `الأعمدة: ${headers.join("، ")}`;
          this._validateFile(headers);
        }
      }

      this.elements.fileInfo.style.display = "block";
      this.elements.uploadArea.style.display = "none";
    }

    // ============================================
    // التحقق من صحة الملف
    // ============================================
    _validateFile(headers) {
      const features = MODEL_FEATURES[this.currentModelKey].features;
      const featuresAr = MODEL_FEATURES[this.currentModelKey].features_ar;
      const missing = features.filter((f) => !headers.includes(f));

      if (missing.length > 0) {
        this.elements.fileValidation.style.display = "block";
        this.elements.fileValidationMessage.innerHTML = `
          <strong>⚠️ الميزات غير موجودة:</strong><br>
          ${missing.map((f) => featuresAr[features.indexOf(f)]).join("، ")}
        `;
        this.elements.predictBtn.disabled = true;
      } else {
        this.elements.fileValidation.style.display = "none";
        this.elements.predictBtn.disabled = false;
      }
    }

    // ============================================
    // التنبؤ المجمع
    // ============================================
    async _predictBatch() {
      if (!this.selectedFile || this.isPredicting) return;

      this.isPredicting = true;
      const formData = new FormData();
      formData.append("file", this.selectedFile);
      formData.append("model", this.currentModelKey);

      this.elements.loadingMessage.textContent = "جاري تحليل البيانات...";
      this.elements.loadingOverlay.style.display = "flex";
      this.elements.predictBtn.disabled = true;

      try {
        const response = await fetch("/api/batch-predict", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();

        if (data.success) {
          this.batchResults = data;
          this._displayResults(data);
          showNotification("تم التنبؤ بنجاح!", "success");
        } else {
          this._showError(data.error || "خطأ غير معروف");
          showNotification(data.error || "خطأ", "error");
        }
      } catch (error) {
        this._showError("خطأ في الاتصال بالخادم");
        showNotification("خطأ في الاتصال بالخادم", "error");
        console.error("Error:", error);
      } finally {
        this.isPredicting = false;
        this.elements.loadingOverlay.style.display = "none";
        this.elements.predictBtn.disabled = false;
      }
    }

    // ============================================
    // عرض النتائج
    // ============================================
    _displayResults(data) {
      const container = this.elements.resultsContainer;

      let html = `
        <div class="result-summary">
          <div class="row text-center">
            <div class="col-md-3"><h2>${data.total_records}</h2><small>إجمالي</small></div>
            <div class="col-md-3"><h2 style="color:#ff6b6b">${data.disease_count}</h2><small>مرضى</small></div>
            <div class="col-md-3"><h2 style="color:#51cf66">${data.healthy_count}</h2><small>أصحاء</small></div>
            <div class="col-md-3"><h2>${data.avg_risk_percent}</h2><small>متوسط الخطر</small></div>
          </div>
          <div class="text-center mt-3">
            <small>النموذج: ${data.model_used} | ناجح: ${data.successful}</small>
            ${data.failed > 0 ? `<br><small class="text-warning">فشل: ${data.failed}</small>` : ""}
          </div>
        </div>
        <div class="result-card">
          <h5><i class="fas fa-table me-2"></i>نتائج التنبؤ</h5>
          <div class="result-table">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>#</th>
                  <th>النتيجة</th>
                  <th>الاحتمالية</th>
                  <th>مستوى الخطر</th>
                  <th>إجراءات</th>
                </tr>
              </thead>
              <tbody>
      `;

      data.results.forEach((r, index) => {
        if (r.error) {
          html += `<tr class="table-danger"><td>${r.row_index}</td><td colspan="4">❌ ${r.error}</td></tr>`;
        } else {
          const bc = r.prediction === 1 ? "badge-danger" : "badge-success";
          const rc =
            r.risk_level === "HIGH"
              ? "badge-danger"
              : r.risk_level === "MEDIUM"
                ? "badge-warning"
                : "badge-success";
          html += `
            <tr class="${r.doctor_modified ? "row-modified" : ""}">
              <td>
                ${r.row_index}
                ${r.doctor_modified ? '<span class="modified-badge">👨‍⚕️ معدل</span>' : ""}
              </td>
              <td><span class="badge ${bc}">${r.prediction === 1 ? "مريض" : "سليم"}</span></td>
              <td>${r.probability_percent}</td>
              <td><span class="badge ${rc}">${r.risk_level_ar}</span></td>
              <td>
                <button class="btn-edit-row" onclick="window.batchPredictor._openEditModal(${r.row_index})">
                  <i class="fas fa-edit"></i> تعديل
                </button>
              </td>
            </tr>
          `;
        }
      });

      html += `
              </tbody>
            </table>
          </div>
          <div class="action-buttons">
            <button class="btn-save-all" onclick="window.batchPredictor._saveAllResults()">
              <i class="fas fa-save me-2"></i> حفظ جميع النتائج
            </button>
            <button class="btn-export-csv" onclick="window.batchPredictor._exportCSV()">
              <i class="fas fa-file-csv me-2"></i> تصدير CSV
            </button>
          </div>
          <div class="save-progress" id="saveProgress">
            <div class="spinner-border spinner-border-sm text-primary me-2"></div>
            <span>جاري الحفظ...</span>
          </div>
          <div id="saveResult" class="mt-3 text-center"></div>
        </div>
      `;

      container.innerHTML = html;
      container.style.display = "block";
      container.scrollIntoView({ behavior: "smooth" });
    }

    // ============================================
    // عرض الخطأ
    // ============================================
    _showError(message) {
      const container = this.elements.resultsContainer;
      container.innerHTML = `
        <div class="alert alert-danger mt-3">
          <h5>❌ فشل</h5>
          <p>${message}</p>
          <button class="btn btn-outline-danger btn-sm mt-2" onclick="this.closest('.alert').remove()">
            <i class="fas fa-times"></i> إغلاق
          </button>
        </div>
      `;
      container.style.display = "block";
    }

    // ============================================
    // فتح نافذة تعديل التشخيص
    // ============================================
    _openEditModal(rowIndex) {
      if (!this.batchResults) return;

      const r = this.batchResults.results.find((r) => r.row_index === rowIndex);
      if (!r || r.error) {
        showNotification("لا يمكن تعديل هذا السجل", "error");
        return;
      }

      document.getElementById("editRowIndex").value = rowIndex;
      document.getElementById("editPrediction").value =
        r.doctor_prediction !== undefined ? r.doctor_prediction : r.prediction;
      document.getElementById("editProbability").value = (
        (r.probability || 0) * 100
      ).toFixed(1);
      document.getElementById("editNotes").value = r.doctor_notes || "";

      const modal = new bootstrap.Modal(document.getElementById("editModal"));
      modal.show();
    }

    // ============================================
    // تطبيق التعديل
    // ============================================
    _applyEdit() {
      const ri = parseInt(document.getElementById("editRowIndex").value);
      const np = parseInt(document.getElementById("editPrediction").value);
      const nprob =
        parseFloat(document.getElementById("editProbability").value) / 100;
      const notes = document.getElementById("editNotes").value;

      if (isNaN(np) || isNaN(nprob)) {
        showNotification("الرجاء إدخال قيم صحيحة", "error");
        return;
      }

      const r = this.batchResults.results.find((r) => r.row_index === ri);
      if (r) {
        r.doctor_modified = true;
        r.doctor_prediction = np;
        r.doctor_notes = notes;
        r.prediction = np;
        r.probability = nprob;
        r.probability_percent = (nprob * 100).toFixed(1) + "%";
        r.result = np === 1 ? "DISEASE" : "HEALTHY";
        r.result_ar = np === 1 ? "مريض" : "سليم";

        if (nprob > 0.7) {
          r.risk_level = "HIGH";
          r.risk_level_ar = "عالي 🔴";
        } else if (nprob > 0.3) {
          r.risk_level = "MEDIUM";
          r.risk_level_ar = "متوسط 🟡";
        } else {
          r.risk_level = "LOW";
          r.risk_level_ar = "منخفض 🟢";
        }
      }

      // تحديث الإحصائيات
      const suc = this.batchResults.results.filter((r) => !r.error);
      this.batchResults.disease_count = suc.filter(
        (r) => r.prediction === 1,
      ).length;
      this.batchResults.healthy_count = suc.filter(
        (r) => r.prediction === 0,
      ).length;
      const probs = suc
        .filter((r) => r.probability !== undefined)
        .map((r) => r.probability);
      this.batchResults.avg_risk_percent =
        probs.length > 0
          ? ((probs.reduce((a, b) => a + b, 0) / probs.length) * 100).toFixed(
              1,
            ) + "%"
          : "0%";

      this._displayResults(this.batchResults);
      bootstrap.Modal.getInstance(document.getElementById("editModal")).hide();
      showNotification(`تم تعديل الصف ${ri} بنجاح`, "success");
    }

    // ============================================
    // حفظ جميع النتائج
    // ============================================
    async _saveAllResults() {
      if (!this.batchResults?.results || this.isSaving) return;

      const valid = this.batchResults.results.filter(
        (r) => !r.error && r.can_save !== false,
      );
      if (valid.length === 0) {
        showNotification("لا توجد نتائج صالحة للحفظ", "error");
        return;
      }

      this.isSaving = true;
      const saveBtn = document.getElementById("saveAllBtn");
      const pd = document.getElementById("saveProgress");
      const sr = document.getElementById("saveResult");

      if (saveBtn) {
        saveBtn.disabled = true;
        saveBtn.innerHTML =
          '<span class="spinner-border spinner-border-sm me-2"></span> جاري الحفظ...';
      }
      if (pd) pd.classList.add("active");

      try {
        const response = await fetch("/api/batch-save-all", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            model_name: this.batchResults.model_key || this.currentModelKey,
            results: valid,
          }),
        });

        const data = await response.json();
        if (pd) pd.classList.remove("active");

        if (data.success && sr) {
          sr.innerHTML = `
            <div class="alert alert-success">
              <i class="fas fa-check-circle me-2"></i>
              <strong>${data.message}</strong><br>
              <span class="saved-count">✅ تم الحفظ: ${data.total_saved}</span>
              ${data.total_modified > 0 ? `<br><span class="modified-count">👨‍⚕️ المعدلة: ${data.total_modified}</span>` : ""}
              ${data.total_failed > 0 ? `<br><span class="text-danger">❌ فشل: ${data.total_failed}</span>` : ""}
            </div>
          `;
          if (saveBtn) {
            saveBtn.innerHTML = '<i class="fas fa-check me-2"></i> تم الحفظ';
            saveBtn.style.background =
              "linear-gradient(135deg,#2ecc71,#27ae60)";
            saveBtn.disabled = true;
          }
          showNotification(data.message, "success");
        } else if (sr) {
          sr.innerHTML = `<div class="alert alert-danger">${data.error || "فشل في حفظ البيانات"}</div>`;
          if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML =
              '<i class="fas fa-save me-2"></i> حفظ جميع النتائج';
          }
          showNotification(data.error || "فشل في الحفظ", "error");
        }
      } catch (error) {
        if (pd) pd.classList.remove("active");
        if (saveBtn) {
          saveBtn.disabled = false;
          saveBtn.innerHTML =
            '<i class="fas fa-save me-2"></i> حفظ جميع النتائج';
        }
        showNotification("خطأ في الاتصال بالخادم", "error");
        console.error("Error:", error);
      } finally {
        this.isSaving = false;
      }
    }

    // ============================================
    // تصدير CSV
    // ============================================
    _exportCSV() {
      if (!this.batchResults?.results) {
        showNotification("لا توجد نتائج للتصدير", "error");
        return;
      }

      const features = MODEL_FEATURES[this.currentModelKey].features;
      const featuresAr = MODEL_FEATURES[this.currentModelKey].features_ar;

      let csv = "\uFEFF";
      const headers = [
        ...featuresAr,
        "النتيجة",
        "الاحتمالية (%)",
        "مستوى الخطر",
        "معدل",
      ];
      csv += headers.join(",") + "\n";

      this.batchResults.results.forEach((r) => {
        if (!r.error && r.patient_data) {
          const values = features.map((f) =>
            r.patient_data[f] !== undefined ? r.patient_data[f] : "",
          );
          values.push(r.result_ar || (r.prediction === 1 ? "مريض" : "سليم"));
          values.push(
            r.probability_percent ||
              ((r.probability || 0) * 100).toFixed(1) + "%",
          );
          values.push(r.risk_level_ar || "");
          values.push(r.doctor_modified ? "معدل" : "");
          csv += values.join(",") + "\n";
        }
      });

      const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `batch_results_${this.currentModelKey}_${new Date().toISOString().slice(0, 10)}.csv`;
      a.click();
      window.URL.revokeObjectURL(url);

      showNotification("تم تصدير CSV بنجاح", "success");
    }

    // ============================================
    // معالجة إسقاط الملف
    // ============================================
    _handleFileDrop(e) {
      const file = e.dataTransfer.files[0];
      if (file) this._handleFile(file);
    }
  }

  // ============================================
  // ✅ تهيئة الصفحة
  // ============================================
  document.addEventListener("DOMContentLoaded", function () {
    window.batchPredictor = new BatchPredictor();
    console.log("📊 Batch Predict page loaded successfully");
  });
})();
