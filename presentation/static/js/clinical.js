// static/js/clinical.js
// ============================================
// كود صفحة البيانات السريرية - منفصل عن HTML
// ============================================

(function () {
  "use strict";

  // ============================================
  // ✅ تهيئة الصفحة
  // ============================================
  function initClinicalPage() {
    console.log("📊 Clinical Data page loaded successfully");

    // إضافة تأثيرات تفاعلية للبطاقات
    const methodCards = document.querySelectorAll(".method-card");

    methodCards.forEach((card) => {
      // تأثير hover
      card.addEventListener("mouseenter", function () {
        const icon = this.querySelector(".method-icon");
        if (icon) {
          icon.style.transform = "scale(1.1) rotate(-5deg)";
        }
      });

      card.addEventListener("mouseleave", function () {
        const icon = this.querySelector(".method-icon");
        if (icon) {
          icon.style.transform = "scale(1) rotate(0deg)";
        }
      });

      // تأثير النقر
      card.addEventListener("click", function () {
        this.style.transform = "scale(0.98)";
        setTimeout(() => {
          this.style.transform = "";
        }, 200);
      });
    });

    // عرض إشعار ترحيبي
    setTimeout(() => {
      showNotification("👋 مرحباً! اختر طريقة إدخال البيانات المناسبة", "info");
    }, 1000);

    // التحقق من صحة الخادم
    checkServerHealth();
  }

  // ============================================
  // ✅ التحقق من صحة الخادم
  // ============================================
  async function checkServerHealth() {
    try {
      const response = await fetch("/api/health");
      if (response.ok) {
        console.log("✅ Server is healthy");
      } else {
        console.warn("⚠️ Server responded with status:", response.status);
        showNotification(
          "تنبيه: الخادم يعمل ولكن قد يكون هناك تأخير",
          "warning",
        );
      }
    } catch (error) {
      console.warn("⚠️ Server connection issue:", error.message);
      showNotification("تنبيه: مشكلة في الاتصال بالخادم", "warning");
    }
  }

  // ============================================
  // ✅ دالة التنقل الآمن
  // ============================================
  window.navigateTo = function (url, options = {}) {
    try {
      if (options.confirm && !confirm(options.confirm)) {
        return;
      }
      window.location.href = url;
    } catch (error) {
      console.error("Navigation error:", error);
      showNotification("حدث خطأ أثناء التنقل", "error");
    }
  };

  // ============================================
  // ✅ تهيئة عند تحميل الصفحة
  // ============================================
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initClinicalPage);
  } else {
    initClinicalPage();
  }

  // تصدير الدوال للاستخدام في HTML
  window.checkServerHealth = checkServerHealth;
})();
