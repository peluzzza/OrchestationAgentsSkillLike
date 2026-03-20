# Demo Script: Atlas Microservice Orchestration

## Overview
This demo showcases **Atlas**, our AI Orchestrator, building a production-ready Java Microservice using Spring Boot and Hexagonal Architecture. It highlights the seamless transitions between specialized subagents: **Hermes**, **Sisyphus**, and **Argus**, while maintaining synchronization with **Jira**.

---

## 1. Scenario Setup
**Narrative:** We are starting a new "User Management" service. We have a Jira ticket (USER-101) describing the requirements.

**Initial Prompt to Atlas:**
> "Atlas, I need to create a new Spring Boot microservice for User Management based on Jira ticket USER-101. Follow Hexagonal Architecture principles. Start by researching the best libraries for user authentication that fit our enterprise standards."

---

## 2. Orchestration in Action

### Phase A: Research & Design (Hermes)
**Atlas Action:** Delegates to **Hermes**.
*   **Prompt to Hermes:** "Analyze Jira USER-101. Define the Domain Model for 'User' and identify required outbound ports for persistence (PostgreSQL) and inbound ports for REST. Research latest Spring Security best practices for JWT."
*   **Audience Highlight:** *Atlas doesn't just code; it thinks. It validates architectural decisions against enterprise standards before a single line of code is written.*

### Phase B: Implementation (Sisyphus)
**Atlas Action:** Hands the design specs to **Sisyphus**.
*   **Prompt to Sisyphus:** "Generate the project structure using Spring Initializr-like logic. Implement the Domain Layer first, then the Application Layer (Service Ports), and finally the Infrastructure Layer (Adapters). Ensure strict separation of concerns."
*   **Command Example:** `sisyphus --task "Create User entity, repository interface, and REST controller in /src/main/java/com/accenture/usermgmt"`
*   **Audience Highlight:** *Developer productivity. Sisyphus handles the boilerplate and complex mappings, ensuring the Hexagonal boundaries are never breached.*

### Phase C: Quality Assurance & TDD (Argus)
**Atlas Action:** Triggers **Argus** once Sisyphus finishes a module.
*   **Prompt to Argus:** "Write unit tests for the UserService using Mockito. Write integration tests for the REST endpoints using Testcontainers. Verify 80% code coverage."
*   **Command Example:** `argus --test-suite "UserMgmtIntegrationTests" --fix-on-fail`
*   **Audience Highlight:** *Reliability. Argus ensures that the code isn't just generated, but validated. It can even loop back to Sisyphus to fix failed tests automatically.*

---

## 3. Integration & Deployment (Hephaestus)
**Atlas Action:** Prepares for rollout.
*   **Prompt to Hephaestus:** "Generate a Dockerfile and a Kubernetes deployment manifest for this microservice. Add it to the CI/CD pipeline."
*   **Audience Highlight:** *End-to-end automation. From Jira ticket to K8s manifest without manual context switching.*

---

## 4. Why This Matters for Enterprise Developers

### Token Budget Management
Atlas manages the context window efficiently. Instead of feeding 50 files into one LLM call, it breaks tasks down so subagents only see what they need, saving costs and improving accuracy.

### Enforced Architecture (Hexagonal)
Most AI prompts result in "spaghetti code." Atlas is programmed to enforce **Hexagonal Architecture**, ensuring that the domain logic remains isolated from external dependencies like Spring or Hibernate.

### Jira & Atlassian Syncing
Every major milestone is updated in Jira. 
- When Hermes finishes design -> Jira Comment updated with architecture diagram link.
- When Argus passes tests -> Jira Status moved to "Ready for Review".
- **Benefit:** Project managers see real-time progress without bothering developers.

---

## 5. Closing Demo Prompt
**The "One-Click" Finalization:**
> "Atlas, the tests pass. Update USER-101 to 'Done', push the code to Bitbucket, and notify the #user-mgmt-devs Slack channel."

**End of Script.**
