import { getJSON } from './utils.js';

export const Api = {
  wards: () => getJSON('/api/wards'),
  ward: (id) => getJSON(`/api/wards/${id}`),
  recommendations: (wardId) => getJSON(`/api/recommendations?ward_id=${wardId}`),
  benchmarks: (wardId) => getJSON(`/api/benchmarks/${wardId}`),
  simulate: (wardId, action) => fetch('/api/simulations/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ward_id: wardId, action })
  }).then(r => r.json()),
  validation: () => getJSON('/api/validation'),
};
