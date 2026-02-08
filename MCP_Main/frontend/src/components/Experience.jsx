import React from "react";
import { motion } from "framer-motion";

const timeline = [
  {
    title: "MCP Architecture Setup",
    period: "Phase 01",
    detail: "Established MCP tool schema, FastAPI backend endpoints, and LLM integration workflow."
  },
  {
    title: "AI Code Generation Engine",
    period: "Phase 02",
    detail: "Implemented structured firmware generation using Ollama with board-aware templates and const-safe patterns."
  },
  {
    title: "Smart Dependency & Quality Layer",
    period: "Phase 03",
    detail: "Integrated automatic library detection, intelligent error classification, and code quality validation."
  },
  {
    title: "Compilation & Output Validation",
    period: "Phase 04",
    detail: "Enabled Arduino CLI verification, structured failure analysis, and clean documentation generation pipeline."
  }
];

export default function Experience() {
  return (
    <section id="experience" className="mx-auto w-full max-w-6xl px-6 py-16">
      <div className="mb-10">
        <div className="text-xs uppercase tracking-[0.3em] text-slate-500">System Timeline</div>
        <h2 className="mt-4 text-3xl font-semibold text-white">Execution state transitions</h2>
      </div>
      <div className="relative border-l border-slate-800/70 pl-6">
        {timeline.map((item, idx) => (
          <motion.div
            key={item.title}
            className="mb-8 rounded-2xl border border-slate-800/70 bg-slate-900/60 p-5"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ type: "spring", stiffness: 120, damping: 18, delay: idx * 0.05 }}
            viewport={{ once: true, amount: 0.4 }}
          >
            <div className="absolute -left-[9px] mt-2 h-4 w-4 rounded-full border border-cyan-400 bg-slate-950" />
            <div className="text-xs uppercase tracking-[0.3em] text-slate-500">{item.period}</div>
            <h3 className="mt-2 text-lg font-semibold text-white">{item.title}</h3>
            <p className="mt-2 text-sm text-slate-400">{item.detail}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
