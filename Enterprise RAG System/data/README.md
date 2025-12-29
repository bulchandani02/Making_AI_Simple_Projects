# TechCorp Dataset

This folder contains the sample dataset used throughout the 7-day RAG project.

## Why TechCorp?

We use a **fictional company dataset** that mimics real enterprise documentation:

1. **Realistic Content**: HR policies, technical docs, org charts — just like real companies
2. **Diverse Document Types**: Text, tables, hierarchies — tests different RAG capabilities
3. **Cross-Document Relationships**: Teams reference each other, policies reference procedures
4. **Safe to Share**: No real company data, can be used in demos and tutorials


## Documents

### `employee_handbook.md`
**Pages**: ~15 | **Tokens**: ~4,500

Contents:
- Company overview and values
- Employment policies (PTO, leave, holidays)
- Compensation and benefits
- Performance reviews and promotions
- Code of conduct
- IT and security basics
- Travel and expenses

**Good for testing**:
- Policy lookups ("How much PTO do I get?")
- Table queries ("What are the pay grades?")
- Multi-part questions ("What's the parental leave policy and when can I take it?")


### `technical_architecture.md`
**Pages**: ~20 | **Tokens**: ~6,000

Contents:
- System overview and principles
- Infrastructure (AWS, Kubernetes)
- Core services catalog
- Data architecture (databases, retention)
- Event-driven architecture (Kafka)
- Security architecture
- API reference
- Monitoring and observability

**Good for testing**:
- Technical lookups ("What database does the auth service use?")
- Architecture questions ("How is data encrypted?")
- Cross-referencing ("Which team owns the workflow engine?")


### `security_policies.md`
**Pages**: ~12 | **Tokens**: ~4,000

Contents:
- Data classification levels
- Access control policies
- Authentication requirements (passwords, MFA)
- Network security
- Endpoint security
- Incident response procedures
- Compliance requirements

**Good for testing**:
- Security procedures ("How do I report a security incident?")
- Policy questions ("What are the password requirements?")
- Compliance queries ("What certifications does TechCorp have?")


### `org_structure.md`
**Pages**: ~8 | **Tokens**: ~3,000

Contents:
- Executive leadership team
- Engineering division (teams, managers)
- Sales, Marketing, Finance divisions
- Office locations
- Career levels
- Cross-functional teams

**Good for testing**:
- Org queries ("Who leads the AI/ML team?")
- Structural questions ("How many people are in engineering?")
- Relationship queries ("Who does the Platform team report to?")


## Dataset Statistics

| Document | Words | Tokens (est.) | Tables | Lists |
|----------|-------|---------------|--------|-------|
| Employee Handbook | ~3,500 | ~4,500 | 8 | 15 |
| Technical Architecture | ~4,800 | ~6,000 | 12 | 10 |
| Security Policies | ~3,200 | ~4,000 | 6 | 20 |
| Org Structure | ~2,400 | ~3,000 | 10 | 5 |
| **Total** | **~14,000** | **~17,500** | **36** | **50** |


## Sample Test Questions

### Easy (Single document, direct answer)
1. "How many days of PTO do employees with 3 years tenure get?"
2. "What is the password minimum length?"
3. "Who is the CTO of TechCorp?"

### Medium (Requires understanding context)
4. "What should I do if I receive a suspicious email?"
5. "How does TechCorp handle database backups?"
6. "What's the career progression for an engineer?"

### Hard (Cross-document or complex reasoning)
7. "If I want to access production databases, what approvals and training do I need?"
8. "Compare the security requirements for Confidential vs Restricted data."
9. "Who should I contact if there's a security incident affecting the workflow engine?"

### Edge Cases (Tests system limitations)
10. "What's TechCorp's stock price?" (Not in docs)
11. "Summarize all HR policies" (Too broad)
12. "What changed in version 2.3 of the handbook?" (Specific detail)


## Folder Structure

```
data/
├── raw/                    # Original documents
│   ├── employee_handbook.md
│   ├── technical_architecture.md
│   ├── security_policies.md
│   └── org_structure.md
│
├── processed/              # Generated during notebooks
│   ├── chunks/             # Chunked documents
│   └── metadata/           # Extracted metadata
│
└── evaluation/             # Test datasets (Day 18)
    ├── test_questions.json
    └── ground_truth.json
```


## Notes

- This is **fictional data** created for educational purposes
- Any resemblance to real companies is coincidental
- Feel free to modify for your own experiments
- When adding new documents, update this README

---

*Created for Making AI Simple series — Days 12-18*
