import React, { useEffect, useState } from "react";
import { AnimatePresence, motion, useAnimationFrame, useMotionValue, useReducedMotion, useSpring } from "framer-motion";

const keywords = [
  "Intelligent",
  "Protocol-Driven",
  "Deterministic",
  "Scalable",
  "Firmware-Aware"
];

export default function Hero() {
  const [index, setIndex] = useState(0);
  const reduceMotion = useReducedMotion();
  const rotX = useMotionValue(10);
  const rotY = useMotionValue(0);
  const springX = useSpring(rotX, { stiffness: 60, damping: 16 });
  const springY = useSpring(rotY, { stiffness: 60, damping: 16 });

  useAnimationFrame((t) => {
    if (reduceMotion) return;
    const time = t / 1000;
    rotX.set(8 + Math.sin(time * 0.8) * 6);
    rotY.set(Math.cos(time * 0.6) * 10);
  });

  useEffect(() => {
    if (reduceMotion) return undefined;
    const id = setInterval(() => {
      setIndex((prev) => (prev + 1) % keywords.length);
    }, 2400);
    return () => clearInterval(id);
  }, [reduceMotion]);

  return (
    <section id="core" className="relative overflow-hidden">
      <div className="neural-grid absolute inset-0 opacity-60" />
      <div className="relative mx-auto grid w-full max-w-6xl items-center gap-12 px-6 py-16 md:grid-cols-[1.1fr_0.9fr] md:py-24">
        <div className="space-y-6">
          <div className="inline-flex items-center gap-3 rounded-full border border-indigo-500/40 bg-indigo-500/10 px-4 py-1 text-xs uppercase tracking-[0.3em] text-indigo-200">
            MCP firmware generator
          </div>
          <h1 className="text-4xl font-semibold leading-tight text-white md:text-5xl">
            AI Core that orchestrates <span className="text-cyan-300">system intelligence</span>
          </h1>
          <p className="max-w-xl text-base text-slate-300 md:text-lg">
            A research-grade interface for firmware pipelines, toolchains, and deterministic execution.
            Every signal is observable. Every decision is auditable.
          </p>
          <div className="flex items-center gap-4 text-sm text-slate-400">
            <span className="rounded-full border border-slate-700 px-3 py-1">MCP pipelines</span>
            <span className="rounded-full border border-slate-700 px-3 py-1">Protocol layers</span>
            <span className="rounded-full border border-slate-700 px-3 py-1">Signal graphs</span>
          </div>
          <div className="relative h-10 overflow-hidden">
            <AnimatePresence mode="wait">
              <motion.span
                key={keywords[index]}
                initial={{ opacity: 0, y: 18 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -18 }}
                transition={{ type: "spring", stiffness: 120, damping: 18 }}
                className="absolute left-0 top-0 text-lg font-semibold text-cyan-200"
              >
                {keywords[index]}
              </motion.span>
            </AnimatePresence>
          </div>
        </div>
        <div className="scanline card-glass rounded-3xl p-6 shadow-core">
          <motion.div
            className="ai-chip-shell-3d"
            style={{ rotateX: springX, rotateY: springY }}
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ type: "spring", stiffness: 120, damping: 18 }}
          >
            <div className="ai-chip-bg-grid" />
            <div className="ai-chip-wires-top" />
            <div className="ai-chip-plate">
              <div className="ai-chip-die-3d">
                <div className="ai-chip-die-top" />
                <div className="ai-chip-die-glow" />
              </div>
              <div className="ai-chip-wireburst" />
              <div className="ai-chip-traces-3d" />
            </div>
            <div className="ai-chip-rim" />
            <div className="ai-chip-pin-row ai-chip-pin-row-top" />
            <div className="ai-chip-pin-row ai-chip-pin-row-bottom" />
            <div className="ai-chip-pin-col ai-chip-pin-col-left" />
            <div className="ai-chip-pin-col ai-chip-pin-col-right" />
            <div className="ai-chip-wires-bottom" />
          </motion.div>
        </div>
      </div>
    </section>
  );
}
