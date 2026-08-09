/* ================================================
   report_form.js - With Edit Support + Data Loading + Notifications
   ================================================ */

const templateId = document.getElementById("templateId")?.value;
const editReportId = window.EDIT_REPORT ? window.EDIT_REPORT.id : null;
const editReportData = window.EDIT_REPORT ? window.EDIT_REPORT.data : null;

// ============================================
// ✅ دوال الإشعارات (مدمجة)
// ============================================
function showNotification(message, type = "info") {
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
}

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
// ✅ تحميل بيانات التعديل
// ============================================
if (editReportData) {
  console.log("📝 Loading edit data for report:", editReportId);

  setTimeout(() => {
    // استعادة التوقيعات على Canvas
    for (const [key, value] of Object.entries(editReportData)) {
      if (typeof value === "string" && value.startsWith("data:image")) {
        const canvas = document.getElementById(`canvas_${key}`);
        if (canvas) {
          const ctx = canvas.getContext("2d");
          const img = new Image();
          img.onload = function () {
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            canvas.classList.add("has-signature");
          };
          img.onerror = function () {
            console.warn("⚠️ Could not load signature for:", key);
          };
          img.src = value;
        }
      }
    }
    console.log("✅ Edit data loaded successfully");
  }, 500);
}

// ============================================
// ✅ التوقيع (Canvas)
// ============================================
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".signature-canvas").forEach((c) => {
    initSignatureCanvas(c);
  });

  document.querySelectorAll(".form-check-input").forEach((input) => {
    const wrapper = input.closest(".field-wrapper");
    if (wrapper) {
      const label = wrapper.querySelector(".form-label");
      if (label) label.classList.remove("required-field");
    }
  });

  console.log("📝 Report form initialized");
  console.log("📋 Template ID:", templateId);
  console.log("✏️ Edit mode:", !!editReportId);
});

function initSignatureCanvas(canvas) {
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
}

function updateSignature(canvas) {
  const fieldName = canvas.dataset.field;
  const input = document.getElementById(`field_${fieldName}`);
  if (input) {
    input.value = canvas.toDataURL("image/png");
    canvas.classList.add("has-signature");
  }
}

function clearSignature(fieldName) {
  const canvas = document.getElementById(`canvas_${fieldName}`);
  if (canvas) {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    canvas.classList.remove("has-signature");
    const input = document.getElementById(`field_${fieldName}`);
    if (input) input.value = "";
  }
}

// ============================================
// ✅ جمع بيانات النموذج
// ============================================
function collectFormData() {
  const form = document.getElementById("reportForm");
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

  // إضافة بيانات التوقيع من Canvas
  document.querySelectorAll(".signature-canvas").forEach((canvas) => {
    const fieldName = canvas.dataset.field;
    const input = document.getElementById(`field_${fieldName}`);
    if (input && input.value) {
      data[fieldName] = input.value;
    }
  });

  return data;
}

// ============================================
// ✅ التحقق من النموذج
// ============================================
function validateForm() {
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
}

// ============================================
// ✅ حفظ التقرير
// ============================================
async function saveReport() {
  if (!validateForm()) {
    showNotification("الرجاء تعبئة جميع الحقول المطلوبة", "error");
    return;
  }

  const url = editReportId ? `/api/reports/${editReportId}` : "/api/reports";
  const method = editReportId ? "PUT" : "POST";
  const formData = collectFormData();

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

      // ✅ تحديث معرف التقرير
      if (report?.id) {
        document.getElementById("reportId").value = report.id;
      }

      document.getElementById("saveResult").innerHTML = `
        <div class="alert alert-success">
          <i class="fas fa-check-circle me-2"></i>
          <strong>تم ${editReportId ? "تعديل" : "حفظ"} التقرير بنجاح!</strong>
          <br>
          <small>تقرير: <code>${report?.report_uid || "N/A"}</code></small>
          ${report?.patient_uid ? `<br><small>مريض: <code>${report.patient_uid}</code></small>` : ""}
        </div>
      `;

      showNotification(
        `✅ تم ${editReportId ? "تعديل" : "حفظ"} التقرير`,
        "success",
      );

      if (!editReportId) {
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
}

// ============================================
// ✅ حفظ وتوليد PDF (المعدل - الحل النهائي)
// ============================================
async function saveAndGeneratePDF() {
  if (!validateForm()) {
    showNotification("الرجاء تعبئة جميع الحقول المطلوبة", "error");
    return;
  }

  const url = editReportId ? `/api/reports/${editReportId}` : "/api/reports";
  const method = editReportId ? "PUT" : "POST";
  const formData = collectFormData();

  const resultDiv = document.getElementById("saveResult");
  resultDiv.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">جاري ${editReportId ? "تعديل" : "حفظ"} التقرير...</p>
    </div>
  `;

  try {
    // ✅ 1. حفظ التقرير
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
      resultDiv.innerHTML = "";
      return;
    }

    const report = result.report;
    const reportId = report?.id;
    const reportUid = report?.report_uid;

    // ✅ 2. التحقق من وجود reportId
    if (!reportId || reportId === "" || reportId === "undefined") {
      showNotification("❌ لا يمكن توليد PDF: معرف التقرير غير صحيح", "error");
      resultDiv.innerHTML = `
        <div class="alert alert-danger">
          <i class="fas fa-exclamation-triangle me-2"></i>
          <strong>فشل توليد PDF</strong>
          <br>
          <small>معرف التقرير غير صحيح</small>
        </div>
      `;
      return;
    }

    // ✅ 3. عرض رسالة نجاح
    resultDiv.innerHTML = `
      <div class="alert alert-success">
        <i class="fas fa-check-circle me-2"></i>
        <strong>تم ${editReportId ? "تعديل" : "حفظ"} التقرير!</strong>
        <br>
        <small>تقرير: <code>${reportUid}</code></small>
        <br>
        <small>جاري تحميل PDF...</small>
      </div>
    `;

    showNotification("✅ جاري تحميل PDF...", "success");

    // ✅ 4. فتح PDF في نافذة جديدة
    const pdfUrl = `/api/reports/${reportId}/pdf`;
    window.open(pdfUrl, "_blank");
  } catch (error) {
    console.error("Error:", error);
    showNotification("خطأ في الاتصال بالخادم", "error");
    resultDiv.innerHTML = "";
  }
}
