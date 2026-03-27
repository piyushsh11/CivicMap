const humanizeLabel = (str) => (str || '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

(function() {
  const ctx = document.getElementById('wardChart');
  if (ctx && window.WARD_KPIS) {
    new Chart(ctx.getContext('2d'), {
      type: 'radar',
      data: {
        labels: window.WARD_KPIS.map(k => humanizeLabel(k.metric)),
        datasets: [
          { label: 'Value', data: window.WARD_KPIS.map(k => k.value), borderColor: '#0f6ccf', fill: false },
          { label: 'Target', data: window.WARD_KPIS.map(k => k.target), borderColor: '#0ab68b', fill: false }
        ]
      },
      options: { responsive: true }
    });
  }

  const form = document.getElementById('simForm');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const wardId = form.querySelector('input[name="ward_id"]').value;
      const action = form.querySelector('select[name="action"]').value;
      const res = await fetch('/api/simulations/run', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ward_id: Number(wardId), action })});
      const data = await res.json();
      document.getElementById('simResult').innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    });
  }
})();
