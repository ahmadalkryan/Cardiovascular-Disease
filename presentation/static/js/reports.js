// static/js/reports.js
// ============================================
// دوال التقارير المشتركة - منفصلة عن HTML
// ============================================

(function () {
  "use strict";

  // ============================================
  // ✅ دوال الإشعارات الموحدة
  // ============================================
  window.showNotification = function (message, type = "info") {
    const container =
      document.getElementById("notification-container") ||
      createNotificationContainer();

    const colors = {
      success: "#2ecc71",
      error: "#e74c3c",
      warning: "#f39c12",
      info: "#3498db",
    };

    const notification = document.createElement("div");
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
      background: ${colors[type] || "#3498db"};
      color: white;
      padding: 15px 25px;
      border-radius: 10px;
      font-weight: 600;
      box-shadow: 0 5px 25px rgba(0,0,0,0.2);
      animation: slideIn 0.3s ease;
      min-width: 250px;
      max-width: 500px;
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
    `;
    notification.textContent = message;

    container.appendChild(notification);

    setTimeout(() => {
      notification.style.opacity = "0";
      notification.style.transition = "opacity 0.3s ease";
      setTimeout(() => notification.remove(), 300);
    }, 4000);
  };

  function createNotificationContainer() {
    const container = document.createElement("div");
    container.id = "notification-container";
    container.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
    `;
    document.body.appendChild(container);
    return container;
  }

  // ============================================
  // ✅ دوال مساعدة للتوقيع
  // ============================================
  window.initSignatureCanvas = function (canvas) {
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    let drawing = false;
    let lastX = 0;
    let lastY = 0;

    ctx.strokeStyle = "#1a1a6e";
    ctx.lineWidth = 2.5;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";

    function getPos(e) {
      const rect = canvas.getBoundingClientRect();
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      return {
        x: (clientX - rect.left) * (canvas.width / rect.width),
        y: (clientY - rect.top) * (canvas.height / rect.height),
      };
    }

    function startDrawing(e) {
      e.preventDefault();
      drawing = true;
      const pos = getPos(e);
      lastX = pos.x;
      lastY = pos.y;
      ctx.beginPath();
      ctx.moveTo(lastX, lastY);
    }

    function draw(e) {
      if (!drawing) return;
      e.preventDefault();
      const pos = getPos(e);
      ctx.lineTo(pos.x, pos.y);
      ctx.stroke();
      lastX = pos.x;
      lastY = pos.y;
    }

    function stopDrawing() {
      if (drawing) {
        drawing = false;
        updateSignature(canvas);
      }
    }

    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mouseleave", stopDrawing);
    canvas.addEventListener("touchstart", startDrawing, { passive: false });
    canvas.addEventListener("touchmove", draw, { passive: false });
    canvas.addEventListener("touchend", stopDrawing);
    canvas.addEventListener("touchcancel", stopDrawing);
  };

  function updateSignature(canvas) {
    const fieldName = canvas.dataset.field;
    const input = document.getElementById(`field_${fieldName}`);
    if (input) {
      input.value = canvas.toDataURL("image/png");
      canvas.classList.add("has-signature");
    }
  }

  window.clearSignature = function (fieldName) {
    const canvas = document.getElementById(`canvas_${fieldName}`);
    if (canvas) {
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      canvas.classList.remove("has-signature");
      const input = document.getElementById(`field_${fieldName}`);
      if (input) input.value = "";
    }
  };

  // ============================================
  // ✅ دوال التحقق من النموذج
  // ============================================
  window.validateReportForm = function () {
    let valid = true;
    document.querySelectorAll("[required]").forEach((field) => {
      if (field.type === "checkbox") {
        if (!field.checked) {
          field.classList.add("is-invalid");
          valid = false;
        } else {
          field.classList.remove("is-invalid");
        }
      } else if (!field.value.trim()) {
        field.classList.add("is-invalid");
        valid = false;
      } else {
        field.classList.remove("is-invalid");
      }
    });
    return valid;
  };

  // ============================================
  // ✅ دوال جمع البيانات
  // ============================================
  window.collectReportData = function () {
    const form = document.getElementById("reportForm");
    if (!form) return {};

    const formData = new FormData(form);
    const data = {};

    formData.forEach((value, key) => {
      const input = document.getElementById(key);
      if (input && input.type === "checkbox") {
        data[key] = input.checked ? "1" : "0";
      } else {
        data[key] = value;
      }
    });

    // إضافة بيانات التوقيع
    document.querySelectorAll(".signature-canvas").forEach((canvas) => {
      const fieldName = canvas.dataset.field;
      const input = document.getElementById(`field_${fieldName}`);
      if (input && input.value) {
        data[fieldName] = input.value;
      }
    });

    return data;
  };

  // ============================================
  // ✅ دوال حفظ التقرير
  // ============================================
  window.saveReport = async function (templateId, reportId, onSuccess) {
    if (!validateReportForm()) {
      showNotification("الرجاء تعبئة جميع الحقول المطلوبة", "error");
      return;
    }

    const url = reportId ? `/api/reports/${reportId}` : "/api/reports";
    const method = reportId ? "PUT" : "POST";
    const formData = collectReportData();

    try {
      const response = await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          template_id: parseInt(templateId),
          form_data: formData,
          patient_uid: null,
        }),
      });

      const result = await response.json();

      if (result.success) {
        const report = result.report;
        if (report?.id) {
          document.getElementById("reportId").value = report.id;
        }

        const resultDiv = document.getElementById("saveResult");
        if (resultDiv) {
          resultDiv.innerHTML = `
            <div class="alert alert-success">
              <i class="fas fa-check-circle me-2"></i>
              <strong>تم ${reportId ? "تعديل" : "حفظ"} التقرير بنجاح!</strong>
              <br>
              <small>تقرير: <code>${report?.report_uid || "N/A"}</code></small>
              ${report?.patient_uid ? `<br><small>مريض: <code>${report.patient_uid}</code></small>` : ""}
            </div>
          `;
        }

        showNotification(
          `✅ تم ${reportId ? "تعديل" : "حفظ"} التقرير`,
          "success",
        );

        if (typeof onSuccess === "function") {
          onSuccess(report);
        }

        if (!reportId) {
          setTimeout(() => {
            window.location.href = "/reports";
          }, 1500);
        }
      } else {
        showNotification(result.error || "فشل حفظ التقرير", "error");
      }
    } catch (error) {
      console.error("Error saving report:", error);
      showNotification("خطأ في الاتصال بالخادم", "error");
    }
  };

  // ============================================
  // ✅ حفظ وتوليد PDF
  // ============================================
  window.saveAndGeneratePDF = async function (templateId, reportId) {
    if (!validateReportForm()) {
      showNotification("الرجاء تعبئة جميع الحقول المطلوبة", "error");
      return;
    }

    const resultDiv = document.getElementById("saveResult");
    if (resultDiv) {
      resultDiv.innerHTML = `
        <div class="text-center py-3">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="mt-2 text-muted">جاري ${reportId ? "تعديل" : "حفظ"} التقرير...</p>
        </div>
      `;
    }

    try {
      // 1. حفظ التقرير
      const url = reportId ? `/api/reports/${reportId}` : "/api/reports";
      const method = reportId ? "PUT" : "POST";
      const formData = collectReportData();

      const response = await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          template_id: parseInt(templateId),
          form_data: formData,
          patient_uid: null,
        }),
      });

      const result = await response.json();

      if (!result.success) {
        showNotification(result.error || "فشل حفظ التقرير", "error");
        if (resultDiv) resultDiv.innerHTML = "";
        return;
      }

      const report = result.report;
      const reportIdResult = report?.id;

      if (
        !reportIdResult ||
        reportIdResult === "" ||
        reportIdResult === "undefined"
      ) {
        showNotification(
          "❌ لا يمكن توليد PDF: معرف التقرير غير صحيح",
          "error",
        );
        if (resultDiv) {
          resultDiv.innerHTML = `
            <div class="alert alert-danger">
              <i class="fas fa-exclamation-triangle me-2"></i>
              <strong>فشل توليد PDF</strong>
              <br>
              <small>معرف التقرير غير صحيح</small>
            </div>
          `;
        }
        return;
      }

      if (resultDiv) {
        resultDiv.innerHTML = `
          <div class="alert alert-success">
            <i class="fas fa-check-circle me-2"></i>
            <strong>تم ${reportId ? "تعديل" : "حفظ"} التقرير!</strong>
            <br>
            <small>تقرير: <code>${report?.report_uid}</code></small>
            <br>
            <small>جاري تحميل PDF...</small>
          </div>
        `;
      }

      showNotification("✅ جاري تحميل PDF...", "success");

      // 2. فتح PDF في نافذة جديدة
      const pdfUrl = `/api/reports/${reportIdResult}/pdf`;
      window.open(pdfUrl, "_blank");
    } catch (error) {
      console.error("Error:", error);
      showNotification("خطأ في الاتصال بالخادم", "error");
      if (resultDiv) resultDiv.innerHTML = "";
    }
  };

  // ============================================
  // ✅ دوال التصفح والفلترة
  // ============================================
  window.filterByCategory = function () {
    const category = document.getElementById("categoryFilter").value;
    window.loadReports && window.loadReports(category);
  };

  window.scrollToReports = function (templateId) {
    const element = document.getElementById(`reports-${templateId}`);
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "center" });
      element.style.transition = "background 0.5s";
      element.style.background = "#e8ebff";
      setTimeout(() => {
        element.style.background = "transparent";
      }, 2000);
    }
  };

  // ============================================
  // ✅ تهيئة الصفحة
  // ============================================
  console.log("📄 Reports common functions loaded");
})();
