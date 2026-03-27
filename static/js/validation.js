(function() {
  const gauge = document.getElementById('confidenceGauge');
  const bar = document.getElementById('accuracyBar');
  if (!gauge || !bar) return;
  fetch('/api/validation').then(r => r.json()).then(data => {
    new Chart(gauge.getContext('2d'), {
      type: 'doughnut',
      data: { labels: ['Confidence', 'Gap'], datasets: [{ data: [data.latest.confidence * 100, 100 - data.latest.confidence * 100], backgroundColor: ['#10b981', '#e2e8f0'] }]},
      options: { cutout: '70%' }
    });
    const labels = Object.keys(data.latest.discrepancies || {});
    const vals = labels.map(k => Math.abs(data.latest.discrepancies[k]) * 100);
    new Chart(bar.getContext('2d'), {
      type: 'bar',
      data: { labels, datasets: [{ label: 'Discrepancy %', data: vals, backgroundColor: '#ef4444' }]},
      options: { scales: { y: { min: 0, max: 20 } } }
    });
  });
})();
