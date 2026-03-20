// Tab switching
function switchTab(tab, el) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById('tab-analyze').classList.add('hidden');
  document.getElementById('tab-reports').classList.add('hidden');

  document.getElementById(`tab-${tab}`).classList.remove('hidden');
  el.classList.add('active');

  if (tab === 'reports') loadReports();
}

// Password visibility toggle
function togglePassword() {
  const input = document.getElementById('passwordInput');
  input.type = input.type === 'password' ? 'text' : 'password';
}

// Live password strength indicator
document.getElementById('passwordInput').addEventListener('input', function () {
  const pw = this.value;
  let score = 0;
  if (pw.length >= 8) score++;
  if (pw.length >= 12) score++;
  if (/[A-Z]/.test(pw)) score++;
  if (/[a-z]/.test(pw)) score++;
  if (/\d/.test(pw)) score++;
  if (/[!@#$%^&*(),.?":{}|<>]/.test(pw)) score++;

  const fill = document.getElementById('strengthFill');
  const label = document.getElementById('strengthLabel');
  const pct = Math.round((score / 6) * 100);
  fill.style.width = pct + '%';

  if (score <= 2) {
    fill.style.background = '#ef4444';
    label.textContent = 'Weak';
    label.style.color = '#ef4444';
  } else if (score <= 4) {
    fill.style.background = '#f59e0b';
    label.textContent = 'Moderate';
    label.style.color = '#f59e0b';
  } else {
    fill.style.background = '#22c55e';
    label.textContent = 'Strong';
    label.style.color = '#22c55e';
  }
});

// Form submit
document.getElementById('riskForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const btn = document.querySelector('.btn-analyze');
  btn.disabled = true;
  btn.textContent = 'Analyzing...';

  const fd = new FormData(this);
  const payload = {
    email: fd.get('email'),
    username: fd.get('username'),
    password: fd.get('password'),
    dob_public: fd.get('dob_public') === 'on',
    phone_public: fd.get('phone_public') === 'on',
    address_public: fd.get('address_public') === 'on',
    email_public: fd.get('email_public') === 'on',
    password_reuse: fd.get('password_reuse') === 'on',
    clicks_unknown: fd.get('clicks_unknown') === 'on',
    public_wifi: fd.get('public_wifi') === 'on',
  };

  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    alert('Error connecting to server. Make sure server.py is running.');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Analyze My Risk';
  }
});

function renderResults(data) {
  const resultsEl = document.getElementById('results');
  resultsEl.classList.remove('hidden');
  resultsEl.scrollIntoView({ behavior: 'smooth' });

  // Animated score counter
  animateCount('totalScore', data.total_score);

  // Circle arc (circumference = 326.7)
  const arc = document.getElementById('circleArc');
  const offset = 326.7 - (data.total_score / 100) * 326.7;
  arc.style.strokeDashoffset = offset;
  arc.style.stroke = data.risk_level === 'LOW' ? '#22c55e'
    : data.risk_level === 'MODERATE' ? '#f59e0b' : '#ef4444';

  // Risk badge
  const badge = document.getElementById('riskBadge');
  badge.textContent = `${data.risk_level} RISK ${data.risk_emoji}`;
  badge.className = 'risk-badge ' + (
    data.risk_level === 'LOW' ? 'risk-low'
    : data.risk_level === 'MODERATE' ? 'risk-moderate' : 'risk-high'
  );

  // Score bars
  setBar('password', data.password_risk, 25);
  setBar('email', data.email_risk, 15);
  setBar('username', data.username_risk, 15);
  setBar('privacy', data.privacy_risk, 15);
  setBar('behavior', data.behavior_risk, 10);
  setBar('breach', data.breach_risk, 20);

  // Recommendations
  const recSection = document.getElementById('recommendations');
  const recList = document.getElementById('recList');
  recList.innerHTML = '';
  if (data.recommendations && data.recommendations.length) {
    data.recommendations.forEach(r => {
      const li = document.createElement('li');
      li.textContent = r;
      recList.appendChild(li);
    });
    recSection.classList.remove('hidden');
  } else {
    recSection.classList.add('hidden');
  }
}

function setBar(key, value, max) {
  const pct = Math.round((value / max) * 100);
  const bar = document.getElementById(`bar-${key}`);
  const val = document.getElementById(`val-${key}`);
  bar.style.width = pct + '%';
  bar.style.background = pct < 40 ? '#22c55e' : pct < 70 ? '#f59e0b' : '#ef4444';
  val.textContent = `${value}/${max}`;
}

function animateCount(id, target) {
  const el = document.getElementById(id);
  let current = 0;
  const step = Math.ceil(target / 40);
  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = current;
    if (current >= target) clearInterval(timer);
  }, 25);
}

// Load previous reports
async function loadReports() {
  const container = document.getElementById('reportsList');
  container.innerHTML = '<p class="no-reports">Loading...</p>';
  try {
    const res = await fetch('/api/reports');
    const reports = await res.json();
    if (!reports.length) {
      container.innerHTML = '<p class="no-reports">No previous reports found.</p>';
      return;
    }
    container.innerHTML = reports.map(r => `
      <div class="report-card">
        <div class="report-header">
          <span class="report-ts">🕐 ${r.timestamp || 'Unknown time'}</span>
          <span class="report-score ${
            (r.risk_level || '').includes('LOW') ? 'risk-low'
            : (r.risk_level || '').includes('MODERATE') ? 'risk-moderate' : 'risk-high'
          }">${r.total_score || '?'}/100 — ${r.risk_level || ''}</span>
        </div>
        <div class="report-rows">
          <span>Password: ${r.password_risk || '-'}</span>
          <span>Email: ${r.email_risk || '-'}</span>
          <span>Username: ${r.username_risk || '-'}</span>
          <span>Privacy: ${r.privacy_risk || '-'}</span>
          <span>Behavior: ${r.behavior_risk || '-'}</span>
          <span>Breach: ${r.breach_risk || '-'}</span>
        </div>
      </div>
    `).join('');
  } catch {
    container.innerHTML = '<p class="no-reports">Failed to load reports.</p>';
  }
}
