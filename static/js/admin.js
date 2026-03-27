(function() {
  const saveBtn = document.getElementById('saveAdmin');
  if (!saveBtn) return;
  saveBtn.addEventListener('click', () => {
    alert('Thresholds and weights saved (demo).');
  });
})();
