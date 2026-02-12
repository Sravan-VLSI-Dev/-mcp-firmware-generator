import React, { useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import api from "../api";

const tabs = ["code", "analysis", "docs"];

export default function CodeGeneration() {
  const [prompt, setPrompt] = useState("");
  const [mode, setMode] = useState("direct");
  const [compile, setCompile] = useState(true);
  const [generateDocs, setGenerateDocs] = useState(true);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [activeTab, setActiveTab] = useState("code");
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [showModal, setShowModal] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const lineCount = useMemo(() => {
    if (!result?.generated_code) return "--";
    return result.generated_code.split("\n").length;
  }, [result]);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError("Please enter a project description.");
      return;
    }
    setError("");
    if (mode === "refined") {
      await fetchQuestions();
      return;
    }
    await generateCode(prompt, null);
  };

  const fetchQuestions = async () => {
    setLoading(true);
    setProgress(10);
    try {
      const response = await api.post(api.clarifyingQuestions, { description: prompt });
      if (!response.ok) throw new Error("Failed to get clarifying questions");
      const data = await response.json();
      setQuestions(data.clarifying_questions || []);
      setAnswers({});
      setShowModal(true);
      setProgress(100);
    } catch (err) {
      setError(err.message || "Error getting clarifying questions");
    }
    setLoading(false);
    setTimeout(() => setProgress(0), 600);
  };

  const submitAnswers = async () => {
    const missing = questions.some((q) => !answers[q]?.trim());
    if (missing) {
      setError("Please answer all questions.");
      return;
    }
    setShowModal(false);
    await generateCode(prompt, answers);
  };

  const generateCode = async (description, refinementAnswers) => {
    setLoading(true);
    setProgress(15);
    setResult(null);

    let current = 15;
    const interval = setInterval(() => {
      current = Math.min(90, current + Math.random() * 18);
      setProgress(current);
    }, 300);

    try {
      const payload = {
        description,
        compile,
        generate_docs: generateDocs,
        context: refinementAnswers ? JSON.stringify(refinementAnswers) : null
      };
      const response = await api.post(api.generateCode, payload);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setResult(data);
      setActiveTab("code");
      setProgress(100);
    } catch (err) {
      setError(err.message || "Generation failed");
    }
    clearInterval(interval);
    setLoading(false);
    setTimeout(() => setProgress(0), 800);
  };

  const downloadDocs = () => {
    if (!result?.documentation) return;
    const docsText = typeof result.documentation === "string"
      ? result.documentation
      : result.documentation?.content || "";
    const element = document.createElement("a");
    element.setAttribute("href", `data:text/markdown;charset=utf-8,${encodeURIComponent(docsText)}`);
    element.setAttribute("download", "firmware_docs.md");
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const compilationReason = useMemo(() => {
    if (!result) return "";
    const raw =
      result.compilation_error_summary ||
      result.error_summary ||
      result.compilation_output ||
      "";

    const lower = raw.toLowerCase();
    if (!lower) return "";
    if (lower.includes("no such file") || lower.includes("not found") || lower.includes("missing")) {
      return "Missing library or header file.";
    }
    if (lower.includes("undefined reference") || lower.includes("undefined symbol")) {
      return "Undefined reference during linking.";
    }
    if (lower.includes("syntax error") || lower.includes("expected") || lower.includes("parse")) {
      return "Syntax error in generated code.";
    }
    if (lower.includes("out of memory") || lower.includes("insufficient")) {
      return "Compilation ran out of memory.";
    }
    if (lower.includes("board") || lower.includes("platform")) {
      return "Board configuration or platform mismatch.";
    }
    return "Compilation failed. Check libraries and configuration.";
  }, [result]);

  return (
    <section id="generator" className="mx-auto w-full max-w-6xl px-6 py-16">
      <div className="mb-10">
        <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Firmware Generator</div>
        <h2 className="mt-4 text-3xl font-semibold text-white">AI-driven code generation</h2>
        <p className="mt-3 max-w-2xl text-slate-400">
          Describe the system behavior. The generator returns code, documentation, and quality analysis.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[0.6fr_0.4fr]">
        <div className="card-glass rounded-3xl p-6">
          <label className="text-xs uppercase tracking-[0.3em] text-slate-500">Description</label>
          <textarea
            className="mt-3 h-40 w-full resize-none rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-sm text-white outline-none focus:border-cyan-500/40"
            placeholder="Example: ESP32 temperature sensor with MQTT publishing and OLED status display"
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
          />
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <label className="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-xs text-slate-300">
              <input type="checkbox" checked={compile} onChange={() => setCompile((prev) => !prev)} />
              Compile code
            </label>
            <label className="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-xs text-slate-300">
              <input type="checkbox" checked={generateDocs} onChange={() => setGenerateDocs((prev) => !prev)} />
              Generate docs
            </label>
          </div>
          <div className="mt-4 flex flex-wrap items-center gap-3">
            <select
              className="rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-xs uppercase tracking-[0.3em] text-slate-300"
              value={mode}
              onChange={(event) => setMode(event.target.value)}
            >
              <option value="direct">Direct generation</option>
              <option value="refined">Refined (clarifying questions)</option>
            </select>
            <button
              className="rounded-xl bg-gradient-to-r from-indigo-500 via-cyan-400 to-indigo-500 px-5 py-3 text-xs font-semibold uppercase tracking-[0.3em] text-slate-950"
              onClick={handleGenerate}
              disabled={loading}
            >
              {loading ? "Processing" : "Generate code"}
            </button>
          </div>
          {error && <div className="mt-4 rounded-xl border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">{error}</div>}
        </div>

        <div className="card-glass rounded-3xl p-6">
          <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Status</div>
          <div className="mt-4 rounded-2xl border border-slate-800/70 bg-slate-950/70 p-4 text-sm text-slate-300">
            {loading ? "Generation in progress..." : "Ready for prompts."}
          </div>
          <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-800">
            <div className="h-full bg-gradient-to-r from-indigo-500 via-cyan-400 to-indigo-500" style={{ width: `${progress}%` }} />
          </div>
          <div className="mt-4 text-xs text-slate-500">Output files are stored in the platformio project folder.</div>
        </div>
      </div>

      <div className="mt-10">
        <div className="flex flex-wrap gap-3">
          {tabs.map((tab) => (
            <button
              key={tab}
              className={`rounded-full px-4 py-2 text-xs uppercase tracking-[0.3em] ${
                activeTab === tab
                  ? "border border-cyan-500/40 bg-cyan-500/10 text-cyan-200"
                  : "border border-slate-800 text-slate-400"
              }`}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>
          ))}
        </div>

        <div
          className={`mt-6 grid gap-6 ${
            activeTab === "docs" ? "grid-cols-1" : "lg:grid-cols-[0.6fr_0.4fr]"
          }`}
        >
          <div className="card-glass rounded-3xl p-6">
            {activeTab === "code" && (
              <pre className="max-h-[420px] overflow-auto whitespace-pre-wrap text-sm text-slate-200">
                {result?.generated_code || "Enter a description and run generation."}
              </pre>
            )}
            {activeTab === "docs" && (
              <div className="space-y-4 text-sm text-slate-300">
                <div className="rounded-2xl border border-slate-800/70 bg-slate-950/70 p-4 text-sm text-slate-200">
                  {result?.documentation
                    ? "Documentation includes: overview, hardware setup, pin configuration, library installation, code walkthrough, troubleshooting, and safety notes."
                    : "Documentation will appear here."}
                </div>
                <button
                  className="rounded-full border border-cyan-500/40 px-4 py-2 text-xs uppercase tracking-[0.3em] text-cyan-200"
                  onClick={downloadDocs}
                >
                  Download docs
                </button>
              </div>
            )}
            {activeTab === "analysis" && (
              <div className="space-y-4 text-sm text-slate-300">
                <div className="grid gap-4 md:grid-cols-3">
                  <div className="rounded-2xl border border-slate-800/70 bg-slate-950/70 p-4">
                    <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Quality</div>
                    <div className="mt-3 text-2xl text-cyan-200">
                      {result?.code_quality_score ?? "--"}
                      {result?.code_quality_score !== undefined ? "/100" : ""}
                    </div>
                  </div>
                  <div className="rounded-2xl border border-slate-800/70 bg-slate-950/70 p-4">
                    <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Memory</div>
                    <div className="mt-3 text-2xl text-indigo-200">
                      {result?.memory_usage !== undefined && result?.memory_usage !== null
                        ? `${result.memory_usage.toFixed(2)}%`
                        : "--"}
                    </div>
                  </div>
                  <div className="rounded-2xl border border-slate-800/70 bg-slate-950/70 p-4">
                    <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Lines</div>
                    <div className="mt-3 text-2xl text-slate-200">{lineCount}</div>
                  </div>
                </div>
                <div className="rounded-2xl border border-slate-800/70 bg-slate-950/70 p-4">
                  <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Issues</div>
                  <div className="mt-3 space-y-2">
                    {result?.quality_issues?.length
                      ? result.quality_issues.map((issue, idx) => (
                          <div key={idx} className="rounded-xl border border-rose-500/40 bg-rose-500/10 px-3 py-2">
                            {typeof issue === "string" ? issue : issue.message || issue.description || JSON.stringify(issue)}
                          </div>
                        ))
                      : <div className="rounded-xl border border-emerald-500/40 bg-emerald-500/10 px-3 py-2">No issues detected</div>}
                  </div>
                </div>
                <div className="rounded-2xl border border-slate-800/70 bg-slate-950/70 p-4">
                  <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Warnings</div>
                  <div className="mt-3 space-y-2">
                    {result?.quality_warnings?.length
                      ? result.quality_warnings.map((issue, idx) => (
                          <div key={idx} className="rounded-xl border border-amber-500/40 bg-amber-500/10 px-3 py-2">
                            {typeof issue === "string" ? issue : issue.message || issue.description || JSON.stringify(issue)}
                          </div>
                        ))
                      : <div className="rounded-xl border border-slate-700 px-3 py-2">No warnings</div>}
                  </div>
                </div>
              </div>
            )}
          </div>
          {activeTab !== "docs" && (
            <div className="card-glass rounded-3xl p-6">
            <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Compilation</div>
            <div className="mt-3 text-sm text-slate-300">
              {result?.compilation_status || "No compilation data yet."}
            </div>
            {result?.compilation_status === "failed" && compilationReason && (
              <div className="mt-3 rounded-xl border border-rose-500/40 bg-rose-500/10 px-3 py-2 text-xs text-rose-200">
                Reason: {compilationReason}
              </div>
            )}
            <div className="mt-4 text-xs text-slate-500">Detected libraries</div>
            <div className="mt-2 flex flex-wrap gap-2 text-xs">
              {result?.detected_libraries?.length
                ? result.detected_libraries.map((lib) => (
                    <span key={lib} className="rounded-full border border-slate-800 px-3 py-1 text-slate-300">
                      {lib}
                    </span>
                  ))
                : <span className="text-slate-500">None reported</span>}
            </div>
            <div className="mt-6 text-xs uppercase tracking-[0.3em] text-slate-500">Install guide</div>
            <pre className="mt-3 max-h-[200px] overflow-auto whitespace-pre-wrap rounded-2xl border border-slate-800/70 bg-slate-950/70 p-3 text-xs text-slate-300">
              {result?.installation_guide || "Installation guide will appear here."}
            </pre>
            </div>
          )}
        </div>
      </div>

      <AnimatePresence>
        {showModal && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ type: "spring", stiffness: 120, damping: 18 }}
          >
            <motion.div
              className="card-glass mx-6 w-full max-w-2xl rounded-3xl p-6"
              initial={{ y: 30, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: 30, opacity: 0 }}
              transition={{ type: "spring", stiffness: 120, damping: 18 }}
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Clarifying questions</div>
                  <h3 className="mt-2 text-xl font-semibold text-white">Provide additional context</h3>
                </div>
                <button
                  className="rounded-full border border-slate-700 px-3 py-1 text-xs uppercase tracking-[0.3em] text-slate-300"
                  onClick={() => setShowModal(false)}
                >
                  Close
                </button>
              </div>
              <div className="mt-6 space-y-4">
                {questions.map((question, idx) => (
                  <div key={question} className="space-y-2">
                    <label className="text-sm text-slate-300">
                      {idx + 1}. {question}
                    </label>
                    <input
                      className="w-full rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-2 text-sm text-white outline-none focus:border-cyan-500/40"
                      value={answers[question] || ""}
                      onChange={(event) =>
                        setAnswers((prev) => ({ ...prev, [question]: event.target.value }))
                      }
                    />
                  </div>
                ))}
              </div>
              <button
                className="mt-6 w-full rounded-xl bg-gradient-to-r from-indigo-500 via-cyan-400 to-indigo-500 px-4 py-3 text-xs font-semibold uppercase tracking-[0.3em] text-slate-950"
                onClick={submitAnswers}
              >
                Generate optimized code
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
}
