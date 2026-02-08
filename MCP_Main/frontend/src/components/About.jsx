import React, { useRef } from "react";
import { motion } from "framer-motion";
import SystemGraphCanvas from "./SystemGraphCanvas";
import OrbitingStack from "./OrbitingStack";

const blocks = [
  { title: "MCP", detail: "Agent protocol coordination" },
  { title: "Firmware Layers", detail: "Boot, HAL, RTOS, IO" },
  { title: "Toolchains", detail: "Build, validate, deploy" },
  { title: "AI Agents", detail: "Deterministic planners" }
];

export default function About() {
  const constraintRef = useRef(null);

  return (
    <section id="about" className="relative mx-auto w-full max-w-6xl px-6 py-16">
      <div className="mb-10 flex flex-col gap-4">
        <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Systems Overview</div>
        <h2 className="text-3xl font-semibold text-white">Composable intelligence blocks</h2>
        <p className="max-w-2xl text-slate-400">
          Modular firmware primitives, protocol-aware orchestration, and MCP pipelines working in a single
          deterministic environment.
        </p>
      </div>

      <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-6">
          <div className="card-glass scanline rounded-3xl p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-xs uppercase tracking-[0.3em] text-slate-500">System graph</div>
                <h3 className="text-xl font-semibold text-white">Neural protocol mesh</h3>
              </div>
              <div className="rounded-full border border-slate-700/60 px-3 py-1 text-xs text-slate-400">
                Live sync
              </div>
            </div>
            <div className="mt-4 min-h-[240px] overflow-hidden rounded-2xl border border-slate-800/60 bg-slate-950/40 p-3">
              <SystemGraphCanvas />
            </div>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <div className="card-glass rounded-3xl p-6">
              <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Tooling orbit</div>
              <h3 className="mt-2 text-lg font-semibold text-white">Stack alignment</h3>
              <p className="mt-2 text-sm text-slate-400">
                Observe how core tooling stays synchronized with the MCP runtime as it rotates.
              </p>
              <div className="mt-4 rounded-2xl border border-slate-800/60 bg-slate-950/40 p-4">
                <div className="scale-110">
                  <OrbitingStack />
                </div>
              </div>
            </div>

            <div className="card-glass rounded-3xl p-6">
              <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Orchestration</div>
              <h3 className="mt-2 text-lg font-semibold text-white">Draggable system blocks</h3>
              <p className="mt-2 text-sm text-slate-400">
                Test dependency adjacency between MCP, firmware layers, and agent planners.
              </p>
              <div ref={constraintRef} className="relative mt-4 h-52 rounded-2xl border border-slate-800/60 p-3">
                <div className="grid h-full grid-cols-2 gap-3">
                  {blocks.map((block) => (
                    <motion.div
                      key={block.title}
                      drag
                      dragConstraints={constraintRef}
                      dragElastic={0.2}
                      dragTransition={{ bounceStiffness: 240, bounceDamping: 18 }}
                      className="flex items-center justify-center rounded-xl border border-slate-700/70 bg-slate-900/80 px-3 py-2 text-xs text-slate-200"
                    >
                      <div className="text-center">
                        <div className="text-[10px] uppercase tracking-[0.2em] text-slate-400">{block.title}</div>
                        <div className="font-semibold text-white">{block.detail}</div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="card-glass rounded-3xl p-6">
          <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Firmware disciplines</div>
          <h3 className="mt-2 text-xl font-semibold text-white">Deterministic control planes</h3>
          <p className="mt-4 text-sm text-slate-400">
            Built to audit toolchain decisions, validate execution branches, and preserve signal fidelity across
            microcontroller fleets.
          </p>
          <ul className="mt-6 space-y-3 text-sm text-slate-300">
            <li className="flex items-center gap-3">
              <span className="h-2 w-2 rounded-full bg-cyan-400" />
              Protocol schemas versioned per release train.
            </li>
            <li className="flex items-center gap-3">
              <span className="h-2 w-2 rounded-full bg-indigo-400" />
              Firmware blocks validated with AI-guided tests.
            </li>
            <li className="flex items-center gap-3">
              <span className="h-2 w-2 rounded-full bg-slate-500" />
              MCP agents coordinate deterministic rollouts.
            </li>
          </ul>
        </div>
      </div>
    </section>
  );
}
