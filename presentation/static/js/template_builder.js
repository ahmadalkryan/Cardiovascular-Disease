// // // // // // /* ================================================
// // // // // //    template_builder.js - Enhanced Template Builder
// // // // // //    ================================================ */

// // // // // // let templateFields = [];
// // // // // // let fieldCounter = 0;
// // // // // // let selectedFieldIndex = -1;

// // // // // // // Load existing template
// // // // // // if (window.EDIT_TEMPLATE) {
// // // // // //   templateFields = window.EDIT_TEMPLATE.structure || [];
// // // // // //   fieldCounter = templateFields.length;
// // // // // //   document.getElementById("templateTitle").value =
// // // // // //     window.EDIT_TEMPLATE.title || "";
// // // // // //   document.getElementById("templateDescription").value =
// // // // // //     window.EDIT_TEMPLATE.description || "";
// // // // // //   document.getElementById("templateCategory").value =
// // // // // //     window.EDIT_TEMPLATE.category || "general";
// // // // // //   renderCanvas();
// // // // // // }

// // // // // // // ================================================
// // // // // // // Add Field
// // // // // // // ================================================
// // // // // // function addField(type) {
// // // // // //   const typeLabels = {
// // // // // //     text: "نص قصير",
// // // // // //     textarea: "نص طويل",
// // // // // //     number: "رقم",
// // // // // //     date: "تاريخ",
// // // // // //     email: "بريد إلكتروني",
// // // // // //     phone: "رقم هاتف",
// // // // // //     select: "قائمة منسدلة",
// // // // // //     radio: "اختيار واحد",
// // // // // //     checkbox: "مربع اختيار",
// // // // // //     heading: "عنوان رئيسي",
// // // // // //     subheading: "عنوان فرعي",
// // // // // //     divider: "فاصل",
// // // // // //     vitals: "علامات حيوية",
// // // // // //     diagnosis: "تشخيص",
// // // // // //     medication: "دواء",
// // // // // //   };

// // // // // //   fieldCounter++;
// // // // // //   const field = {
// // // // // //     id: `field_${Date.now()}`,
// // // // // //     type: type,
// // // // // //     name: `${type}_${fieldCounter}`,
// // // // // //     label: typeLabels[type] || `حقل ${fieldCounter}`,
// // // // // //     placeholder: "",
// // // // // //     required: false,
// // // // // //     options: type === "select" || type === "radio" ? ["خيار 1", "خيار 2"] : [],
// // // // // //   };

// // // // // //   templateFields.push(field);
// // // // // //   selectField(templateFields.length - 1);
// // // // // //   renderCanvas();
// // // // // // }

// // // // // // // ================================================
// // // // // // // Select Field
// // // // // // // ================================================
// // // // // // function selectField(index) {
// // // // // //   selectedFieldIndex = index;

// // // // // //   // Highlight in canvas
// // // // // //   document
// // // // // //     .querySelectorAll(".field-item")
// // // // // //     .forEach((el) => el.classList.remove("selected"));
// // // // // //   const fieldEl = document.querySelector(`.field-item[data-index="${index}"]`);
// // // // // //   if (fieldEl) fieldEl.classList.add("selected");

// // // // // //   // Show properties
// // // // // //   const field = templateFields[index];
// // // // // //   if (!field) {
// // // // // //     document.getElementById("propertiesPanel").style.display = "none";
// // // // // //     return;
// // // // // //   }

// // // // // //   document.getElementById("propertiesPanel").style.display = "block";
// // // // // //   document.getElementById("selectedFieldIndex").value = index;
// // // // // //   document.getElementById("propName").value = field.name || "";
// // // // // //   document.getElementById("propLabel").value = field.label || "";
// // // // // //   document.getElementById("propPlaceholder").value = field.placeholder || "";
// // // // // //   document.getElementById("propRequired").checked = field.required || false;

// // // // // //   // Options section
// // // // // //   const isChoice = field.type === "select" || field.type === "radio";
// // // // // //   document.getElementById("optionsSection").style.display = isChoice
// // // // // //     ? "block"
// // // // // //     : "none";
// // // // // //   if (isChoice) renderOptionsList(field.options || []);
// // // // // // }

// // // // // // function applyProperty(key, value) {
// // // // // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // // // // //   if (index >= 0 && templateFields[index]) {
// // // // // //     templateFields[index][key] = value;
// // // // // //     if (key === "label" || key === "placeholder") renderCanvas();
// // // // // //   }
// // // // // // }

// // // // // // function deleteSelectedField() {
// // // // // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // // // // //   if (index >= 0) {
// // // // // //     templateFields.splice(index, 1);
// // // // // //     selectedFieldIndex = -1;
// // // // // //     document.getElementById("propertiesPanel").style.display = "none";
// // // // // //     renderCanvas();
// // // // // //   }
// // // // // // }

// // // // // // // ================================================
// // // // // // // Options Management
// // // // // // // ================================================
// // // // // // function addOption() {
// // // // // //   const input = document.getElementById("newOption");
// // // // // //   const value = input.value.trim();
// // // // // //   if (!value) return;

// // // // // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // // // // //   if (index >= 0 && templateFields[index]) {
// // // // // //     if (!templateFields[index].options) templateFields[index].options = [];
// // // // // //     templateFields[index].options.push(value);
// // // // // //     renderOptionsList(templateFields[index].options);
// // // // // //     renderCanvas();
// // // // // //   }
// // // // // //   input.value = "";
// // // // // // }

// // // // // // function removeOption(optIndex) {
// // // // // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // // // // //   if (index >= 0 && templateFields[index]) {
// // // // // //     templateFields[index].options.splice(optIndex, 1);
// // // // // //     renderOptionsList(templateFields[index].options);
// // // // // //     renderCanvas();
// // // // // //   }
// // // // // // }

// // // // // // function renderOptionsList(options) {
// // // // // //   document.getElementById("optionsList").innerHTML = (options || [])
// // // // // //     .map(
// // // // // //       (o, i) => `
// // // // // //     <span class="option-chip">${o} <span class="remove-option" onclick="removeOption(${i})">&times;</span></span>
// // // // // //   `,
// // // // // //     )
// // // // // //     .join("");
// // // // // // }

// // // // // // // ================================================
// // // // // // // Render Canvas
// // // // // // // ================================================
// // // // // // function renderCanvas() {
// // // // // //   const canvas = document.getElementById("templateCanvas");

// // // // // //   if (templateFields.length === 0) {
// // // // // //     canvas.innerHTML = `<div class="canvas-empty">
// // // // // //       <i class="fas fa-arrow-left fa-3x mb-3" style="color:#ccc"></i>
// // // // // //       <p>أضف حقولاً من القائمة الجانبية لبناء القالب</p>
// // // // // //     </div>`;
// // // // // //     return;
// // // // // //   }

// // // // // //   const typeLabels = {
// // // // // //     text: "نص قصير",
// // // // // //     textarea: "نص طويل",
// // // // // //     number: "رقم",
// // // // // //     date: "تاريخ",
// // // // // //     email: "بريد إلكتروني",
// // // // // //     phone: "رقم هاتف",
// // // // // //     select: "قائمة منسدلة",
// // // // // //     radio: "اختيار واحد",
// // // // // //     checkbox: "مربع اختيار",
// // // // // //     heading: "عنوان رئيسي",
// // // // // //     subheading: "عنوان فرعي",
// // // // // //     divider: "فاصل",
// // // // // //     vitals: "علامات حيوية",
// // // // // //     diagnosis: "تشخيص",
// // // // // //     medication: "دواء",
// // // // // //   };

// // // // // //   canvas.innerHTML = templateFields
// // // // // //     .map((field, index) => {
// // // // // //       if (field.type === "heading") {
// // // // // //         return `<div class="field-item" data-index="${index}" onclick="selectField(${index})">
// // // // // //         <div class="field-header">
// // // // // //           <span class="field-type-badge"><i class="fas fa-heading"></i> عنوان رئيسي</span>
// // // // // //           <div class="d-flex gap-1">
// // // // // //             <button class="btn-action" onclick="event.stopPropagation();moveField(${index},-1)"><i class="fas fa-arrow-up"></i></button>
// // // // // //             <button class="btn-action" onclick="event.stopPropagation();moveField(${index},1)"><i class="fas fa-arrow-down"></i></button>
// // // // // //             <button class="btn-action danger" onclick="event.stopPropagation();removeField(${index})"><i class="fas fa-trash"></i></button>
// // // // // //           </div>
// // // // // //         </div>
// // // // // //         <h5 style="color:#1a5276;margin:0">${field.label}</h5>
// // // // // //       </div>`;
// // // // // //       }

// // // // // //       if (field.type === "divider") {
// // // // // //         return `<div class="field-item" data-index="${index}" onclick="selectField(${index})">
// // // // // //         <div class="field-header">
// // // // // //           <span class="field-type-badge"><i class="fas fa-minus"></i> فاصل</span>
// // // // // //           <div class="d-flex gap-1">
// // // // // //             <button class="btn-action" onclick="event.stopPropagation();moveField(${index},-1)"><i class="fas fa-arrow-up"></i></button>
// // // // // //             <button class="btn-action" onclick="event.stopPropagation();moveField(${index},1)"><i class="fas fa-arrow-down"></i></button>
// // // // // //             <button class="btn-action danger" onclick="event.stopPropagation();removeField(${index})"><i class="fas fa-trash"></i></button>
// // // // // //           </div>
// // // // // //         </div>
// // // // // //         <hr style="border-style:dashed;color:#ddd">
// // // // // //       </div>`;
// // // // // //       }

// // // // // //       if (field.type === "subheading") {
// // // // // //         return `<div class="field-item" data-index="${index}" onclick="selectField(${index})">
// // // // // //         <div class="field-header">
// // // // // //           <span class="field-type-badge"><i class="fas fa-heading"></i> عنوان فرعي</span>
// // // // // //           <div class="d-flex gap-1">
// // // // // //             <button class="btn-action" onclick="event.stopPropagation();moveField(${index},-1)"><i class="fas fa-arrow-up"></i></button>
// // // // // //             <button class="btn-action" onclick="event.stopPropagation();moveField(${index},1)"><i class="fas fa-arrow-down"></i></button>
// // // // // //             <button class="btn-action danger" onclick="event.stopPropagation();removeField(${index})"><i class="fas fa-trash"></i></button>
// // // // // //           </div>
// // // // // //         </div>
// // // // // //         <h6 style="color:#2c3e50;margin:0">${field.label}</h6>
// // // // // //       </div>`;
// // // // // //       }

// // // // // //       // Form fields
// // // // // //       let preview = "";
// // // // // //       switch (field.type) {
// // // // // //         case "text":
// // // // // //         case "email":
// // // // // //         case "phone":
// // // // // //           preview = `<input type="${field.type}" class="form-control form-control-sm" placeholder="${field.placeholder || ""}" disabled>`;
// // // // // //           break;
// // // // // //         case "textarea":
// // // // // //           preview = `<textarea class="form-control form-control-sm" rows="2" disabled></textarea>`;
// // // // // //           break;
// // // // // //         case "number":
// // // // // //           preview = `<input type="number" class="form-control form-control-sm" disabled>`;
// // // // // //           break;
// // // // // //         case "date":
// // // // // //           preview = `<input type="date" class="form-control form-control-sm" disabled>`;
// // // // // //           break;
// // // // // //         case "select":
// // // // // //           preview = `<select class="form-select form-select-sm" disabled>${(field.options || []).map((o) => `<option>${o}</option>`).join("")}</select>`;
// // // // // //           break;
// // // // // //         case "radio":
// // // // // //           preview = (field.options || [])
// // // // // //             .map(
// // // // // //               (o) =>
// // // // // //                 `<div class="form-check"><input type="radio" class="form-check-input" disabled><label class="form-check-label small">${o}</label></div>`,
// // // // // //             )
// // // // // //             .join("");
// // // // // //           break;
// // // // // //         case "checkbox":
// // // // // //           preview = `<div class="form-check"><input type="checkbox" class="form-check-input" disabled><label class="form-check-label small">${field.label}</label></div>`;
// // // // // //           break;
// // // // // //         case "vitals":
// // // // // //           preview = `<div class="row g-1"><div class="col-3"><input class="form-control form-control-sm" placeholder="انقباضي" disabled></div><div class="col-3"><input class="form-control form-control-sm" placeholder="انبساطي" disabled></div><div class="col-3"><input class="form-control form-control-sm" placeholder="النبض" disabled></div><div class="col-3"><input class="form-control form-control-sm" placeholder="الحرارة" disabled></div></div>`;
// // // // // //           break;
// // // // // //         case "medication":
// // // // // //           preview = `<div class="row g-1"><div class="col-5"><input class="form-control form-control-sm" placeholder="اسم الدواء" disabled></div><div class="col-3"><input class="form-control form-control-sm" placeholder="الجرعة" disabled></div><div class="col-4"><input class="form-control form-control-sm" placeholder="التكرار" disabled></div></div>`;
// // // // // //           break;
// // // // // //         default:
// // // // // //           preview = `<input type="text" class="form-control form-control-sm" disabled>`;
// // // // // //       }

// // // // // //       return `<div class="field-item" data-index="${index}" onclick="selectField(${index})">
// // // // // //       <div class="field-header">
// // // // // //         <span class="field-type-badge"><i class="fas fa-${field.type === "vitals" ? "heartbeat" : field.type === "medication" ? "pills" : field.type === "diagnosis" ? "stethoscope" : "pen"}"></i> ${typeLabels[field.type] || field.type}</span>
// // // // // //         <div class="d-flex gap-1">
// // // // // //           <button class="btn-action" onclick="event.stopPropagation();moveField(${index},-1)"><i class="fas fa-arrow-up"></i></button>
// // // // // //           <button class="btn-action" onclick="event.stopPropagation();moveField(${index},1)"><i class="fas fa-arrow-down"></i></button>
// // // // // //           <button class="btn-action danger" onclick="event.stopPropagation();removeField(${index})"><i class="fas fa-trash"></i></button>
// // // // // //         </div>
// // // // // //       </div>
// // // // // //       <label class="fw-bold small mb-1 d-block">${field.label} ${field.required ? '<span class="text-danger">*</span>' : ""}</label>
// // // // // //       ${preview}
// // // // // //     </div>`;
// // // // // //     })
// // // // // //     .join("");

// // // // // //   // Re-select if needed
// // // // // //   if (selectedFieldIndex >= 0 && selectedFieldIndex < templateFields.length) {
// // // // // //     const el = canvas.querySelector(
// // // // // //       `.field-item[data-index="${selectedFieldIndex}"]`,
// // // // // //     );
// // // // // //     if (el) el.classList.add("selected");
// // // // // //   }
// // // // // // }

// // // // // // // ================================================
// // // // // // // Move & Remove
// // // // // // // ================================================
// // // // // // function moveField(index, direction) {
// // // // // //   const newIndex = index + direction;
// // // // // //   if (newIndex < 0 || newIndex >= templateFields.length) return;
// // // // // //   [templateFields[index], templateFields[newIndex]] = [
// // // // // //     templateFields[newIndex],
// // // // // //     templateFields[index],
// // // // // //   ];
// // // // // //   selectedFieldIndex = newIndex;
// // // // // //   renderCanvas();
// // // // // // }

// // // // // // function removeField(index) {
// // // // // //   templateFields.splice(index, 1);
// // // // // //   if (selectedFieldIndex === index) {
// // // // // //     selectedFieldIndex = -1;
// // // // // //     document.getElementById("propertiesPanel").style.display = "none";
// // // // // //   }
// // // // // //   renderCanvas();
// // // // // // }

// // // // // // // ================================================
// // // // // // // Preview
// // // // // // // ================================================
// // // // // // function previewTemplate() {
// // // // // //   let html = `<h4>${document.getElementById("templateTitle").value || "معاينة القالب"}</h4><hr>`;
// // // // // //   templateFields.forEach((f) => {
// // // // // //     if (f.type === "heading")
// // // // // //       html += `<h5 style="color:#1a5276;margin-top:16px">${f.label}</h5>`;
// // // // // //     else if (f.type === "divider") html += '<hr style="border-style:dashed">';
// // // // // //     else
// // // // // //       html += `<div style="margin-bottom:12px"><label class="fw-bold small">${f.label} ${f.required ? '<span style="color:red">*</span>' : ""}</label><br><input class="form-control form-control-sm" style="width:100%" disabled></div>`;
// // // // // //   });
// // // // // //   document.getElementById("previewContent").innerHTML = html;
// // // // // //   new bootstrap.Modal(document.getElementById("previewModal")).show();
// // // // // // }

// // // // // // // ================================================
// // // // // // // Save
// // // // // // // ================================================
// // // // // // async function saveTemplate() {
// // // // // //   const title = document.getElementById("templateTitle").value.trim();
// // // // // //   if (!title) {
// // // // // //     showNotification("الرجاء إدخال اسم القالب", "error");
// // // // // //     return;
// // // // // //   }
// // // // // //   if (templateFields.length === 0) {
// // // // // //     showNotification("أضف حقلاً واحداً على الأقل", "error");
// // // // // //     return;
// // // // // //   }

// // // // // //   const data = {
// // // // // //     title,
// // // // // //     description: document.getElementById("templateDescription").value,
// // // // // //     category: document.getElementById("templateCategory").value,
// // // // // //     structure: templateFields,
// // // // // //   };

// // // // // //   const url = window.EDIT_TEMPLATE
// // // // // //     ? `/api/templates/${window.EDIT_TEMPLATE.id}`
// // // // // //     : "/api/templates";
// // // // // //   try {
// // // // // //     const res = await fetch(url, {
// // // // // //       method: window.EDIT_TEMPLATE ? "PUT" : "POST",
// // // // // //       headers: { "Content-Type": "application/json" },
// // // // // //       body: JSON.stringify(data),
// // // // // //     });
// // // // // //     const result = await res.json();
// // // // // //     if (result.success) {
// // // // // //       showNotification("تم الحفظ بنجاح", "success");
// // // // // //       setTimeout(() => (location.href = "/reports"), 800);
// // // // // //     } else {
// // // // // //       showNotification(result.error || "فشل الحفظ", "error");
// // // // // //     }
// // // // // //   } catch (e) {
// // // // // //     showNotification("خطأ في الاتصال", "error");
// // // // // //   }
// // // // // // }

// // // // // /* ================================================
// // // // //    template_builder.js - Complete with Drag & Drop + Signature
// // // // //    ================================================ */

// // // // // let templateFields = [];
// // // // // let fieldCounter = 0;
// // // // // let selectedFieldIndex = -1;
// // // // // let draggedIndex = -1;

// // // // // // Load existing template if editing
// // // // // if (window.EDIT_TEMPLATE) {
// // // // //   templateFields = window.EDIT_TEMPLATE.structure || [];
// // // // //   fieldCounter = templateFields.length;
// // // // //   document.getElementById("templateTitle").value =
// // // // //     window.EDIT_TEMPLATE.title || "";
// // // // //   document.getElementById("templateDescription").value =
// // // // //     window.EDIT_TEMPLATE.description || "";
// // // // //   document.getElementById("templateCategory").value =
// // // // //     window.EDIT_TEMPLATE.category || "general";
// // // // //   renderCanvas();
// // // // // }

// // // // // // ================================================
// // // // // // Type Definitions
// // // // // // ================================================
// // // // // const TYPE_LABELS = {
// // // // //   text: "نص قصير",
// // // // //   textarea: "نص طويل",
// // // // //   number: "رقم",
// // // // //   date: "تاريخ",
// // // // //   email: "بريد إلكتروني",
// // // // //   phone: "رقم هاتف",
// // // // //   select: "قائمة منسدلة",
// // // // //   radio: "اختيار واحد",
// // // // //   checkbox: "مربع اختيار",
// // // // //   heading: "عنوان رئيسي",
// // // // //   subheading: "عنوان فرعي",
// // // // //   divider: "فاصل",
// // // // //   vitals: "علامات حيوية",
// // // // //   diagnosis: "تشخيص",
// // // // //   medication: "دواء",
// // // // //   signature: "توقيع الطبيب",
// // // // // };

// // // // // const TYPE_ICONS = {
// // // // //   text: "fa-font",
// // // // //   textarea: "fa-align-left",
// // // // //   number: "fa-hashtag",
// // // // //   date: "fa-calendar",
// // // // //   email: "fa-envelope",
// // // // //   phone: "fa-phone",
// // // // //   select: "fa-list",
// // // // //   radio: "fa-dot-circle",
// // // // //   checkbox: "fa-check-square",
// // // // //   heading: "fa-heading",
// // // // //   subheading: "fa-heading",
// // // // //   divider: "fa-minus",
// // // // //   vitals: "fa-heartbeat",
// // // // //   diagnosis: "fa-stethoscope",
// // // // //   medication: "fa-pills",
// // // // //   signature: "fa-signature",
// // // // // };

// // // // // // ================================================
// // // // // // Add Field
// // // // // // ================================================
// // // // // function addField(type) {
// // // // //   fieldCounter++;

// // // // //   // Default options for select/radio
// // // // //   let options = [];
// // // // //   if (type === "select" || type === "radio") {
// // // // //     options = ["خيار 1", "خيار 2"];
// // // // //   }

// // // // //   const field = {
// // // // //     id: `field_${Date.now()}`,
// // // // //     type: type,
// // // // //     name: `${type}_${fieldCounter}`,
// // // // //     label: TYPE_LABELS[type] || `حقل ${fieldCounter}`,
// // // // //     placeholder: "",
// // // // //     required: false,
// // // // //     options: options,
// // // // //   };

// // // // //   templateFields.push(field);
// // // // //   selectField(templateFields.length - 1);
// // // // //   renderCanvas();
// // // // // }

// // // // // // ================================================
// // // // // // Drag & Drop Handlers
// // // // // // ================================================
// // // // // function handleDragStart(e, index) {
// // // // //   draggedIndex = index;
// // // // //   const item = e.target.closest(".field-item");
// // // // //   if (item) {
// // // // //     item.style.opacity = "0.4";
// // // // //   }
// // // // //   e.dataTransfer.effectAllowed = "move";
// // // // //   e.dataTransfer.setData("text/plain", index);
// // // // // }

// // // // // function handleDragOver(e) {
// // // // //   e.preventDefault();
// // // // //   e.dataTransfer.dropEffect = "move";
// // // // // }

// // // // // function handleDrop(e, dropIndex) {
// // // // //   e.preventDefault();
// // // // //   e.stopPropagation();

// // // // //   // Remove visual indicators
// // // // //   document.querySelectorAll(".field-item").forEach((el) => {
// // // // //     el.style.borderTop = "";
// // // // //     el.style.borderBottom = "";
// // // // //   });

// // // // //   if (
// // // // //     draggedIndex !== -1 &&
// // // // //     draggedIndex !== dropIndex &&
// // // // //     draggedIndex !== undefined
// // // // //   ) {
// // // // //     // Reorder array
// // // // //     const [movedItem] = templateFields.splice(draggedIndex, 1);
// // // // //     const newIndex = dropIndex > draggedIndex ? dropIndex - 1 : dropIndex;
// // // // //     templateFields.splice(newIndex >= 0 ? newIndex : 0, 0, movedItem);
// // // // //     selectedFieldIndex = newIndex >= 0 ? newIndex : 0;
// // // // //   }

// // // // //   draggedIndex = -1;
// // // // //   renderCanvas();

// // // // //   // Re-select
// // // // //   if (selectedFieldIndex >= 0 && selectedFieldIndex < templateFields.length) {
// // // // //     const el = document.querySelector(
// // // // //       `.field-item[data-index="${selectedFieldIndex}"]`,
// // // // //     );
// // // // //     if (el) el.classList.add("selected");
// // // // //   }
// // // // // }

// // // // // function handleDragEnd(e) {
// // // // //   const item = e.target.closest(".field-item");
// // // // //   if (item) {
// // // // //     item.style.opacity = "1";
// // // // //   }
// // // // //   document.querySelectorAll(".field-item").forEach((el) => {
// // // // //     el.style.borderTop = "";
// // // // //     el.style.borderBottom = "";
// // // // //   });
// // // // //   draggedIndex = -1;
// // // // // }

// // // // // // ================================================
// // // // // // Select Field
// // // // // // ================================================
// // // // // function selectField(index, event) {
// // // // //   if (event) {
// // // // //     event.stopPropagation();
// // // // //     event.preventDefault();
// // // // //   }

// // // // //   selectedFieldIndex = index;

// // // // //   // Remove selected class from all
// // // // //   document
// // // // //     .querySelectorAll(".field-item")
// // // // //     .forEach((el) => el.classList.remove("selected"));

// // // // //   // Add selected class to current
// // // // //   const fieldEl = document.querySelector(`.field-item[data-index="${index}"]`);
// // // // //   if (fieldEl) fieldEl.classList.add("selected");

// // // // //   const field = templateFields[index];
// // // // //   if (!field) {
// // // // //     document.getElementById("propertiesPanel").style.display = "none";
// // // // //     return;
// // // // //   }

// // // // //   // Show properties panel
// // // // //   document.getElementById("propertiesPanel").style.display = "block";
// // // // //   document.getElementById("selectedFieldIndex").value = index;
// // // // //   document.getElementById("propName").value = field.name || "";
// // // // //   document.getElementById("propLabel").value = field.label || "";
// // // // //   document.getElementById("propPlaceholder").value = field.placeholder || "";
// // // // //   document.getElementById("propRequired").checked = field.required || false;

// // // // //   // Show options section for select/radio
// // // // //   const isChoice = field.type === "select" || field.type === "radio";
// // // // //   document.getElementById("optionsSection").style.display = isChoice
// // // // //     ? "block"
// // // // //     : "none";
// // // // //   if (isChoice) {
// // // // //     renderOptionsList(field.options || []);
// // // // //   }
// // // // // }

// // // // // // ================================================
// // // // // // Properties
// // // // // // ================================================
// // // // // function applyProperty(key, value) {
// // // // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // // // //   if (index >= 0 && index < templateFields.length && templateFields[index]) {
// // // // //     templateFields[index][key] = value;
// // // // //     if (key === "label" || key === "placeholder") {
// // // // //       renderCanvas();
// // // // //       // Re-select
// // // // //       const el = document.querySelector(`.field-item[data-index="${index}"]`);
// // // // //       if (el) el.classList.add("selected");
// // // // //     }
// // // // //   }
// // // // // }

// // // // // function deleteSelectedField() {
// // // // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // // // //   if (index >= 0 && index < templateFields.length) {
// // // // //     templateFields.splice(index, 1);
// // // // //     selectedFieldIndex = -1;
// // // // //     document.getElementById("propertiesPanel").style.display = "none";
// // // // //     renderCanvas();
// // // // //   }
// // // // // }

// // // // // // ================================================
// // // // // // Options Management
// // // // // // ================================================
// // // // // function addOption() {
// // // // //   const input = document.getElementById("newOption");
// // // // //   const value = input.value.trim();
// // // // //   if (!value) return;

// // // // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // // // //   if (index >= 0 && index < templateFields.length && templateFields[index]) {
// // // // //     if (!templateFields[index].options) {
// // // // //       templateFields[index].options = [];
// // // // //     }
// // // // //     templateFields[index].options.push(value);
// // // // //     renderOptionsList(templateFields[index].options);
// // // // //     renderCanvas();
// // // // //     const el = document.querySelector(`.field-item[data-index="${index}"]`);
// // // // //     if (el) el.classList.add("selected");
// // // // //   }
// // // // //   input.value = "";
// // // // //   input.focus();
// // // // // }

// // // // // function removeOption(optIndex) {
// // // // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // // // //   if (index >= 0 && index < templateFields.length && templateFields[index]) {
// // // // //     templateFields[index].options.splice(optIndex, 1);
// // // // //     renderOptionsList(templateFields[index].options);
// // // // //     renderCanvas();
// // // // //     const el = document.querySelector(`.field-item[data-index="${index}"]`);
// // // // //     if (el) el.classList.add("selected");
// // // // //   }
// // // // // }

// // // // // function renderOptionsList(options) {
// // // // //   const container = document.getElementById("optionsList");
// // // // //   if (!container) return;

// // // // //   container.innerHTML = (options || [])
// // // // //     .map(
// // // // //       (o, i) => `
// // // // //     <span class="option-chip">
// // // // //       ${o}
// // // // //       <span class="remove-option" onclick="removeOption(${i})" style="cursor:pointer;color:#e74c3c;font-weight:bold;margin-right:4px">&times;</span>
// // // // //     </span>
// // // // //   `,
// // // // //     )
// // // // //     .join("");
// // // // // }

// // // // // // ================================================
// // // // // // Render Canvas
// // // // // // ================================================
// // // // // function renderCanvas() {
// // // // //   const canvas = document.getElementById("templateCanvas");
// // // // //   if (!canvas) return;

// // // // //   if (templateFields.length === 0) {
// // // // //     canvas.innerHTML = `
// // // // //       <div class="canvas-empty">
// // // // //         <i class="fas fa-arrow-left fa-3x mb-3" style="color:#ccc"></i>
// // // // //         <p>أضف حقولاً من القائمة الجانبية لبناء القالب</p>
// // // // //         <small class="text-muted">يمكنك سحب وإفلات الحقول لإعادة ترتيبها</small>
// // // // //       </div>`;
// // // // //     return;
// // // // //   }

// // // // //   canvas.innerHTML = templateFields
// // // // //     .map((field, index) => {
// // // // //       return renderField(field, index);
// // // // //     })
// // // // //     .join("");

// // // // //   // Re-select previously selected field
// // // // //   if (selectedFieldIndex >= 0 && selectedFieldIndex < templateFields.length) {
// // // // //     const el = canvas.querySelector(
// // // // //       `.field-item[data-index="${selectedFieldIndex}"]`,
// // // // //     );
// // // // //     if (el) el.classList.add("selected");
// // // // //   }
// // // // // }

// // // // // function renderField(field, index) {
// // // // //   const isSelected = index === selectedFieldIndex;
// // // // //   const selectedClass = isSelected ? "selected" : "";

// // // // //   const dragAttrs = `draggable="true"
// // // // //     ondragstart="handleDragStart(event, ${index})"
// // // // //     ondragover="handleDragOver(event)"
// // // // //     ondrop="handleDrop(event, ${index})"
// // // // //     ondragend="handleDragEnd(event)"`;

// // // // //   const actionButtons = `
// // // // //     <button class="btn-action" onclick="event.stopPropagation();moveField(${index},-1)" title="للأعلى"><i class="fas fa-arrow-up"></i></button>
// // // // //     <button class="btn-action" onclick="event.stopPropagation();moveField(${index},1)" title="للأسفل"><i class="fas fa-arrow-down"></i></button>
// // // // //     <button class="btn-action danger" onclick="event.stopPropagation();removeField(${index})" title="حذف"><i class="fas fa-trash"></i></button>
// // // // //   `;

// // // // //   const label_html = `${field.label} ${field.required ? '<span class="text-danger">*</span>' : ""}`;

// // // // //   // ── Heading ──
// // // // //   if (field.type === "heading") {
// // // // //     return `
// // // // //     <div class="field-item ${selectedClass}" data-index="${index}" ${dragAttrs} onclick="selectField(${index}, event)">
// // // // //       <div class="drag-handle" title="اسحب للتحريك">⋮⋮</div>
// // // // //       <div class="field-header">
// // // // //         <span class="field-type-badge"><i class="fas fa-heading"></i> عنوان رئيسي</span>
// // // // //         <div class="d-flex gap-1">${actionButtons}</div>
// // // // //       </div>
// // // // //       <h5 style="color:#1a5276;margin:0">${field.label}</h5>
// // // // //     </div>`;
// // // // //   }

// // // // //   // ── Divider ──
// // // // //   if (field.type === "divider") {
// // // // //     return `
// // // // //     <div class="field-item ${selectedClass}" data-index="${index}" ${dragAttrs} onclick="selectField(${index}, event)">
// // // // //       <div class="drag-handle" title="اسحب للتحريك">⋮⋮</div>
// // // // //       <div class="field-header">
// // // // //         <span class="field-type-badge"><i class="fas fa-minus"></i> فاصل</span>
// // // // //         <div class="d-flex gap-1">${actionButtons}</div>
// // // // //       </div>
// // // // //       <hr style="border-style:dashed;color:#ddd;margin:4px 0">
// // // // //     </div>`;
// // // // //   }

// // // // //   // ── Subheading ──
// // // // //   if (field.type === "subheading") {
// // // // //     return `
// // // // //     <div class="field-item ${selectedClass}" data-index="${index}" ${dragAttrs} onclick="selectField(${index}, event)">
// // // // //       <div class="drag-handle" title="اسحب للتحريك">⋮⋮</div>
// // // // //       <div class="field-header">
// // // // //         <span class="field-type-badge"><i class="fas fa-heading"></i> عنوان فرعي</span>
// // // // //         <div class="d-flex gap-1">${actionButtons}</div>
// // // // //       </div>
// // // // //       <h6 style="color:#2c3e50;margin:0">${field.label}</h6>
// // // // //     </div>`;
// // // // //   }

// // // // //   // ── Signature ──
// // // // //   if (field.type === "signature") {
// // // // //     return `
// // // // //     <div class="field-item ${selectedClass}" data-index="${index}" ${dragAttrs} onclick="selectField(${index}, event)">
// // // // //       <div class="drag-handle" title="اسحب للتحريك">⋮⋮</div>
// // // // //       <div class="field-header">
// // // // //         <span class="field-type-badge"><i class="fas fa-signature"></i> توقيع</span>
// // // // //         <div class="d-flex gap-1">${actionButtons}</div>
// // // // //       </div>
// // // // //       <div style="border:1px dashed #ccc;border-radius:8px;padding:15px;text-align:center;color:#999;margin-top:5px">
// // // // //         <i class="fas fa-signature fa-2x mb-2 d-block"></i>
// // // // //         <small>مكان توقيع الطبيب</small>
// // // // //         <div style="border-bottom:1px solid #ccc;width:60%;margin:10px auto 0"></div>
// // // // //       </div>
// // // // //     </div>`;
// // // // //   }

// // // // //   // ── Form Fields ──
// // // // //   let preview = "";

// // // // //   switch (field.type) {
// // // // //     case "text":
// // // // //       preview = `<input type="text" class="form-control form-control-sm" placeholder="${field.placeholder || "نص قصير"}" disabled>`;
// // // // //       break;
// // // // //     case "textarea":
// // // // //     case "diagnosis":
// // // // //       preview = `<textarea class="form-control form-control-sm" rows="2" placeholder="${field.placeholder || "نص طويل"}" disabled></textarea>`;
// // // // //       break;
// // // // //     case "number":
// // // // //       preview = `<input type="number" class="form-control form-control-sm" placeholder="${field.placeholder || "0"}" disabled>`;
// // // // //       break;
// // // // //     case "date":
// // // // //       preview = `<input type="date" class="form-control form-control-sm" disabled>`;
// // // // //       break;
// // // // //     case "email":
// // // // //       preview = `<input type="email" class="form-control form-control-sm" placeholder="${field.placeholder || "example@domain.com"}" disabled>`;
// // // // //       break;
// // // // //     case "phone":
// // // // //       preview = `<input type="tel" class="form-control form-control-sm" placeholder="${field.placeholder || "05xxxxxxxx"}" disabled>`;
// // // // //       break;
// // // // //     case "select":
// // // // //       preview = `<select class="form-select form-select-sm" disabled>
// // // // //         ${(field.options || []).map((o) => `<option>${o}</option>`).join("")}
// // // // //       </select>`;
// // // // //       break;
// // // // //     case "radio":
// // // // //       preview = (field.options || [])
// // // // //         .map(
// // // // //           (o) => `
// // // // //         <div class="form-check">
// // // // //           <input type="radio" class="form-check-input" disabled>
// // // // //           <label class="form-check-label small">${o}</label>
// // // // //         </div>`,
// // // // //         )
// // // // //         .join("");
// // // // //       break;
// // // // //     case "checkbox":
// // // // //       preview = `<div class="form-check">
// // // // //         <input type="checkbox" class="form-check-input" disabled>
// // // // //         <label class="form-check-label small">${field.label}</label>
// // // // //       </div>`;
// // // // //       break;
// // // // //     case "vitals":
// // // // //       preview = `<div class="row g-1">
// // // // //         <div class="col-3"><input class="form-control form-control-sm" placeholder="انقباضي" disabled></div>
// // // // //         <div class="col-3"><input class="form-control form-control-sm" placeholder="انبساطي" disabled></div>
// // // // //         <div class="col-3"><input class="form-control form-control-sm" placeholder="النبض" disabled></div>
// // // // //         <div class="col-3"><input class="form-control form-control-sm" placeholder="الحرارة" disabled></div>
// // // // //       </div>`;
// // // // //       break;
// // // // //     case "medication":
// // // // //       preview = `<div class="row g-1">
// // // // //         <div class="col-5"><input class="form-control form-control-sm" placeholder="اسم الدواء" disabled></div>
// // // // //         <div class="col-3"><input class="form-control form-control-sm" placeholder="الجرعة" disabled></div>
// // // // //         <div class="col-4"><input class="form-control form-control-sm" placeholder="التكرار" disabled></div>
// // // // //       </div>`;
// // // // //       break;
// // // // //     default:
// // // // //       preview = `<input type="text" class="form-control form-control-sm" disabled>`;
// // // // //   }

// // // // //   return `
// // // // //   <div class="field-item ${selectedClass}" data-index="${index}" ${dragAttrs} onclick="selectField(${index}, event)">
// // // // //     <div class="drag-handle" title="اسحب للتحريك">⋮⋮</div>
// // // // //     <div class="field-header">
// // // // //       <span class="field-type-badge">
// // // // //         <i class="fas ${TYPE_ICONS[field.type] || "fa-pen"}"></i>
// // // // //         ${TYPE_LABELS[field.type] || field.type}
// // // // //       </span>
// // // // //       <div class="d-flex gap-1">${actionButtons}</div>
// // // // //     </div>
// // // // //     <label class="fw-bold small mb-1 d-block">${label_html}</label>
// // // // //     ${preview}
// // // // //   </div>`;
// // // // // }

// // // // // // ================================================
// // // // // // Move & Remove
// // // // // // ================================================
// // // // // function moveField(index, direction) {
// // // // //   const newIndex = index + direction;
// // // // //   if (newIndex < 0 || newIndex >= templateFields.length) return;

// // // // //   [templateFields[index], templateFields[newIndex]] = [
// // // // //     templateFields[newIndex],
// // // // //     templateFields[index],
// // // // //   ];
// // // // //   selectedFieldIndex = newIndex;
// // // // //   renderCanvas();

// // // // //   const el = document.querySelector(`.field-item[data-index="${newIndex}"]`);
// // // // //   if (el) {
// // // // //     el.classList.add("selected");
// // // // //     showPropertiesForIndex(newIndex);
// // // // //   }
// // // // // }

// // // // // function removeField(index) {
// // // // //   if (!confirm("هل أنت متأكد من حذف هذا الحقل؟")) return;

// // // // //   templateFields.splice(index, 1);

// // // // //   if (
// // // // //     selectedFieldIndex === index ||
// // // // //     selectedFieldIndex >= templateFields.length
// // // // //   ) {
// // // // //     selectedFieldIndex =
// // // // //       templateFields.length > 0 ? templateFields.length - 1 : -1;
// // // // //   }

// // // // //   if (selectedFieldIndex === -1) {
// // // // //     document.getElementById("propertiesPanel").style.display = "none";
// // // // //   }

// // // // //   renderCanvas();

// // // // //   if (selectedFieldIndex >= 0) {
// // // // //     const el = document.querySelector(
// // // // //       `.field-item[data-index="${selectedFieldIndex}"]`,
// // // // //     );
// // // // //     if (el) {
// // // // //       el.classList.add("selected");
// // // // //       showPropertiesForIndex(selectedFieldIndex);
// // // // //     }
// // // // //   }
// // // // // }

// // // // // function showPropertiesForIndex(index) {
// // // // //   const field = templateFields[index];
// // // // //   if (!field) return;

// // // // //   document.getElementById("propertiesPanel").style.display = "block";
// // // // //   document.getElementById("selectedFieldIndex").value = index;
// // // // //   document.getElementById("propName").value = field.name || "";
// // // // //   document.getElementById("propLabel").value = field.label || "";
// // // // //   document.getElementById("propPlaceholder").value = field.placeholder || "";
// // // // //   document.getElementById("propRequired").checked = field.required || false;

// // // // //   const isChoice = field.type === "select" || field.type === "radio";
// // // // //   document.getElementById("optionsSection").style.display = isChoice
// // // // //     ? "block"
// // // // //     : "none";
// // // // //   if (isChoice) renderOptionsList(field.options || []);
// // // // // }

// // // // // // ================================================
// // // // // // Preview & Save
// // // // // // ================================================
// // // // // function previewTemplate() {
// // // // //   const title =
// // // // //     document.getElementById("templateTitle").value || "معاينة القالب";
// // // // //   let html = `<h4 style="text-align:right">${title}</h4><hr>`;

// // // // //   templateFields.forEach((f) => {
// // // // //     if (f.type === "heading") {
// // // // //       html += `<h5 style="color:#1a5276;margin-top:16px;text-align:right">📌 ${f.label}</h5>`;
// // // // //     } else if (f.type === "subheading") {
// // // // //       html += `<h6 style="color:#2c3e50;text-align:right">${f.label}</h6>`;
// // // // //     } else if (f.type === "divider") {
// // // // //       html += '<hr style="border-style:dashed">';
// // // // //     } else if (f.type === "signature") {
// // // // //       html += `<div style="border:1px dashed #ccc;border-radius:8px;padding:20px;text-align:center;color:#999;margin:10px 0">
// // // // //         <i class="fas fa-signature fa-2x mb-2 d-block"></i>
// // // // //         <small>مكان توقيع الطبيب</small>
// // // // //         <div style="border-bottom:1px solid #ccc;width:50%;margin:10px auto 0"></div>
// // // // //       </div>`;
// // // // //     } else if (f.type === "checkbox") {
// // // // //       html += `<div class="form-check mb-2" style="text-align:right">
// // // // //         <input type="checkbox" class="form-check-input" disabled>
// // // // //         <label class="form-check-label">${f.label} ${f.required ? '<span style="color:red">*</span>' : ""}</label>
// // // // //       </div>`;
// // // // //     } else {
// // // // //       html += `<div class="mb-2" style="text-align:right">
// // // // //         <label class="fw-bold small">${f.label} ${f.required ? '<span style="color:red">*</span>' : ""}</label>
// // // // //         <input class="form-control form-control-sm" disabled>
// // // // //       </div>`;
// // // // //     }
// // // // //   });

// // // // //   document.getElementById("previewContent").innerHTML = html;
// // // // //   new bootstrap.Modal(document.getElementById("previewModal")).show();
// // // // // }

// // // // // async function saveTemplate() {
// // // // //   const title = document.getElementById("templateTitle").value.trim();
// // // // //   if (!title) {
// // // // //     showNotification("الرجاء إدخال اسم القالب", "error");
// // // // //     return;
// // // // //   }
// // // // //   if (templateFields.length === 0) {
// // // // //     showNotification("أضف حقلاً واحداً على الأقل", "error");
// // // // //     return;
// // // // //   }

// // // // //   const data = {
// // // // //     title: title,
// // // // //     description: document.getElementById("templateDescription").value.trim(),
// // // // //     category: document.getElementById("templateCategory").value,
// // // // //     structure: templateFields,
// // // // //   };

// // // // //   const url = window.EDIT_TEMPLATE
// // // // //     ? `/api/templates/${window.EDIT_TEMPLATE.id}`
// // // // //     : "/api/templates";

// // // // //   const method = window.EDIT_TEMPLATE ? "PUT" : "POST";

// // // // //   try {
// // // // //     const res = await fetch(url, {
// // // // //       method: method,
// // // // //       headers: { "Content-Type": "application/json" },
// // // // //       body: JSON.stringify(data),
// // // // //     });
// // // // //     const result = await res.json();

// // // // //     if (result.success) {
// // // // //       showNotification("تم حفظ القالب بنجاح", "success");
// // // // //       setTimeout(() => (location.href = "/reports"), 800);
// // // // //     } else {
// // // // //       showNotification(result.error || "فشل في حفظ القالب", "error");
// // // // //     }
// // // // //   } catch (e) {
// // // // //     console.error(e);
// // // // //     showNotification("خطأ في الاتصال بالخادم", "error");
// // // // //   }
// // // // // }

// // // // // // ================================================
// // // // // // Initialize - Keyboard shortcuts
// // // // // // ================================================
// // // // // document.addEventListener("keydown", function (e) {
// // // // //   // Ctrl+S to save
// // // // //   if (e.ctrlKey && e.key === "s") {
// // // // //     e.preventDefault();
// // // // //     saveTemplate();
// // // // //   }
// // // // //   // Delete key to remove selected field
// // // // //   if (e.key === "Delete" && selectedFieldIndex >= 0) {
// // // // //     e.preventDefault();
// // // // //     removeField(selectedFieldIndex);
// // // // //   }
// // // // // });

// // // // /* ================================================
// // // //    template_builder.js - Fixed Template Loading
// // // //    ================================================ */

// // // // let templateFields = [];
// // // // let fieldCounter = 0;
// // // // let selectedFieldIndex = -1;
// // // // let draggedIndex = -1;

// // // // // ═══════════════════════════════════════════
// // // // // Load existing template if editing - FIXED
// // // // // ═══════════════════════════════════════════
// // // // if (window.EDIT_TEMPLATE) {
// // // //   console.log("📋 Editing template:", window.EDIT_TEMPLATE);

// // // //   // استخراج structure من الكائن
// // // //   const structure = window.EDIT_TEMPLATE.structure || [];
// // // //   console.log("📋 Structure loaded:", structure.length, "fields");

// // // //   templateFields = JSON.parse(JSON.stringify(structure)); // Deep copy
// // // //   fieldCounter = templateFields.length;

// // // //   // تحميل البيانات الأساسية
// // // //   document.getElementById("templateTitle").value =
// // // //     window.EDIT_TEMPLATE.title || "";
// // // //   document.getElementById("templateDescription").value =
// // // //     window.EDIT_TEMPLATE.description || "";
// // // //   document.getElementById("templateCategory").value =
// // // //     window.EDIT_TEMPLATE.category || "general";

// // // //   // تأكيد التحميل
// // // //   console.log("✅ Loaded", templateFields.length, "fields for editing");

// // // //   // عرض القالب
// // // //   setTimeout(() => {
// // // //     renderCanvas();
// // // //   }, 100);
// // // // }

// // // // // ═══════════════════════════════════════════
// // // // // 10 Types Only
// // // // // ═══════════════════════════════════════════
// // // // const TYPE_LABELS = {
// // // //   text: "نص قصير",
// // // //   textarea: "نص طويل",
// // // //   number: "رقم",
// // // //   date: "تاريخ",
// // // //   select: "قائمة منسدلة",
// // // //   checkbox: "مربع اختيار",
// // // //   heading: "عنوان قسم",
// // // //   subheading: "عنوان فرعي",
// // // //   divider: "فاصل",
// // // //   signature: "توقيع الطبيب",
// // // // };

// // // // const TYPE_ICONS = {
// // // //   text: "fa-font",
// // // //   textarea: "fa-align-left",
// // // //   number: "fa-hashtag",
// // // //   date: "fa-calendar",
// // // //   select: "fa-list",
// // // //   checkbox: "fa-check-square",
// // // //   heading: "fa-heading",
// // // //   subheading: "fa-heading",
// // // //   divider: "fa-minus",
// // // //   signature: "fa-signature",
// // // // };

// // // // // ═══════════════════════════════════════════
// // // // // Add Field
// // // // // ═══════════════════════════════════════════
// // // // function addField(type) {
// // // //   fieldCounter++;
// // // //   let options = type === "select" ? ["خيار 1", "خيار 2"] : [];

// // // //   const field = {
// // // //     id: `field_${Date.now()}`,
// // // //     type: type,
// // // //     name: `${type}_${fieldCounter}`,
// // // //     label: TYPE_LABELS[type] || `حقل ${fieldCounter}`,
// // // //     placeholder: "",
// // // //     required: false,
// // // //     options: options,
// // // //   };

// // // //   templateFields.push(field);
// // // //   selectField(templateFields.length - 1);
// // // //   renderCanvas();
// // // // }

// // // // // ═══════════════════════════════════════════
// // // // // Drag & Drop
// // // // // ═══════════════════════════════════════════
// // // // function handleDragStart(e, index) {
// // // //   draggedIndex = index;
// // // //   const item = e.target.closest(".field-item");
// // // //   if (item) item.style.opacity = "0.4";
// // // //   e.dataTransfer.effectAllowed = "move";
// // // // }

// // // // function handleDragOver(e) {
// // // //   e.preventDefault();
// // // // }

// // // // function handleDrop(e, dropIndex) {
// // // //   e.preventDefault();
// // // //   e.stopPropagation();
// // // //   document.querySelectorAll(".field-item").forEach((el) => {
// // // //     el.style.borderTop = "";
// // // //   });
// // // //   if (
// // // //     draggedIndex !== -1 &&
// // // //     draggedIndex !== dropIndex &&
// // // //     draggedIndex !== undefined
// // // //   ) {
// // // //     const [moved] = templateFields.splice(draggedIndex, 1);
// // // //     const ni = dropIndex > draggedIndex ? dropIndex - 1 : dropIndex;
// // // //     templateFields.splice(ni >= 0 ? ni : 0, 0, moved);
// // // //     selectedFieldIndex = ni >= 0 ? ni : 0;
// // // //   }
// // // //   draggedIndex = -1;
// // // //   renderCanvas();
// // // //   if (selectedFieldIndex >= 0 && selectedFieldIndex < templateFields.length) {
// // // //     const el = document.querySelector(
// // // //       `.field-item[data-index="${selectedFieldIndex}"]`,
// // // //     );
// // // //     if (el) el.classList.add("selected");
// // // //   }
// // // // }

// // // // function handleDragEnd(e) {
// // // //   const item = e.target.closest(".field-item");
// // // //   if (item) item.style.opacity = "1";
// // // //   document.querySelectorAll(".field-item").forEach((el) => {
// // // //     el.style.borderTop = "";
// // // //   });
// // // //   draggedIndex = -1;
// // // // }

// // // // // ═══════════════════════════════════════════
// // // // // Select Field
// // // // // ═══════════════════════════════════════════
// // // // function selectField(index, event) {
// // // //   if (event) {
// // // //     event.stopPropagation();
// // // //     event.preventDefault();
// // // //   }
// // // //   selectedFieldIndex = index;
// // // //   document
// // // //     .querySelectorAll(".field-item")
// // // //     .forEach((el) => el.classList.remove("selected"));
// // // //   const el = document.querySelector(`.field-item[data-index="${index}"]`);
// // // //   if (el) el.classList.add("selected");

// // // //   const field = templateFields[index];
// // // //   if (!field) {
// // // //     document.getElementById("propertiesPanel").style.display = "none";
// // // //     return;
// // // //   }

// // // //   document.getElementById("propertiesPanel").style.display = "block";
// // // //   document.getElementById("selectedFieldIndex").value = index;
// // // //   document.getElementById("propName").value = field.name || "";
// // // //   document.getElementById("propLabel").value = field.label || "";
// // // //   document.getElementById("propPlaceholder").value = field.placeholder || "";
// // // //   document.getElementById("propRequired").checked = field.required || false;

// // // //   document.getElementById("optionsSection").style.display =
// // // //     field.type === "select" ? "block" : "none";
// // // //   if (field.type === "select") renderOptionsList(field.options || []);
// // // // }

// // // // function applyProperty(key, value) {
// // // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // // //   if (index >= 0 && templateFields[index]) {
// // // //     templateFields[index][key] = value;
// // // //     if (key === "label" || key === "placeholder") {
// // // //       renderCanvas();
// // // //       selectField(index);
// // // //     }
// // // //   }
// // // // }

// // // // function deleteSelectedField() {
// // // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // // //   if (index >= 0) {
// // // //     templateFields.splice(index, 1);
// // // //     selectedFieldIndex = -1;
// // // //     document.getElementById("propertiesPanel").style.display = "none";
// // // //     renderCanvas();
// // // //   }
// // // // }

// // // // // ═══════════════════════════════════════════
// // // // // Options
// // // // // ═══════════════════════════════════════════
// // // // function addOption() {
// // // //   const val = document.getElementById("newOption").value.trim();
// // // //   if (!val) return;
// // // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // // //   if (index >= 0 && templateFields[index]) {
// // // //     if (!templateFields[index].options) templateFields[index].options = [];
// // // //     templateFields[index].options.push(val);
// // // //     renderOptionsList(templateFields[index].options);
// // // //     renderCanvas();
// // // //     selectField(index);
// // // //   }
// // // //   document.getElementById("newOption").value = "";
// // // // }

// // // // function removeOption(i) {
// // // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // // //   if (index >= 0 && templateFields[index]) {
// // // //     templateFields[index].options.splice(i, 1);
// // // //     renderOptionsList(templateFields[index].options);
// // // //     renderCanvas();
// // // //     selectField(index);
// // // //   }
// // // // }

// // // // function renderOptionsList(opts) {
// // // //   document.getElementById("optionsList").innerHTML = (opts || [])
// // // //     .map(
// // // //       (o, i) =>
// // // //         `<span class="option-chip">${o} <span class="remove-option" onclick="removeOption(${i})">&times;</span></span>`,
// // // //     )
// // // //     .join("");
// // // // }

// // // // // ═══════════════════════════════════════════
// // // // // Render Canvas
// // // // // ═══════════════════════════════════════════
// // // // function renderCanvas() {
// // // //   const canvas = document.getElementById("templateCanvas");
// // // //   if (!canvas) return;
// // // //   if (templateFields.length === 0) {
// // // //     canvas.innerHTML = `<div class="canvas-empty"><i class="fas fa-arrow-left fa-3x mb-3" style="color:#ccc"></i><p>أضف حقولاً من القائمة الجانبية</p></div>`;
// // // //     return;
// // // //   }
// // // //   canvas.innerHTML = templateFields.map((f, i) => renderField(f, i)).join("");
// // // //   if (selectedFieldIndex >= 0 && selectedFieldIndex < templateFields.length) {
// // // //     const el = canvas.querySelector(
// // // //       `.field-item[data-index="${selectedFieldIndex}"]`,
// // // //     );
// // // //     if (el) el.classList.add("selected");
// // // //   }
// // // // }

// // // // function renderField(field, index) {
// // // //   const sel = index === selectedFieldIndex ? "selected" : "";
// // // //   const drag = `draggable="true" ondragstart="handleDragStart(event,${index})" ondragover="handleDragOver(event)" ondrop="handleDrop(event,${index})" ondragend="handleDragEnd(event)"`;
// // // //   const btns = `<button class="btn-action" onclick="event.stopPropagation();moveField(${index},-1)"><i class="fas fa-arrow-up"></i></button><button class="btn-action" onclick="event.stopPropagation();moveField(${index},1)"><i class="fas fa-arrow-down"></i></button><button class="btn-action danger" onclick="event.stopPropagation();removeField(${index})"><i class="fas fa-trash"></i></button>`;
// // // //   const lbl = `${field.label} ${field.required ? '<span class="text-danger">*</span>' : ""}`;

// // // //   if (field.type === "heading")
// // // //     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-heading"></i> عنوان قسم</span><div class="d-flex gap-1">${btns}</div></div><h5 style="color:#1a5276;margin:0">${field.label}</h5></div>`;
// // // //   if (field.type === "divider")
// // // //     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-minus"></i> فاصل</span><div class="d-flex gap-1">${btns}</div></div><hr style="border-style:dashed;color:#ddd;margin:4px 0"></div>`;
// // // //   if (field.type === "subheading")
// // // //     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-heading"></i> عنوان فرعي</span><div class="d-flex gap-1">${btns}</div></div><h6 style="color:#2c3e50;margin:0">${field.label}</h6></div>`;
// // // //   if (field.type === "signature")
// // // //     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-signature"></i> توقيع</span><div class="d-flex gap-1">${btns}</div></div><div style="border:1px dashed #ccc;border-radius:8px;padding:15px;text-align:center;color:#999;margin-top:5px"><i class="fas fa-signature fa-2x mb-2 d-block"></i><small>مكان توقيع الطبيب</small><div style="border-bottom:1px solid #ccc;width:60%;margin:10px auto 0"></div></div></div>`;

// // // //   let preview = "";
// // // //   switch (field.type) {
// // // //     case "text":
// // // //       preview = `<input type="text" class="form-control form-control-sm" placeholder="${field.placeholder || "نص قصير"}" disabled>`;
// // // //       break;
// // // //     case "textarea":
// // // //       preview = `<textarea class="form-control form-control-sm" rows="2" disabled></textarea>`;
// // // //       break;
// // // //     case "number":
// // // //       preview = `<input type="number" class="form-control form-control-sm" disabled>`;
// // // //       break;
// // // //     case "date":
// // // //       preview = `<input type="date" class="form-control form-control-sm" disabled>`;
// // // //       break;
// // // //     case "select":
// // // //       preview = `<select class="form-select form-select-sm" disabled>${(field.options || []).map((o) => `<option>${o}</option>`).join("")}</select>`;
// // // //       break;
// // // //     case "checkbox":
// // // //       preview = `<div class="form-check"><input type="checkbox" class="form-check-input" disabled><label class="form-check-label small">${field.label}</label></div>`;
// // // //       break;
// // // //     default:
// // // //       preview = `<input type="text" class="form-control form-control-sm" disabled>`;
// // // //   }

// // // //   return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas ${TYPE_ICONS[field.type] || "fa-pen"}"></i> ${TYPE_LABELS[field.type] || field.type}</span><div class="d-flex gap-1">${btns}</div></div><label class="fw-bold small mb-1 d-block">${lbl}</label>${preview}</div>`;
// // // // }

// // // // // ═══════════════════════════════════════════
// // // // // Move & Remove
// // // // // ═══════════════════════════════════════════
// // // // function moveField(index, dir) {
// // // //   const ni = index + dir;
// // // //   if (ni < 0 || ni >= templateFields.length) return;
// // // //   [templateFields[index], templateFields[ni]] = [
// // // //     templateFields[ni],
// // // //     templateFields[index],
// // // //   ];
// // // //   selectedFieldIndex = ni;
// // // //   renderCanvas();
// // // //   selectField(ni);
// // // // }

// // // // function removeField(index) {
// // // //   if (!confirm("حذف هذا الحقل؟")) return;
// // // //   templateFields.splice(index, 1);
// // // //   selectedFieldIndex =
// // // //     templateFields.length > 0 ? Math.min(index, templateFields.length - 1) : -1;
// // // //   if (selectedFieldIndex === -1)
// // // //     document.getElementById("propertiesPanel").style.display = "none";
// // // //   renderCanvas();
// // // //   if (selectedFieldIndex >= 0) selectField(selectedFieldIndex);
// // // // }

// // // // // ═══════════════════════════════════════════
// // // // // Preview & Save
// // // // // ═══════════════════════════════════════════
// // // // function previewTemplate() {
// // // //   let h = `<h4>${document.getElementById("templateTitle").value || "معاينة"}</h4><hr>`;
// // // //   templateFields.forEach((f) => {
// // // //     if (f.type === "heading")
// // // //       h += `<h5 style="color:#1a5276;margin-top:16px">${f.label}</h5>`;
// // // //     else if (f.type === "subheading")
// // // //       h += `<h6 style="color:#2c3e50">${f.label}</h6>`;
// // // //     else if (f.type === "divider") h += '<hr style="border-style:dashed">';
// // // //     else if (f.type === "signature")
// // // //       h += `<div style="border:1px dashed #ccc;border-radius:8px;padding:20px;text-align:center;color:#999;margin:10px 0"><i class="fas fa-signature fa-2x mb-2"></i><small>توقيع الطبيب</small></div>`;
// // // //     else if (f.type === "checkbox")
// // // //       h += `<div class="form-check mb-2"><input type="checkbox" disabled><label>${f.label}${f.required ? '<span style="color:red">*</span>' : ""}</label></div>`;
// // // //     else
// // // //       h += `<div class="mb-2"><label class="fw-bold small">${f.label}${f.required ? '<span style="color:red">*</span>' : ""}</label><input class="form-control form-control-sm" disabled></div>`;
// // // //   });
// // // //   document.getElementById("previewContent").innerHTML = h;
// // // //   new bootstrap.Modal(document.getElementById("previewModal")).show();
// // // // }

// // // // async function saveTemplate() {
// // // //   const title = document.getElementById("templateTitle").value.trim();
// // // //   if (!title) {
// // // //     showNotification("أدخل اسم القالب", "error");
// // // //     return;
// // // //   }
// // // //   if (!templateFields.length) {
// // // //     showNotification("أضف حقلاً واحداً", "error");
// // // //     return;
// // // //   }
// // // //   const data = {
// // // //     title,
// // // //     description: document.getElementById("templateDescription").value.trim(),
// // // //     category: document.getElementById("templateCategory").value,
// // // //     structure: templateFields,
// // // //   };
// // // //   const url = window.EDIT_TEMPLATE
// // // //     ? `/api/templates/${window.EDIT_TEMPLATE.id}`
// // // //     : "/api/templates";
// // // //   try {
// // // //     const r = await fetch(url, {
// // // //       method: window.EDIT_TEMPLATE ? "PUT" : "POST",
// // // //       headers: { "Content-Type": "application/json" },
// // // //       body: JSON.stringify(data),
// // // //     });
// // // //     const j = await r.json();
// // // //     if (j.success) {
// // // //       showNotification("تم الحفظ", "success");
// // // //       setTimeout(() => (location.href = "/reports"), 800);
// // // //     } else showNotification(j.error || "فشل", "error");
// // // //   } catch (e) {
// // // //     showNotification("خطأ اتصال", "error");
// // // //   }
// // // // }

// // // // document.addEventListener("keydown", (e) => {
// // // //   if (e.ctrlKey && e.key === "s") {
// // // //     e.preventDefault();
// // // //     saveTemplate();
// // // //   }
// // // //   if (e.key === "Delete" && selectedFieldIndex >= 0) {
// // // //     e.preventDefault();
// // // //     removeField(selectedFieldIndex);
// // // //   }
// // // // });
// // // /* ================================================
// // //    template_builder.js - Final Version
// // //    ================================================ */

// // // let templateFields = [];
// // // let fieldCounter = 0;
// // // let selectedFieldIndex = -1;
// // // let draggedIndex = -1;
// // // let pendingDeleteIndex = -1;

// // // // ═══════════════════════════════════════════
// // // // Load existing template if editing
// // // // ═══════════════════════════════════════════
// // // if (window.EDIT_TEMPLATE) {
// // //   const structure = window.EDIT_TEMPLATE.structure || [];
// // //   templateFields = JSON.parse(JSON.stringify(structure));
// // //   fieldCounter = templateFields.length;
// // //   document.getElementById("templateTitle").value =
// // //     window.EDIT_TEMPLATE.title || "";
// // //   document.getElementById("templateDescription").value =
// // //     window.EDIT_TEMPLATE.description || "";
// // //   document.getElementById("templateCategory").value =
// // //     window.EDIT_TEMPLATE.category || "general";
// // //   setTimeout(() => renderCanvas(), 100);
// // // }

// // // // ═══════════════════════════════════════════
// // // // 10 Types
// // // // ═══════════════════════════════════════════
// // // const TYPE_LABELS = {
// // //   text: "نص قصير",
// // //   textarea: "نص طويل",
// // //   number: "رقم",
// // //   date: "تاريخ",
// // //   select: "قائمة منسدلة",
// // //   checkbox: "مربع اختيار",
// // //   heading: "عنوان قسم",
// // //   subheading: "عنوان فرعي",
// // //   divider: "فاصل",
// // //   signature: "توقيع الطبيب",
// // // };

// // // const TYPE_ICONS = {
// // //   text: "fa-font",
// // //   textarea: "fa-align-left",
// // //   number: "fa-hashtag",
// // //   date: "fa-calendar",
// // //   select: "fa-list",
// // //   checkbox: "fa-check-square",
// // //   heading: "fa-heading",
// // //   subheading: "fa-heading",
// // //   divider: "fa-minus",
// // //   signature: "fa-signature",
// // // };

// // // // ═══════════════════════════════════════════
// // // // Add Field
// // // // ═══════════════════════════════════════════
// // // function addField(type) {
// // //   fieldCounter++;
// // //   let options = type === "select" ? ["خيار 1", "خيار 2"] : [];
// // //   const field = {
// // //     id: `field_${Date.now()}`,
// // //     type: type,
// // //     name: `${type}_${fieldCounter}`,
// // //     label: TYPE_LABELS[type] || `حقل ${fieldCounter}`,
// // //     placeholder: "",
// // //     required: false,
// // //     options: options,
// // //   };
// // //   templateFields.push(field);
// // //   selectField(templateFields.length - 1);
// // //   renderCanvas();
// // // }

// // // // ═══════════════════════════════════════════
// // // // Drag & Drop
// // // // ═══════════════════════════════════════════
// // // function handleDragStart(e, index) {
// // //   draggedIndex = index;
// // //   e.target.closest(".field-item").style.opacity = "0.4";
// // //   e.dataTransfer.effectAllowed = "move";
// // // }
// // // function handleDragOver(e) {
// // //   e.preventDefault();
// // // }
// // // function handleDrop(e, dropIndex) {
// // //   e.preventDefault();
// // //   e.stopPropagation();
// // //   document
// // //     .querySelectorAll(".field-item")
// // //     .forEach((el) => (el.style.borderTop = ""));
// // //   if (draggedIndex !== -1 && draggedIndex !== dropIndex) {
// // //     const [moved] = templateFields.splice(draggedIndex, 1);
// // //     const ni = dropIndex > draggedIndex ? dropIndex - 1 : dropIndex;
// // //     templateFields.splice(ni >= 0 ? ni : 0, 0, moved);
// // //     selectedFieldIndex = ni >= 0 ? ni : 0;
// // //   }
// // //   draggedIndex = -1;
// // //   renderCanvas();
// // //   if (selectedFieldIndex >= 0) {
// // //     const el = document.querySelector(
// // //       `.field-item[data-index="${selectedFieldIndex}"]`,
// // //     );
// // //     if (el) el.classList.add("selected");
// // //   }
// // // }
// // // function handleDragEnd(e) {
// // //   const item = e.target.closest(".field-item");
// // //   if (item) item.style.opacity = "1";
// // //   document
// // //     .querySelectorAll(".field-item")
// // //     .forEach((el) => (el.style.borderTop = ""));
// // //   draggedIndex = -1;
// // // }

// // // // ═══════════════════════════════════════════
// // // // Select & Properties
// // // // ═══════════════════════════════════════════
// // // function selectField(index, event) {
// // //   if (event) {
// // //     event.stopPropagation();
// // //     event.preventDefault();
// // //   }
// // //   selectedFieldIndex = index;
// // //   document
// // //     .querySelectorAll(".field-item")
// // //     .forEach((el) => el.classList.remove("selected"));
// // //   const el = document.querySelector(`.field-item[data-index="${index}"]`);
// // //   if (el) el.classList.add("selected");
// // //   const field = templateFields[index];
// // //   if (!field) {
// // //     document.getElementById("propertiesPanel").style.display = "none";
// // //     return;
// // //   }
// // //   document.getElementById("propertiesPanel").style.display = "block";
// // //   document.getElementById("selectedFieldIndex").value = index;
// // //   document.getElementById("propName").value = field.name || "";
// // //   document.getElementById("propLabel").value = field.label || "";
// // //   document.getElementById("propPlaceholder").value = field.placeholder || "";
// // //   document.getElementById("propRequired").checked = field.required || false;
// // //   document.getElementById("optionsSection").style.display =
// // //     field.type === "select" ? "block" : "none";
// // //   if (field.type === "select") renderOptionsList(field.options || []);
// // // }

// // // function applyProperty(key, value) {
// // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // //   if (index >= 0 && templateFields[index]) {
// // //     templateFields[index][key] = value;
// // //     if (key === "label" || key === "placeholder") {
// // //       renderCanvas();
// // //       selectField(index);
// // //     }
// // //   }
// // // }

// // // // ═══════════════════════════════════════════
// // // // Delete with Modal Confirmation
// // // // ═══════════════════════════════════════════
// // // function deleteSelectedField() {
// // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // //   if (index >= 0) {
// // //     pendingDeleteIndex = index;
// // //     new bootstrap.Modal(document.getElementById("confirmDeleteModal")).show();
// // //   }
// // // }

// // // function removeField(index) {
// // //   pendingDeleteIndex = index;
// // //   new bootstrap.Modal(document.getElementById("confirmDeleteModal")).show();
// // // }

// // // // Confirm delete button handler
// // // document.addEventListener("DOMContentLoaded", () => {
// // //   const confirmBtn = document.getElementById("confirmDeleteBtn");
// // //   if (confirmBtn) {
// // //     confirmBtn.addEventListener("click", () => {
// // //       if (pendingDeleteIndex >= 0) {
// // //         templateFields.splice(pendingDeleteIndex, 1);
// // //         selectedFieldIndex =
// // //           templateFields.length > 0
// // //             ? Math.min(pendingDeleteIndex, templateFields.length - 1)
// // //             : -1;
// // //         if (selectedFieldIndex === -1)
// // //           document.getElementById("propertiesPanel").style.display = "none";
// // //         renderCanvas();
// // //         if (selectedFieldIndex >= 0) selectField(selectedFieldIndex);
// // //         pendingDeleteIndex = -1;
// // //         bootstrap.Modal.getInstance(
// // //           document.getElementById("confirmDeleteModal"),
// // //         ).hide();
// // //       }
// // //     });
// // //   }
// // // });

// // // // ═══════════════════════════════════════════
// // // // Options
// // // // ═══════════════════════════════════════════
// // // function addOption() {
// // //   const val = document.getElementById("newOption").value.trim();
// // //   if (!val) return;
// // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // //   if (index >= 0 && templateFields[index]) {
// // //     if (!templateFields[index].options) templateFields[index].options = [];
// // //     templateFields[index].options.push(val);
// // //     renderOptionsList(templateFields[index].options);
// // //     renderCanvas();
// // //     selectField(index);
// // //   }
// // //   document.getElementById("newOption").value = "";
// // // }
// // // function removeOption(i) {
// // //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// // //   if (index >= 0 && templateFields[index]) {
// // //     templateFields[index].options.splice(i, 1);
// // //     renderOptionsList(templateFields[index].options);
// // //     renderCanvas();
// // //     selectField(index);
// // //   }
// // // }
// // // function renderOptionsList(opts) {
// // //   document.getElementById("optionsList").innerHTML = (opts || [])
// // //     .map(
// // //       (o, i) =>
// // //         `<span class="option-chip">${o} <span class="remove-option" onclick="removeOption(${i})">&times;</span></span>`,
// // //     )
// // //     .join("");
// // // }

// // // // ═══════════════════════════════════════════
// // // // Render Canvas
// // // // ═══════════════════════════════════════════
// // // function renderCanvas() {
// // //   const canvas = document.getElementById("templateCanvas");
// // //   if (!canvas) return;
// // //   if (templateFields.length === 0) {
// // //     canvas.innerHTML = `<div class="canvas-empty"><i class="fas fa-arrow-left fa-3x mb-3" style="color:#ccc"></i><p>أضف حقولاً من القائمة الجانبية</p></div>`;
// // //     return;
// // //   }
// // //   canvas.innerHTML = templateFields.map((f, i) => renderField(f, i)).join("");
// // //   if (selectedFieldIndex >= 0 && selectedFieldIndex < templateFields.length) {
// // //     const el = canvas.querySelector(
// // //       `.field-item[data-index="${selectedFieldIndex}"]`,
// // //     );
// // //     if (el) el.classList.add("selected");
// // //   }
// // // }

// // // function renderField(field, index) {
// // //   const sel = index === selectedFieldIndex ? "selected" : "";
// // //   const drag = `draggable="true" ondragstart="handleDragStart(event,${index})" ondragover="handleDragOver(event)" ondrop="handleDrop(event,${index})" ondragend="handleDragEnd(event)"`;
// // //   const btns = `<button class="btn-action" onclick="event.stopPropagation();moveField(${index},-1)"><i class="fas fa-arrow-up"></i></button><button class="btn-action" onclick="event.stopPropagation();moveField(${index},1)"><i class="fas fa-arrow-down"></i></button><button class="btn-action danger" onclick="event.stopPropagation();removeField(${index})"><i class="fas fa-trash"></i></button>`;
// // //   const lbl = `${field.label} ${field.required ? '<span class="text-danger">*</span>' : ""}`;

// // //   if (field.type === "heading")
// // //     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-heading"></i> عنوان قسم</span><div class="d-flex gap-1">${btns}</div></div><h5 style="color:#1a5276;margin:0">${field.label}</h5></div>`;
// // //   if (field.type === "divider")
// // //     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-minus"></i> فاصل</span><div class="d-flex gap-1">${btns}</div></div><hr style="border-style:dashed;color:#ddd;margin:4px 0"></div>`;
// // //   if (field.type === "subheading")
// // //     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-heading"></i> عنوان فرعي</span><div class="d-flex gap-1">${btns}</div></div><h6 style="color:#2c3e50;margin:0">${field.label}</h6></div>`;
// // //   if (field.type === "signature")
// // //     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-signature"></i> توقيع</span><div class="d-flex gap-1">${btns}</div></div><div style="border:1px dashed #ccc;border-radius:8px;padding:15px;text-align:center;color:#999;margin-top:5px"><i class="fas fa-signature fa-2x mb-2 d-block"></i><small>مكان توقيع الطبيب</small><div style="border-bottom:1px solid #ccc;width:60%;margin:10px auto 0"></div></div></div>`;

// // //   let preview = "";
// // //   switch (field.type) {
// // //     case "text":
// // //       preview = `<input type="text" class="form-control form-control-sm" placeholder="${field.placeholder || "نص قصير"}" disabled>`;
// // //       break;
// // //     case "textarea":
// // //       preview = `<textarea class="form-control form-control-sm" rows="2" disabled></textarea>`;
// // //       break;
// // //     case "number":
// // //       preview = `<input type="number" class="form-control form-control-sm" disabled>`;
// // //       break;
// // //     case "date":
// // //       preview = `<input type="date" class="form-control form-control-sm" disabled>`;
// // //       break;
// // //     case "select":
// // //       preview = `<select class="form-select form-select-sm" disabled>${(field.options || []).map((o) => `<option>${o}</option>`).join("")}</select>`;
// // //       break;
// // //     case "checkbox":
// // //       preview = `<div class="form-check"><input type="checkbox" class="form-check-input" disabled><label class="form-check-label small">${field.label}</label></div>`;
// // //       break;
// // //     default:
// // //       preview = `<input type="text" class="form-control form-control-sm" disabled>`;
// // //   }
// // //   return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas ${TYPE_ICONS[field.type] || "fa-pen"}"></i> ${TYPE_LABELS[field.type] || field.type}</span><div class="d-flex gap-1">${btns}</div></div><label class="fw-bold small mb-1 d-block">${lbl}</label>${preview}</div>`;
// // // }

// // // // ═══════════════════════════════════════════
// // // // Move
// // // // ═══════════════════════════════════════════
// // // function moveField(index, dir) {
// // //   const ni = index + dir;
// // //   if (ni < 0 || ni >= templateFields.length) return;
// // //   [templateFields[index], templateFields[ni]] = [
// // //     templateFields[ni],
// // //     templateFields[index],
// // //   ];
// // //   selectedFieldIndex = ni;
// // //   renderCanvas();
// // //   selectField(ni);
// // // }

// // // // ═══════════════════════════════════════════
// // // // Preview & Save
// // // // ═══════════════════════════════════════════
// // // function previewTemplate() {
// // //   let h = `<h4>${document.getElementById("templateTitle").value || "معاينة"}</h4><hr>`;
// // //   templateFields.forEach((f) => {
// // //     if (f.type === "heading")
// // //       h += `<h5 style="color:#1a5276;margin-top:16px">${f.label}</h5>`;
// // //     else if (f.type === "subheading")
// // //       h += `<h6 style="color:#2c3e50">${f.label}</h6>`;
// // //     else if (f.type === "divider") h += '<hr style="border-style:dashed">';
// // //     else if (f.type === "signature")
// // //       h += `<div style="border:1px dashed #ccc;border-radius:8px;padding:20px;text-align:center;color:#999;margin:10px 0"><i class="fas fa-signature fa-2x mb-2"></i><small>توقيع الطبيب</small></div>`;
// // //     else if (f.type === "checkbox")
// // //       h += `<div class="form-check mb-2"><input type="checkbox" disabled><label>${f.label}${f.required ? '<span style="color:red">*</span>' : ""}</label></div>`;
// // //     else
// // //       h += `<div class="mb-2"><label class="fw-bold small">${f.label}${f.required ? '<span style="color:red">*</span>' : ""}</label><input class="form-control form-control-sm" disabled></div>`;
// // //   });
// // //   document.getElementById("previewContent").innerHTML = h;
// // //   new bootstrap.Modal(document.getElementById("previewModal")).show();
// // // }

// // // async function saveTemplate() {
// // //   const title = document.getElementById("templateTitle").value.trim();
// // //   if (!title) {
// // //     showNotification("أدخل اسم القالب", "error");
// // //     return;
// // //   }
// // //   if (!templateFields.length) {
// // //     showNotification("أضف حقلاً واحداً", "error");
// // //     return;
// // //   }
// // //   const data = {
// // //     title,
// // //     description: document.getElementById("templateDescription").value.trim(),
// // //     category: document.getElementById("templateCategory").value,
// // //     structure: templateFields,
// // //   };
// // //   const url = window.EDIT_TEMPLATE
// // //     ? `/api/templates/${window.EDIT_TEMPLATE.id}`
// // //     : "/api/templates";
// // //   try {
// // //     const r = await fetch(url, {
// // //       method: window.EDIT_TEMPLATE ? "PUT" : "POST",
// // //       headers: { "Content-Type": "application/json" },
// // //       body: JSON.stringify(data),
// // //     });
// // //     const j = await r.json();
// // //     if (j.success) {
// // //       showNotification("تم الحفظ", "success");
// // //       setTimeout(() => (location.href = "/reports"), 800);
// // //     } else showNotification(j.error || "فشل", "error");
// // //   } catch (e) {
// // //     showNotification("خطأ اتصال", "error");
// // //   }
// // // }

// // // document.addEventListener("keydown", (e) => {
// // //   if (e.ctrlKey && e.key === "s") {
// // //     e.preventDefault();
// // //     saveTemplate();
// // //   }
// // //   if (e.key === "Delete" && selectedFieldIndex >= 0) {
// // //     e.preventDefault();
// // //     removeField(selectedFieldIndex);
// // //   }
// // // });
// // /* ================================================
// //    template_builder.js - Final Version
// //    ================================================ */

// // let templateFields = [];
// // let fieldCounter = 0;
// // let selectedFieldIndex = -1;
// // let draggedIndex = -1;
// // let pendingDeleteIndex = -1;

// // // ═══════════════════════════════════════════
// // // Load existing template if editing
// // // ═══════════════════════════════════════════
// // if (window.EDIT_TEMPLATE) {
// //   const structure = window.EDIT_TEMPLATE.structure || [];
// //   templateFields = JSON.parse(JSON.stringify(structure));
// //   fieldCounter = templateFields.length;
// //   document.getElementById("templateTitle").value =
// //     window.EDIT_TEMPLATE.title || "";
// //   document.getElementById("templateDescription").value =
// //     window.EDIT_TEMPLATE.description || "";
// //   document.getElementById("templateCategory").value =
// //     window.EDIT_TEMPLATE.category || "general";
// //   setTimeout(() => renderCanvas(), 100);
// // }

// // // ═══════════════════════════════════════════
// // // 10 Types
// // // ═══════════════════════════════════════════
// // const TYPE_LABELS = {
// //   text: "نص قصير",
// //   textarea: "نص طويل",
// //   number: "رقم",
// //   date: "تاريخ",
// //   select: "قائمة منسدلة",
// //   checkbox: "مربع اختيار",
// //   heading: "عنوان قسم",
// //   subheading: "عنوان فرعي",
// //   divider: "فاصل",
// //   signature: "توقيع الطبيب",
// // };

// // const TYPE_ICONS = {
// //   text: "fa-font",
// //   textarea: "fa-align-left",
// //   number: "fa-hashtag",
// //   date: "fa-calendar",
// //   select: "fa-list",
// //   checkbox: "fa-check-square",
// //   heading: "fa-heading",
// //   subheading: "fa-heading",
// //   divider: "fa-minus",
// //   signature: "fa-signature",
// // };

// // // ═══════════════════════════════════════════
// // // Add Field
// // // ═══════════════════════════════════════════
// // function addField(type) {
// //   fieldCounter++;
// //   let options = type === "select" ? ["خيار 1", "خيار 2"] : [];
// //   const field = {
// //     id: `field_${Date.now()}`,
// //     type: type,
// //     name: `${type}_${fieldCounter}`,
// //     label: TYPE_LABELS[type] || `حقل ${fieldCounter}`,
// //     placeholder: "",
// //     required: false,
// //     options: options,
// //   };
// //   templateFields.push(field);
// //   selectField(templateFields.length - 1);
// //   renderCanvas();
// // }

// // // ═══════════════════════════════════════════
// // // Drag & Drop
// // // ═══════════════════════════════════════════
// // function handleDragStart(e, index) {
// //   draggedIndex = index;
// //   e.target.closest(".field-item").style.opacity = "0.4";
// //   e.dataTransfer.effectAllowed = "move";
// // }
// // function handleDragOver(e) {
// //   e.preventDefault();
// // }
// // function handleDrop(e, dropIndex) {
// //   e.preventDefault();
// //   e.stopPropagation();
// //   document
// //     .querySelectorAll(".field-item")
// //     .forEach((el) => (el.style.borderTop = ""));
// //   if (draggedIndex !== -1 && draggedIndex !== dropIndex) {
// //     const [moved] = templateFields.splice(draggedIndex, 1);
// //     const ni = dropIndex > draggedIndex ? dropIndex - 1 : dropIndex;
// //     templateFields.splice(ni >= 0 ? ni : 0, 0, moved);
// //     selectedFieldIndex = ni >= 0 ? ni : 0;
// //   }
// //   draggedIndex = -1;
// //   renderCanvas();
// //   if (selectedFieldIndex >= 0) {
// //     const el = document.querySelector(
// //       `.field-item[data-index="${selectedFieldIndex}"]`,
// //     );
// //     if (el) el.classList.add("selected");
// //   }
// // }
// // function handleDragEnd(e) {
// //   const item = e.target.closest(".field-item");
// //   if (item) item.style.opacity = "1";
// //   document
// //     .querySelectorAll(".field-item")
// //     .forEach((el) => (el.style.borderTop = ""));
// //   draggedIndex = -1;
// // }

// // // ═══════════════════════════════════════════
// // // Select & Properties
// // // ═══════════════════════════════════════════
// // function selectField(index, event) {
// //   if (event) {
// //     event.stopPropagation();
// //     event.preventDefault();
// //   }
// //   selectedFieldIndex = index;
// //   document
// //     .querySelectorAll(".field-item")
// //     .forEach((el) => el.classList.remove("selected"));
// //   const el = document.querySelector(`.field-item[data-index="${index}"]`);
// //   if (el) el.classList.add("selected");
// //   const field = templateFields[index];
// //   if (!field) {
// //     document.getElementById("propertiesPanel").style.display = "none";
// //     return;
// //   }
// //   document.getElementById("propertiesPanel").style.display = "block";
// //   document.getElementById("selectedFieldIndex").value = index;
// //   document.getElementById("propName").value = field.name || "";
// //   document.getElementById("propLabel").value = field.label || "";
// //   document.getElementById("propPlaceholder").value = field.placeholder || "";
// //   document.getElementById("propRequired").checked = field.required || false;
// //   document.getElementById("optionsSection").style.display =
// //     field.type === "select" ? "block" : "none";
// //   if (field.type === "select") renderOptionsList(field.options || []);
// // }

// // function applyProperty(key, value) {
// //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// //   if (index >= 0 && templateFields[index]) {
// //     templateFields[index][key] = value;
// //     if (key === "label" || key === "placeholder") {
// //       renderCanvas();
// //       selectField(index);
// //     }
// //   }
// // }

// // // ═══════════════════════════════════════════
// // // Delete with Modal Confirmation
// // // ═══════════════════════════════════════════
// // function deleteSelectedField() {
// //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// //   if (index >= 0) {
// //     pendingDeleteIndex = index;
// //     new bootstrap.Modal(document.getElementById("confirmDeleteModal")).show();
// //   }
// // }

// // function removeField(index) {
// //   pendingDeleteIndex = index;
// //   new bootstrap.Modal(document.getElementById("confirmDeleteModal")).show();
// // }

// // // Confirm delete button handler
// // document.addEventListener("DOMContentLoaded", () => {
// //   const confirmBtn = document.getElementById("confirmDeleteBtn");
// //   if (confirmBtn) {
// //     confirmBtn.addEventListener("click", () => {
// //       if (pendingDeleteIndex >= 0) {
// //         templateFields.splice(pendingDeleteIndex, 1);
// //         selectedFieldIndex =
// //           templateFields.length > 0
// //             ? Math.min(pendingDeleteIndex, templateFields.length - 1)
// //             : -1;
// //         if (selectedFieldIndex === -1)
// //           document.getElementById("propertiesPanel").style.display = "none";
// //         renderCanvas();
// //         if (selectedFieldIndex >= 0) selectField(selectedFieldIndex);
// //         pendingDeleteIndex = -1;
// //         bootstrap.Modal.getInstance(
// //           document.getElementById("confirmDeleteModal"),
// //         ).hide();
// //       }
// //     });
// //   }
// // });

// // // ═══════════════════════════════════════════
// // // Options
// // // ═══════════════════════════════════════════
// // function addOption() {
// //   const val = document.getElementById("newOption").value.trim();
// //   if (!val) return;
// //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// //   if (index >= 0 && templateFields[index]) {
// //     if (!templateFields[index].options) templateFields[index].options = [];
// //     templateFields[index].options.push(val);
// //     renderOptionsList(templateFields[index].options);
// //     renderCanvas();
// //     selectField(index);
// //   }
// //   document.getElementById("newOption").value = "";
// // }
// // function removeOption(i) {
// //   const index = parseInt(document.getElementById("selectedFieldIndex").value);
// //   if (index >= 0 && templateFields[index]) {
// //     templateFields[index].options.splice(i, 1);
// //     renderOptionsList(templateFields[index].options);
// //     renderCanvas();
// //     selectField(index);
// //   }
// // }
// // function renderOptionsList(opts) {
// //   document.getElementById("optionsList").innerHTML = (opts || [])
// //     .map(
// //       (o, i) =>
// //         `<span class="option-chip">${o} <span class="remove-option" onclick="removeOption(${i})">&times;</span></span>`,
// //     )
// //     .join("");
// // }

// // // ═══════════════════════════════════════════
// // // Render Canvas
// // // ═══════════════════════════════════════════
// // function renderCanvas() {
// //   const canvas = document.getElementById("templateCanvas");
// //   if (!canvas) return;
// //   if (templateFields.length === 0) {
// //     canvas.innerHTML = `<div class="canvas-empty"><i class="fas fa-arrow-left fa-3x mb-3" style="color:#ccc"></i><p>أضف حقولاً من القائمة الجانبية</p></div>`;
// //     return;
// //   }
// //   canvas.innerHTML = templateFields.map((f, i) => renderField(f, i)).join("");
// //   if (selectedFieldIndex >= 0 && selectedFieldIndex < templateFields.length) {
// //     const el = canvas.querySelector(
// //       `.field-item[data-index="${selectedFieldIndex}"]`,
// //     );
// //     if (el) el.classList.add("selected");
// //   }
// // }

// // function renderField(field, index) {
// //   const sel = index === selectedFieldIndex ? "selected" : "";
// //   const drag = `draggable="true" ondragstart="handleDragStart(event,${index})" ondragover="handleDragOver(event)" ondrop="handleDrop(event,${index})" ondragend="handleDragEnd(event)"`;
// //   const btns = `<button class="btn-action" onclick="event.stopPropagation();moveField(${index},-1)"><i class="fas fa-arrow-up"></i></button><button class="btn-action" onclick="event.stopPropagation();moveField(${index},1)"><i class="fas fa-arrow-down"></i></button><button class="btn-action danger" onclick="event.stopPropagation();removeField(${index})"><i class="fas fa-trash"></i></button>`;
// //   const lbl = `${field.label} ${field.required ? '<span class="text-danger">*</span>' : ""}`;

// //   if (field.type === "heading")
// //     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-heading"></i> عنوان قسم</span><div class="d-flex gap-1">${btns}</div></div><h5 style="color:#1a5276;margin:0">${field.label}</h5></div>`;
// //   if (field.type === "divider")
// //     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-minus"></i> فاصل</span><div class="d-flex gap-1">${btns}</div></div><hr style="border-style:dashed;color:#ddd;margin:4px 0"></div>`;
// //   if (field.type === "subheading")
// //     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-heading"></i> عنوان فرعي</span><div class="d-flex gap-1">${btns}</div></div><h6 style="color:#2c3e50;margin:0">${field.label}</h6></div>`;
// //   if (field.type === "signature")
// //     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-signature"></i> توقيع</span><div class="d-flex gap-1">${btns}</div></div><div style="border:1px dashed #ccc;border-radius:8px;padding:15px;text-align:center;color:#999;margin-top:5px"><i class="fas fa-signature fa-2x mb-2 d-block"></i><small>مكان توقيع الطبيب</small><div style="border-bottom:1px solid #ccc;width:60%;margin:10px auto 0"></div></div></div>`;

// //   let preview = "";
// //   switch (field.type) {
// //     case "text":
// //       preview = `<input type="text" class="form-control form-control-sm" placeholder="${field.placeholder || "نص قصير"}" disabled>`;
// //       break;
// //     case "textarea":
// //       preview = `<textarea class="form-control form-control-sm" rows="2" disabled></textarea>`;
// //       break;
// //     case "number":
// //       preview = `<input type="number" class="form-control form-control-sm" disabled>`;
// //       break;
// //     case "date":
// //       preview = `<input type="date" class="form-control form-control-sm" disabled>`;
// //       break;
// //     case "select":
// //       preview = `<select class="form-select form-select-sm" disabled>${(field.options || []).map((o) => `<option>${o}</option>`).join("")}</select>`;
// //       break;
// //     case "checkbox":
// //       preview = `<div class="form-check"><input type="checkbox" class="form-check-input" disabled><label class="form-check-label small">${field.label}</label></div>`;
// //       break;
// //     default:
// //       preview = `<input type="text" class="form-control form-control-sm" disabled>`;
// //   }
// //   return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas ${TYPE_ICONS[field.type] || "fa-pen"}"></i> ${TYPE_LABELS[field.type] || field.type}</span><div class="d-flex gap-1">${btns}</div></div><label class="fw-bold small mb-1 d-block">${lbl}</label>${preview}</div>`;
// // }

// // // ═══════════════════════════════════════════
// // // Move
// // // ═══════════════════════════════════════════
// // function moveField(index, dir) {
// //   const ni = index + dir;
// //   if (ni < 0 || ni >= templateFields.length) return;
// //   [templateFields[index], templateFields[ni]] = [
// //     templateFields[ni],
// //     templateFields[index],
// //   ];
// //   selectedFieldIndex = ni;
// //   renderCanvas();
// //   selectField(ni);
// // }

// // // ═══════════════════════════════════════════
// // // Preview & Save
// // // ═══════════════════════════════════════════
// // function previewTemplate() {
// //   let h = `<h4>${document.getElementById("templateTitle").value || "معاينة"}</h4><hr>`;
// //   templateFields.forEach((f) => {
// //     if (f.type === "heading")
// //       h += `<h5 style="color:#1a5276;margin-top:16px">${f.label}</h5>`;
// //     else if (f.type === "subheading")
// //       h += `<h6 style="color:#2c3e50">${f.label}</h6>`;
// //     else if (f.type === "divider") h += '<hr style="border-style:dashed">';
// //     else if (f.type === "signature")
// //       h += `<div style="border:1px dashed #ccc;border-radius:8px;padding:20px;text-align:center;color:#999;margin:10px 0"><i class="fas fa-signature fa-2x mb-2"></i><small>توقيع الطبيب</small></div>`;
// //     else if (f.type === "checkbox")
// //       h += `<div class="form-check mb-2"><input type="checkbox" disabled><label>${f.label}${f.required ? '<span style="color:red">*</span>' : ""}</label></div>`;
// //     else
// //       h += `<div class="mb-2"><label class="fw-bold small">${f.label}${f.required ? '<span style="color:red">*</span>' : ""}</label><input class="form-control form-control-sm" disabled></div>`;
// //   });
// //   document.getElementById("previewContent").innerHTML = h;
// //   new bootstrap.Modal(document.getElementById("previewModal")).show();
// // }

// // async function saveTemplate() {
// //   const title = document.getElementById("templateTitle").value.trim();
// //   if (!title) {
// //     showNotification("أدخل اسم القالب", "error");
// //     return;
// //   }
// //   if (!templateFields.length) {
// //     showNotification("أضف حقلاً واحداً", "error");
// //     return;
// //   }
// //   const data = {
// //     title,
// //     description: document.getElementById("templateDescription").value.trim(),
// //     category: document.getElementById("templateCategory").value,
// //     structure: templateFields,
// //   };
// //   const url = window.EDIT_TEMPLATE
// //     ? `/api/templates/${window.EDIT_TEMPLATE.id}`
// //     : "/api/templates";
// //   try {
// //     const r = await fetch(url, {
// //       method: window.EDIT_TEMPLATE ? "PUT" : "POST",
// //       headers: { "Content-Type": "application/json" },
// //       body: JSON.stringify(data),
// //     });
// //     const j = await r.json();
// //     if (j.success) {
// //       showNotification("تم الحفظ", "success");
// //       setTimeout(() => (location.href = "/reports"), 800);
// //     } else showNotification(j.error || "فشل", "error");
// //   } catch (e) {
// //     showNotification("خطأ اتصال", "error");
// //   }
// // }

// // document.addEventListener("keydown", (e) => {
// //   if (e.ctrlKey && e.key === "s") {
// //     e.preventDefault();
// //     saveTemplate();
// //   }
// //   if (e.key === "Delete" && selectedFieldIndex >= 0) {
// //     e.preventDefault();
// //     removeField(selectedFieldIndex);
// //   }
// // });

// /* ================================================
//    template_builder.js - Final Corrected Version
//    ================================================ */

// let templateFields = [];
// let fieldCounter = 0;
// let selectedFieldIndex = -1;
// let draggedIndex = -1;
// let pendingDeleteIndex = -1;

// // ═══════════════════════════════════════════
// // Load existing template if editing
// // ═══════════════════════════════════════════
// if (window.EDIT_TEMPLATE) {
//   const structure = window.EDIT_TEMPLATE.structure || [];
//   templateFields = JSON.parse(JSON.stringify(structure));
//   fieldCounter = templateFields.length;
//   document.getElementById("templateTitle").value =
//     window.EDIT_TEMPLATE.title || "";
//   document.getElementById("templateDescription").value =
//     window.EDIT_TEMPLATE.description || "";
//   document.getElementById("templateCategory").value =
//     window.EDIT_TEMPLATE.category || "general";
//   setTimeout(() => renderCanvas(), 100);
// }

// // ═══════════════════════════════════════════
// // 10 Types
// // ═══════════════════════════════════════════
// const TYPE_LABELS = {
//   text: "نص قصير",
//   textarea: "نص طويل",
//   number: "رقم",
//   date: "تاريخ",
//   select: "قائمة منسدلة",
//   checkbox: "مربع اختيار",
//   heading: "عنوان قسم",
//   subheading: "عنوان فرعي",
//   divider: "فاصل",
//   signature: "توقيع الطبيب",
// };

// const TYPE_ICONS = {
//   text: "fa-font",
//   textarea: "fa-align-left",
//   number: "fa-hashtag",
//   date: "fa-calendar",
//   select: "fa-list",
//   checkbox: "fa-check-square",
//   heading: "fa-heading",
//   subheading: "fa-heading",
//   divider: "fa-minus",
//   signature: "fa-signature",
// };

// // ═══════════════════════════════════════════
// // Add Field
// // ═══════════════════════════════════════════
// function addField(type) {
//   fieldCounter++;
//   let options = type === "select" ? ["خيار 1", "خيار 2"] : [];
//   const field = {
//     id: `field_${Date.now()}`,
//     type: type,
//     name: `${type}_${fieldCounter}`,
//     label: TYPE_LABELS[type] || `حقل ${fieldCounter}`,
//     placeholder: "",
//     required: false,
//     options: options,
//   };
//   templateFields.push(field);
//   selectField(templateFields.length - 1);
//   renderCanvas();
// }

// // ═══════════════════════════════════════════
// // Drag & Drop
// // ═══════════════════════════════════════════
// function handleDragStart(e, index) {
//   draggedIndex = index;
//   e.target.closest(".field-item").style.opacity = "0.4";
//   e.dataTransfer.effectAllowed = "move";
// }
// function handleDragOver(e) {
//   e.preventDefault();
// }
// function handleDrop(e, dropIndex) {
//   e.preventDefault();
//   e.stopPropagation();
//   document
//     .querySelectorAll(".field-item")
//     .forEach((el) => (el.style.borderTop = ""));
//   if (draggedIndex !== -1 && draggedIndex !== dropIndex) {
//     const [moved] = templateFields.splice(draggedIndex, 1);
//     const ni = dropIndex > draggedIndex ? dropIndex - 1 : dropIndex;
//     templateFields.splice(ni >= 0 ? ni : 0, 0, moved);
//     selectedFieldIndex = ni >= 0 ? ni : 0;
//   }
//   draggedIndex = -1;
//   renderCanvas();
//   if (selectedFieldIndex >= 0) {
//     const el = document.querySelector(
//       `.field-item[data-index="${selectedFieldIndex}"]`,
//     );
//     if (el) el.classList.add("selected");
//   }
// }
// function handleDragEnd(e) {
//   const item = e.target.closest(".field-item");
//   if (item) item.style.opacity = "1";
//   document
//     .querySelectorAll(".field-item")
//     .forEach((el) => (el.style.borderTop = ""));
//   draggedIndex = -1;
// }

// // ═══════════════════════════════════════════
// // Select & Properties
// // ═══════════════════════════════════════════
// function selectField(index, event) {
//   if (event) {
//     event.stopPropagation();
//     event.preventDefault();
//   }
//   selectedFieldIndex = index;
//   document
//     .querySelectorAll(".field-item")
//     .forEach((el) => el.classList.remove("selected"));
//   const el = document.querySelector(`.field-item[data-index="${index}"]`);
//   if (el) el.classList.add("selected");
//   const field = templateFields[index];
//   if (!field) {
//     document.getElementById("propertiesPanel").style.display = "none";
//     return;
//   }
//   document.getElementById("propertiesPanel").style.display = "block";
//   document.getElementById("selectedFieldIndex").value = index;
//   document.getElementById("propName").value = field.name || "";
//   document.getElementById("propLabel").value = field.label || "";
//   document.getElementById("propPlaceholder").value = field.placeholder || "";
//   document.getElementById("propRequired").checked = field.required || false;
//   document.getElementById("optionsSection").style.display =
//     field.type === "select" ? "block" : "none";
//   if (field.type === "select") renderOptionsList(field.options || []);
// }

// function applyProperty(key, value) {
//   const index = parseInt(document.getElementById("selectedFieldIndex").value);
//   if (index >= 0 && templateFields[index]) {
//     templateFields[index][key] = value;
//     if (key === "label" || key === "placeholder") {
//       renderCanvas();
//       selectField(index);
//     }
//   }
// }

// // ═══════════════════════════════════════════
// // Delete with Modal Confirmation
// // ═══════════════════════════════════════════
// function deleteSelectedField() {
//   const index = parseInt(document.getElementById("selectedFieldIndex").value);
//   if (index >= 0) {
//     pendingDeleteIndex = index;
//     new bootstrap.Modal(document.getElementById("confirmDeleteModal")).show();
//   }
// }

// function removeField(index) {
//   pendingDeleteIndex = index;
//   new bootstrap.Modal(document.getElementById("confirmDeleteModal")).show();
// }

// document.addEventListener("DOMContentLoaded", () => {
//   const confirmBtn = document.getElementById("confirmDeleteBtn");
//   if (confirmBtn) {
//     confirmBtn.addEventListener("click", () => {
//       if (pendingDeleteIndex >= 0) {
//         templateFields.splice(pendingDeleteIndex, 1);
//         selectedFieldIndex =
//           templateFields.length > 0
//             ? Math.min(pendingDeleteIndex, templateFields.length - 1)
//             : -1;
//         if (selectedFieldIndex === -1)
//           document.getElementById("propertiesPanel").style.display = "none";
//         renderCanvas();
//         if (selectedFieldIndex >= 0) selectField(selectedFieldIndex);
//         pendingDeleteIndex = -1;
//         bootstrap.Modal.getInstance(
//           document.getElementById("confirmDeleteModal"),
//         ).hide();
//       }
//     });
//   }
// });

// // ═══════════════════════════════════════════
// // Options
// // ═══════════════════════════════════════════
// function addOption() {
//   const val = document.getElementById("newOption").value.trim();
//   if (!val) return;
//   const index = parseInt(document.getElementById("selectedFieldIndex").value);
//   if (index >= 0 && templateFields[index]) {
//     if (!templateFields[index].options) templateFields[index].options = [];
//     templateFields[index].options.push(val);
//     renderOptionsList(templateFields[index].options);
//     renderCanvas();
//     selectField(index);
//   }
//   document.getElementById("newOption").value = "";
// }
// function removeOption(i) {
//   const index = parseInt(document.getElementById("selectedFieldIndex").value);
//   if (index >= 0 && templateFields[index]) {
//     templateFields[index].options.splice(i, 1);
//     renderOptionsList(templateFields[index].options);
//     renderCanvas();
//     selectField(index);
//   }
// }
// function renderOptionsList(opts) {
//   document.getElementById("optionsList").innerHTML = (opts || [])
//     .map(
//       (o, i) =>
//         `<span class="option-chip">${o} <span class="remove-option" onclick="removeOption(${i})">&times;</span></span>`,
//     )
//     .join("");
// }

// // ═══════════════════════════════════════════
// // Render Canvas
// // ═══════════════════════════════════════════
// function renderCanvas() {
//   const canvas = document.getElementById("templateCanvas");
//   if (!canvas) return;
//   if (templateFields.length === 0) {
//     canvas.innerHTML = `<div class="canvas-empty"><i class="fas fa-arrow-left fa-3x mb-3" style="color:#ccc"></i><p>أضف حقولاً من القائمة الجانبية</p></div>`;
//     return;
//   }
//   canvas.innerHTML = templateFields.map((f, i) => renderField(f, i)).join("");
//   if (selectedFieldIndex >= 0 && selectedFieldIndex < templateFields.length) {
//     const el = canvas.querySelector(
//       `.field-item[data-index="${selectedFieldIndex}"]`,
//     );
//     if (el) el.classList.add("selected");
//   }
// }

// function renderField(field, index) {
//   const sel = index === selectedFieldIndex ? "selected" : "";
//   const drag = `draggable="true" ondragstart="handleDragStart(event,${index})" ondragover="handleDragOver(event)" ondrop="handleDrop(event,${index})" ondragend="handleDragEnd(event)"`;
//   const btns = `<button class="btn-action" onclick="event.stopPropagation();moveField(${index},-1)"><i class="fas fa-arrow-up"></i></button><button class="btn-action" onclick="event.stopPropagation();moveField(${index},1)"><i class="fas fa-arrow-down"></i></button><button class="btn-action danger" onclick="event.stopPropagation();removeField(${index})"><i class="fas fa-trash"></i></button>`;

//   // Label - hidden for checkbox (has its own label)
//   const isCheckbox = field.type === "checkbox";
//   const lbl = isCheckbox
//     ? ""
//     : `${field.label} ${field.required ? '<span class="text-danger">*</span>' : ""}`;
//   const labelHtml = isCheckbox
//     ? ""
//     : `<label class="fw-bold small mb-1 d-block">${lbl}</label>`;

//   // ═══ HEADING ═══
//   if (field.type === "heading")
//     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-heading"></i> عنوان قسم</span><div class="d-flex gap-1">${btns}</div></div><h5 style="color:#1a5276;margin:0">${field.label}</h5></div>`;

//   // ═══ DIVIDER ═══
//   if (field.type === "divider")
//     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-minus"></i> فاصل</span><div class="d-flex gap-1">${btns}</div></div><hr style="border-style:dashed;color:#ddd;margin:4px 0"></div>`;

//   // ═══ SUBHEADING ═══
//   if (field.type === "subheading")
//     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-heading"></i> عنوان فرعي</span><div class="d-flex gap-1">${btns}</div></div><h6 style="color:#2c3e50;margin:0">${field.label}</h6></div>`;

//   // ═══ SIGNATURE ═══
//   if (field.type === "signature")
//     return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-signature"></i> توقيع</span><div class="d-flex gap-1">${btns}</div></div><label class="fw-bold small mb-2 d-block">${field.label} ${field.required ? '<span class="text-danger">*</span>' : ""}</label><div style="border:1px dashed #ccc;border-radius:8px;padding:15px;text-align:center;color:#999"><i class="fas fa-signature fa-2x mb-2 d-block"></i><small>مكان توقيع الطبيب</small><div style="border-bottom:1px solid #ccc;width:60%;margin:10px auto 0"></div></div></div>`;

//   // ═══ FORM FIELDS ═══
//   let preview = "";
//   switch (field.type) {
//     case "text":
//       preview = `<input type="text" class="form-control form-control-sm" placeholder="${field.placeholder || "نص قصير"}" disabled>`;
//       break;
//     case "textarea":
//       preview = `<textarea class="form-control form-control-sm" rows="2" disabled></textarea>`;
//       break;
//     case "number":
//       preview = `<input type="number" class="form-control form-control-sm" disabled>`;
//       break;
//     case "date":
//       preview = `<input type="date" class="form-control form-control-sm" disabled>`;
//       break;
//     case "select":
//       preview = `<select class="form-select form-select-sm" disabled>${(field.options || []).map((o) => `<option>${o}</option>`).join("")}</select>`;
//       break;
//     case "checkbox":
//       preview = `<div class="form-check mb-0">
//         <input type="checkbox" class="form-check-input" disabled>
//         <label class="form-check-label small fw-bold">${field.label} ${field.required ? '<span class="text-danger">*</span>' : ""}</label>
//       </div>`;
//       break;
//     default:
//       preview = `<input type="text" class="form-control form-control-sm" disabled>`;
//   }

//   return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas ${TYPE_ICONS[field.type] || "fa-pen"}"></i> ${TYPE_LABELS[field.type] || field.type}</span><div class="d-flex gap-1">${btns}</div></div>${labelHtml}${preview}</div>`;
// }

// // ═══════════════════════════════════════════
// // Move
// // ═══════════════════════════════════════════
// function moveField(index, dir) {
//   const ni = index + dir;
//   if (ni < 0 || ni >= templateFields.length) return;
//   [templateFields[index], templateFields[ni]] = [
//     templateFields[ni],
//     templateFields[index],
//   ];
//   selectedFieldIndex = ni;
//   renderCanvas();
//   selectField(ni);
// }

// // ═══════════════════════════════════════════
// // Preview & Save
// // ═══════════════════════════════════════════
// function previewTemplate() {
//   let h = `<h4>${document.getElementById("templateTitle").value || "معاينة"}</h4><hr>`;
//   templateFields.forEach((f) => {
//     if (f.type === "heading")
//       h += `<h5 style="color:#1a5276;margin-top:16px">${f.label}</h5>`;
//     else if (f.type === "subheading")
//       h += `<h6 style="color:#2c3e50">${f.label}</h6>`;
//     else if (f.type === "divider") h += '<hr style="border-style:dashed">';
//     else if (f.type === "signature")
//       h += `<div style="border:1px dashed #ccc;border-radius:8px;padding:20px;text-align:center;color:#999;margin:10px 0"><i class="fas fa-signature fa-2x mb-2"></i><small>توقيع الطبيب</small></div>`;
//     else if (f.type === "checkbox")
//       h += `<div class="form-check mb-2"><input type="checkbox" disabled><label class="fw-bold">${f.label}${f.required ? '<span style="color:red">*</span>' : ""}</label></div>`;
//     else
//       h += `<div class="mb-2"><label class="fw-bold small">${f.label}${f.required ? '<span style="color:red">*</span>' : ""}</label><input class="form-control form-control-sm" disabled></div>`;
//   });
//   document.getElementById("previewContent").innerHTML = h;
//   new bootstrap.Modal(document.getElementById("previewModal")).show();
// }

// async function saveTemplate() {
//   const title = document.getElementById("templateTitle").value.trim();
//   if (!title) {
//     showNotification("أدخل اسم القالب", "error");
//     return;
//   }
//   if (!templateFields.length) {
//     showNotification("أضف حقلاً واحداً", "error");
//     return;
//   }
//   const data = {
//     title,
//     description: document.getElementById("templateDescription").value.trim(),
//     category: document.getElementById("templateCategory").value,
//     structure: templateFields,
//   };
//   const url = window.EDIT_TEMPLATE
//     ? `/api/templates/${window.EDIT_TEMPLATE.id}`
//     : "/api/templates";
//   try {
//     const r = await fetch(url, {
//       method: window.EDIT_TEMPLATE ? "PUT" : "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(data),
//     });
//     const j = await r.json();
//     if (j.success) {
//       showNotification("تم الحفظ", "success");
//       setTimeout(() => (location.href = "/reports"), 800);
//     } else showNotification(j.error || "فشل", "error");
//   } catch (e) {
//     showNotification("خطأ اتصال", "error");
//   }
// }

// document.addEventListener("keydown", (e) => {
//   if (e.ctrlKey && e.key === "s") {
//     e.preventDefault();
//     saveTemplate();
//   }
//   if (e.key === "Delete" && selectedFieldIndex >= 0) {
//     e.preventDefault();
//     removeField(selectedFieldIndex);
//   }
// });

/* ================================================
   template_builder.js - Final Version with Exit Confirm
   ================================================ */

let templateFields = [];
let fieldCounter = 0;
let selectedFieldIndex = -1;
let draggedIndex = -1;
let pendingDeleteIndex = -1;
let hasChanges = false; // ✅ تتبع التغييرات

// ═══════════════════════════════════════════
// Load existing template if editing
// ═══════════════════════════════════════════
if (window.EDIT_TEMPLATE) {
  const structure = window.EDIT_TEMPLATE.structure || [];
  templateFields = JSON.parse(JSON.stringify(structure));
  fieldCounter = templateFields.length;
  document.getElementById("templateTitle").value =
    window.EDIT_TEMPLATE.title || "";
  document.getElementById("templateDescription").value =
    window.EDIT_TEMPLATE.description || "";
  document.getElementById("templateCategory").value =
    window.EDIT_TEMPLATE.category || "general";
  setTimeout(() => renderCanvas(), 100);
}

// ═══════════════════════════════════════════
// Track Changes
// ═══════════════════════════════════════════
function markChanged() {
  hasChanges = true;
}

// ═══════════════════════════════════════════
// Confirm Exit (عودة بدون حفظ)
// ═══════════════════════════════════════════
function confirmExit() {
  // Check if there are unsaved changes
  const title = document.getElementById("templateTitle").value.trim();
  const desc = document.getElementById("templateDescription").value.trim();
  const cat = document.getElementById("templateCategory").value;

  const hasData = title || desc || templateFields.length > 0;

  if (hasData && hasChanges) {
    // Show modal
    new bootstrap.Modal(document.getElementById("confirmExitModal")).show();
    return false;
  }

  // No changes or empty - go back directly
  return true;
}

document.getElementById("confirmExitBtn").addEventListener("click", () => {
  window.location.href = "/reports";
});

// ═══════════════════════════════════════════
// 10 Types
// ═══════════════════════════════════════════
const TYPE_LABELS = {
  text: "نص قصير",
  textarea: "نص طويل",
  number: "رقم",
  date: "تاريخ",
  select: "قائمة منسدلة",
  checkbox: "مربع اختيار",
  heading: "عنوان قسم",
  subheading: "عنوان فرعي",
  divider: "فاصل",
  signature: "توقيع الطبيب",
};

const TYPE_ICONS = {
  text: "fa-font",
  textarea: "fa-align-left",
  number: "fa-hashtag",
  date: "fa-calendar",
  select: "fa-list",
  checkbox: "fa-check-square",
  heading: "fa-heading",
  subheading: "fa-heading",
  divider: "fa-minus",
  signature: "fa-signature",
};

// ═══════════════════════════════════════════
// Add Field
// ═══════════════════════════════════════════
function addField(type) {
  fieldCounter++;
  let options = type === "select" ? ["خيار 1", "خيار 2"] : [];
  const field = {
    id: `field_${Date.now()}`,
    type: type,
    name: `${type}_${fieldCounter}`,
    label: TYPE_LABELS[type] || `حقل ${fieldCounter}`,
    placeholder: "",
    required: false,
    options: options,
  };
  templateFields.push(field);
  markChanged();
  selectField(templateFields.length - 1);
  renderCanvas();
}

// ═══════════════════════════════════════════
// Drag & Drop
// ═══════════════════════════════════════════
function handleDragStart(e, index) {
  draggedIndex = index;
  e.target.closest(".field-item").style.opacity = "0.4";
  e.dataTransfer.effectAllowed = "move";
}
function handleDragOver(e) {
  e.preventDefault();
}
function handleDrop(e, dropIndex) {
  e.preventDefault();
  e.stopPropagation();
  document
    .querySelectorAll(".field-item")
    .forEach((el) => (el.style.borderTop = ""));
  if (draggedIndex !== -1 && draggedIndex !== dropIndex) {
    const [moved] = templateFields.splice(draggedIndex, 1);
    const ni = dropIndex > draggedIndex ? dropIndex - 1 : dropIndex;
    templateFields.splice(ni >= 0 ? ni : 0, 0, moved);
    selectedFieldIndex = ni >= 0 ? ni : 0;
    markChanged();
  }
  draggedIndex = -1;
  renderCanvas();
  if (selectedFieldIndex >= 0) {
    const el = document.querySelector(
      `.field-item[data-index="${selectedFieldIndex}"]`,
    );
    if (el) el.classList.add("selected");
  }
}
function handleDragEnd(e) {
  const item = e.target.closest(".field-item");
  if (item) item.style.opacity = "1";
  document
    .querySelectorAll(".field-item")
    .forEach((el) => (el.style.borderTop = ""));
  draggedIndex = -1;
}

// ═══════════════════════════════════════════
// Select & Properties
// ═══════════════════════════════════════════
function selectField(index, event) {
  if (event) {
    event.stopPropagation();
    event.preventDefault();
  }
  selectedFieldIndex = index;
  document
    .querySelectorAll(".field-item")
    .forEach((el) => el.classList.remove("selected"));
  const el = document.querySelector(`.field-item[data-index="${index}"]`);
  if (el) el.classList.add("selected");
  const field = templateFields[index];
  if (!field) {
    document.getElementById("propertiesPanel").style.display = "none";
    return;
  }
  document.getElementById("propertiesPanel").style.display = "block";
  document.getElementById("selectedFieldIndex").value = index;
  document.getElementById("propName").value = field.name || "";
  document.getElementById("propLabel").value = field.label || "";
  document.getElementById("propPlaceholder").value = field.placeholder || "";
  document.getElementById("propRequired").checked = field.required || false;
  document.getElementById("optionsSection").style.display =
    field.type === "select" ? "block" : "none";
  if (field.type === "select") renderOptionsList(field.options || []);
}

function applyProperty(key, value) {
  const index = parseInt(document.getElementById("selectedFieldIndex").value);
  if (index >= 0 && templateFields[index]) {
    templateFields[index][key] = value;
    markChanged();
    if (key === "label" || key === "placeholder") {
      renderCanvas();
      selectField(index);
    }
  }
}

// ═══════════════════════════════════════════
// Delete with Modal
// ═══════════════════════════════════════════
function deleteSelectedField() {
  const index = parseInt(document.getElementById("selectedFieldIndex").value);
  if (index >= 0) {
    pendingDeleteIndex = index;
    new bootstrap.Modal(document.getElementById("confirmDeleteModal")).show();
  }
}
function removeField(index) {
  pendingDeleteIndex = index;
  new bootstrap.Modal(document.getElementById("confirmDeleteModal")).show();
}

document.addEventListener("DOMContentLoaded", () => {
  const confirmBtn = document.getElementById("confirmDeleteBtn");
  if (confirmBtn) {
    confirmBtn.addEventListener("click", () => {
      if (pendingDeleteIndex >= 0) {
        templateFields.splice(pendingDeleteIndex, 1);
        markChanged();
        selectedFieldIndex =
          templateFields.length > 0
            ? Math.min(pendingDeleteIndex, templateFields.length - 1)
            : -1;
        if (selectedFieldIndex === -1)
          document.getElementById("propertiesPanel").style.display = "none";
        renderCanvas();
        if (selectedFieldIndex >= 0) selectField(selectedFieldIndex);
        pendingDeleteIndex = -1;
        bootstrap.Modal.getInstance(
          document.getElementById("confirmDeleteModal"),
        ).hide();
      }
    });
  }
});

// ═══════════════════════════════════════════
// Options
// ═══════════════════════════════════════════
function addOption() {
  const val = document.getElementById("newOption").value.trim();
  if (!val) return;
  const index = parseInt(document.getElementById("selectedFieldIndex").value);
  if (index >= 0 && templateFields[index]) {
    if (!templateFields[index].options) templateFields[index].options = [];
    templateFields[index].options.push(val);
    markChanged();
    renderOptionsList(templateFields[index].options);
    renderCanvas();
    selectField(index);
  }
  document.getElementById("newOption").value = "";
}
function removeOption(i) {
  const index = parseInt(document.getElementById("selectedFieldIndex").value);
  if (index >= 0 && templateFields[index]) {
    templateFields[index].options.splice(i, 1);
    markChanged();
    renderOptionsList(templateFields[index].options);
    renderCanvas();
    selectField(index);
  }
}
function renderOptionsList(opts) {
  document.getElementById("optionsList").innerHTML = (opts || [])
    .map(
      (o, i) =>
        `<span class="option-chip">${o} <span class="remove-option" onclick="removeOption(${i})">&times;</span></span>`,
    )
    .join("");
}

// ═══════════════════════════════════════════
// Render Canvas
// ═══════════════════════════════════════════
function renderCanvas() {
  const canvas = document.getElementById("templateCanvas");
  if (!canvas) return;
  if (templateFields.length === 0) {
    canvas.innerHTML = `<div class="canvas-empty"><i class="fas fa-arrow-left fa-3x mb-3" style="color:#ccc"></i><p>أضف حقولاً من القائمة الجانبية</p></div>`;
    return;
  }
  canvas.innerHTML = templateFields.map((f, i) => renderField(f, i)).join("");
  if (selectedFieldIndex >= 0 && selectedFieldIndex < templateFields.length) {
    const el = canvas.querySelector(
      `.field-item[data-index="${selectedFieldIndex}"]`,
    );
    if (el) el.classList.add("selected");
  }
}

function renderField(field, index) {
  const sel = index === selectedFieldIndex ? "selected" : "";
  const drag = `draggable="true" ondragstart="handleDragStart(event,${index})" ondragover="handleDragOver(event)" ondrop="handleDrop(event,${index})" ondragend="handleDragEnd(event)"`;
  const btns = `<button class="btn-action" onclick="event.stopPropagation();moveField(${index},-1)"><i class="fas fa-arrow-up"></i></button><button class="btn-action" onclick="event.stopPropagation();moveField(${index},1)"><i class="fas fa-arrow-down"></i></button><button class="btn-action danger" onclick="event.stopPropagation();removeField(${index})"><i class="fas fa-trash"></i></button>`;
  const isCheckbox = field.type === "checkbox";
  const lbl = isCheckbox
    ? ""
    : `${field.label} ${field.required ? '<span class="text-danger">*</span>' : ""}`;
  const labelHtml = isCheckbox
    ? ""
    : `<label class="fw-bold small mb-1 d-block">${lbl}</label>`;

  if (field.type === "heading")
    return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-heading"></i> عنوان قسم</span><div class="d-flex gap-1">${btns}</div></div><h5 style="color:#1a5276;margin:0">${field.label}</h5></div>`;
  if (field.type === "divider")
    return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-minus"></i> فاصل</span><div class="d-flex gap-1">${btns}</div></div><hr style="border-style:dashed;color:#ddd;margin:4px 0"></div>`;
  if (field.type === "subheading")
    return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-heading"></i> عنوان فرعي</span><div class="d-flex gap-1">${btns}</div></div><h6 style="color:#2c3e50;margin:0">${field.label}</h6></div>`;
  if (field.type === "signature")
    return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas fa-signature"></i> توقيع</span><div class="d-flex gap-1">${btns}</div></div><label class="fw-bold small mb-2 d-block">${field.label} ${field.required ? '<span class="text-danger">*</span>' : ""}</label><div style="border:1px dashed #ccc;border-radius:8px;padding:15px;text-align:center;color:#999"><i class="fas fa-signature fa-2x mb-2 d-block"></i><small>مكان توقيع الطبيب</small><div style="border-bottom:1px solid #ccc;width:60%;margin:10px auto 0"></div></div></div>`;

  let preview = "";
  switch (field.type) {
    case "text":
      preview = `<input type="text" class="form-control form-control-sm" placeholder="${field.placeholder || "نص قصير"}" disabled>`;
      break;
    case "textarea":
      preview = `<textarea class="form-control form-control-sm" rows="2" disabled></textarea>`;
      break;
    case "number":
      preview = `<input type="number" class="form-control form-control-sm" disabled>`;
      break;
    case "date":
      preview = `<input type="date" class="form-control form-control-sm" disabled>`;
      break;
    case "select":
      preview = `<select class="form-select form-select-sm" disabled>${(field.options || []).map((o) => `<option>${o}</option>`).join("")}</select>`;
      break;
    case "checkbox":
      preview = `<div class="form-check mb-0"><input type="checkbox" class="form-check-input" disabled><label class="form-check-label small fw-bold">${field.label} ${field.required ? '<span class="text-danger">*</span>' : ""}</label></div>`;
      break;
    default:
      preview = `<input type="text" class="form-control form-control-sm" disabled>`;
  }
  return `<div class="field-item ${sel}" data-index="${index}" ${drag} onclick="selectField(${index},event)"><div class="drag-handle">⋮⋮</div><div class="field-header"><span class="field-type-badge"><i class="fas ${TYPE_ICONS[field.type] || "fa-pen"}"></i> ${TYPE_LABELS[field.type] || field.type}</span><div class="d-flex gap-1">${btns}</div></div>${labelHtml}${preview}</div>`;
}

// ═══════════════════════════════════════════
// Move
// ═══════════════════════════════════════════
function moveField(index, dir) {
  const ni = index + dir;
  if (ni < 0 || ni >= templateFields.length) return;
  [templateFields[index], templateFields[ni]] = [
    templateFields[ni],
    templateFields[index],
  ];
  selectedFieldIndex = ni;
  renderCanvas();
  selectField(ni);
}

// ═══════════════════════════════════════════
// Preview & Save
// ═══════════════════════════════════════════
function previewTemplate() {
  let h = `<h4>${document.getElementById("templateTitle").value || "معاينة"}</h4><hr>`;
  templateFields.forEach((f) => {
    if (f.type === "heading")
      h += `<h5 style="color:#1a5276;margin-top:16px">${f.label}</h5>`;
    else if (f.type === "subheading")
      h += `<h6 style="color:#2c3e50">${f.label}</h6>`;
    else if (f.type === "divider") h += '<hr style="border-style:dashed">';
    else if (f.type === "signature")
      h += `<div style="border:1px dashed #ccc;border-radius:8px;padding:20px;text-align:center;color:#999;margin:10px 0"><i class="fas fa-signature fa-2x mb-2"></i><small>توقيع الطبيب</small></div>`;
    else if (f.type === "checkbox")
      h += `<div class="form-check mb-2"><input type="checkbox" disabled><label class="fw-bold">${f.label}${f.required ? '<span style="color:red">*</span>' : ""}</label></div>`;
    else
      h += `<div class="mb-2"><label class="fw-bold small">${f.label}${f.required ? '<span style="color:red">*</span>' : ""}</label><input class="form-control form-control-sm" disabled></div>`;
  });
  document.getElementById("previewContent").innerHTML = h;
  new bootstrap.Modal(document.getElementById("previewModal")).show();
}

async function saveTemplate() {
  const title = document.getElementById("templateTitle").value.trim();
  if (!title) {
    showNotification("أدخل اسم القالب", "error");
    return;
  }
  if (!templateFields.length) {
    showNotification("أضف حقلاً واحداً", "error");
    return;
  }
  const data = {
    title,
    description: document.getElementById("templateDescription").value.trim(),
    category: document.getElementById("templateCategory").value,
    structure: templateFields,
  };
  const url = window.EDIT_TEMPLATE
    ? `/api/templates/${window.EDIT_TEMPLATE.id}`
    : "/api/templates";
  try {
    const r = await fetch(url, {
      method: window.EDIT_TEMPLATE ? "PUT" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const j = await r.json();
    if (j.success) {
      hasChanges = false; // ✅ إعادة تعيين
      showNotification("تم الحفظ", "success");
      setTimeout(() => (location.href = "/reports"), 800);
    } else showNotification(j.error || "فشل", "error");
  } catch (e) {
    showNotification("خطأ اتصال", "error");
  }
}

document.addEventListener("keydown", (e) => {
  if (e.ctrlKey && e.key === "s") {
    e.preventDefault();
    saveTemplate();
  }
  if (e.key === "Delete" && selectedFieldIndex >= 0) {
    e.preventDefault();
    removeField(selectedFieldIndex);
  }
});
