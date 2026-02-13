import React from "react";

const links = [
  { label: "Research Notes", href: "#" },
  { label: "Protocol Spec", href: "#" },
  { label: "Security Brief", href: "#" }
];

export default function Footer() {
  return (
    <footer className="mt-10 border-t border-slate-800/60 px-6 py-10">
      <div className="mx-auto w-full max-w-6xl">
        <div className="gradient-divider mb-8" />
        <div className="flex flex-col items-start justify-between gap-6 md:flex-row md:items-center">
          <div>
            <div className="text-xs uppercase tracking-[0.3em] text-slate-500">MCP Firmware Intelligence</div>
            <div className="mt-2 text-sm text-slate-400">System-level AI portfolio and firmware orchestration.</div>
          </div>
          <div className="flex flex-wrap gap-4 text-xs uppercase tracking-[0.3em] text-slate-400">
            {links.map((link) => (
              <a key={link.label} href={link.href} className="transition hover:text-white">
                {link.label}
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
