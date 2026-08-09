// static/js/patients.js
// ============================================
// كود صفحة المرضى - منفصل عن HTML
// ============================================

(function () {
  "use strict";

  const modelNames = {
    minimal: "النموذج المبسط",
    top8: "النموذج المتوسط",
    all11: "النموذج الشامل",
  };

  const modelColors = {
    minimal: "model-minimal",
    top8: "model-top8",
    all11: "model-all11",
  };

  const FEATURES_AR = {
    age: "العمر",
    sex: "الجنس",
    "chest pain type": "نوع ألم الصدر",
    "resting bp s": "ضغط الدم الانقباضي",
    cholesterol: "الكوليسترول",
    "fasting blood sugar": "سكر الدم الصائم",
    "resting ecg": "تخطيط القلب أثناء الراحة",
    "max heart rate": "أقصى معدل لضربات القلب",
    "exercise angina": "ذبحة صدرية أثناء الجهد",
    oldpeak: "انخفاض مقطع ST",
    "ST slope": "ميل مقطع ST",
  };

  const VALUE_TRANSLATIONS = {
    sex: { 0: "أنثى ♀️", 1: "ذكر ♂️" },
    "chest pain type": {
      1: "ذبحة نموذجية",
      2: "ذبحة غير نموذجية",
      3: "ألم غير ذبحي",
      4: "بدون أعراض",
    },
    "fasting blood sugar": { 0: "طبيعي ✅", 1: "مرتفع ⚠️" },
    "resting ecg": {
      0: "طبيعي",
      1: "اضطراب في موجة ST-T",
      2: "تضخم البطين الأيسر",
    },
    "exercise angina": { 0: "لا ❌", 1: "نعم ✅" },
    "ST slope": {
      1: "مائل للأعلى (طبيعي)",
      2: "مسطح (مشبوه)",
      3: "مائل للأسفل (خطير)",
    },
  };

  const UNITS = {
    age: "سنة",
    "resting bp s": "mmHg",
    cholesterol: "mg/dL",
    "max heart rate": "نبضة/دقيقة",
    oldpeak: "ملم",
  };

  // ============================================
  // كلاس Patients
  // ============================================
  class Patients {
    constructor() {
      this.allPatients = [];
      this.currentPage = 1;
      this.itemsPerPage = 15;

      this.elements = {
        tableBody: document.getElementById("tableBody"),
        mobileCards: document.getElementById("mobileCardsContainer"),
        totalCount: document.getElementById("totalCount"),
        recordCount: document.getElementById("recordCount"),
        pagination: document.getElementById("pagination"),
        modelFilter: document.getElementById("modelFilter"),
        searchInput: document.getElementById("searchInput"),
      };

      this.init();
    }

    init() {
      this.bindEvents();
      this.load();
      console.log("📊 Patients page initialized");
    }

    bindEvents() {
      this.elements.modelFilter.addEventListener("change", () => {
        this.currentPage = 1;
        this.load();
      });

      this.elements.searchInput.addEventListener("keyup", () => {
        this.currentPage = 1;
        this.load();
      });
    }

    async load() {
      const model = this.elements.modelFilter.value;
      const search = this.elements.searchInput.value;

      try {
        let url = "/api/patients";
        const params = new URLSearchParams();
        if (model !== "all") params.append("model", model);
        if (search) params.append("search", search);
        if (params.toString()) url += "?" + params.toString();

        const response = await fetch(url);
        const data = await response.json();

        if (data.success) {
          this.allPatients = data.patients || [];
          this.elements.totalCount.textContent = this.allPatients.length;
          this.elements.recordCount.innerHTML = `إجمالي <strong>${this.allPatients.length}</strong> حالة`;
          this.renderTable();
          this.renderMobileCards();
        } else {
          throw new Error(data.error || "Failed to load patients");
        }
      } catch (error) {
        console.error("Error loading patients:", error);
        this.showError(error.message);
      }
    }

    renderTable() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      const pagePatients = this.allPatients.slice(start, end);

      const tbody = this.elements.tableBody;

      if (pagePatients.length === 0) {
        tbody.innerHTML =
          '<tr><td colspan="7" class="text-center py-5">لا توجد بيانات</td></tr>';
        this.elements.pagination.innerHTML = "";
        return;
      }

      tbody.innerHTML = pagePatients
        .map((p) => {
          const modelKey = p.model_used || "";
          const modelDisplay = modelNames[modelKey] || modelKey || "-";
          const modelColor = modelColors[modelKey] || "model-unknown";
          const statusClass =
            p.prediction === 1 ? "status-disease" : "status-healthy";
          const statusText =
            p.result_ar || (p.prediction === 1 ? "مريض" : "سليم");

          return `
          <tr>
            <td><code>${p.patient_id || "-"}</code></td>
            <td>${p.date || "-"}</td>
            <td>${p.time || "-"}</td>
            <td><span class="status-badge ${statusClass}">${statusText}</span></td>
            <td>
              <div class="d-flex align-items-center gap-2">
                <span class="small fw-bold" style="min-width: 45px;">${((p.probability || 0) * 100).toFixed(1)}%</span>
                <div class="progress progress-thin flex-grow-1">
                  <div class="progress-bar ${p.prediction === 1 ? "bg-danger" : "bg-success"}" 
                       style="width: ${Math.min((p.probability || 0) * 100, 100)}%"></div>
                </div>
              </div>
            </td>
            <td><span class="model-badge ${modelColor}">${modelDisplay}</span></td>
            <td>
              <button class="btn-details" onclick="window.patients.showDetail(${JSON.stringify(p).replace(/'/g, "&#39;")})">
                <i class="fas fa-info-circle me-1"></i> تفاصيل
              </button>
            </td>
          </tr>
        `;
        })
        .join("");

      this.renderPagination();
    }

    renderMobileCards() {
      const container = this.elements.mobileCards;
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      const pagePatients = this.allPatients.slice(start, end);

      if (pagePatients.length === 0) {
        container.innerHTML =
          '<div class="text-center py-5 text-muted">لا توجد بيانات</div>';
        return;
      }

      container.innerHTML = pagePatients
        .map((p) => {
          const modelKey = p.model_used || "";
          const modelDisplay = modelNames[modelKey] || modelKey || "-";
          const modelColor = modelColors[modelKey] || "model-unknown";
          const statusClass =
            p.prediction === 1 ? "status-disease" : "status-healthy";
          const statusText =
            p.result_ar || (p.prediction === 1 ? "مريض" : "سليم");

          return `
          <div class="patient-card-mobile">
            <div class="card-row">
              <span class="card-label">المعرف</span>
              <span class="card-value"><code>${p.patient_id || "-"}</code></span>
            </div>
            <div class="card-row">
              <span class="card-label">التاريخ والوقت</span>
              <span class="card-value">${p.date || "-"} ${p.time || "-"}</span>
            </div>
            <div class="card-row">
              <span class="card-label">النتيجة</span>
              <span class="card-value card-status">
                <span class="status-badge ${statusClass}">${statusText}</span>
                <span class="small text-muted">${((p.probability || 0) * 100).toFixed(1)}%</span>
              </span>
            </div>
            <div class="card-row">
              <span class="card-label">النموذج</span>
              <span class="card-value"><span class="model-badge ${modelColor}">${modelDisplay}</span></span>
            </div>
            <div class="card-row mt-2">
              <span></span>
              <button class="btn-details" onclick="window.patients.showDetail(${JSON.stringify(p).replace(/'/g, "&#39;")})">
                <i class="fas fa-info-circle me-1"></i> عرض التفاصيل
              </button>
            </div>
          </div>
        `;
        })
        .join("");
    }

    renderPagination() {
      const totalPages = Math.ceil(this.allPatients.length / this.itemsPerPage);
      let html = '<ul class="pagination mb-0">';

      html += `<li class="page-item ${this.currentPage === 1 ? "disabled" : ""}">
        <a class="page-link" href="#" onclick="window.patients.goToPage(${this.currentPage - 1}); return false;">&laquo;</a>
      </li>`;

      for (let i = 1; i <= totalPages; i++) {
        if (
          i === 1 ||
          i === totalPages ||
          (i >= this.currentPage - 2 && i <= this.currentPage + 2)
        ) {
          html += `<li class="page-item ${this.currentPage === i ? "active" : ""}">
            <a class="page-link" href="#" onclick="window.patients.goToPage(${i}); return false;">${i}</a>
          </li>`;
        } else if (i === this.currentPage - 3 || i === this.currentPage + 3) {
          html +=
            '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
      }

      html += `<li class="page-item ${this.currentPage === totalPages ? "disabled" : ""}">
        <a class="page-link" href="#" onclick="window.patients.goToPage(${this.currentPage + 1}); return false;">&raquo;</a>
      </li>`;
      html += "</ul>";

      this.elements.pagination.innerHTML = html;
    }

    goToPage(page) {
      const totalPages = Math.ceil(this.allPatients.length / this.itemsPerPage);
      if (page >= 1 && page <= totalPages) {
        this.currentPage = page;
        this.renderTable();
        this.renderMobileCards();
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    }

    showDetail(patient) {
      const content = document.getElementById("patientDetailContent");

      const sexValue =
        patient.sex !== undefined && patient.sex !== null
          ? VALUE_TRANSLATIONS.sex[patient.sex] || patient.sex
          : "-";

      const clinicalFeatures = [
        { key: "age", label: FEATURES_AR.age, unit: UNITS.age },
        { key: "sex", label: FEATURES_AR.sex, value: sexValue },
        { key: "chest pain type", label: FEATURES_AR["chest pain type"] },
        {
          key: "resting bp s",
          label: FEATURES_AR["resting bp s"],
          unit: UNITS["resting bp s"],
        },
        {
          key: "cholesterol",
          label: FEATURES_AR.cholesterol,
          unit: UNITS.cholesterol,
        },
        {
          key: "fasting blood sugar",
          label: FEATURES_AR["fasting blood sugar"],
        },
        { key: "resting ecg", label: FEATURES_AR["resting ecg"] },
        {
          key: "max heart rate",
          label: FEATURES_AR["max heart rate"],
          unit: UNITS["max heart rate"],
        },
        { key: "exercise angina", label: FEATURES_AR["exercise angina"] },
        { key: "oldpeak", label: FEATURES_AR.oldpeak, unit: UNITS.oldpeak },
        { key: "ST slope", label: FEATURES_AR["ST slope"] },
      ];

      let clinicalRows = "";
      clinicalFeatures.forEach((feature) => {
        const rawValue = patient[feature.key];
        if (rawValue !== undefined && rawValue !== null && rawValue !== "") {
          let displayValue = rawValue;
          if (VALUE_TRANSLATIONS[feature.key]) {
            displayValue =
              VALUE_TRANSLATIONS[feature.key][rawValue] || rawValue;
          }
          if (feature.unit && !VALUE_TRANSLATIONS[feature.key]) {
            displayValue = `${rawValue} ${feature.unit}`;
          }
          if (feature.value) displayValue = feature.value;

          clinicalRows += `
            <div class="detail-row">
              <span class="detail-label">${feature.label}</span>
              <span class="detail-value">${displayValue}</span>
            </div>
          `;
        }
      });

      const isDisease = patient.prediction === 1;
      const resultColor = isDisease ? "disease" : "healthy";
      const resultIcon = isDisease ? "⚠️" : "✅";
      const resultText = patient.result_ar || (isDisease ? "مريض" : "سليم");

      content.innerHTML = `
        <div class="patient-id-header">
          <i class="fas fa-fingerprint me-2" style="color: #667eea;"></i>
          معرف المريض: <code>${patient.patient_id || "-"}</code>
        </div>

        <div class="detail-section">
          <h6><i class="fas fa-stethoscope me-2"></i>معلومات التشخيص</h6>
          <div class="detail-row">
            <span class="detail-label">التاريخ والوقت</span>
            <span class="detail-value">${patient.date || "-"} | ${patient.time || "-"}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">النتيجة</span>
            <span class="detail-value ${resultColor}">${resultIcon} ${resultText}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">نسبة الاحتمالية</span>
            <span class="detail-value highlight">${((patient.probability || 0) * 100).toFixed(1)}%</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">النموذج المستخدم</span>
            <span class="detail-value">${modelNames[patient.model_used] || patient.model_used || "-"}</span>
          </div>
        </div>

        <div class="detail-section">
          <h6><i class="fas fa-notes-medical me-2"></i>البيانات السريرية</h6>
          ${clinicalRows || '<div class="text-center text-muted py-3">لا توجد بيانات سريرية مسجلة</div>'}
        </div>

        <div class="detail-section">
          <h6><i class="fas fa-info-circle me-2"></i>معلومات إضافية</h6>
          <div class="detail-row">
            <span class="detail-label">وقت التسجيل الكامل</span>
            <span class="detail-value">${patient.timestamp || "-"}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">معرف النموذج</span>
            <span class="detail-value"><code>${patient.model_used || "-"}</code></span>
          </div>
        </div>
      `;

      const modal = new bootstrap.Modal(
        document.getElementById("patientDetailModal"),
      );
      modal.show();
    }

    showError(message) {
      const errorHtml = `
        <tr><td colspan="7" class="text-center text-danger py-5">
          <i class="fas fa-exclamation-triangle fa-2x mb-2 d-block"></i>
          <strong>خطأ في تحميل البيانات</strong>
          <p class="small">${message}</p>
          <button class="btn btn-outline-danger btn-sm mt-2" onclick="window.patients.load()">
            <i class="fas fa-redo"></i> إعادة المحاولة
          </button>
        </td></tr>
      `;
      this.elements.tableBody.innerHTML = errorHtml;
      this.elements.mobileCards.innerHTML = "";
    }

    exportData() {
      const model = this.elements.modelFilter.value;
      let url = "/patients/export";
      if (model !== "all") url += `?model=${model}`;
      window.location.href = url;
    }
  }

  // ============================================
  // تهيئة الصفحة
  // ============================================
  document.addEventListener("DOMContentLoaded", function () {
    window.patients = new Patients();
    console.log("📊 Patients page loaded successfully");
  });
})();
