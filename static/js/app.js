/**
 * CreatorIQ - Application Frontend Logic
 * Milestone 1: Theme Engine, Sidebar Navigation & Chart.js Visualizations
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeEngine();
  initMobileSidebar();
  initDashboardCharts();
});

/* ==========================================================================
   1. Theme Engine (Dark / Light Mode with LocalStorage Persistence)
   ========================================================================== */
function initThemeEngine() {
  const savedTheme = localStorage.getItem('creatoriq-theme') || 'dark';
  applyTheme(savedTheme, false);

  const themeToggleButtons = document.querySelectorAll('.theme-toggle-btn');
  themeToggleButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      applyTheme(newTheme, true);
    });
  });
}

function applyTheme(theme, updateCharts = true) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('creatoriq-theme', theme);

  // Update all toggle buttons on the page
  const toggleIcons = document.querySelectorAll('.theme-toggle-icon');
  toggleIcons.forEach((icon) => {
    if (theme === 'dark') {
      // Moon / Night indicator: show sun icon to prompt toggle to light
      icon.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="5"></circle>
          <line x1="12" y1="1" x2="12" y2="3"></line>
          <line x1="12" y1="21" x2="12" y2="23"></line>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
          <line x1="1" y1="12" x2="3" y2="12"></line>
          <line x1="21" y1="12" x2="23" y2="12"></line>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>`;
      icon.setAttribute('title', 'Switch to Light Mode');
    } else {
      // Sun indicator: show moon icon to prompt toggle to dark
      icon.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>`;
      icon.setAttribute('title', 'Switch to Dark Mode');
    }
  });

  if (updateCharts && window.creatorIQCharts) {
    updateChartsTheme(theme);
  }
}

/* ==========================================================================
   2. Responsive Mobile Sidebar Controller
   ========================================================================== */
function initMobileSidebar() {
  const sidebar = document.getElementById('dashboardSidebar');
  const toggleBtn = document.getElementById('mobileMenuToggle');
  const backdrop = document.getElementById('sidebarBackdrop');

  if (!sidebar || !toggleBtn) return;

  function openSidebar() {
    sidebar.classList.add('open');
    if (backdrop) backdrop.classList.add('active');
  }

  function closeSidebar() {
    sidebar.classList.remove('open');
    if (backdrop) backdrop.classList.remove('active');
  }

  toggleBtn.addEventListener('click', () => {
    if (sidebar.classList.contains('open')) {
      closeSidebar();
    } else {
      openSidebar();
    }
  });

  if (backdrop) {
    backdrop.addEventListener('click', closeSidebar);
  }
}

/* ==========================================================================
   3. Dashboard Visualizations (Chart.js Configuration)
   ========================================================================== */
window.creatorIQCharts = {};

function initDashboardCharts() {
  if (typeof Chart === 'undefined') return;

  const isDark = (document.documentElement.getAttribute('data-theme') || 'dark') === 'dark';
  const textColor = isDark ? '#94a3b8' : '#475569';
  const gridColor = isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.06)';

  // Chart Global Defaults
  Chart.defaults.font.family = "'Outfit', 'Inter', sans-serif";
  Chart.defaults.font.size = 12;

  // 1. Follower Growth Chart (Multi-Platform Line Chart)
  const followerCtx = document.getElementById('followerGrowthChart');
  if (followerCtx) {
    window.creatorIQCharts.follower = new Chart(followerCtx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [
          {
            label: 'YouTube Subscribers',
            data: [18200, 21400, 24800, 28100, 31900, 35400],
            borderColor: '#ff0000',
            backgroundColor: 'rgba(255, 0, 0, 0.08)',
            borderWidth: 2.5,
            fill: true,
            tension: 0.35,
            pointRadius: 3
          },
          {
            label: 'Instagram Followers',
            data: [12000, 14200, 16900, 19800, 22100, 24600],
            borderColor: '#e1306c',
            backgroundColor: 'rgba(225, 48, 108, 0.08)',
            borderWidth: 2.5,
            fill: true,
            tension: 0.35,
            pointRadius: 3
          },
          {
            label: 'LinkedIn Connections',
            data: [3500, 4200, 5100, 6400, 7800, 9200],
            borderColor: '#0a66c2',
            backgroundColor: 'rgba(10, 102, 194, 0.08)',
            borderWidth: 2.5,
            fill: true,
            tension: 0.35,
            pointRadius: 3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: { color: textColor, usePointStyle: true, boxWidth: 8 }
          },
          tooltip: {
            padding: 10,
            cornerRadius: 8
          }
        },
        scales: {
          x: {
            grid: { color: gridColor },
            ticks: { color: textColor }
          },
          y: {
            grid: { color: gridColor },
            ticks: { color: textColor }
          }
        }
      }
    });
  }

  // 2. Views Trend Chart (Bar Chart)
  const viewsCtx = document.getElementById('viewsTrendChart');
  if (viewsCtx) {
    window.creatorIQCharts.views = new Chart(viewsCtx, {
      type: 'bar',
      data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
        datasets: [
          {
            label: 'Weekly Video Views',
            data: [14200, 18900, 23500, 19400, 26800, 31200],
            backgroundColor: '#6366f1',
            borderRadius: 6,
            borderSkipped: false
          },
          {
            label: 'Shorts & Reels Reach',
            data: [9800, 13400, 17200, 15800, 21900, 24800],
            backgroundColor: '#06b6d4',
            borderRadius: 6,
            borderSkipped: false
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: { color: textColor, usePointStyle: true, boxWidth: 8 }
          }
        },
        scales: {
          x: {
            grid: { color: gridColor },
            ticks: { color: textColor }
          },
          y: {
            grid: { color: gridColor },
            ticks: { color: textColor }
          }
        }
      }
    });
  }

  // 3. Engagement Rate Chart (Line Area Chart)
  const engagementCtx = document.getElementById('engagementRateChart');
  if (engagementCtx) {
    window.creatorIQCharts.engagement = new Chart(engagementCtx, {
      type: 'line',
      data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
        datasets: [{
          label: 'Engagement Rate (%)',
          data: [6.8, 7.2, 7.9, 8.1, 8.4, 8.7],
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.15)',
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointBackgroundColor: '#10b981'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: textColor, usePointStyle: true }
          }
        },
        scales: {
          x: {
            grid: { color: gridColor },
            ticks: { color: textColor }
          },
          y: {
            grid: { color: gridColor },
            ticks: {
              color: textColor,
              callback: (value) => value + '%'
            }
          }
        }
      }
    });
  }

  // 4. Platform Performance Distribution (Doughnut Chart)
  const platformCtx = document.getElementById('platformPerformanceChart');
  if (platformCtx) {
    window.creatorIQCharts.platform = new Chart(platformCtx, {
      type: 'doughnut',
      data: {
        labels: ['YouTube', 'Instagram', 'LinkedIn'],
        datasets: [{
          data: [52, 34, 14],
          backgroundColor: ['#ff0000', '#e1306c', '#0a66c2'],
          borderWidth: 0,
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: textColor, usePointStyle: true, padding: 16 }
          }
        }
      }
    });
  }

  // 5. Top Performing Content (Horizontal Bar Chart)
  const topContentCtx = document.getElementById('topContentChart');
  if (topContentCtx) {
    window.creatorIQCharts.topContent = new Chart(topContentCtx, {
      type: 'bar',
      data: {
        labels: [
          'Full-Stack Flask Guide',
          'System Design in 10 Min',
          'How Creators Scale Monetization',
          'Top 10 Developer Tools 2026',
          'Instagram Growth Strategy'
        ],
        datasets: [{
          label: 'Total Views',
          data: [42100, 33400, 26800, 19200, 14500],
          backgroundColor: '#8b5cf6',
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            grid: { color: gridColor },
            ticks: { color: textColor }
          },
          y: {
            grid: { display: false },
            ticks: { color: textColor }
          }
        }
      }
    });
  }
}

function updateChartsTheme(theme) {
  const isDark = theme === 'dark';
  const textColor = isDark ? '#94a3b8' : '#475569';
  const gridColor = isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.06)';

  Object.values(window.creatorIQCharts).forEach((chart) => {
    if (!chart) return;

    if (chart.options.plugins && chart.options.plugins.legend) {
      chart.options.plugins.legend.labels.color = textColor;
    }

    if (chart.options.scales) {
      if (chart.options.scales.x) {
        chart.options.scales.x.ticks.color = textColor;
        if (chart.options.scales.x.grid) chart.options.scales.x.grid.color = gridColor;
      }
      if (chart.options.scales.y) {
        chart.options.scales.y.ticks.color = textColor;
        if (chart.options.scales.y.grid) chart.options.scales.y.grid.color = gridColor;
      }
    }

    chart.update();
  });
}
