// static/js/app.js
// ============================================
// الدوال العامة للتطبيق - تستخدم في جميع الصفحات
// ============================================

(function() {
  'use strict';

  // ============================================
  // ✅ 1. إشعارات موحدة
  // ============================================
  window.showNotification = function(message, type = 'info', duration = 4000) {
    // استخدام Toast من base.html
    const toastElement = document.getElementById('notificationToast');
    if (!toastElement) {
      // Fallback: إنشاء إشعار مخصص
      createFallbackNotification(message, type, duration);
      return;
    }

    const toastBody = document.getElementById('toastMessage');
    const toastHeader = toastElement.querySelector('.toast-header');
    
    if (toastBody) toastBody.textContent = message;
    
    const colors = {
      success: '#2ecc71',
      error: '#e74c3c',
      warning: '#f39c12',
      info: '#667eea'
    };
    
    if (toastHeader) {
      toastHeader.style.background = colors[type] || colors.info;
      toastHeader.style.color = 'white';
      // إضافة أيقونة حسب النوع
      const icon = toastHeader.querySelector('i');
      if (icon) {
        icon.className = `fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'} me-2`;
      }
    }
    
    try {
      const toast = new bootstrap.Toast(toastElement, { delay: duration });
      toast.show();
    } catch (e) {
      console.warn('Toast failed, using fallback:', e);
      createFallbackNotification(message, type, duration);
    }
  };

  // ✅ Fallback للإشعارات (عند عدم وجود Bootstrap)
  function createFallbackNotification(message, type = 'info', duration = 4000) {
    const container = document.getElementById('notificationContainer') || (() => {
      const c = document.createElement('div');
      c.id = 'notificationContainer';
      c.style.cssText = `
        position: fixed; top: 20px; right: 20px; z-index: 9999;
        display: flex; flex-direction: column; gap: 10px;
      `;
      document.body.appendChild(c);
      return c;
    })();

    const colors = {
      success: '#2ecc71',
      error: '#e74c3c',
      warning: '#f39c12',
      info: '#3498db'
    };

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
      background: ${colors[type] || '#3498db'};
      color: white;
      padding: 15px 25px;
      border-radius: 10px;
      font-weight: 600;
      box-shadow: 0 5px 25px rgba(0,0,0,0.2);
      animation: slideIn 0.3s ease;
      min-width: 250px;
      max-width: 500px;
      direction: rtl;
    `;
    notification.textContent = message;

    // إضافة الأنيميشن إذا لم تكن موجودة
    if (!document.getElementById('notificationStyles')) {
      const style = document.createElement('style');
      style.id = 'notificationStyles';
      style.textContent = `
        @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
        .notification {
          animation: slideIn 0.3s ease;
        }
      `;
      document.head.appendChild(style);
    }

    container.appendChild(notification);

    setTimeout(() => {
      notification.style.opacity = '0';
      notification.style.transition = 'opacity 0.3s ease';
      setTimeout(() => notification.remove(), 300);
    }, duration);
  }

  // ============================================
  // ✅ 2. معالج الأخطاء المركزي
  // ============================================
  window.setupGlobalErrorHandler = function() {
    // التقاط الأخطاء غير المعالجة
    window.onerror = function(message, source, lineno, colno, error) {
      console.error('🔥 Global error caught:', {
        message,
        source,
        lineno,
        colno,
        error: error?.stack
      });
      
      // عرض إشعار للمستخدم
      showNotification('حدث خطأ غير متوقع. تم تسجيل المشكلة.', 'error');
      
      // إرسال الخطأ إلى الخادم (اختياري)
      if (window.sendErrorToServer) {
        window.sendErrorToServer({ message, source, lineno, colno, stack: error?.stack });
      }
      
      return true; // منع السلوك الافتراضي
    };

    // التقاط الوعود المرفوضة (Promise rejections)
    window.onunhandledrejection = function(event) {
      console.error('🔥 Unhandled Promise rejection:', event.reason);
      showNotification('حدث خطأ غير متوقع. تم تسجيل المشكلة.', 'error');
      
      if (window.sendErrorToServer) {
        window.sendErrorToServer({ 
          type: 'unhandled_rejection', 
          reason: event.reason?.toString() 
        });
      }
    };
  };

  // ============================================
  // ✅ 3. دالة إرسال الأخطاء إلى الخادم (اختيارية)
  // ============================================
  window.sendErrorToServer = function(errorData) {
    try {
      fetch('/api/log-error', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          timestamp: new Date().toISOString(),
          user_agent: navigator.userAgent,
          url: window.location.href,
          ...errorData
        })
      }).catch(() => { /* تجاهل أخطاء التسجيل */ });
    } catch (_) { /* تجاهل */ }
  };

  // ============================================
  // ✅ 4. دوال مساعدة للتنقل
  // ============================================
  window.navigateTo = function(url, options = {}) {
    try {
      if (options.confirm && !confirm(options.confirm)) {
        return;
      }
      window.location.href = url;
    } catch (error) {
      console.error('Navigation error:', error);
      showNotification('حدث خطأ أثناء التنقل', 'error');
    }
  };

  // ============================================
  // ✅ 5. تهيئة AOS (تأثيرات حركية)
  // ============================================
  window.initAOS = function() {
    if (typeof AOS !== 'undefined') {
      AOS.init({
        duration: 800,
        once: true,
        easing: 'ease-out'
      });
    }
  };

  // ============================================
  // ✅ 6. التحقق من اتصال الخادم
  // ============================================
  window.checkServerHealth = async function(showNotification = false) {
    try {
      const response = await fetch('/api/health', { 
        method: 'GET',
        headers: { 'Accept': 'application/json' },
        signal: AbortSignal.timeout(5000)
      });
      
      if (response.ok) {
        console.log('✅ Server is healthy');
        return { status: 'healthy', ok: true };
      } else {
        console.warn('⚠️ Server responded with status:', response.status);
        if (showNotification) {
          showNotification('تنبيه: الخادم يعمل ولكن قد يكون هناك تأخير', 'warning');
        }
        return { status: 'degraded', ok: false, statusCode: response.status };
      }
    } catch (error) {
      console.warn('⚠️ Server connection issue:', error.message);
      if (showNotification) {
        showNotification('تنبيه: مشكلة في الاتصال بالخادم', 'warning');
      }
      return { status: 'unreachable', ok: false, error: error.message };
    }
  };

  // ============================================
  // ✅ 7. تهيئة الصفحة
  // ============================================
  document.addEventListener('DOMContentLoaded', function() {
    // تهيئة AOS
    initAOS();
    
    // إعداد معالج الأخطاء
    setupGlobalErrorHandler();
    
    console.log('✅ App initialized successfully');
    console.log(`📍 ${window.location.pathname}`);
  });

})();