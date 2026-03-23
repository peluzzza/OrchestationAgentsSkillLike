# Security Workflow

Specialized security compliance and secret detection pack. Provides regulatory compliance auditing and credential scanning to the Atenea security gate.

## Architecture

```
Atenea (L1 God — Security + Safety)
    └── security-workflow pack
        ├── Compliance-Checker  (GDPR, HIPAA, SOC2, PCI-DSS auditing)
        └── Secret-Scanner      (Hardcoded secrets and credential detection)
```

## Agents

| Agent | Role | Invoked By |
|-------|------|-----------|
| **Compliance-Checker** | Regulatory compliance auditing | Atenea |
| **Secret-Scanner** | Detect hardcoded secrets and credentials | Atenea |

## Usage

This pack is invoked by the `Atenea` canonical god agent. It is not user-invocable.

Enable in `.vscode/settings.json`:
```json
"chat.agentFilesLocations": [
  "plugins/security-workflow/agents"
]
```
