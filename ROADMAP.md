# LLM Firewall Development Roadmap

This roadmap defines the future technical development plan for the LLM Firewall project.

Current baseline already implemented:
- FastAPI backend
- Local Ollama integration with Llama3
- Input sanitization
- Prompt injection detection

## Vision

Build a production-grade, modular LLM security gateway that can protect both local and hosted model backends against prompt injection, jailbreak attempts, and sensitive output leakage while remaining easy to integrate for developers.

## Guiding Principles

- Security first: block unsafe requests before model invocation whenever possible.
- Layered defense: combine rule-based, score-based, and model-based protection.
- Observability by default: every security event should be measurable and auditable.
- Extensible architecture: support local models and external providers through the same firewall interface.
- Developer experience: expose a simple Python SDK and clear integration patterns.

## Roadmap Overview

## Phase 1: Security Enhancements (Near Term)

### 1) Prompt Injection Scoring Engine
Objective:
Replace simple binary keyword matching with a scoring-based prompt risk system.

Planned work:
- Define weighted features (instruction override phrases, roleplay jailbreak cues, policy bypass language, suspicious formatting patterns).
- Compute a cumulative risk score per prompt.
- Set threshold bands:
  - Low risk: allow
  - Medium risk: allow with warning/logging
  - High risk: block
- Add explainable score output for internal logs.

Deliverables:
- New scoring module in security pipeline.
- Configurable thresholds.
- Unit tests for scoring behavior.

### 2) Attack Logging System
Objective:
Record blocked and suspicious prompts for auditing and analysis.

Planned work:
- Write structured JSON entries to logs/attack_logs.json.
- Include fields:
  - timestamp
  - attack_type
  - risk_score
  - source (IP/client id if available)
  - prompt_hash and optional redacted prompt
  - action_taken (blocked/allowed_with_warning)
- Add log rotation strategy for long-running deployments.

Deliverables:
- Logging utility and middleware integration.
- JSON schema for attack events.
- Basic retention policy.

### 3) Rate Limiting
Objective:
Prevent prompt spam and brute-force jailbreak attempts.

Planned work:
- Implement per-client and per-IP request throttling.
- Add burst and sustained rate windows.
- Track repeated high-risk attempts and temporarily ban abusive clients.

Deliverables:
- Configurable rate limiter in security/rate_limiter.py.
- Standard API responses for throttled requests.
- Integration tests for abuse scenarios.

### 4) Output Leak Detection
Objective:
Inspect model responses and block sensitive data leakage.

Planned work:
- Build response filter for secrets, system-prompt leakage patterns, and policy-sensitive strings.
- Add response redaction and blocking modes.
- Tag false positives for tuning.

Deliverables:
- Output filter implementation in security/output_filter.py.
- Detection rules and confidence-based decisions.
- End-to-end tests for response filtering.

## Phase 2: Advanced AI Security (Mid Term)

### 1) AI-Based Prompt Classifier
Objective:
Use an ML model to classify prompts as benign or malicious.

Planned work:
- Evaluate lightweight local classifiers for low-latency inference.
- Train/fine-tune on adversarial prompt examples.
- Fuse model confidence with rule-based score.

Deliverables:
- Classifier service/module integrated into prompt decision flow.
- Evaluation report (precision, recall, false positive rate).
- Fallback behavior when classifier is unavailable.

### 2) Context Firewall
Objective:
Ensure only safe context reaches the model during retrieval and augmentation.

Planned work:
- Introduce document-level filtering before RAG context assembly.
- Apply policy-based allow/deny rules and content sanitization.
- Prevent untrusted documents from injecting hidden instructions.

Deliverables:
- Retrieval filter interface.
- Context trust policy configuration.
- Validation tests with malicious documents.

### 3) Adversarial Prompt Dataset
Objective:
Build and maintain a robust jailbreak and injection dataset for evaluation.

Planned work:
- Expand tests/attack_dataset.txt into categorized datasets:
  - instruction override
  - roleplay jailbreak
  - formatting abuse
  - multilingual jailbreak attempts
- Version and tag datasets for reproducible benchmarks.

Deliverables:
- Curated adversarial dataset files.
- Dataset documentation and usage guidelines.
- Benchmark scripts against detection pipeline.

## Phase 3: Monitoring and Analytics (Mid to Long Term)

Objective:
Provide real-time and historical visibility into firewall effectiveness and latency.

Planned work:
- Implement security telemetry pipeline.
- Build dashboard with key metrics:
  - attacks detected count
  - attack type distribution
  - blocked prompt trends
  - response latency (p50/p95/p99)
- Add alerting for spikes in attack volume and error rates.

Deliverables:
- Dashboard backend API.
- Web dashboard views or Grafana-compatible metrics export.
- Alerting rules and runbook.

## Phase 4: Developer SDK (Long Term)

Objective:
Package firewall logic into a reusable Python library.

Target developer API:

```python
from llm_firewall import SecureLLM

bot = SecureLLM()
bot.chat("Hello")
```

Planned work:
- Refactor core pipeline into installable package modules.
- Expose a stable SecureLLM interface.
- Support pluggable providers (OpenAI-compatible, Ollama local, future providers).
- Publish versioned package with semantic versioning.

Deliverables:
- Python package structure.
- API docs and examples.
- Release pipeline for package publishing.

## Phase 5: Deployment Architecture (Production Readiness)

Target production architecture:

```text
User
  |
  v
API Gateway
  |
  v
LLM Firewall
  |
  v
LLM Provider (OpenAI / Local Model)
  |
  v
Response
```

Planned work:
- Containerized deployment profiles.
- Reverse proxy/API gateway integration.
- Environment-based config for provider selection.
- Horizontal scaling strategy for firewall services.

Deliverables:
- Deployment manifests (Docker and optional Kubernetes).
- Secure secrets management guidance.
- Production operations checklist.

## Phase 6: Testing Framework

Objective:
Automate security regression testing using known adversarial prompts.

Planned work:
- Build an attack simulation runner powered by tests/attack_dataset.txt.
- Add CI workflow to run attack suite on every change.
- Track pass/fail trends and detection regressions.

Deliverables:
- Automated attack simulation test harness.
- CI integration.
- Regression report artifacts.

## Phase 7: Research Extensions

Research directions:
- LLM jailbreak detection methods
- AI red-team automation
- Adversarial prompt generation

Planned work:
- Prototype new detection techniques in isolated experiment modules.
- Measure trade-offs between security, latency, and usability.
- Periodically promote successful experiments into core pipeline.

Deliverables:
- Experimental notebooks/reports.
- Evaluation metrics and comparison baselines.
- Candidate features for future roadmap cycles.

## Milestones and Exit Criteria

Milestone A: Core Security Hardening
- Scoring engine active
- Attack logging enabled
- Rate limiting enforced
- Output leak detection integrated

Milestone B: Intelligent Detection
- AI classifier operational
- Context firewall functional
- Adversarial dataset expanded and benchmarked

Milestone C: Operational Maturity
- Security dashboard and alerts live
- CI attack simulation in place
- Production deployment profile documented

Milestone D: Platform and Ecosystem
- Python SDK released
- Multi-provider support available
- Research loop established for continuous improvement

## Risks and Mitigations

- False positives block valid users:
  Mitigation: use score thresholds, review logs, tune rules with dataset feedback.

- Detection latency increases response time:
  Mitigation: optimize pipeline, add asynchronous logging, cache repeated checks.

- Evolving jailbreak techniques reduce effectiveness:
  Mitigation: continuous dataset updates, AI classifier retraining, red-team automation.

- Operational complexity grows with features:
  Mitigation: modular architecture, clear interfaces, staged rollout by feature flags.

## Contribution Focus Areas

High-priority contribution opportunities:
- Scoring algorithm design and evaluation
- Structured attack logging and analytics schema
- Rate limiter implementation and abuse handling
- Output leakage detection rules and benchmarks
- Automated attack simulation and CI reporting

---

This roadmap is intended to evolve as implementation progresses. Each phase should be delivered with measurable security outcomes, test coverage, and clear operational documentation.
