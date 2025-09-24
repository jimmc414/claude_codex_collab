# Architecture Design Prompt Template

## Instructions for Claude

Read the requirements document and design a comprehensive architecture that addresses all requirements while following best practices.

## Phase 1: Analysis

Before designing, analyze:
1. **Functional Requirements**: Map each requirement to potential components
2. **Non-Functional Requirements**: Identify architectural patterns that support them
3. **Constraints**: Note technology and platform limitations
4. **Scale Requirements**: Determine if microservices, monolith, or hybrid approach

## Phase 2: Architecture Design

Design the following:

### 2.1 System Overview
- High-level architecture pattern (MVC, Microservices, Event-Driven, etc.)
- Justification for chosen pattern
- System boundaries and interfaces

### 2.2 Component Design
For each major component:
- Purpose and responsibilities
- Interfaces (APIs, events, messages)
- Data it manages
- Dependencies

### 2.3 Data Architecture
- Data models and entities
- Database choice and justification
- Data flow diagrams
- Caching strategy
- Data consistency approach

### 2.4 API Design
- RESTful endpoints or GraphQL schema
- Authentication/Authorization approach
- Rate limiting and throttling
- Versioning strategy

### 2.5 Security Architecture
- Authentication mechanism
- Authorization model (RBAC, ABAC, etc.)
- Data encryption (at rest and in transit)
- Security headers and CSP
- Threat model considerations

### 2.6 Infrastructure
- Deployment architecture (containers, serverless, VMs)
- Scaling strategy (horizontal/vertical)
- Load balancing approach
- Monitoring and logging
- Disaster recovery plan

## Architecture Document Format

```markdown
# System Architecture: [Project Name]

## 1. Executive Summary
[Brief overview of architectural approach and key decisions]

## 2. Architecture Principles
- [Principle 1]: [Description]
- [Principle 2]: [Description]

## 3. System Overview

### 3.1 Architecture Pattern
[Chosen pattern and justification]

### 3.2 High-Level Diagram
\`\`\`mermaid
graph TB
    A[Client] --> B[API Gateway]
    B --> C[Service 1]
    B --> D[Service 2]
    C --> E[Database]
    D --> E
\`\`\`

## 4. Component Design

### 4.1 [Component Name]
**Purpose**: [Description]
**Responsibilities**:
- [Responsibility 1]
- [Responsibility 2]

**Interfaces**:
- [Interface 1]: [Description]

**Dependencies**:
- [Dependency 1]

## 5. Data Model

### 5.1 Entity Relationship Diagram
\`\`\`mermaid
erDiagram
    User ||--o{ Order : places
    Order ||--|{ OrderItem : contains
    Product ||--o{ OrderItem : includes
\`\`\`

### 5.2 Database Schema
[Table definitions and relationships]

## 6. API Design

### 6.1 RESTful Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET    | /api/v1/users | List users | Yes |
| POST   | /api/v1/users | Create user | Yes |

### 6.2 API Authentication
[Authentication approach]

## 7. Security Architecture

### 7.1 Authentication Flow
[Description and diagram]

### 7.2 Authorization Model
[RBAC/ABAC details]

### 7.3 Security Measures
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF tokens

## 8. Deployment Architecture

### 8.1 Infrastructure Diagram
\`\`\`mermaid
graph LR
    A[Load Balancer] --> B[Web Server 1]
    A --> C[Web Server 2]
    B --> D[App Server 1]
    C --> E[App Server 2]
    D --> F[Database Primary]
    E --> G[Database Replica]
\`\`\`

### 8.2 Scaling Strategy
[Horizontal/Vertical scaling approach]

## 9. Technology Stack

| Layer | Technology | Justification |
|-------|------------|---------------|
| Frontend | [Tech] | [Reason] |
| Backend | [Tech] | [Reason] |
| Database | [Tech] | [Reason] |
| Cache | [Tech] | [Reason] |

## 10. Cross-Cutting Concerns

### 10.1 Logging
[Logging strategy and tools]

### 10.2 Monitoring
[Monitoring approach and metrics]

### 10.3 Error Handling
[Error handling strategy]

## 11. Architecture Decision Records (ADRs)

### ADR-1: [Decision Title]
**Status**: Accepted
**Context**: [Why this decision was needed]
**Decision**: [What was decided]
**Consequences**: [Impact of the decision]
```

## Validation Checklist

Before finalizing architecture:
- [ ] All functional requirements are addressed
- [ ] Non-functional requirements are met
- [ ] Security concerns are addressed
- [ ] Scalability is built-in
- [ ] Technology choices are justified
- [ ] Deployment strategy is clear
- [ ] Monitoring and observability are planned
- [ ] Disaster recovery is considered
- [ ] Cost implications are understood

## Requirements Alignment

For each requirement in requirements.md:
1. Identify which component addresses it
2. Explain how the architecture supports it
3. Note any trade-offs made

## Interactive Flow

1. Start by reading requirements.md
2. Identify key architectural drivers
3. Propose 2-3 architectural options
4. Discuss trade-offs with the user
5. Design detailed architecture based on selection
6. Generate comprehensive architecture document
7. Ensure all requirements are mapped to components