import React from "react";

const items = [
  {
    title: "Quality Analysis",
    detail: "Identify hidden risks in generated firmware: regression gaps, lint drift, and policy violations.",
    status: "Verified"
  },
  {
    title: "Code",
    detail: "Translate requirements into deterministic, board-aware firmware that remains readable and auditable.",
    status: "Tracked"
  },
  {
    title: "Docs",
    detail: "Explain why each decision exists: architecture rationale, runbooks, and MCP flow proofs.",
    status: "Synchronized"
  },
  {
    title: "Hardware",
    detail: "Connect firmware to physical reality: MCU profiles, IO maps, and signal integrity checks.",
    status: "Provisioned"
  }
];

export default function QualityGrid() {
  return (
    <section className="mx-auto w-full max-w-6xl px-6 py-12">
      <div className="mb-6 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <div className="text-xs uppercase tracking-[0.3em] text-slate-500">State</div>
          <h3 className="mt-2 text-2xl font-semibold text-white">Operational assurance layer</h3>
        </div>
        <p className="max-w-xl text-sm text-slate-400">
          This layer ties firmware generation to measurable guarantees: quality gates, code traceability, documentation
          integrity, and hardware-aligned validation before release.
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-4">
        {items.map((item) => (
          <div key={item.title} className="card-glass rounded-2xl p-4">
            <div className="text-xs uppercase tracking-[0.3em] text-slate-500">{item.title}</div>
            <div className="mt-3 text-sm text-slate-300">{item.detail}</div>
            <div className="mt-4 inline-flex items-center gap-2 rounded-full border border-slate-800/70 bg-slate-900/60 px-3 py-1 text-[10px] uppercase tracking-[0.3em] text-cyan-200">
              {item.status}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
