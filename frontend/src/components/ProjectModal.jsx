import React from "react";
import { motion } from "framer-motion";

export default function ProjectModal({ project, onClose }) {
  return (
    <motion.div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 backdrop-blur"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ type: "spring", stiffness: 120, damping: 18 }}
      onClick={onClose}
    >
      <motion.div
        className="card-glass mx-6 w-full max-w-2xl rounded-3xl p-6"
        initial={{ y: 40, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: 40, opacity: 0 }}
        transition={{ type: "spring", stiffness: 120, damping: 18 }}
        onClick={(event) => event.stopPropagation()}
      >
        <div className="flex items-start justify-between">
          <div>
            <div className="text-xs uppercase tracking-[0.3em] text-slate-500">System</div>
            <h3 className="mt-2 text-2xl font-semibold text-white">{project.title}</h3>
          </div>
          <button
            className="rounded-full border border-slate-700 px-3 py-1 text-xs uppercase tracking-[0.3em] text-slate-300"
            onClick={onClose}
          >
            Close
          </button>
        </div>
        <p className="mt-4 text-sm text-slate-300">{project.description}</p>
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <div className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-4">
            <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Architecture</div>
            <ul className="mt-3 space-y-2 text-sm text-slate-300">
              {project.architecture.map((item) => (
                <li key={item} className="flex items-center gap-2">
                  <span className="h-1.5 w-1.5 rounded-full bg-cyan-400" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-4">
            <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Tech stack</div>
            <div className="mt-3 flex flex-wrap gap-2 text-xs text-slate-300">
              {project.stack.map((item) => (
                <span key={item} className="rounded-full border border-slate-700/70 px-3 py-1">
                  {item}
                </span>
              ))}
            </div>
          </div>
        </div>
        <div className="mt-6 flex flex-wrap gap-3 text-xs uppercase tracking-[0.3em] text-cyan-200">
          <span className="rounded-full border border-cyan-500/30 px-3 py-1">Demo ready</span>
          <span className="rounded-full border border-indigo-500/30 px-3 py-1">Repo mirrored</span>
        </div>
      </motion.div>
    </motion.div>
  );
}
