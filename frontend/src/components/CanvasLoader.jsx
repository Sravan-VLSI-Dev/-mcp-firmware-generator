import React from "react";
import { Html, useProgress } from "@react-three/drei";

export default function CanvasLoader({ label = "Initializing" }) {
  const { progress } = useProgress();
  return (
    <Html center>
      <div className="card-glass rounded-xl px-5 py-4 text-xs uppercase tracking-[0.3em] text-slate-200">
        <div className="mb-2 text-[10px] text-slate-400">{label}</div>
        <div className="h-1.5 w-40 overflow-hidden rounded-full bg-slate-800">
          <div
            className="h-full bg-gradient-to-r from-indigo-500 via-cyan-400 to-indigo-500"
            style={{ width: `${Math.round(progress)}%` }}
          />
        </div>
        <div className="mt-2 text-right text-[10px] text-slate-500">
          {Math.round(progress)}%
        </div>
      </div>
    </Html>
  );
}
