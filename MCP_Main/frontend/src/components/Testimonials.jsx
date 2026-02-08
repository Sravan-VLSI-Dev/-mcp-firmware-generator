import React from "react";

const testimonials = [
  {
    name: "Systems Lead",
    detail: "Signal visibility improved firmware regression time by 42%."
  },
  {
    name: "Protocol Engineer",
    detail: "Deterministic orchestration is now a shared, inspectable contract."
  },
  {
    name: "Firmware QA",
    detail: "Quality analysis pipelines catch drift before release gates."
  },
  {
    name: "Embedded Architect",
    detail: "MCP agent flows simplify toolchain reconciliation."
  }
];

export default function Testimonials() {
  const loop = [...testimonials, ...testimonials];

  return (
    <section id="testimonials" className="mx-auto w-full max-w-6xl px-6 pb-16">
      <div className="mb-6">
        <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Operational Reviews</div>
        <h2 className="mt-4 text-3xl font-semibold text-white">Evidence from the field</h2>
      </div>
      <div className="overflow-hidden rounded-2xl border border-slate-800/70 bg-slate-900/60 p-6">
        <div className="marquee">
          {loop.map((item, idx) => (
            <div key={`${item.name}-${idx}`} className="min-w-[240px] rounded-2xl border border-slate-800/70 bg-slate-950/70 p-4">
              <div className="text-xs uppercase tracking-[0.3em] text-slate-500">{item.name}</div>
              <p className="mt-3 text-sm text-slate-300">{item.detail}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
