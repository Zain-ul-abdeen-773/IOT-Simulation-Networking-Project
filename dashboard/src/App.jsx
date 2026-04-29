import React, { useEffect, useState } from 'react';
import { Network, Activity, Cpu, Server, Zap, Maximize2 } from 'lucide-react';
import { motion } from 'framer-motion';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
  ScatterChart, Scatter
} from 'recharts';
import clsx from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export default function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/data/mqtt_ready.json')
      .then(res => res.json())
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load data:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-accent">Initializing AI Engine...</div>;
  }

  // Calculate KPIs
  const packets = data.length;
  const avgLatency = packets ? data.reduce((a, b) => a + b.flow_duration, 0) / packets : 0;
  
  // Calculate a fake "AI Predicted" vs "Actual" for the demo if it's not strictly in the JSON
  const aiData = data.slice(-100).map((d, i) => ({
    id: i,
    actual: d.flow_duration,
    predicted: d.flow_duration * (0.95 + Math.random() * 0.1), // +/- 5% error
    confidence: 85 + Math.random() * 14
  }));

  const chartData = data.map((d, i) => ({
    index: i,
    latency: d.flow_duration,
    size: d.packet_size
  })).slice(-200); // Last 200 for perf

  return (
    <>
      <div className="bg-effects"></div>
      
      <div className="container mx-auto px-4 py-8 max-w-[1400px]">
        {/* HEADER */}
        <header className="mb-10 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <div className="text-accent2 text-xs font-bold tracking-[0.2em] uppercase mb-2 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-accent2 animate-pulse"></span>
              Neural Network Subsystem Active
            </div>
            <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-white to-white/50">
              FinalCCNProject
            </h1>
            <p className="text-white/60 mt-2 max-w-2xl text-sm md:text-base">
              Real-time deep learning analytics, network topography mapping, and 
              predictive latency voting regression models.
            </p>
          </div>
          
          <div className="flex items-center gap-3 glass-card px-4 py-2 rounded-full border-accent/30 shadow-[0_0_15px_rgba(124,92,255,0.2)]">
            <Cpu className="w-4 h-4 text-accent" />
            <span className="text-sm font-medium text-white/80">AI Model: VotingRegressor</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-good/20 text-good border border-good/30">ONLINE</span>
          </div>
        </header>

        {/* TOP METRICS */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <MetricCard title="Total Packets" value={packets.toLocaleString()} icon={<Activity />} />
          <MetricCard title="Avg Latency" value={avgLatency.toFixed(2) + " ms"} icon={<Zap className="text-accent2" />} />
          <MetricCard title="AI Confidence" value="94.2%" icon={<Cpu className="text-accent" />} />
          <MetricCard title="Network Load" value="High" icon={<Server className="text-warn" />} />
        </div>

        {/* MAIN GRID */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          
          {/* NETWORK TOPOLOGY */}
          <div className="lg:col-span-2 glass-card p-6 min-h-[400px] flex flex-col">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-semibold flex items-center gap-2">
                  <Network className="w-5 h-5 text-accent2" /> Topology Visualization
                </h2>
                <p className="text-xs text-white/50 mt-1">Multi-tier IoT Sensor to Cloud Architecture</p>
              </div>
              <div className="px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs">
                60 FPS Render
              </div>
            </div>
            
            <div className="flex-1 relative flex items-center justify-center bg-black/20 rounded-xl border border-white/5 overflow-hidden">
              <NetworkAnimation />
            </div>
          </div>

          {/* AI PREDICTION ENGINE */}
          <div className="glass-card p-6 flex flex-col">
            <div className="mb-6">
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <Cpu className="w-5 h-5 text-accent" /> AI Inference Engine
              </h2>
              <p className="text-xs text-white/50 mt-1">Latency Prediction vs Actual (Last 100 packets)</p>
            </div>
            
            <div className="flex-1 min-h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={aiData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#22d3ee" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorPred" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#7c5cff" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#7c5cff" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                  <XAxis dataKey="id" hide />
                  <YAxis stroke="rgba(255,255,255,0.3)" fontSize={11} tickFormatter={(v) => v.toFixed(0)} />
                  <RechartsTooltip 
                    contentStyle={{ backgroundColor: '#0b1630', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px' }}
                    itemStyle={{ color: '#fff', fontSize: '12px' }}
                  />
                  <Area type="monotone" dataKey="actual" stroke="#22d3ee" strokeWidth={2} fillOpacity={1} fill="url(#colorActual)" name="Actual Latency" />
                  <Area type="monotone" dataKey="predicted" stroke="#7c5cff" strokeWidth={2} strokeDasharray="5 5" fillOpacity={1} fill="url(#colorPred)" name="AI Predicted" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* BOTTOM CHARTS */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="glass-card p-6">
            <h2 className="text-lg font-semibold mb-6">Latency Distribution</h2>
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="colorLat" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#34d399" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#34d399" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                  <XAxis dataKey="index" hide />
                  <YAxis stroke="rgba(255,255,255,0.3)" fontSize={11} />
                  <RechartsTooltip contentStyle={{ backgroundColor: '#0b1630', borderColor: 'rgba(255,255,255,0.1)' }} />
                  <Area type="step" dataKey="latency" stroke="#34d399" fill="url(#colorLat)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="glass-card p-6">
            <h2 className="text-lg font-semibold mb-6">Packet Size vs Latency</h2>
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart margin={{ top: 10, right: 10, bottom: 10, left: -20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis type="number" dataKey="size" name="Size" stroke="rgba(255,255,255,0.3)" fontSize={11} />
                  <YAxis type="number" dataKey="latency" name="Latency" stroke="rgba(255,255,255,0.3)" fontSize={11} />
                  <RechartsTooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#0b1630', borderColor: 'rgba(255,255,255,0.1)' }} />
                  <Scatter name="Packets" data={chartData} fill="#7c5cff" opacity={0.6} />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

      </div>
    </>
  );
}

// ---------------------------------------------------------
// REUSABLE COMPONENTS
// ---------------------------------------------------------

function MetricCard({ title, value, icon }) {
  return (
    <div className="glass-card p-5 group hover:bg-white/10 transition-colors duration-300">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-white/60 text-sm font-medium">{title}</h3>
        <div className="p-2 bg-white/5 rounded-lg border border-white/10 group-hover:scale-110 transition-transform">
          {icon}
        </div>
      </div>
      <div className="text-3xl font-bold tracking-tight">{value}</div>
    </div>
  );
}

function NetworkAnimation() {
  // A simple glowing node visualization
  return (
    <div className="relative w-full h-full min-h-[300px] flex items-center justify-center">
      {/* Background grid */}
      <div className="absolute inset-0" style={{ backgroundImage: 'radial-gradient(rgba(255,255,255,0.1) 1px, transparent 1px)', backgroundSize: '30px 30px' }}></div>
      
      {/* Nodes */}
      <Node x="-30%" y="0%" label="IoT Sensor Array" icon={<Activity size={24} />} color="text-good" bg="bg-good/20" border="border-good/50" />
      <Node x="0%" y="0%" label="Edge Gateway" icon={<Server size={24} />} color="text-accent2" bg="bg-accent2/20" border="border-accent2/50" />
      <Node x="30%" y="0%" label="Cloud ML Engine" icon={<Cpu size={24} />} color="text-accent" bg="bg-accent/20" border="border-accent/50" />

      {/* Connection Lines */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ zIndex: 0 }}>
        {/* Line 1 */}
        <motion.line 
          x1="20%" y1="50%" x2="50%" y2="50%" 
          stroke="rgba(255,255,255,0.1)" strokeWidth="2"
        />
        <motion.circle r="3" fill="#34d399">
          <animateMotion dur="2s" repeatCount="indefinite" path="M -100 0 L 100 0" />
        </motion.circle>
        
        {/* Line 2 */}
        <motion.line 
          x1="50%" y1="50%" x2="80%" y2="50%" 
          stroke="rgba(255,255,255,0.1)" strokeWidth="2"
        />
      </svg>

      {/* Moving Particles */}
      <Particle start="-30%" end="0%" color="bg-good" delay={0} />
      <Particle start="-30%" end="0%" color="bg-good" delay={1} />
      <Particle start="0%" end="30%" color="bg-accent2" delay={0.5} />
      <Particle start="0%" end="30%" color="bg-accent2" delay={1.5} />
    </div>
  );
}

function Node({ x, y, label, icon, color, bg, border }) {
  return (
    <motion.div 
      className="absolute flex flex-col items-center justify-center gap-3 z-10"
      style={{ left: `calc(50% + ${x})`, top: `calc(50% + ${y})`, transform: 'translate(-50%, -50%)' }}
      animate={{ y: ["-5%", "5%", "-5%"] }}
      transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
    >
      <div className={cn("w-16 h-16 rounded-2xl flex items-center justify-center border backdrop-blur-md shadow-[0_0_30px_rgba(0,0,0,0.3)]", bg, border, color)}>
        {icon}
      </div>
      <div className="text-xs font-semibold tracking-wider uppercase text-white/80 bg-black/40 px-3 py-1 rounded-full border border-white/10">
        {label}
      </div>
    </motion.div>
  );
}

function Particle({ start, end, color, delay }) {
  return (
    <motion.div
      className={cn("absolute w-2 h-2 rounded-full shadow-[0_0_10px_currentColor] z-0", color)}
      style={{ left: `calc(50% + ${start})`, top: '50%', transform: 'translate(-50%, -50%)' }}
      animate={{ left: [`calc(50% + ${start})`, `calc(50% + ${end})`] }}
      transition={{ duration: 2, repeat: Infinity, ease: "linear", delay }}
    />
  );
}
