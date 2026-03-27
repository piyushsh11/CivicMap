export async function getJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export function formatNumber(num) {
  return Intl.NumberFormat().format(num);
}

export function humanizeLabel(str) {
  if (!str) return "";
  return str
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

// expose for non-module scripts
window.CivicUtils = { humanizeLabel, getJSON, formatNumber };
