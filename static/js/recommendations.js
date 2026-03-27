const humanizeLabel = (str) => (str || '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

(function() {
  const cards = document.getElementById('recCards');
  if (!cards) return;
  const urgencyFilter = document.getElementById('urgencyFilter');
  const costFilter = document.getElementById('costFilter');

  function applyFilters() {
    const u = urgencyFilter.value;
    const c = costFilter.value;
    cards.querySelectorAll('.rec-card').forEach(card => {
      const matchU = !u || card.dataset.urgency === u;
      const matchC = !c || card.dataset.cost === c;
      card.style.display = matchU && matchC ? '' : 'none';
    });
  }
  urgencyFilter.addEventListener('change', applyFilters);
  costFilter.addEventListener('change', applyFilters);

  cards.addEventListener('click', (e) => {
    if (e.target.classList.contains('view-map')) {
      const ward = e.target.dataset.ward;
      window.location.href = `/map?ward=${ward}`;
    }
    if (e.target.classList.contains('simulate')) {
      const ward = e.target.dataset.ward;
      const action = e.target.dataset.action;
      fetch('/api/simulations/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ward_id: Number(ward), action })
      }).then(r => r.json()).then(data => alert(`Simulated: CDI delta ${data.cdi_delta}`));
    }
  });

  // Humanize any reason text with underscores
  cards.querySelectorAll('.rec-card').forEach(card => {
    card.querySelectorAll('p').forEach(p => {
      p.textContent = p.textContent.replace(/_/g, ' ');
    });
  });
})();
