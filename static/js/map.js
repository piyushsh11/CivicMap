// Plain script (non-module) to avoid import issues
(async function() {
  try {
    const humanizeLabel = (str) => (str || '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    const mapEl = document.getElementById('map');
    if (!mapEl) return;

    const map = L.map('map').setView([19.08, 72.85], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OSM contributors' }).addTo(map);

    const res = await fetch('/api/wards');
    const geo = await res.json();
    L.geoJSON(geo, {
      style: f => ({
        color: '#fff',
        weight: 1.2,
        fillOpacity: 0.55,
        fillColor: colorByDeficit(f.properties.deficit || Math.random())
      }),
      onEachFeature: (feature, layer) => layer.on('click', () => selectWard(feature, layer))
    }).addTo(map);

    function colorByDeficit(d) {
      if (d > 0.6) return '#ef4444';
      if (d > 0.3) return '#f59e0b';
      return '#10b981';
    }

    function formatKpis(kpis) {
      return kpis.map(k => `<div class="kpi"><strong>${humanizeLabel(k.metric)}</strong>: ${k.value} (target ${k.target})</div>`).join('');
    }

    async function selectWard(feature, layer) {
      const wardId = feature.properties.id;
      const detail = await fetch(`/api/wards/${wardId}`).then(r => r.json());
      document.getElementById('wardInfo').innerHTML = `
        <h4>${feature.properties.name}</h4>
        <div>Population: ${feature.properties.population || '-'}</div>
        <div>${formatKpis(detail.kpis)}</div>
        <div class="small">CDI: ${detail.cdi.cdi}</div>`;
      const recList = document.getElementById('recList');
      recList.innerHTML = detail.recommendations.slice(0,3).map(r => `<div class="list-item"><div><div class="badge">${r.category}</div><strong>${r.title}</strong><p>${r.reason_summary}</p></div><div class="pill ${r.urgency}">${r.urgency}</div></div>`).join('');
      map.fitBounds(layer.getBounds());
    }

    const legend = L.control({ position: 'bottomright' });
    legend.onAdd = function () {
      const div = L.DomUtil.create('div', 'card');
      div.innerHTML = '<strong>Deficit</strong><br><span class=\"dot\" style=\"background:#ef4444\"></span> High<br><span class=\"dot\" style=\"background:#f59e0b\"></span> Medium<br><span class=\"dot\" style=\"background:#10b981\"></span> Low';
      return div;
    };
    legend.addTo(map);
  } catch (err) {
    console.error('Map init error', err);
  }
})();
