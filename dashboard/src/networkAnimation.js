function clamp(min, value, max) {
  return Math.max(min, Math.min(max, value));
}

function lerp(a, b, t) {
  return a + (b - a) * t;
}

function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function rgba(hex, a) {
  const h = hex.replace("#", "").trim();
  const full = h.length === 3 ? h.split("").map((c) => c + c).join("") : h;
  const r = parseInt(full.slice(0, 2), 16);
  const g = parseInt(full.slice(2, 4), 16);
  const b = parseInt(full.slice(4, 6), 16);
  return `rgba(${r},${g},${b},${a})`;
}

function cssVar(name, fallback) {
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

class Packet {
  constructor({ from, via, to, radius, hue, travelMs }) {
    this.from = from;
    this.via = via;
    this.to = to;

    this.radius = radius;
    this.hue = hue;

    this.t = 0;
    this.stage = 0;
    this.stageStart = performance.now();
    this.travelMs = travelMs;

    this.trail = [];
    this.trailMax = 12;
  }

  update(now) {
    const stageA = this.stage === 0 ? this.from : this.via;
    const stageB = this.stage === 0 ? this.via : this.to;

    const dt = now - this.stageStart;
    const raw = clamp(0, dt / this.travelMs, 1);
    const t = easeInOutCubic(raw);

    const x = lerp(stageA.x, stageB.x, t);
    const y = lerp(stageA.y, stageB.y, t);

    this.trail.push({ x, y });
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
  }
}

export function createNetworkAnimation(canvas, { rows, spawnEveryMs = 170 } = {}) {
  const ctx = canvas.getContext("2d");
  const dpr = Math.max(1, Math.min(2, window.devicePixelRatio || 1));

  const accent = cssVar("--accent", "#7c5cff");
  const accent2 = cssVar("--accent2", "#22d3ee");
  const good = cssVar("--good", "#34d399");

  let w = 0;
  let h = 0;

  function resize() {
    const rect = canvas.getBoundingClientRect();
    w = Math.floor(rect.width);
    h = Math.floor(rect.height);

    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    layout();
  }

  const state = {
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
    const pad = 36;
    const midY = h * 0.52;

    const leftX = pad + 30;
    const rightX = w - pad - 30;
    const midX = w * 0.5;

    state.nodes.gateway.x = midX;
    state.nodes.gateway.y = midY;

    state.nodes.cloud.x = rightX;
    state.nodes.cloud.y = midY;

    const sensorCount = 7;
    const ringR = Math.min(120, Math.max(70, w * 0.16));
    const ringCx = leftX + 20;
    const ringCy = midY;

    state.nodes.sensors = Array.from({ length: sensorCount }, (_, i) => {
      const a = (i / sensorCount) * Math.PI * 2 - Math.PI / 2;
      return {
        x: ringCx + Math.cos(a) * ringR,
        y: ringCy + Math.sin(a) * ringR,
        r: 10,
      };
    });
  }

  function drawNode(node, label, color, glowAlpha, now) {
    const pulse = 0.5 + 0.5 * Math.sin(now * 0.002);
    const glow = rgba(color, glowAlpha * (0.7 + 0.3 * pulse));

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

  function drawLink(a, b, color, now) {
    const shimmer = 0.5 + 0.5 * Math.sin(now * 0.003);

    const grad = ctx.createLinearGradient(a.x, a.y, b.x, b.y);
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

  function spawn(now) {
    const sensors = state.nodes.sensors;
    if (!sensors.length) return;

    const row = rows?.[state.idx % rows.length];
    state.idx += 1;

    const from = sensors[Math.floor(Math.random() * sensors.length)];
    const via = state.nodes.gateway;
    const to = state.nodes.cloud;

    const packetSize = row ? Number(row.packetSize) : 8;
    const flow = row ? Number(row.flowDuration) : 30;

    const radius = clamp(2.5, 1.5 + packetSize * 0.45, 6.8);
    const travelMs = clamp(650, 420 + flow * 16, 1400);

    // Use flowDuration to gently shift color hue
    const hue = clamp(180, 180 + (flow - 20) * 6, 310);

    state.packets.push(
      new Packet({
        from,
        via,
        to,
        radius,
        hue,
        travelMs,
      })
    );

    state.lastSpawn = now;
  }

  function drawPacket(p) {
    const col = `hsla(${p.hue}, 90%, 64%, 1)`;

    // trail
    ctx.save();
    for (let i = 0; i < p.trail.length; i++) {
      const t = i / p.trail.length;
      const a = 0.05 + t * 0.22;
      const r = p.radius * (0.6 + t * 0.6);
      const pt = p.trail[i];
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, r, 0, Math.PI * 2);
      ctx.fillStyle = `hsla(${p.hue}, 90%, 64%, ${a})`;
      ctx.fill();
    }
    ctx.restore();

    // head glow
    ctx.save();
    ctx.shadowColor = col;
    ctx.shadowBlur = 18;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
    ctx.fillStyle = col;
    ctx.fill();
    ctx.restore();
  }

  function drawBackground(now) {
    ctx.clearRect(0, 0, w, h);

    // subtle grid
    ctx.save();
    ctx.globalAlpha = 0.12;
    ctx.strokeStyle = "rgba(255,255,255,0.08)";
    ctx.lineWidth = 1;

    const step = 44;
    const ox = (now * 0.02) % step;
    const oy = (now * 0.015) % step;

    for (let x = -step; x < w + step; x += step) {
      ctx.beginPath();
      ctx.moveTo(x + ox, 0);
      ctx.lineTo(x + ox, h);
      ctx.stroke();
    }

    for (let y = -step; y < h + step; y += step) {
      ctx.beginPath();
      ctx.moveTo(0, y + oy);
      ctx.lineTo(w, y + oy);
      ctx.stroke();
    }

    ctx.restore();
  }

  function frame(now) {
    if (!state.running) return;

    if (now - state.lastSpawn > spawnEveryMs) spawn(now);

    drawBackground(now);

    // links
    for (const s of state.nodes.sensors) {
      drawLink(s, state.nodes.gateway, accent, now);
    }
    drawLink(state.nodes.gateway, state.nodes.cloud, accent2, now);

    // nodes
    for (let i = 0; i < state.nodes.sensors.length; i++) {
      drawNode(state.nodes.sensors[i], `S${i + 1}`, good, 0.50, now);
    }
    drawNode(state.nodes.gateway, "Gateway", accent, 0.55, now);
    drawNode(state.nodes.cloud, "Cloud", accent2, 0.55, now);

    // packets
    for (const p of state.packets) {
      p.update(now);
      drawPacket(p);
    }
    state.packets = state.packets.filter((p) => !p.done);

    requestAnimationFrame(frame);
  }

  window.addEventListener("resize", resize);
  resize();

  return {
    start() {
      if (state.running) return;
      state.running = true;
      requestAnimationFrame(frame);
    },
    stop() {
      state.running = false;
    },
    setSpawnEveryMs(ms) {
      spawnEveryMs = clamp(50, ms, 700);
    },
  };
}
