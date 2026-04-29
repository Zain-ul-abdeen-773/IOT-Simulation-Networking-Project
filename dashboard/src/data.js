function clamp(min, value, max) {
  return Math.max(min, Math.min(max, value));
}

export async function loadMqttReadyData() {
  const url = new URL("../data/mqtt_ready.json", import.meta.url);
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to load data: ${res.status} ${res.statusText}`);
  }

  const payload = await res.json();
  const rows = Array.isArray(payload) ? payload : payload.rows;
  if (!Array.isArray(rows)) {
    throw new Error("Invalid data format: expected payload.rows to be an array");
  }

  return { rows, meta: payload };
}

export function computeStats(values) {
  if (values.length === 0) {
    return { count: 0, min: 0, max: 0, mean: 0, std: 0 };
  }

  let min = Infinity;
  let max = -Infinity;
  let mean = 0;
  let m2 = 0;
  let count = 0;

  for (const v of values) {
    count += 1;
    if (v < min) min = v;
    if (v > max) max = v;

    const delta = v - mean;
    mean += delta / count;
    const delta2 = v - mean;
    m2 += delta * delta2;
  }

  const variance = count > 1 ? m2 / (count - 1) : 0;
  const std = Math.sqrt(variance);

  return { count, min, max, mean, std };
}

export function computeSummary(rows) {
  const latencies = rows.map((r) => Number(r.flowDuration)).filter((n) => Number.isFinite(n));
  const sizes = rows.map((r) => Number(r.packetSize)).filter((n) => Number.isFinite(n));
  const inter = rows.map((r) => Number(r.interArrival)).filter((n) => Number.isFinite(n));

  const latencyStats = computeStats(latencies);
  const sizeStats = computeStats(sizes);
  const interStats = computeStats(inter);

  // Useful for animation pacing; keep it in a stable range
  const interArrivalSpawnMs = clamp(70, (interStats.mean || 2500000) / 8000, 520);

  return {
    packetCount: rows.length,
    latencyStats,
    sizeStats,
    interStats,
    interArrivalSpawnMs,
  };
}

export function sampleRows(rows, maxPoints) {
  if (rows.length <= maxPoints) return rows;

  const step = Math.ceil(rows.length / maxPoints);
  const sampled = [];
  for (let i = 0; i < rows.length; i += step) {
    sampled.push(rows[i]);
  }
  return sampled;
}

export function histogram(values, binCount = 16) {
  if (values.length === 0) {
    return { labels: [], counts: [] };
  }

  let min = Infinity;
  let max = -Infinity;
  for (const v of values) {
    if (v < min) min = v;
    if (v > max) max = v;
  }

  if (min === max) {
    return { labels: [`${min.toFixed(2)}`], counts: [values.length] };
  }

  const bins = Array.from({ length: binCount }, () => 0);
  const width = (max - min) / binCount;

  for (const v of values) {
    const idx = Math.min(binCount - 1, Math.max(0, Math.floor((v - min) / width)));
    bins[idx] += 1;
  }

  const labels = bins.map((_, i) => {
    const a = min + i * width;
    const b = a + width;
    return `${a.toFixed(1)}–${b.toFixed(1)}`;
  });

  return { labels, counts: bins };
}
