import { histogram, sampleRows } from "./data.js";

function cssVar(name, fallback) {
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

function makeCommonOptions() {
  const grid = "rgba(255,255,255,0.08)";
  const ticks = "rgba(255,255,255,0.65)";

  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 900,
      easing: "easeOutQuart",
    },
    plugins: {
      legend: {
        labels: {
          color: ticks,
          boxWidth: 10,
        },
      },
      tooltip: {
        backgroundColor: "rgba(8, 12, 22, 0.92)",
        borderColor: "rgba(255,255,255,0.10)",
        borderWidth: 1,
        titleColor: "rgba(255,255,255,0.90)",
        bodyColor: "rgba(255,255,255,0.78)",
      },
    },
    scales: {
      x: {
        grid: { color: grid },
        ticks: { color: ticks, maxTicksLimit: 6 },
      },
      y: {
        grid: { color: grid },
        ticks: { color: ticks, maxTicksLimit: 6 },
      },
    },
  };
}

export function createCharts(rows) {
  const accent = cssVar("--accent", "#7c5cff");
  const accent2 = cssVar("--accent2", "#22d3ee");
  const good = cssVar("--good", "#34d399");

  // Latency over time (sampled)
  const series = sampleRows(rows, 280);
  const labels = series.map((r, i) => r.arrivalTimestamp || `#${i}`);
  const latency = series.map((r) => Number(r.flowDuration));

  const latencyCtx = document.getElementById("chartLatency");
  const latencyChart = new Chart(latencyCtx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Flow duration (latency)",
          data: latency,
          borderColor: accent2,
          backgroundColor: "rgba(34, 211, 238, 0.10)",
          fill: true,
          pointRadius: 0,
          borderWidth: 2,
          tension: 0.22,
        },
      ],
    },
    options: {
      ...makeCommonOptions(),
      scales: {
        x: {
          grid: { color: "rgba(255,255,255,0.06)" },
          ticks: {
            color: "rgba(255,255,255,0.65)",
            maxTicksLimit: 5,
            callback: (val) => {
              const s = labels[val] ?? "";
              return typeof s === "string" ? s.slice(11, 19) : s;
            },
          },
        },
        y: {
          grid: { color: "rgba(255,255,255,0.06)" },
          ticks: { color: "rgba(255,255,255,0.65)", maxTicksLimit: 6 },
          title: {
            display: true,
            text: "seconds",
            color: "rgba(255,255,255,0.55)",
          },
        },
      },
    },
  });

  // Histogram
  const values = rows.map((r) => Number(r.flowDuration)).filter((n) => Number.isFinite(n));
  const hist = histogram(values, 14);

  const histCtx = document.getElementById("chartHist");
  const histChart = new Chart(histCtx, {
    type: "bar",
    data: {
      labels: hist.labels,
      datasets: [
        {
          label: "Count",
          data: hist.counts,
          backgroundColor: "rgba(124, 92, 255, 0.20)",
          borderColor: "rgba(124, 92, 255, 0.40)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      ...makeCommonOptions(),
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: "rgba(255,255,255,0.65)", maxTicksLimit: 7 },
        },
        y: {
          grid: { color: "rgba(255,255,255,0.06)" },
          ticks: { color: "rgba(255,255,255,0.65)", maxTicksLimit: 5 },
        },
      },
    },
  });

  // Scatter: packet size vs latency (sampled)
  const scatterSample = sampleRows(rows, 350)
    .map((r) => ({
      x: Number(r.packetSize),
      y: Number(r.flowDuration),
    }))
    .filter((p) => Number.isFinite(p.x) && Number.isFinite(p.y));

  const scatterCtx = document.getElementById("chartScatter");
  const scatterChart = new Chart(scatterCtx, {
    type: "scatter",
    data: {
      datasets: [
        {
          label: "Packets",
          data: scatterSample,
          pointRadius: 2,
          pointHoverRadius: 4,
          backgroundColor: "rgba(52, 211, 153, 0.55)",
          borderColor: good,
        },
      ],
    },
    options: {
      ...makeCommonOptions(),
      scales: {
        x: {
          grid: { color: "rgba(255,255,255,0.06)" },
          ticks: { color: "rgba(255,255,255,0.65)", maxTicksLimit: 6 },
          title: {
            display: true,
            text: "packetSize",
            color: "rgba(255,255,255,0.55)",
          },
        },
        y: {
          grid: { color: "rgba(255,255,255,0.06)" },
          ticks: { color: "rgba(255,255,255,0.65)", maxTicksLimit: 6 },
          title: {
            display: true,
            text: "flowDuration (s)",
            color: "rgba(255,255,255,0.55)",
          },
        },
      },
    },
  });

  return { latencyChart, histChart, scatterChart };
}
