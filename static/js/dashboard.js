const humanizeLabel = (str) => (str || '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

(async function() {
  const canvas = document.getElementById('cdiChart');
  if (!canvas) return;
  const wardId = 1;
  const bench = await fetch(`/api/benchmarks/${wardId}`).then(r => r.json());
  const labels = bench.kpis.map(k => humanizeLabel(k.metric));
  const deficits = bench.kpis.map(k => k.deficit);
  new Chart(canvas.getContext('2d'), {
    type: 'bar',
    data: { labels, datasets: [{ label: 'Deficit', data: deficits, backgroundColor: '#4f46e5' }]},
    options: { scales: { y: { min: 0, max: 1 } } }
  });

  const kpiMap = {
    hospitals_per_10k: { el: 'kpi-hosp', trend: 'kpi-hosp-trend' },
    schools_per_1k_children: { el: 'kpi-sch', trend: 'kpi-sch-trend' },
    green_cover_pct: { el: 'kpi-green', trend: 'kpi-green-trend' },
    road_density_km_per_sqkm: { el: 'kpi-road', trend: 'kpi-road-trend' },
  };
  bench.kpis.forEach(k => {
    const entry = kpiMap[k.metric];
    if (!entry) return;
    document.getElementById(entry.el).textContent = k.value;
    document.getElementById(entry.trend).textContent = `${k.deficit > 0 ? '↓' : '↑'} ${(k.deficit*100).toFixed(1)}%`;
    document.getElementById(entry.trend).className = `kpi-trend ${k.deficit > 0 ? 'down' : 'up'}`;
  });

  const alerts = document.getElementById('alertList');
  if (alerts) {
    alerts.innerHTML = `
      <div class="alert-item">Ward D: Healthcare deficit high</div>
      <div class="alert-item">Ward K/E: Road connectivity poor</div>
      <div class="alert-item">Green cover below target in 60% area</div>
    `;
  }
})();
