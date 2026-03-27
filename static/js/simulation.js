(function() {
  const form = document.getElementById('simPageForm');
  if (!form) return;
  const ctx = document.getElementById('simChart').getContext('2d');
  let chart;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const wardId = form.querySelector('#wardSelect').value;
      const action = form.querySelector('select[name="action"]').value;
      const res = await fetch('/api/simulations/run', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ward_id: Number(wardId), action })});
    const data = await res.json();
    const before = data.before.components;
    const after = data.after.components;
    document.getElementById('beforeHosp').textContent = `Hospital ratio: ${before.healthcare?.deficit.toFixed(2) ?? '-'}`;
    document.getElementById('afterHosp').textContent = `Hospital ratio: ${after.healthcare?.deficit.toFixed(2) ?? '-'}`;
    document.getElementById('beforeSchool').textContent = `School ratio: ${before.education?.deficit.toFixed(2) ?? '-'}`;
    document.getElementById('afterSchool').textContent = `School ratio: ${after.education?.deficit.toFixed(2) ?? '-'}`;
    document.getElementById('beforeGreen').textContent = `Green cover: ${before.green?.deficit.toFixed(2) ?? '-'}`;
    document.getElementById('afterGreen').textContent = `Green cover: ${after.green?.deficit.toFixed(2) ?? '-'}`;
    document.getElementById('simSummary').textContent = `Adding ${action.replace('_',' ')} improves CDI by ${data.cdi_delta}`;

    const labels = Object.keys(after);
    const beforeVals = labels.map(l => before[l]?.deficit ?? 0);
    const afterVals = labels.map(l => after[l]?.deficit ?? 0);
    if (chart) chart.destroy();
    chart = new Chart(ctx, {
      type: 'bar',
      data: { labels, datasets: [
        { label: 'Before', data: beforeVals, backgroundColor: '#cbd5e1' },
        { label: 'After', data: afterVals, backgroundColor: '#4f46e5' }
      ]},
      options: { scales: { y: { min: 0, max: 1 } } }
    });
  });
})();
