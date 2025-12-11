# 🔒 KubeZap

> The first GitOps-native security gate that scans every deploy, not every sprint.

## The Problem

- **47 days**: Average MTTR (Mean Time to Remediation) for vulnerabilities.
- **68%** of breaches start with a known but unfixed vulnerability.
- Security scanners usually run in CI (static code) or weekly (runtime), missing the critical deploy window.
- Devs ignore 200-page PDF reports.

## The Solution

**KubeZap** intercepts every ArgoCD/Flux sync, runs a lightning-fast OWASP ZAP scan in runtime, and uses AI to filter noise and generate ready-to-merge fixes.

### Key Features

- ⚡ **Instant Scanning**: Every git push triggers a runtime DAST scan.
- 🤖 **AI Prioritization**: No more 500-item lists. See only the top exploitables.
- 🔧 **Auto-Fix PRs**: One-click generation of NetworkPolicies, WAF rules, and patches.
- 🚫 **Deploy Blocking**: Stop vulnerabilities from reaching production based on Risk Score.
- 📊 **Compliance Reports**: Generate SOC2 and PCI-DSS artifacts instantly.

## Quick Start (< 2 minutes)

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (optional, for local dev)

### Option 1: Docker Compose (Demo)
```bash
git clone https://github.com/yourusername/kubezap
cd kubezap
docker-compose up
# The dashboard will be available at http://localhost:3000
```

### Option 2: Local Dev (No Docker)
```bash
# Setup Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run everything (requires bash)
./start-dev.sh
```

### Option 3: Helm (Production)
```bash
helm repo add kubezap https://charts.kubezap.io
helm install kubezap kubezap/kubezap \
  --set argocd.webhook.secret=your-secret
```

## Architecture

1. **Webhook Receiver**: Listens to ArgoCD/Flux sync events.
2. **Scanner Engine**: Triggers OWASP ZAP against the new pods.
3. **AI Analyzer**: Feeds raw ZAP output to LLM to assess exploitability.
4. **Policy Enforcer**: Blocks the rollout if Score > Threshold.
5. **Dashboard**: Visualizes risk and manages remediation.

## Tech Stack

- **Frontend**: Next.js 14, Tailwind CSS, Shadcn/ui, Recharts.
- **Backend**: FastAPI, Python 3.11, SQLModel.
- **AI**: Integration with OpenAI/Anthropic (Mocked for MVP).

## Roadmap

- [ ] Flux native integration
- [ ] SBOM generation
- [ ] Custom scan policies
- [ ] Terraform provider

## License

Apache 2.0
# kubezap2
