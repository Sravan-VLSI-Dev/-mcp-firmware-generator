import React from "react";
import { motion, useScroll, useTransform } from "framer-motion";

export default function ParallaxLayers() {
  const { scrollYProgress } = useScroll();
  const layerOne = useTransform(scrollYProgress, [0, 1], [0, -120]);
  const layerTwo = useTransform(scrollYProgress, [0, 1], [0, -220]);
  const layerThree = useTransform(scrollYProgress, [0, 1], [0, -320]);

  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">
      <motion.div
        style={{ y: layerOne }}
        className="absolute -top-20 left-1/2 h-[520px] w-[680px] -translate-x-1/2 rounded-full bg-[radial-gradient(circle_at_center,rgba(99,102,241,0.28),transparent_60%)] blur-3xl"
      />
      <motion.div
        style={{ y: layerTwo }}
        className="absolute right-[-10%] top-12 h-[420px] w-[420px] rounded-full bg-[radial-gradient(circle_at_center,rgba(34,211,238,0.25),transparent_60%)] blur-2xl"
      />
      <motion.div
        style={{ y: layerThree }}
        className="absolute left-[-15%] top-36 h-[360px] w-[520px] rounded-full bg-[radial-gradient(circle_at_center,rgba(129,140,248,0.22),transparent_60%)] blur-2xl"
      />
      <motion.div
        style={{ y: layerTwo }}
        className="absolute bottom-[-120px] left-1/2 h-[360px] w-[760px] -translate-x-1/2 rounded-[40%] border border-slate-700/40 bg-gradient-to-r from-slate-900/60 via-slate-950/40 to-slate-900/60"
      />
      <motion.div
        style={{ y: layerOne }}
        className="absolute inset-x-0 top-0 h-56 code-stream opacity-30"
      />
      <motion.div
        style={{ y: layerThree }}
        className="absolute inset-x-0 bottom-0 h-64 protocol-diagram opacity-40"
      />
    </div>
  );
}
