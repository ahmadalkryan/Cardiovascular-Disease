// static/js/dashboard.js
// ============================================
// كود لوحة التحكم - منفصل عن HTML
// ============================================

(function () {
  "use strict";

  // ============================================
  // تكوين النماذج
  // ============================================
  const MODEL_CONFIG = {
    minimal: {
      name: "النموذج المبسط",
      color: "#3498db",
      icon: "⚡",
      features: "4 ميزات",
      algo: "Logistic Regression",
    },
    top8: {
      name: "النموذج المتوسط",
      color: "#f39c12",
      icon: "⭐",
      features: "8 ميزات",
      algo: "Random Forest",
    },
    all11: {
      name: "النموذج الشامل",
      color: "#9b59b6",
      icon: "🏆",
      features: "11 ميزة",
      algo: "KNN",
    },
  };

  // ============================================
  // كلاس Dashboard
  // ============================================
  class Dashboard {
    constructor() {
      this.statusChart = null;
      this.modelChart = null;
      this.isLoading = false;
      this.autoRefreshInterval = null;

      this.elements = {
        totalPatients: document.getElementById("totalPatients"),
        diseaseCount: document.getElementById("diseaseCount"),
        healthyCount: document.getElementById("healthyCount"),
        avgProbability: document.getElementById("avgProbability"),
        recentTableBody: document.getElementById("recentTableBody"),
        statusChart: document.getElementById("statusChart"),
        modelChart: document.getElementById("modelChart"),
        refreshBtn: document.querySelector(".refresh-btn"),
      };

      this.init();
    }

    init() {
      // ربط أحداث التحديث
      if (this.elements.refreshBtn) {
        this.elements.refreshBtn.addEventListener("click", () => this.load());
      }

      // تحميل البيانات
      setTimeout(() => this.load(), 500);

      // تحديث تلقائي كل 30 ثانية
      this.autoRefreshInterval = setInterval(() => this.load(), 30000);

      // إيقاف التحديث عند مغادرة الصفحة
      window.addEventListener("beforeunload", () => {
        if (this.autoRefreshInterval) {
          clearInterval(this.autoRefreshInterval);
        }
      });

      console.log("📊 Dashboard initialized");
    }

    // ============================================
    // تحميل البيانات
    // ============================================
    async load() {
      if (this.isLoading) return;
      this.isLoading = true;

      try {
        this._showLoading();

        const response = await fetch("/api/statistics");
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
          this._updateStats(data.statistics);
          this._updateCharts(data.statistics);
          this._updateRecent(data.statistics);
          showNotification("تم تحديث البيانات بنجاح", "success");
        } else {
          throw new Error(data.error || "فشل تحميل البيانات");
        }
      } catch (error) {
        console.error("Error loading dashboard:", error);
        this._showError(error.message);
        showNotification("خطأ في تحميل البيانات", "error");
      } finally {
        this.isLoading = false;
      }
    }

    // ============================================
    // عرض حالة التحميل
    // ============================================
    _showLoading() {
      const loadingHTML = '<div class="loading-spinner"></div>';
      this.elements.totalPatients.innerHTML = loadingHTML;
      this.elements.diseaseCount.innerHTML = loadingHTML;
      this.elements.healthyCount.innerHTML = loadingHTML;
      this.elements.avgProbability.innerHTML = loadingHTML;
    }

    // ============================================
    // تحديث الإحصائيات
    // ============================================
    _updateStats(stats) {
      this.elements.totalPatients.textContent = stats.total || 0;
      this.elements.diseaseCount.textContent = stats.disease || 0;
      this.elements.healthyCount.textContent = stats.healthy || 0;
      this.elements.avgProbability.textContent =
        (stats.avg_probability || 0).toFixed(1) + "%";
    }

    // ============================================
    // تحديث الرسوم البيانية
    // ============================================
    _updateCharts(stats) {
      // رسم بياني للحالات
      this._updateStatusChart(stats);

      // رسم بياني للنماذج
      this._updateModelChart(stats);
    }

    _updateStatusChart(stats) {
      const ctx = this.elements.statusChart?.getContext("2d");
      if (!ctx) return;

      if (this.statusChart) {
        this.statusChart.destroy();
      }

      const disease = stats.disease || 0;
      const healthy = stats.healthy || 0;
      const total = disease + healthy;

      this.statusChart = new Chart(ctx, {
        type: "pie",
        data: {
          labels: [`مرضى (${disease})`, `أصحاء (${healthy})`],
          datasets: [
            {
              data: [disease, healthy],
              backgroundColor: ["#e74c3c", "#2ecc71"],
              borderWidth: 0,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: { position: "bottom" },
            tooltip: {
              callbacks: {
                label: function (context) {
                  const percentage =
                    total > 0 ? ((context.raw / total) * 100).toFixed(1) : 0;
                  return `${context.label}: ${context.raw} (${percentage}%)`;
                },
              },
            },
          },
        },
      });
    }

    _updateModelChart(stats) {
      const ctx = this.elements.modelChart?.getContext("2d");
      if (!ctx) return;

      if (this.modelChart) {
        this.modelChart.destroy();
      }

      const byModel = stats.by_model || {};
      const labels = Object.keys(byModel).map(
        (key) => MODEL_CONFIG[key]?.name || key,
      );
      const data = Object.values(byModel);
      const colors = Object.keys(byModel).map(
        (key) => MODEL_CONFIG[key]?.color || "#667eea",
      );

      this.modelChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "عدد الحالات",
              data: data,
              backgroundColor: colors,
              borderRadius: 10,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: function (context) {
                  const modelKey = Object.keys(byModel)[context.dataIndex];
                  const config = MODEL_CONFIG[modelKey];
                  if (config) {
                    return `${context.raw} حالة (${config.features} - ${config.algo})`;
                  }
                  return `${context.raw} حالة`;
                },
              },
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              title: { display: true, text: "عدد الحالات" },
              ticks: { stepSize: 1 },
            },
          },
        },
      });
    }

    // ============================================
    // تحديث الجدول الأخير
    // ============================================
    _updateRecent(stats) {
      const tbody = this.elements.recentTableBody;

      if (stats.recent && stats.recent.length > 0) {
        tbody.innerHTML = stats.recent
          .map((p) => {
            const modelKey = p.model_used || "";
            const modelDisplay =
              MODEL_CONFIG[modelKey]?.name || modelKey || "-";
            const modelBadge = modelKey
              ? `<span class="model-badge model-${modelKey}">${modelDisplay}</span>`
              : "-";

            return `
            <tr>
              <td><code>${p.patient_id || "-"}</code></td>
              <td>${p.date || "-"}</td>
              <td>${p.time || "-"}</td>
              <td>
                <span class="badge ${p.prediction === 1 ? "bg-danger" : "bg-success"}">
                  ${p.result_ar || (p.prediction === 1 ? "مريض" : "سليم")}
                </span>
              </td>
              <td>${((p.probability || 0) * 100).toFixed(1)}%</td>
              <td>${modelBadge}</td>
            </tr>
          `;
          })
          .join("");
      } else {
        tbody.innerHTML =
          '<tr><td colspan="6" class="text-center text-muted">لا توجد بيانات بعد</td></tr>';
      }
    }

    // ============================================
    // عرض الخطأ
    // ============================================
    _showError(message) {
      const tbody = this.elements.recentTableBody;
      tbody.innerHTML = `
        <tr>
          <td colspan="6" class="text-center">
            <div class="error-message">
              <i class="fas fa-exclamation-triangle fa-2x mb-2 d-block"></i>
              <strong>خطأ في تحميل البيانات</strong>
              <p class="small mb-2">${message}</p>
              <button class="retry-btn" onclick="window.dashboard?.load()">
                <i class="fas fa-redo"></i> إعادة المحاولة
              </button>
            </div>
          </td>
        </tr>
      `;
    }
  }

  // ============================================
  // تهيئة الصفحة
  // ============================================
  document.addEventListener("DOMContentLoaded", function () {
    window.dashboard = new Dashboard();
    console.log("📊 Dashboard page loaded successfully");
  });
})();
