import React, { useState } from "react";
import { motion, useAnimationFrame, useMotionValue, useTransform } from "framer-motion";

const orbiters = [
  { label: "R3F", tone: "from-indigo-500 to-cyan-400" },
  { label: "Drei", tone: "from-slate-700 to-slate-500" },
  { label: "Motion", tone: "from-cyan-500 to-indigo-500" },
  { label: "Tailwind", tone: "from-sky-500 to-cyan-300" },
  { label: "MCP", tone: "from-indigo-400 to-slate-700" },
  { label: "Maath", tone: "from-slate-600 to-indigo-400" }
];

function OrbitItem({ index, total, angle, paused, label, tone }) {
  const offset = (Math.PI * 2 * index) / total;
  const radius = 92;
  const x = useTransform(angle, (value) => Math.cos(value + offset) * radius);
  const y = useTransform(angle, (value) => Math.sin(value + offset) * radius);

  return (
    <motion.div
      style={{ x, y }}
      className="absolute left-1/2 top-1/2"
    >
      <div
        className={`flex -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full bg-gradient-to-r ${tone} px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.2em] text-slate-950 shadow-lg`}
      >
        {label}
      </div>
      {paused && (
        <div className="mt-1 text-center text-[10px] uppercase tracking-[0.3em] text-slate-500">
          Paused
        </div>
      )}
    </motion.div>
  );
}

export default function OrbitingStack() {
  const angle = useMotionValue(0);
  const [paused, setPaused] = useState(false);

  useAnimationFrame((_, delta) => {
    if (paused) return;
    angle.set(angle.get() + delta * 0.00035);
  });

  return (
    <div
      className="relative flex h-60 items-center justify-center"
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
    >
      <div className="absolute h-12 w-12 rounded-full bg-gradient-to-br from-indigo-500 via-cyan-400 to-slate-900" />
      <div className="absolute h-28 w-28 rounded-full border border-slate-700/70" />
      {orbiters.map((orbiter, idx) => (
        <OrbitItem
          key={orbiter.label}
          index={idx}
          total={orbiters.length}
          angle={angle}
          paused={paused}
          {...orbiter}
        />
      ))}
    </div>
  );
}
