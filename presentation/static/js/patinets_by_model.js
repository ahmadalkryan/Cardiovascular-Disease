// static/js/patients_by_model.js
// ============================================
// كود المرضى حسب النموذج - منفصل عن HTML
// ============================================

(function () {
  "use strict";

  const modelNames = {
    minimal: {
      name: "النموذج المبسط",
      icon: "⚡",
      color: "#3498db",
      class: "model-minimal",
    },
    top8: {
      name: "النموذج المتوسط",
      icon: "⭐",
      color: "#f39c12",
      class: "model-top8",
    },
    all11: {
      name: "النموذج الشامل",
      icon: "🏆",
      color: "#9b59b6",
      class: "model-all11",
    },
  };

  // ============================================
  // كلاس PatientsByModel
  // ============================================
  class PatientsByModel {
    constructor() {
      this.container = document.getElementById("modelsContainer");
      this.init();
    }

    async init() {
      await this.load();
      console.log("📊 Patients by Model page loaded");
    }

    async load() {
      try {
        const response = await fetch("/api/patients");
        const data = await response.json();

        if (!data.success) {
          throw new Error(data.error || "فشل في تحميل البيانات");
        }

        const patients = data.patients || [];

        if (patients.length === 0) {
          this.showEmpty();
          return;
        }

        this.render(patients);
      } catch (error) {
        console.error("Error loading data:", error);
        this.showError(error.message);
      }
    }

    render(patients) {
      // تجميع المرضى حسب النموذج
      const grouped = {};
      patients.forEach((p) => {
        const modelKey = p.model_used || "unknown";
        if (!grouped[modelKey]) grouped[modelKey] = [];
        grouped[modelKey].push(p);
      });

      let html = "";

      for (const [key, list] of Object.entries(grouped)) {
        const info = modelNames[key] || {
          name: key,
          icon: "📊",
          color: "#6c757d",
          class: "",
        };

        const disease = list.filter((p) => p.prediction === 1).length;
        const healthy = list.length - disease;
        const diseasePercent =
          list.length > 0 ? ((disease / list.length) * 100).toFixed(1) : 0;
        const healthyPercent =
          list.length > 0 ? ((healthy / list.length) * 100).toFixed(1) : 0;

        html += `
          <div class="card-wrapper model-card-wrapper ${info.class}">
            <div class="model-card-header">
              <div class="d-flex justify-content-between align-items-center flex-wrap">
                <h5 class="mb-0">
                  <span class="model-icon">${info.icon}</span>
                  ${info.name}
                  <span class="model-badge">${list.length} حالة</span>
                </h5>
                <div>
                  <span class="badge bg-light text-dark me-1">
                    <i class="fas fa-circle text-danger"></i> ${disease} مريض
                  </span>
                  <span class="badge bg-light text-dark">
                    <i class="fas fa-circle text-success"></i> ${healthy} سليم
                  </span>
                </div>
              </div>
            </div>
            <div class="card-body">
              <div class="row g-3 mb-3">
                <div class="col-md-3 col-6">
                  <div class="stat-box stat-box-danger">
                    <div class="stat-number">${disease}</div>
                    <small>مرضى</small>
                    <br><small class="text-muted">${diseasePercent}%</small>
                  </div>
                </div>
                <div class="col-md-3 col-6">
                  <div class="stat-box stat-box-success">
                    <div class="stat-number">${healthy}</div>
                    <small>أصحاء</small>
                    <br><small class="text-muted">${healthyPercent}%</small>
                  </div>
                </div>
                <div class="col-md-3 col-6">
                  <div class="stat-box" style="background: #e3f2fd; color: #0d47a1;">
                    <div class="stat-number">${list.length}</div>
                    <small>إجمالي</small>
                  </div>
                </div>
                <div class="col-md-3 col-6">
                  <div class="stat-box" style="background: #fff3e0; color: #e65100;">
                    <div class="stat-number">${diseasePercent}%</div>
                    <small>نسبة المرضى</small>
                  </div>
                </div>
              </div>
              
              <div class="table-responsive">
                <table class="table table-hover table-sm">
                  <thead>
                    <tr>
                      <th>المعرف</th>
                      <th>التاريخ</th>
                      <th>الوقت</th>
                      <th>النتيجة</th>
                      <th>الاحتمالية</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${list
                      .slice(-10)
                      .reverse()
                      .map(
                        (p) => `
                      <tr>
                        <td><code>${p.patient_id || "-"}</code></td>
                        <td>${p.date || "-"}</td>
                        <td>${p.time || "-"}</td>
                        <td>
                          <span class="badge ${p.prediction === 1 ? "bg-danger" : "bg-success"}">
                            ${p.prediction === 1 ? "مريض" : "سليم"}
                          </span>
                        </td>
                        <td>
                          <div class="d-flex align-items-center gap-2">
                            <span>${((p.probability || 0) * 100).toFixed(1)}%</span>
                            <div class="progress flex-grow-1" style="height: 5px; max-width: 80px;">
                              <div class="progress-bar ${p.prediction === 1 ? "bg-danger" : "bg-success"}" 
                                   style="width: ${(p.probability || 0) * 100}%"></div>
                            </div>
                          </div>
                        </td>
                      </tr>
                    `,
                      )
                      .join("")}
                  </tbody>
                </table>
                ${
                  list.length > 10
                    ? `
                  <div class="text-center text-muted small mt-2">
                    عرض آخر 10 حالات من أصل ${list.length}
                  </div>
                `
                    : ""
                }
              </div>
            </div>
          </div>
        `;
      }

      this.container.innerHTML = html;
    }

    showEmpty() {
      this.container.innerHTML = `
        <div class="card shadow-sm border-0 rounded-4">
          <div class="card-body">
            <div class="empty-state">
              <i class="fas fa-users"></i>
              <h5>لا توجد بيانات</h5>
              <p class="text-muted">لم يتم تسجيل أي مريض بعد. قم بإجراء تشخيص أولاً.</p>
              <a href="/" class="btn btn-primary">
                <i class="fas fa-stethoscope"></i> تشخيص جديد
              </a>
            </div>
          </div>
        </div>
      `;
    }

    showError(message) {
      this.container.innerHTML = `
        <div class="alert alert-danger">
          <i class="fas fa-exclamation-triangle me-2"></i>
          <strong>خطأ في تحميل البيانات:</strong> ${message}
          <br>
          <button class="btn btn-outline-danger mt-2" onclick="window.patientsByModel.load()">
            <i class="fas fa-redo"></i> إعادة المحاولة
          </button>
        </div>
      `;
    }
  }

  // ============================================
  // تهيئة الصفحة
  // ============================================
  document.addEventListener("DOMContentLoaded", function () {
    window.patientsByModel = new PatientsByModel();
  });
})();
