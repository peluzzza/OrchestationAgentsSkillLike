# DevOps Workflow

A specialized multi-agent orchestration system for DevOps, following the bigguy345/Atlas conductor pattern.

## Architecture

```
DevOps-Atlas (Conductor - User Visible)
    ├── DevOps-Planner (Autonomous Planning)
    ├── Infra-Architect (Terraform/Pulumi/IaC)
    ├── Pipeline-Engineer (CI/CD Automation)
    ├── Container-Master (Docker/Kubernetes)
    ├── Monitor-Sentinel (Observability)
    ├── Security-Ops (DevSecOps)
    └── Deploy-Strategist (Release Strategies)
    
    Handoffs → Backend-Atlas, Afrodita, Data-Atlas
```

## Agents

| Agent | Role | Model |
|-------|------|-------|
| **DevOps-Atlas** | Conductor - orchestrates the team | GPT-5.4 |
| **DevOps-Planner** | Autonomous planning for complex tasks | GPT-5.4 |
| **Infra-Architect** | IaC with Terraform/Pulumi | GPT-5.4 |
| **Pipeline-Engineer** | CI/CD pipelines | Claude Opus 4.6 |
| **Container-Master** | Docker & Kubernetes | Claude Opus 4.6 |
| **Monitor-Sentinel** | Monitoring & alerting | Claude Opus 4.6 |
| **Security-Ops** | Security scanning & compliance | Claude Opus 4.6 |
| **Deploy-Strategist** | Deployment strategies | GPT-5.4 |

## Workflow

1. **Planning Phase** (for complex tasks)
   - `DevOps-Planner` researches and creates phased plan
   - User reviews and approves infrastructure plan

2. **Design Phase**
   - `Infra-Architect` designs cloud infrastructure
   - `Pipeline-Engineer` designs CI/CD workflows
   - `Container-Master` designs container strategy
   - User approves infrastructure plan

3. **Implementation Phase**
   - Execute IaC with proper state management
   - Build container images and K8s manifests
   - Configure pipelines with quality gates

3. **Security Phase**
   - `Security-Ops` scans for vulnerabilities
   - Compliance verification
   - Security gates in pipeline

4. **Observability Phase**
   - `Monitor-Sentinel` sets up monitoring
   - Dashboards and alerting
   - SLI/SLO definition

5. **Deployment Phase**
   - `Deploy-Strategist` implements release strategy
   - Test in staging
   - Production deployment with rollback plan

## Usage

```
@DevOps-Atlas Set up Kubernetes infrastructure for our microservices with CI/CD
```

DevOps-Atlas will:
1. Design infrastructure with Infra-Architect
2. Create K8s manifests with Container-Master
3. Set up pipelines with Pipeline-Engineer
4. Configure monitoring with Monitor-Sentinel
5. Add security scanning with Security-Ops
6. Plan deployment strategy with Deploy-Strategist

## Supported Platforms

### Cloud
- AWS (EKS, ECR, RDS, etc.)
- GCP (GKE, GCR, Cloud SQL, etc.)
- Azure (AKS, ACR, Azure SQL, etc.)

### CI/CD
- GitHub Actions
- GitLab CI
- Jenkins
- Azure DevOps
- ArgoCD

### Observability
- Prometheus + Grafana
- Datadog
- CloudWatch
- ELK Stack
- OpenTelemetry

## Best Practices

All DevOps configurations must:
- Use Infrastructure as Code
- Implement security scanning in pipelines
- Follow least privilege for IAM
- Use multi-stage Docker builds
- Implement proper health checks
- Have rollback procedures

## Installation

Copy the `agents/` folder to your workspace or VS Code prompts directory.
