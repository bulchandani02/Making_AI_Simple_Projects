# TechCorp Platform Technical Architecture
**Version 3.1 | Last Updated: January 2025**
**Classification: Internal Use Only**

---

## 1. System Overview

### 1.1 Platform Summary

TechCorp Platform is a cloud-native, AI-powered enterprise software solution that helps businesses automate workflows, analyze data, and integrate systems.

**Key Statistics**:
- 500+ enterprise customers
- 2 million daily active users
- 99.95% uptime SLA
- Processing 50 million API requests/day
- 10 petabytes of customer data under management

### 1.2 Architecture Principles

1. **Cloud-Native**: Designed for Kubernetes, auto-scaling by default
2. **API-First**: Every capability exposed via REST and GraphQL APIs
3. **Multi-Tenant**: Single codebase serves all customers with data isolation
4. **Event-Driven**: Asynchronous processing for scalability
5. **Security by Design**: Zero-trust architecture, encrypted everywhere

---

## 2. Infrastructure

### 2.1 Cloud Providers

**Primary**: Amazon Web Services (AWS) — US and EU regions
**Secondary**: Microsoft Azure — APAC regions, specific enterprise requirements

| Region | Cloud | Purpose |
|--------|-------|---------|
| us-east-1 | AWS | Primary US, main databases |
| us-west-2 | AWS | US failover, DR |
| eu-west-1 | AWS | EU customers (GDPR) |
| ap-southeast-1 | Azure | APAC customers |

### 2.2 Kubernetes Clusters

All services run on Amazon EKS (AWS) or AKS (Azure).

**Cluster Configuration**:
- Production: 3 clusters (us-east, eu-west, ap-southeast)
- Staging: 1 cluster (us-east)
- Development: 1 cluster (us-west)

**Node Pools**:
| Pool | Instance Type | Count | Purpose |
|------|---------------|-------|---------|
| general | m6i.2xlarge | 20-50 | API services |
| compute | c6i.4xlarge | 10-30 | Data processing |
| memory | r6i.4xlarge | 5-15 | Caching, search |
| gpu | p4d.24xlarge | 2-8 | ML inference |

### 2.3 Networking

**VPC Design**: Hub-and-spoke model with Transit Gateway

**Security Groups**:
- Public-facing: ALB only, ports 443
- Application tier: Internal only, cluster-to-cluster
- Data tier: Database-specific, no direct access

**DNS**: Route 53 with latency-based routing

---

## 3. Core Services

### 3.1 Service Catalog

| Service | Language | Database | Owner Team |
|---------|----------|----------|------------|
| api-gateway | Go | Redis | Platform |
| auth-service | Go | PostgreSQL | Security |
| user-service | Python | PostgreSQL | Platform |
| workflow-engine | Java | PostgreSQL, Redis | Workflows |
| analytics-service | Python | ClickHouse | Data |
| notification-service | Node.js | MongoDB | Platform |
| search-service | Python | Elasticsearch | Search |
| ml-inference | Python | Redis | AI/ML |
| billing-service | Go | PostgreSQL | Billing |
| integration-hub | Java | PostgreSQL | Integrations |

### 3.2 API Gateway

**Technology**: Kong Gateway (Enterprise)

**Features**:
- Rate limiting: 1000 req/min (standard), 10000 req/min (enterprise)
- Authentication: OAuth 2.0, API keys, SAML
- Request/response transformation
- Circuit breaker pattern

**Endpoints**:
- Production: https://api.techcorp.com
- Staging: https://api.staging.techcorp.com
- Sandbox: https://api.sandbox.techcorp.com

**Rate Limits by Plan**:
| Plan | Requests/min | Requests/day |
|------|--------------|--------------|
| Free | 100 | 10,000 |
| Starter | 500 | 50,000 |
| Professional | 2,000 | 500,000 |
| Enterprise | 10,000 | Unlimited |

### 3.3 Authentication Service

**Stack**: Go, PostgreSQL, Redis

**Supported Auth Methods**:
- Username/password with MFA
- SSO via SAML 2.0 (Okta, Azure AD, OneLogin)
- OAuth 2.0 (Google, Microsoft, GitHub)
- API keys for service-to-service

**Token Management**:
- Access tokens: JWT, 15-minute expiry
- Refresh tokens: Opaque, 7-day expiry
- API keys: No expiry, revocable

**Session Limits**:
- Maximum 5 concurrent sessions per user
- Session timeout: 8 hours inactive
- Forced re-auth: Every 24 hours

### 3.4 Workflow Engine

**Stack**: Java 17, Spring Boot, PostgreSQL, Redis

**Capabilities**:
- Visual workflow builder
- 100+ pre-built connectors
- Conditional branching, loops
- Error handling and retry logic
- Scheduled and event-triggered execution

**Limits**:
| Plan | Workflows | Executions/month | Steps/workflow |
|------|-----------|------------------|----------------|
| Starter | 10 | 5,000 | 20 |
| Professional | 100 | 100,000 | 100 |
| Enterprise | Unlimited | Unlimited | 500 |

**Execution SLAs**:
- Workflow start: < 500ms from trigger
- Step execution: < 2s for standard steps
- End-to-end: Depends on workflow complexity

### 3.5 ML Inference Service

**Stack**: Python 3.11, FastAPI, PyTorch, Redis

**Available Models**:
| Model | Purpose | Latency (p99) | Cost/1K requests |
|-------|---------|---------------|------------------|
| text-classifier-v2 | Document classification | 50ms | $0.10 |
| sentiment-v3 | Sentiment analysis | 30ms | $0.05 |
| ner-v2 | Named entity recognition | 80ms | $0.15 |
| summarizer-v1 | Text summarization | 500ms | $0.50 |
| embeddings-v2 | Text embeddings | 20ms | $0.02 |

**Scaling**:
- Auto-scales 2-8 GPU nodes based on queue depth
- Cold start: ~30 seconds
- Warm inference: < 100ms

---

## 4. Data Architecture

### 4.1 Databases

**PostgreSQL** (Primary transactional database)
- Version: 15.4
- Deployment: AWS RDS Multi-AZ
- Instance: db.r6g.2xlarge
- Storage: 2TB gp3, auto-scaling to 10TB
- Backups: Daily snapshots, 30-day retention
- Replication: 2 read replicas per region

**Redis** (Caching and queues)
- Version: 7.0
- Deployment: AWS ElastiCache
- Cluster mode: Enabled, 6 shards
- Instance: cache.r6g.xlarge
- Use cases: Session cache, rate limiting, job queues

**ClickHouse** (Analytics)
- Version: 23.8
- Deployment: Self-managed on EC2
- Cluster: 6 nodes, 3 shards, 2 replicas
- Storage: 50TB per node
- Use case: Product analytics, audit logs

**Elasticsearch** (Search)
- Version: 8.11
- Deployment: AWS OpenSearch
- Cluster: 9 nodes (3 master, 6 data)
- Storage: 10TB total
- Use case: Full-text search, log aggregation

**MongoDB** (Document store)
- Version: 7.0
- Deployment: MongoDB Atlas
- Cluster: M40 dedicated
- Use case: Notifications, user preferences, flexible schemas

### 4.2 Data Flow

```
User Request → API Gateway → Service → Database
                    ↓
              Event Bus (Kafka)
                    ↓
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
Analytics    Notifications    Audit Log
(ClickHouse)    (MongoDB)    (Elasticsearch)
```

### 4.3 Data Retention

| Data Type | Retention | Storage |
|-----------|-----------|---------|
| User data | Account lifetime + 90 days | PostgreSQL |
| Workflow logs | 90 days | ClickHouse |
| Audit logs | 7 years | S3 + Elasticsearch |
| Analytics | 2 years | ClickHouse |
| Session data | 7 days | Redis |
| Temp files | 24 hours | S3 |

### 4.4 Backup & Recovery

**RPO (Recovery Point Objective)**: 1 hour
**RTO (Recovery Time Objective)**: 4 hours

**Backup Strategy**:
- PostgreSQL: Continuous WAL archiving + daily snapshots
- Redis: Hourly RDB snapshots
- ClickHouse: Daily backups to S3
- Elasticsearch: Daily snapshots

**Disaster Recovery**:
- Active-passive setup: us-west-2 as DR site
- Failover: Manual, 2-hour process
- DR testing: Quarterly

---

## 5. Event-Driven Architecture

### 5.1 Message Broker

**Technology**: Apache Kafka (AWS MSK)

**Configuration**:
- Brokers: 6 (3 AZs × 2 brokers)
- Version: 3.5.1
- Retention: 7 days default
- Partitions: Varies by topic (12-48)

**Key Topics**:
| Topic | Partitions | Consumers | Events/sec |
|-------|------------|-----------|------------|
| user-events | 24 | 8 | 5,000 |
| workflow-events | 48 | 16 | 20,000 |
| analytics-events | 48 | 12 | 50,000 |
| notification-events | 12 | 4 | 2,000 |
| audit-events | 24 | 6 | 10,000 |

### 5.2 Event Schema

All events follow CloudEvents specification.

**Example Event**:
```json
{
  "specversion": "1.0",
  "type": "com.techcorp.workflow.completed",
  "source": "/workflows/wf_abc123",
  "id": "evt_xyz789",
  "time": "2025-01-15T10:30:00Z",
  "datacontenttype": "application/json",
  "data": {
    "workflow_id": "wf_abc123",
    "status": "completed",
    "duration_ms": 1234,
    "steps_executed": 5
  }
}
```

---

## 6. Security Architecture

### 6.1 Authentication & Authorization

**Identity Provider**: Auth0 (primary), SAML/OIDC federation

**Authorization Model**: RBAC + ABAC hybrid

**Default Roles**:
| Role | Permissions |
|------|-------------|
| Viewer | Read-only access to assigned resources |
| Editor | Create, edit, delete assigned resources |
| Admin | Full access to organization |
| Owner | Admin + billing + user management |

### 6.2 Data Encryption

**In Transit**: TLS 1.3 everywhere, minimum TLS 1.2

**At Rest**:
- AWS S3: SSE-S3 (AES-256)
- RDS: AWS KMS (customer-managed keys available)
- Redis: At-rest encryption enabled
- Elasticsearch: Encrypted volumes

**Application-Level**:
- PII fields: AES-256-GCM with per-tenant keys
- Secrets: HashiCorp Vault

### 6.3 Network Security

**WAF**: AWS WAF with managed rule sets
- OWASP Top 10 protection
- Rate limiting
- Geo-blocking (configurable)
- Bot detection

**DDoS Protection**: AWS Shield Advanced

**Private Connectivity**:
- VPC Peering for enterprise customers
- AWS PrivateLink available
- VPN for admin access only

### 6.4 Compliance

**Certifications**:
- SOC 2 Type II (annual audit)
- ISO 27001 (certified 2023)
- GDPR compliant (EU data residency available)
- HIPAA compliant (BAA available for healthcare)

**Audit Logging**:
- All API calls logged
- Admin actions logged with before/after
- Logs immutable, stored 7 years
- SIEM integration: Splunk

---

## 7. Monitoring & Observability

### 7.1 Metrics

**Platform**: Datadog

**Key Metrics**:
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| API latency (p99) | < 200ms | > 500ms |
| Error rate | < 0.1% | > 1% |
| CPU utilization | < 70% | > 85% |
| Memory utilization | < 80% | > 90% |
| Queue depth | < 1000 | > 5000 |

### 7.2 Logging

**Platform**: Datadog Logs + S3 archival

**Log Levels**:
- Production: INFO and above
- Staging: DEBUG and above
- Sensitive data: Masked in logs

**Retention**:
- Hot (searchable): 30 days
- Warm (S3): 1 year
- Cold (Glacier): 7 years

### 7.3 Tracing

**Platform**: Datadog APM

**Instrumentation**: OpenTelemetry

**Sample Rate**:
- Production: 10% of requests
- Errors: 100% of errors
- Slow requests: 100% of p99+

### 7.4 Alerting

**On-Call**: PagerDuty

**Escalation**:
1. Primary on-call (5 min response)
2. Secondary on-call (15 min escalation)
3. Engineering Manager (30 min escalation)
4. VP Engineering (1 hour, P0 only)

**Severity Levels**:
| Severity | Definition | Response Time |
|----------|------------|---------------|
| P0 | Complete outage | 15 min |
| P1 | Major feature broken | 1 hour |
| P2 | Minor feature broken | 4 hours |
| P3 | Non-critical issue | 24 hours |

---

## 8. API Reference

### 8.1 Base URLs

| Environment | URL |
|-------------|-----|
| Production | https://api.techcorp.com/v1 |
| Staging | https://api.staging.techcorp.com/v1 |
| Sandbox | https://api.sandbox.techcorp.com/v1 |

### 8.2 Authentication

All API requests require authentication:

**API Key** (Header):
```
Authorization: Bearer tc_live_abc123xyz
```

**OAuth 2.0** (Header):
```
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

### 8.3 Common Endpoints

**Users**
- `GET /users` — List users
- `GET /users/{id}` — Get user
- `POST /users` — Create user
- `PATCH /users/{id}` — Update user
- `DELETE /users/{id}` — Delete user

**Workflows**
- `GET /workflows` — List workflows
- `GET /workflows/{id}` — Get workflow
- `POST /workflows` — Create workflow
- `POST /workflows/{id}/execute` — Execute workflow
- `GET /workflows/{id}/executions` — List executions

**Analytics**
- `POST /analytics/query` — Run analytics query
- `GET /analytics/reports` — List reports
- `GET /analytics/reports/{id}` — Get report

### 8.4 Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request — Invalid parameters |
| 401 | Unauthorized — Invalid or missing auth |
| 403 | Forbidden — Insufficient permissions |
| 404 | Not Found — Resource doesn't exist |
| 429 | Too Many Requests — Rate limit exceeded |
| 500 | Internal Error — Something went wrong |

**Error Response Format**:
```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "You have exceeded the rate limit of 1000 requests/minute",
    "request_id": "req_abc123",
    "docs_url": "https://docs.techcorp.com/errors/rate-limit"
  }
}
```

---

## 9. Development & Deployment

### 9.1 CI/CD Pipeline

**Platform**: GitHub Actions + ArgoCD

**Pipeline Stages**:
1. **Build**: Docker image, run linters
2. **Test**: Unit tests (>80% coverage required)
3. **Security Scan**: Snyk, Trivy
4. **Deploy Staging**: Automatic on merge to main
5. **Integration Tests**: Automated test suite
6. **Deploy Production**: Manual approval, canary rollout

**Deployment Strategy**:
- Staging: Direct deploy
- Production: Canary (5% → 25% → 100%)
- Rollback: Automatic on error rate spike

### 9.2 Environments

| Environment | Purpose | Data |
|-------------|---------|------|
| Development | Local development | Synthetic |
| Staging | Pre-production testing | Anonymized prod copy |
| Sandbox | Customer testing | Isolated, synthetic |
| Production | Live customers | Real |

### 9.3 Feature Flags

**Platform**: LaunchDarkly

**Usage**:
- New features: Flag-controlled rollout
- A/B tests: Percentage-based targeting
- Kill switches: Instant disable for problematic features

---

## 10. Support & Contacts

### 10.1 Team Ownership

| Domain | Team | Slack | On-Call |
|--------|------|-------|---------|
| API Gateway | Platform | #team-platform | @platform-oncall |
| Auth | Security | #team-security | @security-oncall |
| Workflows | Workflows | #team-workflows | @workflows-oncall |
| Data | Data Platform | #team-data | @data-oncall |
| ML/AI | AI Team | #team-ai | @ai-oncall |
| Infra | SRE | #team-sre | @sre-oncall |

### 10.2 Runbooks

All runbooks are in Notion: https://notion.techcorp.com/runbooks

**Critical Runbooks**:
- [Database Failover](https://notion.techcorp.com/runbooks/db-failover)
- [Kafka Recovery](https://notion.techcorp.com/runbooks/kafka-recovery)
- [API Gateway Issues](https://notion.techcorp.com/runbooks/api-gateway)
- [Auth Service Outage](https://notion.techcorp.com/runbooks/auth-outage)

---

*Document Owner: Platform Team*
*Last Review: January 2025*
*Next Review: April 2025*
