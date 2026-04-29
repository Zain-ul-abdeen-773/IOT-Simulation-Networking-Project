(function () {
  "use strict";

  function $(id) {
    return document.getElementById(id);
  }

  function clamp(min, value, max) {
    return Math.max(min, Math.min(max, value));
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  function formatNumber(n, digits) {
    if (!Number.isFinite(n)) return "—";
    return n.toFixed(digits);
  }

  function setStatus(text) {
    var el = $("status");
    if (el) el.textContent = text;
  }

  function cssVar(name, fallback) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v || fallback;
  }

  // -------------------------
  // Data + stats
  // -------------------------

  function computeStats(values) {
    if (!values.length) {
      return { count: 0, min: 0, max: 0, mean: 0, std: 0 };
    }

    var min = Infinity;
    var max = -Infinity;
    var mean = 0;
    var m2 = 0;
    var count = 0;

    for (var i = 0; i < values.length; i++) {
      var v = values[i];
      count += 1;
      if (v < min) min = v;
      if (v > max) max = v;

      var delta = v - mean;
      mean += delta / count;
      var delta2 = v - mean;
      m2 += delta * delta2;
    }

    var variance = count > 1 ? m2 / (count - 1) : 0;
    var std = Math.sqrt(variance);

    return { count: count, min: min, max: max, mean: mean, std: std };
  }

  function computeSummary(rows) {
    var latencies = [];
    var sizes = [];
    var inter = [];

    for (var i = 0; i < rows.length; i++) {
      var r = rows[i];
      var l = Number(r.flowDuration);
      var s = Number(r.packetSize);
      var ia = Number(r.interArrival);

      if (Number.isFinite(l)) latencies.push(l);
      if (Number.isFinite(s)) sizes.push(s);
      if (Number.isFinite(ia)) inter.push(ia);
    }

    var latencyStats = computeStats(latencies);
    var sizeStats = computeStats(sizes);
    var interStats = computeStats(inter);

    // Useful for animation pacing; keep it in a stable range
    var interArrivalSpawnMs = clamp(70, (interStats.mean || 2500000) / 8000, 520);

    return {
      packetCount: rows.length,
      latencyStats: latencyStats,
      sizeStats: sizeStats,
      interStats: interStats,
      interArrivalSpawnMs: interArrivalSpawnMs,
    };
  }

  function sampleRows(rows, maxPoints) {
    if (rows.length <= maxPoints) return rows;

    var step = Math.ceil(rows.length / maxPoints);
    var sampled = [];
    for (var i = 0; i < rows.length; i += step) {
      sampled.push(rows[i]);
    }
    return sampled;
  }

  function histogram(values, binCount) {
    if (!values.length) {
      return { labels: [], counts: [] };
    }

    var min = Infinity;
    var max = -Infinity;
    for (var i = 0; i < values.length; i++) {
      var v = values[i];
      if (v < min) min = v;
      if (v > max) max = v;
    }

    if (min === max) {
      return { labels: [min.toFixed(2)], counts: [values.length] };
    }

    var bins = Array.from({ length: binCount }, function () {
      return 0;
    });
    var width = (max - min) / binCount;

    for (var j = 0; j < values.length; j++) {
      var vv = values[j];
      var idx = Math.min(binCount - 1, Math.max(0, Math.floor((vv - min) / width)));
      bins[idx] += 1;
    }

    var labels = bins.map(function (_, i2) {
      var a = min + i2 * width;
      var b = a + width;
      return a.toFixed(1) + "–" + b.toFixed(1);
    });

    return { labels: labels, counts: bins };
  }

  async function loadRows() {
    // Zero-setup path: open dashboard/index.html directly (file://) and it still works.
    if (window.__MQTT_READY__ && Array.isArray(window.__MQTT_READY__.rows)) {
      return { rows: window.__MQTT_READY__.rows, meta: window.__MQTT_READY__ };
    }

    // Served path (http://...): fetch JSON.
    var res = await fetch("./data/mqtt_ready.json", { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to load data: " + res.status + " " + res.statusText);
    var payload = await res.json();
    return { rows: payload.rows || [], meta: payload };
  }

  // -------------------------
  // Charts (Chart.js)
  // -------------------------

  function makeCommonChartOptions() {
    var grid = "rgba(255,255,255,0.08)";
    var ticks = "rgba(255,255,255,0.65)";

    return {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 900, easing: "easeOutQuart" },
      plugins: {
        legend: { labels: { color: ticks, boxWidth: 10 } },
        tooltip: {
          backgroundColor: "rgba(8, 12, 22, 0.92)",
          borderColor: "rgba(255,255,255,0.10)",
          borderWidth: 1,
          titleColor: "rgba(255,255,255,0.90)",
          bodyColor: "rgba(255,255,255,0.78)",
        },
      },
      scales: {
        x: { grid: { color: grid }, ticks: { color: ticks, maxTicksLimit: 6 } },
        y: { grid: { color: grid }, ticks: { color: ticks, maxTicksLimit: 6 } },
      },
    };
  }

  function createCharts(rows) {
    if (!window.Chart) {
      setStatus("Charts unavailable (Chart.js not loaded)");
      return;
    }

    var accent = cssVar("--accent", "#7c5cff");
    var accent2 = cssVar("--accent2", "#22d3ee");
    var good = cssVar("--good", "#34d399");

    // Latency over time
    var series = sampleRows(rows, 280);
    var labels = series.map(function (r, i) {
      return r.arrivalTimestamp || "#" + i;
    });
    var latency = series.map(function (r) {
      return Number(r.flowDuration);
    });

    var latencyCtx = $("chartLatency");
    new Chart(latencyCtx, {
      type: "line",
      data: {
        labels: labels,
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
      options: Object.assign({}, makeCommonChartOptions(), {
        scales: {
          x: {
            grid: { color: "rgba(255,255,255,0.06)" },
            ticks: {
              color: "rgba(255,255,255,0.65)",
              maxTicksLimit: 5,
              callback: function (val) {
                var s = labels[val] || "";
                return typeof s === "string" ? s.slice(11, 19) : s;
              },
            },
          },
          y: {
            grid: { color: "rgba(255,255,255,0.06)" },
            ticks: { color: "rgba(255,255,255,0.65)", maxTicksLimit: 6 },
            title: { display: true, text: "seconds", color: "rgba(255,255,255,0.55)" },
          },
        },
      }),
    });

    // Histogram
    var values = rows
      .map(function (r) {
        return Number(r.flowDuration);
      })
      .filter(function (n) {
        return Number.isFinite(n);
      });

    var hist = histogram(values, 14);

    var histCtx = $("chartHist");
    new Chart(histCtx, {
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
      options: Object.assign({}, makeCommonChartOptions(), {
        scales: {
          x: { grid: { display: false }, ticks: { color: "rgba(255,255,255,0.65)", maxTicksLimit: 7 } },
          y: { grid: { color: "rgba(255,255,255,0.06)" }, ticks: { color: "rgba(255,255,255,0.65)", maxTicksLimit: 5 } },
        },
      }),
    });

    // Scatter: packet size vs latency
    var scatterSample = sampleRows(rows, 350)
      .map(function (r) {
        return { x: Number(r.packetSize), y: Number(r.flowDuration) };
      })
      .filter(function (p) {
        return Number.isFinite(p.x) && Number.isFinite(p.y);
      });

    var scatterCtx = $("chartScatter");
    new Chart(scatterCtx, {
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
      options: Object.assign({}, makeCommonChartOptions(), {
        scales: {
          x: { grid: { color: "rgba(255,255,255,0.06)" }, ticks: { color: "rgba(255,255,255,0.65)", maxTicksLimit: 6 }, title: { display: true, text: "packetSize", color: "rgba(255,255,255,0.55)" } },
          y: { grid: { color: "rgba(255,255,255,0.06)" }, ticks: { color: "rgba(255,255,255,0.65)", maxTicksLimit: 6 }, title: { display: true, text: "flowDuration (s)", color: "rgba(255,255,255,0.55)" } },
        },
      }),
    });
  }

  // -------------------------
  // Canvas network animation
  // -------------------------

  function rgba(hex, a) {
    var h = hex.replace("#", "").trim();
    var full = h.length === 3 ? h.split("").map(function (c) { return c + c; }).join("") : h;
    var r = parseInt(full.slice(0, 2), 16);
    var g = parseInt(full.slice(2, 4), 16);
    var b = parseInt(full.slice(4, 6), 16);
    return "rgba(" + r + "," + g + "," + b + "," + a + ")";
  }

  function Packet(opts) {
    this.from = opts.from;
    this.via = opts.via;
    this.to = opts.to;
    this.radius = opts.radius;
    this.hue = opts.hue;
    this.stage = 0;
    this.stageStart = performance.now();
    this.travelMs = opts.travelMs;
    this.trail = [];
    this.trailMax = 12;
    this.done = false;
    this.x = this.from.x;
    this.y = this.from.y;
  }

  Packet.prototype.update = function (now) {
    var stageA = this.stage === 0 ? this.from : this.via;
    var stageB = this.stage === 0 ? this.via : this.to;

    var dt = now - this.stageStart;
    var raw = clamp(0, dt / this.travelMs, 1);
    var t = easeInOutCubic(raw);

    var x = lerp(stageA.x, stageB.x, t);
    var y = lerp(stageA.y, stageB.y, t);

    this.trail.push({ x: x, y: y });
    if (this.trail.length > this.trailMax) this.trail.shift();

    if (raw >= 1) {
      if (this.stage === 0) {
        this.stage = 1;
        this.stageStart = now;
      } else {
        this.done = true;
      }
    }

    this.x = x;
    this.y = y;
  };

  function createNetworkAnimation(canvas, rows, spawnEveryMs) {
    var ctx = canvas.getContext("2d");
    var dpr = Math.max(1, Math.min(2, window.devicePixelRatio || 1));

    var accent = cssVar("--accent", "#7c5cff");
    var accent2 = cssVar("--accent2", "#22d3ee");
    var good = cssVar("--good", "#34d399");

    var w = 0;
    var h = 0;

    var state = {
      nodes: {
        sensors: [],
        gateway: { x: 0, y: 0, r: 22 },
        cloud: { x: 0, y: 0, r: 26 },
      },
      packets: [],
      running: false,
      lastSpawn: 0,
      idx: 0,
    };

    function layout() {
      var pad = 36;
      var midY = h * 0.52;
      var leftX = pad + 30;
      var rightX = w - pad - 30;
      var midX = w * 0.5;

      state.nodes.gateway.x = midX;
      state.nodes.gateway.y = midY;

      state.nodes.cloud.x = rightX;
      state.nodes.cloud.y = midY;

      var sensorCount = 7;
      var ringR = Math.min(120, Math.max(70, w * 0.16));
      var ringCx = leftX + 20;
      var ringCy = midY;

      state.nodes.sensors = Array.from({ length: sensorCount }, function (_, i) {
        var a = (i / sensorCount) * Math.PI * 2 - Math.PI / 2;
        return {
          x: ringCx + Math.cos(a) * ringR,
          y: ringCy + Math.sin(a) * ringR,
          r: 10,
        };
      });
    }

    function resize() {
      var rect = canvas.getBoundingClientRect();
      w = Math.floor(rect.width);
      h = Math.floor(rect.height);
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      layout();
    }

    function drawBackground(now) {
      ctx.clearRect(0, 0, w, h);

      ctx.save();
      ctx.globalAlpha = 0.12;
      ctx.strokeStyle = "rgba(255,255,255,0.08)";
      ctx.lineWidth = 1;

      var step = 44;
      var ox = (now * 0.02) % step;
      var oy = (now * 0.015) % step;

      for (var x = -step; x < w + step; x += step) {
        ctx.beginPath();
        ctx.moveTo(x + ox, 0);
        ctx.lineTo(x + ox, h);
        ctx.stroke();
      }

      for (var y = -step; y < h + step; y += step) {
        ctx.beginPath();
        ctx.moveTo(0, y + oy);
        ctx.lineTo(w, y + oy);
        ctx.stroke();
      }

      ctx.restore();
    }

    function drawLink(a, b, color, now) {
      var shimmer = 0.5 + 0.5 * Math.sin(now * 0.003);

      var grad = ctx.createLinearGradient(a.x, a.y, b.x, b.y);
      grad.addColorStop(0, rgba(color, 0.08));
      grad.addColorStop(0.5, rgba(color, 0.24 + shimmer * 0.08));
      grad.addColorStop(1, rgba(color, 0.10));

      ctx.lineWidth = 2;
      ctx.strokeStyle = grad;

      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    }

    function drawNode(node, label, color, glowAlpha, now) {
      var pulse = 0.5 + 0.5 * Math.sin(now * 0.002);
      var glow = rgba(color, glowAlpha * (0.7 + 0.3 * pulse));

      ctx.save();
      ctx.shadowColor = glow;
      ctx.shadowBlur = 18;

      ctx.beginPath();
      ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);
      ctx.fillStyle = rgba(color, 0.24);
      ctx.fill();

      ctx.shadowBlur = 0;
      ctx.lineWidth = 1;
      ctx.strokeStyle = rgba(color, 0.55);
      ctx.stroke();

      ctx.fillStyle = "rgba(255,255,255,0.82)";
      ctx.font = "12px ui-sans-serif, system-ui, -apple-system, Segoe UI";
      ctx.textAlign = "center";
      ctx.textBaseline = "top";
      ctx.fillText(label, node.x, node.y + node.r + 8);

      ctx.restore();
    }

    function drawPacket(p) {
      var col = "hsla(" + p.hue + ", 90%, 64%, 1)";

      ctx.save();
      for (var i = 0; i < p.trail.length; i++) {
        var t = i / p.trail.length;
        var a = 0.05 + t * 0.22;
        var r = p.radius * (0.6 + t * 0.6);
        var pt = p.trail[i];
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, r, 0, Math.PI * 2);
        ctx.fillStyle = "hsla(" + p.hue + ", 90%, 64%, " + a + ")";
        ctx.fill();
      }
      ctx.restore();

      ctx.save();
      ctx.shadowColor = col;
      ctx.shadowBlur = 18;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = col;
      ctx.fill();
      ctx.restore();
    }

    function spawn(now) {
      var sensors = state.nodes.sensors;
      if (!sensors.length) return;

      var row = rows && rows.length ? rows[state.idx % rows.length] : null;
      state.idx += 1;

      var from = sensors[Math.floor(Math.random() * sensors.length)];
      var via = state.nodes.gateway;
      var to = state.nodes.cloud;

      var packetSize = row ? Number(row.packetSize) : 8;
      var flow = row ? Number(row.flowDuration) : 30;

      var radius = clamp(2.5, 1.5 + packetSize * 0.45, 6.8);
      var travelMs = clamp(650, 420 + flow * 16, 1400);
      var hue = clamp(180, 180 + (flow - 20) * 6, 310);

      state.packets.push(
        new Packet({ from: from, via: via, to: to, radius: radius, hue: hue, travelMs: travelMs })
      );

      state.lastSpawn = now;
    }

    function frame(now) {
      if (!state.running) return;

      if (now - state.lastSpawn > spawnEveryMs) spawn(now);

      drawBackground(now);

      for (var i = 0; i < state.nodes.sensors.length; i++) {
        drawLink(state.nodes.sensors[i], state.nodes.gateway, accent, now);
      }
      drawLink(state.nodes.gateway, state.nodes.cloud, accent2, now);

      for (var j = 0; j < state.nodes.sensors.length; j++) {
        drawNode(state.nodes.sensors[j], "S" + (j + 1), good, 0.5, now);
      }
      drawNode(state.nodes.gateway, "Gateway", accent, 0.55, now);
      drawNode(state.nodes.cloud, "Cloud", accent2, 0.55, now);

      for (var k = 0; k < state.packets.length; k++) {
        var p = state.packets[k];
        p.update(now);
        drawPacket(p);
      }
      state.packets = state.packets.filter(function (p2) {
        return !p2.done;
      });

      requestAnimationFrame(frame);
    }

    window.addEventListener("resize", resize);
    resize();

    return {
      start: function () {
        if (state.running) return;
        state.running = true;
        requestAnimationFrame(frame);
      },
    };
  }

  // -------------------------
  // KPI animation
  // -------------------------

  function animateCounter(el, toValue, opts) {
    opts = opts || {};
    var suffix = opts.suffix || "";
    var durationMs = opts.durationMs || 900;
    var digits = typeof opts.digits === "number" ? opts.digits : 2;

    var from = 0;
    var start = performance.now();

    function easeOutQuart(t) {
      return 1 - Math.pow(1 - t, 4);
    }

    function frame(now) {
      var t = Math.min(1, (now - start) / durationMs);
      var v = from + (toValue - from) * easeOutQuart(t);
      el.textContent = formatNumber(v, digits) + suffix;
      if (t < 1) requestAnimationFrame(frame);
    }

    requestAnimationFrame(frame);
  }

  // -------------------------
  // Main
  // -------------------------

  (async function main() {
    try {
      setStatus("Loading data…");

      var loaded = await loadRows();
      var rows = loaded.rows || [];
      var meta = loaded.meta || {};
      var summary = computeSummary(rows);

      // KPIs
      $("kpiPackets").textContent = String(summary.packetCount);

      animateCounter($("kpiAvg"), summary.latencyStats.mean, { suffix: " s", digits: 2, durationMs: 1000 });
      $("kpiMinMax").textContent =
        formatNumber(summary.latencyStats.min, 2) +
        " s / " +
        formatNumber(summary.latencyStats.max, 2) +
        " s";
      animateCounter($("kpiStd"), summary.latencyStats.std, { suffix: " s", digits: 2, durationMs: 1000 });

      // Charts
      createCharts(rows);

      // Network animation
      var anim = createNetworkAnimation($("networkCanvas"), rows, summary.interArrivalSpawnMs);
      anim.start();

      var gen = meta.generatedAt ? " • data: " + meta.generatedAt : "";
      setStatus("Ready" + gen);
    } catch (err) {
      console.error(err);
      setStatus("Failed to load data (see console)");
    }
  })();
})();
