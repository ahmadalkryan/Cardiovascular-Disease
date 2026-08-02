// // // // /* ================================================
// // // //    report_form.js - Report Form Logic
// // // //    ================================================ */

// // // // const templateId = document.getElementById("templateId").value;
// // // // let lastReportId = null;

// // // // // ================================================
// // // // // Collect Form Data
// // // // // ================================================
// // // // function collectFormData() {
// // // //   const form = document.getElementById("reportForm");
// // // //   const formData = new FormData(form);
// // // //   const data = {};

// // // //   formData.forEach((value, key) => {
// // // //     // Convert checkbox values
// // // //     const input = document.getElementById(key);
// // // //     if (input && input.type === "checkbox") {
// // // //       data[key] = input.checked;
// // // //     } else {
// // // //       data[key] = value;
// // // //     }
// // // //   });

// // // //   return data;
// // // // }

// // // // // ================================================
// // // // // Validate Form
// // // // // ================================================
// // // // function validateForm() {
// // // //   const requiredFields = document.querySelectorAll("[required]");
// // // //   let isValid = true;

// // // //   requiredFields.forEach((field) => {
// // // //     if (!field.value.trim()) {
// // // //       field.classList.add("is-invalid");
// // // //       isValid = false;
// // // //     } else {
// // // //       field.classList.remove("is-invalid");
// // // //     }
// // // //   });

// // // //   return isValid;
// // // // }

// // // // // ================================================
// // // // // Save Report
// // // // // ================================================
// // // // async function saveReport() {
// // // //   if (!validateForm()) {
// // // //     showNotification("الرجاء ملء جميع الحقول المطلوبة", "error");
// // // //     return;
// // // //   }

// // // //   const formData = collectFormData();
// // // //   const patientId = document.getElementById("patientId").value || null;
// // // //   const doctorId = document.getElementById("doctorId").value || null;

// // // //   try {
// // // //     const response = await fetch("/api/reports", {
// // // //       method: "POST",
// // // //       headers: { "Content-Type": "application/json" },
// // // //       body: JSON.stringify({
// // // //         template_id: parseInt(templateId),
// // // //         form_data: formData,
// // // //         patient_id: patientId,
// // // //         doctor_id: doctorId,
// // // //       }),
// // // //     });

// // // //     const result = await response.json();

// // // //     if (result.success) {
// // // //       lastReportId = result.report.id;
// // // //       document.getElementById("saveResult").innerHTML = `
// // // //         <div class="alert alert-success">
// // // //           <i class="fas fa-check-circle me-2"></i>
// // // //           <strong>تم حفظ التقرير بنجاح!</strong>
// // // //           <br>معرف التقرير: <code>${result.report.id}</code>
// // // //         </div>`;
// // // //       showNotification("تم حفظ التقرير بنجاح", "success");
// // // //     } else {
// // // //       showNotification(result.error || "فشل في حفظ التقرير", "error");
// // // //     }
// // // //   } catch (error) {
// // // //     console.error("Error saving report:", error);
// // // //     showNotification("خطأ في الاتصال بالخادم", "error");
// // // //   }
// // // // }

// // // // // ================================================
// // // // // Save and Generate PDF
// // // // // ================================================
// // // // async function saveAndGeneratePDF() {
// // // //   if (!validateForm()) {
// // // //     showNotification("الرجاء ملء جميع الحقول المطلوبة", "error");
// // // //     return;
// // // //   }

// // // //   // First save
// // // //   const formData = collectFormData();
// // // //   const patientId = document.getElementById("patientId").value || null;
// // // //   const doctorId = document.getElementById("doctorId").value || null;

// // // //   try {
// // // //     document.getElementById("saveResult").innerHTML = `
// // // //       <div class="text-center">
// // // //         <div class="spinner-border text-primary" role="status"></div>
// // // //         <p class="mt-2">جاري حفظ التقرير وتوليد PDF...</p>
// // // //       </div>`;

// // // //     const saveResponse = await fetch("/api/reports", {
// // // //       method: "POST",
// // // //       headers: { "Content-Type": "application/json" },
// // // //       body: JSON.stringify({
// // // //         template_id: parseInt(templateId),
// // // //         form_data: formData,
// // // //         patient_id: patientId,
// // // //         doctor_id: doctorId,
// // // //       }),
// // // //     });

// // // //     const saveResult = await saveResponse.json();

// // // //     if (!saveResult.success) {
// // // //       showNotification(saveResult.error || "فشل في حفظ التقرير", "error");
// // // //       document.getElementById("saveResult").innerHTML = "";
// // // //       return;
// // // //     }

// // // //     lastReportId = saveResult.report.id;

// // // //     // Then generate PDF
// // // //     window.location.href = `/api/reports/${saveResult.report.id}/pdf`;

// // // //     document.getElementById("saveResult").innerHTML = `
// // // //       <div class="alert alert-success">
// // // //         <i class="fas fa-check-circle me-2"></i>
// // // //         <strong>تم حفظ التقرير وجاري تحميل PDF...</strong>
// // // //       </div>`;
// // // //   } catch (error) {
// // // //     console.error("Error:", error);
// // // //     showNotification("خطأ في الاتصال بالخادم", "error");
// // // //     document.getElementById("saveResult").innerHTML = "";
// // // //   }
// // // // }

// // // // // ================================================
// // // // // Initialize
// // // // // ================================================
// // // // document.addEventListener("DOMContentLoaded", () => {
// // // //   // Remove required attribute from checkbox labels (they have their own)
// // // //   document.querySelectorAll(".form-check-input").forEach((input) => {
// // // //     const wrapper = input.closest(".field-wrapper");
// // // //     if (wrapper) {
// // // //       const label = wrapper.querySelector(".form-label");
// // // //       if (label) label.classList.remove("required-field");
// // // //     }
// // // //   });
// // // // });
// // // /* ================================================
// // //    report_form.js - With Signature Support
// // //    ================================================ */

// // // const templateId = document.getElementById("templateId").value;

// // // // ================================================
// // // // Signature Functions
// // // // ================================================
// // // document.addEventListener("DOMContentLoaded", () => {
// // //   // Init all signature canvases
// // //   document.querySelectorAll(".signature-canvas").forEach((canvas) => {
// // //     initSignatureCanvas(canvas);
// // //   });

// // //   // Remove required from checkbox labels
// // //   document.querySelectorAll(".form-check-input").forEach((input) => {
// // //     const wrapper = input.closest(".field-wrapper");
// // //     if (wrapper) {
// // //       const label = wrapper.querySelector(".form-label");
// // //       if (label) label.classList.remove("required-field");
// // //     }
// // //   });
// // // });

// // // function initSignatureCanvas(canvas) {
// // //   const ctx = canvas.getContext("2d");
// // //   let drawing = false;

// // //   ctx.strokeStyle = "#000066";
// // //   ctx.lineWidth = 2.5;
// // //   ctx.lineCap = "round";
// // //   ctx.lineJoin = "round";

// // //   function getPos(e) {
// // //     const rect = canvas.getBoundingClientRect();
// // //     const scaleX = canvas.width / rect.width;
// // //     const scaleY = canvas.height / rect.height;
// // //     const clientX = e.touches ? e.touches[0].clientX : e.clientX;
// // //     const clientY = e.touches ? e.touches[0].clientY : e.clientY;
// // //     return {
// // //       x: (clientX - rect.left) * scaleX,
// // //       y: (clientY - rect.top) * scaleY,
// // //     };
// // //   }

// // //   function startDraw(e) {
// // //     e.preventDefault();
// // //     drawing = true;
// // //     ctx.beginPath();
// // //     const pos = getPos(e);
// // //     ctx.moveTo(pos.x, pos.y);
// // //   }

// // //   function draw(e) {
// // //     if (!drawing) return;
// // //     e.preventDefault();
// // //     const pos = getPos(e);
// // //     ctx.lineTo(pos.x, pos.y);
// // //     ctx.stroke();
// // //   }

// // //   function endDraw() {
// // //     drawing = false;
// // //     updateSignatureValue(canvas);
// // //   }

// // //   canvas.addEventListener("mousedown", startDraw);
// // //   canvas.addEventListener("mousemove", draw);
// // //   canvas.addEventListener("mouseup", endDraw);
// // //   canvas.addEventListener("mouseleave", endDraw);
// // //   canvas.addEventListener("touchstart", startDraw, { passive: false });
// // //   canvas.addEventListener("touchmove", draw, { passive: false });
// // //   canvas.addEventListener("touchend", endDraw);
// // // }

// // // function updateSignatureValue(canvas) {
// // //   const fieldName = canvas.dataset.field;
// // //   const dataUrl = canvas.toDataURL("image/png");
// // //   const hiddenInput = document.getElementById(`field_${fieldName}`);
// // //   if (hiddenInput) hiddenInput.value = dataUrl;
// // // }

// // // function clearSignature(fieldName) {
// // //   const canvas = document.getElementById(`canvas_${fieldName}`);
// // //   if (canvas) {
// // //     const ctx = canvas.getContext("2d");
// // //     ctx.clearRect(0, 0, canvas.width, canvas.height);
// // //     const hiddenInput = document.getElementById(`field_${fieldName}`);
// // //     if (hiddenInput) hiddenInput.value = "";
// // //   }
// // // }

// // // function uploadSignatureImage(input, fieldName) {
// // //   const file = input.files[0];
// // //   if (!file) return;

// // //   const reader = new FileReader();
// // //   reader.onload = function (e) {
// // //     const preview = document.getElementById(`preview_${fieldName}`);
// // //     if (preview) {
// // //       preview.src = e.target.result;
// // //       preview.style.display = "block";
// // //     }
// // //     const hiddenInput = document.getElementById(`field_${fieldName}`);
// // //     if (hiddenInput) hiddenInput.value = e.target.result;
// // //   };
// // //   reader.readAsDataURL(file);
// // // }

// // // function clearUploadedSignature(fieldName) {
// // //   const preview = document.getElementById(`preview_${fieldName}`);
// // //   if (preview) {
// // //     preview.src = "";
// // //     preview.style.display = "none";
// // //   }
// // //   const hiddenInput = document.getElementById(`field_${fieldName}`);
// // //   if (hiddenInput) hiddenInput.value = "";
// // //   const fileInput = document.querySelector(
// // //     `#upload-${fieldName} input[type="file"]`,
// // //   );
// // //   if (fileInput) fileInput.value = "";
// // // }

// // // // ================================================
// // // // Collect Form Data
// // // // ================================================
// // // function collectFormData() {
// // //   const form = document.getElementById("reportForm");
// // //   const formData = new FormData(form);
// // //   const data = {};

// // //   formData.forEach((value, key) => {
// // //     const input = document.getElementById(key);
// // //     if (input && input.type === "checkbox") {
// // //       data[key] = input.checked;
// // //     } else {
// // //       data[key] = value;
// // //     }
// // //   });
// // //   return data;
// // // }

// // // // ================================================
// // // // Validate Form
// // // // ================================================
// // // function validateForm() {
// // //   const requiredFields = document.querySelectorAll("[required]");
// // //   let isValid = true;
// // //   requiredFields.forEach((field) => {
// // //     if (!field.value.trim()) {
// // //       field.classList.add("is-invalid");
// // //       isValid = false;
// // //     } else {
// // //       field.classList.remove("is-invalid");
// // //     }
// // //   });
// // //   return isValid;
// // // }

// // // // ================================================
// // // // Save Report
// // // // ================================================
// // // async function saveReport() {
// // //   if (!validateForm()) {
// // //     showNotification("الرجاء ملء جميع الحقول المطلوبة", "error");
// // //     return;
// // //   }

// // //   const formData = collectFormData();
// // //   const patientId = document.getElementById("patientId").value.trim() || null;

// // //   try {
// // //     const response = await fetch("/api/reports", {
// // //       method: "POST",
// // //       headers: { "Content-Type": "application/json" },
// // //       body: JSON.stringify({
// // //         template_id: parseInt(templateId),
// // //         form_data: formData,
// // //         patient_uid: patientId,
// // //       }),
// // //     });

// // //     const result = await response.json();

// // //     if (result.success) {
// // //       document.getElementById("saveResult").innerHTML = `
// // //                 <div class="alert alert-success">
// // //                     <i class="fas fa-check-circle me-2"></i>
// // //                     <strong>تم حفظ التقرير بنجاح!</strong>
// // //                     <br>رقم التقرير: <code>${result.report.report_uid}</code>
// // //                     <br>معرف المريض: <code>${result.report.patient_uid}</code>
// // //                 </div>`;
// // //       showNotification("تم حفظ التقرير بنجاح", "success");
// // //     } else {
// // //       showNotification(result.error || "فشل في حفظ التقرير", "error");
// // //     }
// // //   } catch (error) {
// // //     console.error("Error saving report:", error);
// // //     showNotification("خطأ في الاتصال بالخادم", "error");
// // //   }
// // // }

// // // // ================================================
// // // // Save and Generate PDF
// // // // ================================================
// // // async function saveAndGeneratePDF() {
// // //   if (!validateForm()) {
// // //     showNotification("الرجاء ملء جميع الحقول المطلوبة", "error");
// // //     return;
// // //   }

// // //   const formData = collectFormData();
// // //   const patientId = document.getElementById("patientId").value.trim() || null;

// // //   try {
// // //     document.getElementById("saveResult").innerHTML = `
// // //             <div class="text-center">
// // //                 <div class="spinner-border text-primary" role="status"></div>
// // //                 <p class="mt-2">جاري حفظ التقرير وتوليد PDF...</p>
// // //             </div>`;

// // //     const saveResponse = await fetch("/api/reports", {
// // //       method: "POST",
// // //       headers: { "Content-Type": "application/json" },
// // //       body: JSON.stringify({
// // //         template_id: parseInt(templateId),
// // //         form_data: formData,
// // //         patient_uid: patientId,
// // //       }),
// // //     });

// // //     const saveResult = await saveResponse.json();

// // //     if (!saveResult.success) {
// // //       showNotification(saveResult.error || "فشل في حفظ التقرير", "error");
// // //       document.getElementById("saveResult").innerHTML = "";
// // //       return;
// // //     }

// // //     window.location.href = `/api/reports/${saveResult.report.id}/pdf`;

// // //     document.getElementById("saveResult").innerHTML = `
// // //             <div class="alert alert-success">
// // //                 <i class="fas fa-check-circle me-2"></i>
// // //                 <strong>تم حفظ التقرير وجاري تحميل PDF...</strong>
// // //                 <br>رقم التقرير: <code>${saveResult.report.report_uid}</code>
// // //             </div>`;
// // //   } catch (error) {
// // //     console.error("Error:", error);
// // //     showNotification("خطأ في الاتصال بالخادم", "error");
// // //     document.getElementById("saveResult").innerHTML = "";
// // //   }
// // // }
// // /* ================================================
// //    report_form.js - Final Version
// //    ================================================ */

// // const templateId = document.getElementById("templateId").value;

// // // ═══════════════════════════════════════════
// // // Signature (Canvas only)
// // // ═══════════════════════════════════════════
// // document.addEventListener("DOMContentLoaded", () => {
// //   document
// //     .querySelectorAll(".signature-canvas")
// //     .forEach((c) => initSignatureCanvas(c));
// //   document.querySelectorAll(".form-check-input").forEach((input) => {
// //     const w = input.closest(".field-wrapper");
// //     if (w) {
// //       const l = w.querySelector(".form-label");
// //       if (l) l.classList.remove("required-field");
// //     }
// //   });
// // });

// // function initSignatureCanvas(canvas) {
// //   const ctx = canvas.getContext("2d");
// //   let drawing = false;
// //   ctx.strokeStyle = "#1a1a6e";
// //   ctx.lineWidth = 2.5;
// //   ctx.lineCap = "round";
// //   ctx.lineJoin = "round";

// //   function getPos(e) {
// //     const r = canvas.getBoundingClientRect();
// //     return {
// //       x:
// //         ((e.touches ? e.touches[0].clientX : e.clientX) - r.left) *
// //         (canvas.width / r.width),
// //       y:
// //         ((e.touches ? e.touches[0].clientY : e.clientY) - r.top) *
// //         (canvas.height / r.height),
// //     };
// //   }

// //   function start(e) {
// //     e.preventDefault();
// //     drawing = true;
// //     ctx.beginPath();
// //     const p = getPos(e);
// //     ctx.moveTo(p.x, p.y);
// //   }
// //   function move(e) {
// //     if (!drawing) return;
// //     e.preventDefault();
// //     const p = getPos(e);
// //     ctx.lineTo(p.x, p.y);
// //     ctx.stroke();
// //   }
// //   function end() {
// //     drawing = false;
// //     updateSignature(canvas);
// //   }

// //   canvas.addEventListener("mousedown", start);
// //   canvas.addEventListener("mousemove", move);
// //   canvas.addEventListener("mouseup", end);
// //   canvas.addEventListener("mouseleave", end);
// //   canvas.addEventListener("touchstart", start, { passive: false });
// //   canvas.addEventListener("touchmove", move, { passive: false });
// //   canvas.addEventListener("touchend", end);
// // }

// // function updateSignature(canvas) {
// //   const input = document.getElementById(`field_${canvas.dataset.field}`);
// //   if (input) input.value = canvas.toDataURL("image/png");
// // }

// // function clearSignature(fieldName) {
// //   const canvas = document.getElementById(`canvas_${fieldName}`);
// //   if (canvas) {
// //     canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
// //     const input = document.getElementById(`field_${fieldName}`);
// //     if (input) input.value = "";
// //   }
// // }

// // // ═══════════════════════════════════════════
// // // Form Data
// // // ═══════════════════════════════════════════
// // function collectFormData() {
// //   const fd = new FormData(document.getElementById("reportForm"));
// //   const data = {};
// //   fd.forEach((v, k) => {
// //     const input = document.getElementById(k);
// //     data[k] = input && input.type === "checkbox" ? input.checked : v;
// //   });
// //   return data;
// // }

// // function validateForm() {
// //   let valid = true;
// //   document.querySelectorAll("[required]").forEach((f) => {
// //     if (!f.value.trim()) {
// //       f.classList.add("is-invalid");
// //       valid = false;
// //     } else f.classList.remove("is-invalid");
// //   });
// //   return valid;
// // }

// // // ═══════════════════════════════════════════
// // // API Calls (patient_uid = null → auto)
// // // ═══════════════════════════════════════════
// // async function saveReport() {
// //   if (!validateForm()) {
// //     showNotification("املأ الحقول المطلوبة", "error");
// //     return;
// //   }
// //   try {
// //     const r = await fetch("/api/reports", {
// //       method: "POST",
// //       headers: { "Content-Type": "application/json" },
// //       body: JSON.stringify({
// //         template_id: parseInt(templateId),
// //         form_data: collectFormData(),
// //         patient_uid: null,
// //       }),
// //     });
// //     const j = await r.json();
// //     if (j.success) {
// //       document.getElementById("saveResult").innerHTML =
// //         `<div class="alert alert-success"><i class="fas fa-check-circle me-2"></i><strong>تم الحفظ!</strong><br>تقرير: <code>${j.report.report_uid}</code> | مريض: <code>${j.report.patient_uid}</code></div>`;
// //       showNotification("تم الحفظ", "success");
// //     } else showNotification(j.error || "فشل", "error");
// //   } catch (e) {
// //     showNotification("خطأ اتصال", "error");
// //   }
// // }

// // async function saveAndGeneratePDF() {
// //   if (!validateForm()) {
// //     showNotification("املأ الحقول المطلوبة", "error");
// //     return;
// //   }
// //   try {
// //     document.getElementById("saveResult").innerHTML =
// //       `<div class="text-center"><div class="spinner-border text-primary"></div><p class="mt-2">جاري الحفظ وتوليد PDF...</p></div>`;
// //     const r = await fetch("/api/reports", {
// //       method: "POST",
// //       headers: { "Content-Type": "application/json" },
// //       body: JSON.stringify({
// //         template_id: parseInt(templateId),
// //         form_data: collectFormData(),
// //         patient_uid: null,
// //       }),
// //     });
// //     const j = await r.json();
// //     if (j.success) {
// //       window.location.href = `/api/reports/${j.report.id}/pdf`;
// //       document.getElementById("saveResult").innerHTML =
// //         `<div class="alert alert-success"><i class="fas fa-check-circle me-2"></i><strong>جاري تحميل PDF...</strong><br>تقرير: <code>${j.report.report_uid}</code></div>`;
// //     } else {
// //       showNotification(j.error || "فشل", "error");
// //       document.getElementById("saveResult").innerHTML = "";
// //     }
// //   } catch (e) {
// //     showNotification("خطأ اتصال", "error");
// //     document.getElementById("saveResult").innerHTML = "";
// //   }
// // }
// /* ================================================
//    report_form.js - With Edit Support
//    ================================================ */

// const templateId = document.getElementById("templateId").value;
// const editReportId = window.EDIT_REPORT ? window.EDIT_REPORT.id : null;
// const editReportData = window.EDIT_REPORT ? window.EDIT_REPORT.data : null;

// // ═══════════════════════════════════════════
// // Load existing data if editing
// // ═══════════════════════════════════════════
// if (editReportData) {
//   setTimeout(() => {
//     for (const [key, value] of Object.entries(editReportData)) {
//       const input = document.getElementById(`field_${key}`);
//       if (input) {
//         if (input.type === "checkbox") {
//           input.checked = value === true || value === "1" || value === 1;
//         } else if (
//           input.type === "hidden" &&
//           typeof value === "string" &&
//           value.startsWith("data:image")
//         ) {
//           // Signature - keep Base64 value
//           input.value = value;
//         } else {
//           input.value = value || "";
//         }
//       }
//     }
//   }, 300);
// }

// // ═══════════════════════════════════════════
// // Signature (Canvas only)
// // ═══════════════════════════════════════════
// document.addEventListener("DOMContentLoaded", () => {
//   document
//     .querySelectorAll(".signature-canvas")
//     .forEach((c) => initSignatureCanvas(c));
//   document.querySelectorAll(".form-check-input").forEach((input) => {
//     const w = input.closest(".field-wrapper");
//     if (w) {
//       const l = w.querySelector(".form-label");
//       if (l) l.classList.remove("required-field");
//     }
//   });
// });

// function initSignatureCanvas(canvas) {
//   const ctx = canvas.getContext("2d");
//   let drawing = false;
//   ctx.strokeStyle = "#1a1a6e";
//   ctx.lineWidth = 2.5;
//   ctx.lineCap = "round";
//   ctx.lineJoin = "round";

//   function getPos(e) {
//     const r = canvas.getBoundingClientRect();
//     return {
//       x:
//         ((e.touches ? e.touches[0].clientX : e.clientX) - r.left) *
//         (canvas.width / r.width),
//       y:
//         ((e.touches ? e.touches[0].clientY : e.clientY) - r.top) *
//         (canvas.height / r.height),
//     };
//   }

//   function start(e) {
//     e.preventDefault();
//     drawing = true;
//     ctx.beginPath();
//     const p = getPos(e);
//     ctx.moveTo(p.x, p.y);
//   }
//   function move(e) {
//     if (!drawing) return;
//     e.preventDefault();
//     const p = getPos(e);
//     ctx.lineTo(p.x, p.y);
//     ctx.stroke();
//   }
//   function end() {
//     drawing = false;
//     updateSignature(canvas);
//   }

//   canvas.addEventListener("mousedown", start);
//   canvas.addEventListener("mousemove", move);
//   canvas.addEventListener("mouseup", end);
//   canvas.addEventListener("mouseleave", end);
//   canvas.addEventListener("touchstart", start, { passive: false });
//   canvas.addEventListener("touchmove", move, { passive: false });
//   canvas.addEventListener("touchend", end);
// }

// function updateSignature(canvas) {
//   const input = document.getElementById(`field_${canvas.dataset.field}`);
//   if (input) input.value = canvas.toDataURL("image/png");
// }

// function clearSignature(fieldName) {
//   const canvas = document.getElementById(`canvas_${fieldName}`);
//   if (canvas) {
//     canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
//     const input = document.getElementById(`field_${fieldName}`);
//     if (input) input.value = "";
//   }
// }

// // ═══════════════════════════════════════════
// // Form Data
// // ═══════════════════════════════════════════
// function collectFormData() {
//   const fd = new FormData(document.getElementById("reportForm"));
//   const data = {};
//   fd.forEach((v, k) => {
//     const input = document.getElementById(k);
//     data[k] = input && input.type === "checkbox" ? input.checked : v;
//   });
//   return data;
// }

// function validateForm() {
//   let valid = true;
//   document.querySelectorAll("[required]").forEach((f) => {
//     if (!f.value.trim()) {
//       f.classList.add("is-invalid");
//       valid = false;
//     } else f.classList.remove("is-invalid");
//   });
//   return valid;
// }

// // ═══════════════════════════════════════════
// // API Calls (Create or Update)
// // ═══════════════════════════════════════════
// async function saveReport() {
//   if (!validateForm()) {
//     showNotification("املأ الحقول المطلوبة", "error");
//     return;
//   }

//   const url = editReportId ? `/api/reports/${editReportId}` : "/api/reports";
//   const method = editReportId ? "PUT" : "POST";

//   try {
//     const r = await fetch(url, {
//       method: method,
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({
//         template_id: parseInt(templateId),
//         form_data: collectFormData(),
//         patient_uid: null,
//       }),
//     });
//     const j = await r.json();
//     if (j.success) {
//       document.getElementById("saveResult").innerHTML =
//         `<div class="alert alert-success"><i class="fas fa-check-circle me-2"></i><strong>تم ${editReportId ? "تعديل" : "حفظ"} التقرير!</strong><br>تقرير: <code>${j.report.report_uid}</code> | مريض: <code>${j.report.patient_uid}</code></div>`;
//       showNotification(
//         `تم ${editReportId ? "تعديل" : "حفظ"} التقرير`,
//         "success",
//       );
//       if (!editReportId) setTimeout(() => (location.href = "/reports"), 1000);
//     } else showNotification(j.error || "فشل", "error");
//   } catch (e) {
//     showNotification("خطأ اتصال", "error");
//   }
// }

// async function saveAndGeneratePDF() {
//   if (!validateForm()) {
//     showNotification("املأ الحقول المطلوبة", "error");
//     return;
//   }

//   const url = editReportId ? `/api/reports/${editReportId}` : "/api/reports";
//   const method = editReportId ? "PUT" : "POST";

//   try {
//     document.getElementById("saveResult").innerHTML =
//       `<div class="text-center"><div class="spinner-border text-primary"></div><p class="mt-2">جاري ${editReportId ? "تعديل" : "حفظ"} التقرير وتوليد PDF...</p></div>`;
//     const r = await fetch(url, {
//       method: method,
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({
//         template_id: parseInt(templateId),
//         form_data: collectFormData(),
//         patient_uid: null,
//       }),
//     });
//     const j = await r.json();
//     if (j.success) {
//       window.location.href = `/api/reports/${j.report.id}/pdf`;
//       document.getElementById("saveResult").innerHTML =
//         `<div class="alert alert-success"><i class="fas fa-check-circle me-2"></i><strong>جاري تحميل PDF...</strong><br>تقرير: <code>${j.report.report_uid}</code></div>`;
//     } else {
//       showNotification(j.error || "فشل", "error");
//       document.getElementById("saveResult").innerHTML = "";
//     }
//   } catch (e) {
//     showNotification("خطأ اتصال", "error");
//     document.getElementById("saveResult").innerHTML = "";
//   }
// }
/* ================================================
   report_form.js - With Edit Support + Data Loading
   ================================================ */

const templateId = document.getElementById("templateId").value;
const editReportId = window.EDIT_REPORT ? window.EDIT_REPORT.id : null;
const editReportData = window.EDIT_REPORT ? window.EDIT_REPORT.data : null;

// ═══════════════════════════════════════════
// Load existing data if editing (from Jinja2)
// ═══════════════════════════════════════════
// Data is already loaded via Jinja2 value="{{ edit_report.data.get(...) }}"
// But we also need to handle signature canvas restoration
if (editReportData) {
  setTimeout(() => {
    // Restore signature images onto canvas
    for (const [key, value] of Object.entries(editReportData)) {
      if (typeof value === "string" && value.startsWith("data:image")) {
        const canvas = document.getElementById(`canvas_${key}`);
        if (canvas) {
          const ctx = canvas.getContext("2d");
          const img = new Image();
          img.onload = function () {
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
          };
          img.src = value;
        }
      }
    }
    console.log("✅ Edit data loaded for report:", editReportId);
  }, 500);
}

// ═══════════════════════════════════════════
// Signature (Canvas only)
// ═══════════════════════════════════════════
document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelectorAll(".signature-canvas")
    .forEach((c) => initSignatureCanvas(c));
  document.querySelectorAll(".form-check-input").forEach((input) => {
    const w = input.closest(".field-wrapper");
    if (w) {
      const l = w.querySelector(".form-label");
      if (l) l.classList.remove("required-field");
    }
  });
});

function initSignatureCanvas(canvas) {
  const ctx = canvas.getContext("2d");
  let drawing = false;
  ctx.strokeStyle = "#1a1a6e";
  ctx.lineWidth = 2.5;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";

  function getPos(e) {
    const r = canvas.getBoundingClientRect();
    return {
      x:
        ((e.touches ? e.touches[0].clientX : e.clientX) - r.left) *
        (canvas.width / r.width),
      y:
        ((e.touches ? e.touches[0].clientY : e.clientY) - r.top) *
        (canvas.height / r.height),
    };
  }

  function start(e) {
    e.preventDefault();
    drawing = true;
    ctx.beginPath();
    const p = getPos(e);
    ctx.moveTo(p.x, p.y);
  }
  function move(e) {
    if (!drawing) return;
    e.preventDefault();
    const p = getPos(e);
    ctx.lineTo(p.x, p.y);
    ctx.stroke();
  }
  function end() {
    drawing = false;
    updateSignature(canvas);
  }

  canvas.addEventListener("mousedown", start);
  canvas.addEventListener("mousemove", move);
  canvas.addEventListener("mouseup", end);
  canvas.addEventListener("mouseleave", end);
  canvas.addEventListener("touchstart", start, { passive: false });
  canvas.addEventListener("touchmove", move, { passive: false });
  canvas.addEventListener("touchend", end);
}

function updateSignature(canvas) {
  const input = document.getElementById(`field_${canvas.dataset.field}`);
  if (input) input.value = canvas.toDataURL("image/png");
}

function clearSignature(fieldName) {
  const canvas = document.getElementById(`canvas_${fieldName}`);
  if (canvas) {
    canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
    const input = document.getElementById(`field_${fieldName}`);
    if (input) input.value = "";
  }
}

// ═══════════════════════════════════════════
// Form Data
// ═══════════════════════════════════════════
function collectFormData() {
  const fd = new FormData(document.getElementById("reportForm"));
  const data = {};
  fd.forEach((v, k) => {
    const input = document.getElementById(k);
    data[k] = input && input.type === "checkbox" ? input.checked : v;
  });
  return data;
}

function validateForm() {
  let valid = true;
  document.querySelectorAll("[required]").forEach((f) => {
    if (!f.value.trim()) {
      f.classList.add("is-invalid");
      valid = false;
    } else f.classList.remove("is-invalid");
  });
  return valid;
}

// ═══════════════════════════════════════════
// API Calls (Create or Update)
// ═══════════════════════════════════════════
async function saveReport() {
  if (!validateForm()) {
    showNotification("املأ الحقول المطلوبة", "error");
    return;
  }

  const url = editReportId ? `/api/reports/${editReportId}` : "/api/reports";
  const method = editReportId ? "PUT" : "POST";

  try {
    const r = await fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        template_id: parseInt(templateId),
        form_data: collectFormData(),
        patient_uid: null,
      }),
    });
    const j = await r.json();
    if (j.success) {
      document.getElementById("saveResult").innerHTML =
        `<div class="alert alert-success"><i class="fas fa-check-circle me-2"></i><strong>تم ${editReportId ? "تعديل" : "حفظ"} التقرير!</strong><br>تقرير: <code>${j.report.report_uid}</code> | مريض: <code>${j.report.patient_uid}</code></div>`;
      showNotification(
        `تم ${editReportId ? "تعديل" : "حفظ"} التقرير`,
        "success",
      );
      if (!editReportId) setTimeout(() => (location.href = "/reports"), 1000);
    } else showNotification(j.error || "فشل", "error");
  } catch (e) {
    showNotification("خطأ اتصال", "error");
  }
}

async function saveAndGeneratePDF() {
  if (!validateForm()) {
    showNotification("املأ الحقول المطلوبة", "error");
    return;
  }

  const url = editReportId ? `/api/reports/${editReportId}` : "/api/reports";
  const method = editReportId ? "PUT" : "POST";

  try {
    document.getElementById("saveResult").innerHTML =
      `<div class="text-center"><div class="spinner-border text-primary"></div><p class="mt-2">جاري ${editReportId ? "تعديل" : "حفظ"} التقرير وتوليد PDF...</p></div>`;
    const r = await fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        template_id: parseInt(templateId),
        form_data: collectFormData(),
        patient_uid: null,
      }),
    });
    const j = await r.json();
    if (j.success) {
      window.location.href = `/api/reports/${j.report.id}/pdf`;
      document.getElementById("saveResult").innerHTML =
        `<div class="alert alert-success"><i class="fas fa-check-circle me-2"></i><strong>جاري تحميل PDF...</strong><br>تقرير: <code>${j.report.report_uid}</code></div>`;
    } else {
      showNotification(j.error || "فشل", "error");
      document.getElementById("saveResult").innerHTML = "";
    }
  } catch (e) {
    showNotification("خطأ اتصال", "error");
    document.getElementById("saveResult").innerHTML = "";
  }
}
