import React, { useState } from "react";

const articles = [
  {
    title: "AI’s Hidden Security Debt",
    preview: "/assets/preview-mcp.svg",
    description: "How AI-assisted coding can introduce subtle vulnerabilities and security debt.",
    relevance: "Highlights why firmware output must be validated against hidden security debt before release.",
    highlights: [
      "Automated code risks",
      "Security quality blind spots",
      "Hidden vulnerability chains"
    ],
    meta: "The Hacker News · 8 min read",
    url: "https://thehackernews.com/expert-insights/2025/08/ais-hidden-security-debt.html"
  },
  {
    title: "AI Hallucinations Create Supply Chain Threats",
    preview: "/assets/preview-graph.svg",
    description: "Hallucinated code components can propagate into dangerous supply chain weaknesses.",
    relevance: "Reinforces the need for dependency vetting and MCP-level verification in our pipeline.",
    highlights: [
      "Slopsquatting risks",
      "Dependency poisoning",
      "Verification gaps"
    ],
    meta: "Infosecurity Magazine · 6 min read",
    url: "https://www.infosecurity-magazine.com/news/ai-hallucinations-slopsquatting/"
  },
  {
    title: "AI-Generated Code Is Becoming a Major Security Risk",
    preview: "/assets/preview-console.svg",
    description: "AI-generated code can ship subtle defects that appear correct to teams.",
    relevance: "Maps to our quality analysis layer that flags hidden flaws in generated firmware.",
    highlights: [
      "Illusion of correctness",
      "Hidden vulnerability density",
      "Audit pressure"
    ],
    meta: "ITPro · 5 min read",
    url: "https://www.itpro.com/software/development/ai-generated-code-is-fast-becoming-the-biggest-enterprise-security-risk-as-teams-struggle-with-the-illusion-of-correctness"
  },
  {
    title: "AI Tools May Improve Productivity but Risk Developer Skills",
    preview: "/assets/preview-mcp.svg",
    description: "Efficiency gains can come at the cost of foundational debugging skills.",
    relevance: "Supports our emphasis on documentation, traceability, and disciplined review.",
    highlights: [
      "Skill atrophy",
      "Over-trust in AI output",
      "Quality review gaps"
    ],
    meta: "ITPro · 4 min read",
    url: "https://www.itpro.com/software/development/anthropic-research-ai-coding-skills-formation-impact"
  }
];

export default function Projects() {
  const [active, setActive] = useState(articles[0]);

  return (
    <section
      id="news"
      className="relative mx-auto w-full max-w-6xl px-6 py-16"
    >
      <div className="mb-10 flex flex-col gap-4">
        <div className="text-xs uppercase tracking-[0.3em] text-slate-500">System Intelligence News</div>
        <h2 className="text-3xl font-semibold text-white">Latest firmware intelligence articles</h2>
        <p className="max-w-2xl text-slate-400">
          Hover a headline to inspect the live preview. Each article captures key MCP and firmware insights.
        </p>
      </div>
      <div className="grid gap-6 lg:grid-cols-[0.55fr_0.45fr]">
        <div className="space-y-4">
          {articles.map((article) => (
            <a
              key={article.title}
              href={article.url}
              target="_blank"
              rel="noreferrer"
              className="card-glass block cursor-pointer rounded-2xl p-5 transition hover:border-cyan-500/40"
              onMouseEnter={() => setActive(article)}
            >
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Article</div>
                  <h3 className="mt-2 text-lg font-semibold text-white">{article.title}</h3>
                </div>
                <div className="rounded-full border border-slate-700 px-3 py-1 text-xs uppercase tracking-[0.3em] text-slate-400">
                  {article.meta}
                </div>
              </div>
              <p className="mt-3 text-sm text-slate-400">{article.description}</p>
              <div className="mt-4 inline-flex items-center gap-2 text-xs uppercase tracking-[0.3em] text-cyan-200">
                Read article
                <span className="h-1.5 w-1.5 rounded-full bg-cyan-400" />
              </div>
            </a>
          ))}
        </div>
        <div className="card-glass relative min-h-[320px] rounded-3xl p-6">
          <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Article brief</div>
          <div className="mt-3 text-sm text-slate-300">
            {active.description}
            <div className="mt-3 text-sm text-slate-400">
              This analysis surfaces how AI-generated code can introduce security debt and supply-chain blind spots,
              directly reinforcing the need for deterministic firmware validation and MCP-governed review.
            </div>
          </div>
          <div className="mt-4 rounded-2xl border border-slate-800/70 bg-slate-900/70 p-4 text-xs text-slate-300">
            <div className="text-xs uppercase tracking-[0.3em] text-slate-500">Relevance</div>
            <div className="mt-2">{active.relevance}</div>
          </div>
          <div className="mt-4 rounded-2xl border border-slate-800/70 bg-slate-900/70 p-4 text-xs text-slate-400">
            Key highlights
            <ul className="mt-3 space-y-2">
              {active.highlights.map((item) => (
                <li key={item} className="flex items-center gap-2">
                  <span className="h-1.5 w-1.5 rounded-full bg-cyan-400" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
