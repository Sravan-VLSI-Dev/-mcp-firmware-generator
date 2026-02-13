import React from "react";

export default function Contact() {
  return (
    <section id="contact" className="relative mx-auto w-full max-w-6xl px-6 py-16">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(34,211,238,0.16),transparent_50%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_30%,rgba(99,102,241,0.18),transparent_55%)]" />
        <div className="absolute bottom-0 left-1/3 h-64 w-64 rounded-full bg-cyan-500/10 blur-3xl" />
      </div>

      <div className="relative grid gap-10 lg:grid-cols-[0.6fr_0.4fr]">
        <div>
          <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Contact</div>
          <h2 className="mt-4 text-3xl font-semibold text-white">Engineer a secure collaboration</h2>
          <p className="mt-3 text-slate-400">
            Describe your firmware pipeline, validation constraints, and deployment targets. We will map a deterministic plan.
          </p>
          <div className="mt-6 space-y-3 text-sm text-slate-300">
            <div className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-4">
              Response window: 24-48 hours
            </div>
            <div className="rounded-2xl border border-slate-800/70 bg-slate-900/60 p-4">
              MCP protocol alignment session
            </div>
          </div>
        </div>
        <div className="card-glass rounded-3xl p-6">
          <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Contributors</div>
          <h3 className="mt-3 text-lg font-semibold text-white">Project LinkedIn profiles</h3>
          <div className="mt-6 grid gap-4">
            {[
              { name: "Sravan N", url: "https://www.linkedin.com/in/sravan-vlsi-dev" },
              { name: "John Victor Jose", url: "https://www.linkedin.com/in/john-victor-jose-028217380/" },
              { name: "Sanjai Kumar Y", url: "https://www.linkedin.com/in/sanjai-kumar-y-8b937a37a/" },
              { name: "Tarun Sam Emmanuel", url: "https://www.linkedin.com/in/tarun-sam-emmanuel-316435317/" }
            ].map((person) => (
              <a
                key={person.name}
                href={person.url}
                className="flex items-center justify-between rounded-2xl border border-slate-800/70 bg-slate-950/70 px-4 py-3 text-sm text-slate-300 transition hover:border-cyan-500/40"
                target="_blank"
                rel="noreferrer"
              >
                <span>{person.name}</span>
                <span className="flex items-center gap-2 rounded-full border border-cyan-500/40 px-3 py-1 text-[10px] uppercase tracking-[0.3em] text-cyan-200">
                  <span className="h-2 w-2 rounded-full bg-cyan-400" />
                  LinkedIn
                </span>
              </a>
            ))}
          </div>
          <div className="mt-6 text-xs text-slate-500">
            Research-grade collaboration, mapped to verified engineering profiles.
          </div>
        </div>
      </div>
    </section>
  );
}
