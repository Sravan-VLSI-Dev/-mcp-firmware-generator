import React, { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { twMerge } from "tailwind-merge";

const links = [
  { label: "Core", href: "#core" },
  { label: "About", href: "#about" },
  { label: "Generate", href: "#generator" },
  { label: "News", href: "#news" },
  { label: "Contact", href: "#contact" }
];

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800/60 bg-slate-950/70 backdrop-blur">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-br from-indigo-500 via-slate-900 to-cyan-400 p-[1px]">
            <div className="flex h-full w-full items-center justify-center rounded-[10px] bg-slate-950 text-xs font-semibold text-cyan-200">
              MCP
            </div>
          </div>
          <div>
            <div className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-300">Firmware</div>
            <div className="text-lg font-semibold text-white">Systems Intelligence</div>
          </div>
        </div>
        <nav className="hidden items-center gap-6 text-sm text-slate-300 md:flex">
          {links.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="transition hover:text-white"
              onClick={(event) => {
                event.preventDefault();
                const target = document.querySelector(link.href);
                if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
              }}
            >
              {link.label}
            </a>
          ))}
        </nav>
        <button
          className="md:hidden rounded-full border border-slate-700 px-3 py-2 text-xs uppercase tracking-[0.2em] text-slate-300"
          onClick={() => setOpen((prev) => !prev)}
          aria-expanded={open}
        >
          Menu
        </button>
      </div>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ type: "spring", stiffness: 120, damping: 18 }}
            className={twMerge("border-t border-slate-800 bg-slate-950/90 px-6 py-4 md:hidden")}
          >
            <div className="flex flex-col gap-4 text-sm text-slate-300">
              {links.map((link) => (
                <a
                  key={link.href}
                  href={link.href}
                  className="transition hover:text-white"
                  onClick={(event) => {
                    event.preventDefault();
                    const target = document.querySelector(link.href);
                    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
                    setOpen(false);
                  }}
                >
                  {link.label}
                </a>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
