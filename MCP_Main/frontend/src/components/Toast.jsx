import React from "react";
import { motion } from "framer-motion";

export default function Toast({ message, tone = "info" }) {
  const palette = {
    info: "border-indigo-500/40 text-indigo-200",
    success: "border-cyan-500/40 text-cyan-200",
    error: "border-rose-500/40 text-rose-200"
  };

  return (
    <motion.div
      className={`card-glass rounded-2xl border px-4 py-3 text-sm ${palette[tone]}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      transition={{ type: "spring", stiffness: 120, damping: 18 }}
    >
      {message}
    </motion.div>
  );
}
