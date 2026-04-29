import { computeSummary, loadMqttReadyData } from "./data.js";
import { createCharts } from "./charts.js";
import { createNetworkAnimation } from "./networkAnimation.js";

function $(id) {
  return document.getElementById(id);
}

function formatNumber(n, digits = 2) {
  if (!Number.isFinite(n)) return "—";
  return n.toFixed(digits);
}

function animateCounter(el, toValue, { suffix = "", durationMs = 900, digits = 2 } = {}) {
  const from = 0;
  const start = performance.now();

  function easeOutQuart(t) {
    return 1 - Math.pow(1 - t, 4);
  }

  function frame(now) {
    const t = Math.min(1, (now - start) / durationMs);
    const v = from + (toValue - from) * easeOutQuart(t);
    el.textContent = `${formatNumber(v, digits)}${suffix}`;
    if (t < 1) requestAnimationFrame(frame);
  }

  requestAnimationFrame(frame);
}

function setStatus(text) {
  const el = $("status");
  if (el) el.textContent = text;
}

async function main() {
  try {
    setStatus("Loading dashboard data…");

    const { rows, meta } = await loadMqttReadyData();
    const summary = computeSummary(rows);

    // KPIs
    $("kpiPackets").textContent = String(summary.packetCount);

    animateCounter($("kpiAvg"), summary.latencyStats.mean, { suffix: " s", digits: 2, durationMs: 1000 });
    $("kpiMinMax").textContent = `${formatNumber(summary.latencyStats.min, 2)} s / ${formatNumber(
      summary.latencyStats.max,
      2
    )} s`;
    animateCounter($("kpiStd"), summary.latencyStats.std, { suffix: " s", digits: 2, durationMs: 1000 });

    // Charts
    createCharts(rows);

    // Network animation
    const anim = createNetworkAnimation($("networkCanvas"), {
      rows,
      spawnEveryMs: summary.interArrivalSpawnMs,
    });
    anim.start();

    const gen = meta?.generatedAt ? ` • data: ${meta.generatedAt}` : "";
    setStatus(`Ready${gen}`);
  } catch (err) {
    console.error(err);
    setStatus("Failed to load data (see console)");
  }
}

main();
