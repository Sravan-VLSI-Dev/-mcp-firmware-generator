import React from "react";
import "./TaglineSection.css";

const TaglineSection = () => {
  return (
    <div className="tagline-card">
      <div className="tagline-content">
        <h3>System-grade firmware intelligence</h3>
        <p>Deterministic operations, protocol-aware tooling, and traceable decision graphs.</p>
        <div className="company-badge">
          <span className="powered-by">Powered by</span>
          <span className="company-name">MCP Systems</span>
        </div>
      </div>
    </div>
  );
};

export default TaglineSection;
