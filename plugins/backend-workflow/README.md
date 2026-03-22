# Backend Workflow

A specialized multi-agent orchestration system for backend development, following the bigguy345/Atlas conductor pattern.

## Architecture

```
Backend-Atlas (Conductor - User Visible)
    ├── Backend-Planner (Autonomous Planning)
    ├── API-Designer (REST/GraphQL Design)
    ├── Database-Engineer (Schema & Migrations)
    ├── Security-Guard (Auth & Security)
    ├── Service-Builder (TDD Implementation)
    ├── Performance-Tuner (Optimization)
    └── Backend-Reviewer (Code Review Gate)
    
    Handoffs → Afrodita, DevOps-Atlas, Data-Atlas
```

## Agents

| Agent | Role | Model |
|-------|------|-------|
| **Backend-Atlas** | Conductor - orchestrates the team | GPT-5.4 |
| **Backend-Planner** | Autonomous planning for complex tasks | GPT-5.4 |
| **API-Designer** | REST/GraphQL endpoint design | GPT-5.4 |
| **Database-Engineer** | Schema, migrations, queries | Claude Opus 4.6 |
| **Security-Guard** | Auth, authz, OWASP compliance | Claude Opus 4.6 |
| **Service-Builder** | TDD service implementation | Claude Opus 4.6 |
| **Performance-Tuner** | Query optimization, caching | Claude Opus 4.6 |
| **Backend-Reviewer** | Code review gate | GPT-5.3-Codex |

## Workflow

1. **Planning Phase** (for complex tasks)
   - `Backend-Planner` researches and creates phased plan
   - User reviews and approves plan

2. **Design Phase**
   - `API-Designer` creates endpoint specifications
   - `Database-Engineer` designs schema and migrations
   - `Security-Guard` defines auth/authz patterns
   - User approves API contract

3. **Implementation Phase**
   - `Service-Builder` implements with TDD (tests first)
   - `Performance-Tuner` optimizes queries and caching

3. **Review Phase**
   - `Backend-Reviewer` validates code quality and security
   - Returns: APPROVED | NEEDS_REVISION | FAILED

4. **Verification**
   - Integration tests pass
   - Security audit complete
   - Performance benchmarks met

## Usage

```
@Backend-Atlas Add user registration with email verification
```

Backend-Atlas will:
1. Delegate API design to API-Designer
2. Create schema with Database-Engineer
3. Implement auth with Security-Guard
4. Build services via Service-Builder
5. Code review via Backend-Reviewer
6. Return completion summary

## Security Standards

All backend code must:
- Follow OWASP Top 10 guidelines
- Use proper authentication (JWT/OAuth2)
- Implement authorization checks
- Validate and sanitize all input
- Use parameterized queries
- Log security events

## Stack Support

- **Java**: Spring Boot, JPA/Hibernate
- **Node.js**: Express, NestJS, Prisma
- **Python**: FastAPI, Django, SQLAlchemy
- **Database**: PostgreSQL, MySQL, MongoDB
- **Auth**: JWT, OAuth2, OIDC

## Installation

Copy the `agents/` folder to your workspace or VS Code prompts directory.
