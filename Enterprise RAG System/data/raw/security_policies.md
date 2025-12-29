# TechCorp Security Policies
**Version 2.1 | Last Updated: January 2025**
**Classification: Internal — All Employees**

---

## 1. Information Security Policy

### 1.1 Purpose

This policy establishes the security requirements for protecting TechCorp's information assets, customer data, and systems.

All employees, contractors, and third parties with access to TechCorp systems must comply with this policy.

### 1.2 Data Classification

TechCorp classifies data into four categories:

| Classification | Description | Examples |
|----------------|-------------|----------|
| **Public** | Information freely available | Marketing materials, blog posts |
| **Internal** | Business information for employees | Org charts, internal memos |
| **Confidential** | Sensitive business information | Financial reports, roadmaps |
| **Restricted** | Highly sensitive, regulated data | Customer PII, credentials, keys |

### 1.3 Handling Requirements by Classification

**Public**:
- No special handling required
- May be shared externally

**Internal**:
- Share only with TechCorp employees
- No posting on public channels
- Acceptable in internal Slack, email, Google Drive

**Confidential**:
- Need-to-know basis only
- Encrypted in transit and at rest
- No external sharing without VP approval
- Access logged

**Restricted**:
- Strict need-to-know
- End-to-end encryption required
- Access requires security team approval
- All access logged and audited
- Cannot be stored on personal devices

---

## 2. Access Control Policy

### 2.1 Principle of Least Privilege

Users receive minimum access necessary to perform their job functions.

Access is granted based on:
1. Job role and responsibilities
2. Project requirements (time-limited)
3. Manager approval

### 2.2 Account Management

**Account Creation**:
- Initiated by HR upon hire
- Manager specifies required access
- IT provisions within 24 hours of start date

**Account Modification**:
- Role changes require manager request
- Processed within 48 hours
- Old access removed before new access granted

**Account Termination**:
- Access disabled within 1 hour of termination
- Full deprovisioning within 24 hours
- Includes: SSO, email, Slack, AWS, GitHub, all SaaS tools

### 2.3 Privileged Access

**Definition**: Admin access to production systems, databases, or infrastructure.

**Requirements**:
- Security team approval required
- Background check completed
- Privileged access training completed
- MFA mandatory (hardware key preferred)
- Access reviewed quarterly

**Privileged Access Roles**:
| Role | Access Level | Approval Required |
|------|--------------|-------------------|
| Database Admin | Production databases | Security + VP Eng |
| Infrastructure Admin | AWS/Azure root | Security + CTO |
| Security Admin | IAM, Vault, WAF | CISO |
| On-Call Engineer | Limited prod access | Pre-approved for rotation |

### 2.4 Service Accounts

- All service accounts documented in ServiceNow
- No shared credentials between services
- Secrets stored in HashiCorp Vault only
- Rotated every 90 days (automated)
- Owner assigned for each account

---

## 3. Authentication Policy

### 3.1 Password Requirements

**Minimum Standards**:
- Length: 12 characters minimum
- Complexity: uppercase, lowercase, number, symbol
- No dictionary words or common patterns
- No reuse of last 10 passwords
- Change every 90 days

**Password Storage**:
- Use approved password manager: 1Password (company-provided)
- Never store passwords in plain text, documents, or code
- Never share passwords via email or Slack

### 3.2 Multi-Factor Authentication (MFA)

**Required for**:
- All employee accounts (SSO, email)
- AWS Console access
- GitHub access
- VPN access
- Any system with Confidential or Restricted data

**Approved MFA Methods**:
| Method | Use Case | Security Level |
|--------|----------|----------------|
| Hardware key (YubiKey) | Privileged access | Highest |
| Authenticator app | Standard access | High |
| SMS (emergency only) | Account recovery | Medium |

**Hardware Keys**:
- Provided to all employees
- Required for: Infrastructure admins, on-call engineers, executives
- Backup key must be registered
- Report lost keys immediately to security@techcorp.com

### 3.3 Single Sign-On (SSO)

**Provider**: Okta

**Integrated Applications**: All approved SaaS tools must use Okta SSO.

**Session Policy**:
- Session duration: 8 hours
- Re-authentication required for sensitive actions
- Concurrent session limit: 5

---

## 4. Network Security Policy

### 4.1 Network Access

**Office Network**:
- Requires device certificate (auto-installed on company devices)
- Guest network available for visitors (isolated, internet only)
- No personal devices on corporate network

**Remote Access**:
- VPN required for accessing internal resources
- Split tunneling disabled
- VPN timeout: 8 hours
- Approved client: Cloudflare WARP (company-managed)

### 4.2 Firewall Rules

**Default Stance**: Deny all, allow by exception

**Permitted Outbound**:
- HTTPS (443)
- DNS (company resolver only)
- Approved SaaS applications

**Prohibited**:
- Direct database access from corporate network
- SSH to production (use bastion only)
- Torrents, P2P protocols
- TOR network

### 4.3 Wireless Security

**Corporate WiFi**:
- WPA3 Enterprise
- Certificate-based authentication
- Network: TechCorp-Secure

**Guest WiFi**:
- WPA3 Personal
- Isolated VLAN
- 24-hour access codes
- Network: TechCorp-Guest

---

## 5. Endpoint Security Policy

### 5.1 Device Requirements

All devices accessing TechCorp data must have:

- [ ] Full disk encryption enabled
- [ ] Screen lock after 5 minutes idle
- [ ] Company-managed antivirus (CrowdStrike Falcon)
- [ ] Automatic OS updates enabled
- [ ] Company MDM profile installed

### 5.2 Approved Devices

**Company-Issued** (Preferred):
- MacBook Pro (M2/M3)
- Dell XPS 15 (Windows 11 Enterprise)
- iPhone (iOS 17+) — for Slack, email only

**Personal Devices** (BYOD):
- Must meet all security requirements
- MDM profile required
- Can access: Email, Slack, Docs
- Cannot access: Production systems, Restricted data
- Subject to remote wipe if lost/stolen

### 5.3 Prohibited Software

Do not install:
- Cracked or pirated software
- Browser extensions not approved by IT
- Remote access tools (TeamViewer, AnyDesk) — use approved tools only
- Cryptocurrency miners
- Games on work devices

**Approved Software List**: https://techcorp.okta.com/apps

### 5.4 Lost or Stolen Devices

**Immediate Actions**:
1. Report to security@techcorp.com within 1 hour
2. IT initiates remote wipe
3. Change SSO password immediately
4. Security reviews access logs

---

## 6. Data Protection Policy

### 6.1 Customer Data

**Handling Rules**:
- Customer data is always Restricted classification
- Access logged and audited
- No downloading to local machines
- No sharing in screenshots, demos without masking
- Delete when no longer needed

**Customer Data Locations** (Approved):
- Production databases (encrypted)
- Approved analytics tools with BAA
- Support tickets (Zendesk — masked after 90 days)

**Not Approved for Customer Data**:
- Personal email
- Personal cloud storage
- Local spreadsheets
- Slack (except incident response)

### 6.2 PII Protection

**Personally Identifiable Information (PII)**:
- Names, email addresses
- Phone numbers, addresses
- SSN, government IDs
- Financial information
- Health information

**Protection Requirements**:
- Encrypted at rest and in transit
- Masked in logs and non-production environments
- Access requires business justification
- Retention limited to business need

### 6.3 Data Retention & Deletion

| Data Type | Retention Period | Deletion Method |
|-----------|------------------|-----------------|
| Active customer data | Account lifetime | On account deletion |
| Inactive accounts | 90 days | Automated purge |
| Audit logs | 7 years | Archived to cold storage |
| Analytics | 2 years | Aggregated, PII stripped |
| Support tickets | 2 years | Archived, masked |
| Employee data | Employment + 7 years | HR managed |

---

## 7. Incident Response Policy

### 7.1 What is a Security Incident?

**Examples**:
- Unauthorized access to systems or data
- Malware infection
- Data breach or data leak
- Phishing attack (successful or attempted)
- Lost or stolen device with company data
- Suspicious account activity
- Policy violations

### 7.2 Reporting Incidents

**Report Immediately To**:
- Slack: #security-incidents (24/7 monitored)
- Email: security@techcorp.com
- Phone: +1-555-SEC-RITY (after hours)

**What to Include**:
- What happened (be specific)
- When it happened
- Systems/data affected
- Actions you've taken

**Do NOT**:
- Try to fix it yourself
- Delete evidence
- Discuss on public channels
- Inform external parties (PR/Legal handles)

### 7.3 Incident Severity

| Severity | Definition | Examples | Response Time |
|----------|------------|----------|---------------|
| Critical | Active breach, data exfiltration | Ransomware, confirmed breach | 15 minutes |
| High | Potential breach, active attack | Phishing, unauthorized access | 1 hour |
| Medium | Contained incident, policy violation | Lost device, suspicious login | 4 hours |
| Low | Minor issue, no data at risk | Failed phishing, policy question | 24 hours |

### 7.4 Incident Response Process

1. **Detection**: Incident identified and reported
2. **Triage**: Security team assesses severity
3. **Containment**: Limit damage (isolate systems, revoke access)
4. **Investigation**: Determine root cause and scope
5. **Eradication**: Remove threat, patch vulnerabilities
6. **Recovery**: Restore systems, verify security
7. **Post-Mortem**: Document lessons learned, update controls

---

## 8. Security Awareness

### 8.1 Training Requirements

**All Employees**:
- Security awareness training: Annual (mandatory)
- Phishing simulation: Quarterly
- Policy acknowledgment: Annual

**Engineering**:
- Secure coding training: Annual
- OWASP Top 10 review: Annual

**Privileged Users**:
- Advanced security training: Annual
- Incident response training: Annual

### 8.2 Phishing Awareness

**How to Identify Phishing**:
- Urgent or threatening language
- Unexpected attachments
- Links to unfamiliar domains
- Requests for credentials or sensitive data
- Poor grammar or formatting
- Sender address doesn't match company

**If You Receive a Suspicious Email**:
1. Do NOT click links or download attachments
2. Report via Slack: #security-incidents or email phishing@techcorp.com
3. Forward the email as attachment
4. Delete from inbox

### 8.3 Social Engineering

**Common Tactics**:
- Impersonating IT support ("We need your password to fix an issue")
- Impersonating executives ("The CEO needs this wire transfer immediately")
- Tailgating into secure areas
- USB drops ("Found this USB drive in the parking lot")

**Defense**:
- Verify requests through known channels
- Never share passwords, even with IT
- Challenge unknown visitors
- Never plug in unknown USB devices

---

## 9. Third-Party Security

### 9.1 Vendor Assessment

All vendors with access to TechCorp data must:
- Complete security questionnaire
- Provide SOC 2 report or equivalent
- Sign DPA (Data Processing Agreement)
- Undergo annual review

**Risk Tiers**:
| Tier | Data Access | Assessment |
|------|-------------|------------|
| Critical | Customer data, production | Full assessment, annual audit |
| High | Internal data, systems | Questionnaire, SOC 2 review |
| Medium | Limited data, tools | Questionnaire |
| Low | No data access | Basic review |

### 9.2 Approved Vendors

See approved vendor list: https://wiki.techcorp.com/security/approved-vendors

**Adding New Vendors**:
1. Submit request to #security-requests
2. Security reviews vendor
3. Legal reviews contract
4. Procurement processes
5. Access provisioned by IT

---

## 10. Physical Security

### 10.1 Office Access

**Badge Access**:
- Required for all TechCorp offices
- Badge must be visible at all times
- Do not share or lend badges
- Report lost badges immediately

**Visitors**:
- Must sign in at reception
- Visitor badge required (visually distinct)
- Must be escorted at all times
- NDAs required for non-public areas

### 10.2 Secure Areas

**Server Rooms / Data Centers**:
- Access: Security team + SRE only
- Requires badge + biometric
- All access logged
- No phones or cameras

**Executive Floors**:
- Restricted to L5+ and approved personnel
- Separate badge access

### 10.3 Clean Desk Policy

End of each day:
- Lock laptop or log out
- Store sensitive documents in locked cabinet
- Whiteboards with sensitive info: Erased
- No passwords on sticky notes

---

## 11. Compliance

### 11.1 Regulatory Requirements

**GDPR** (EU Customers):
- Data minimization
- Purpose limitation
- Right to deletion
- Breach notification (72 hours)

**SOC 2**:
- Annual audit
- Controls testing
- Evidence collection (ongoing)

**HIPAA** (Healthcare Customers):
- BAA required
- Additional access controls
- Audit logging
- Encryption requirements

### 11.2 Policy Compliance

**Monitoring**:
- Automated compliance checks
- Quarterly access reviews
- Annual policy audit

**Violations**:
- First offense: Training, documented warning
- Second offense: Manager escalation, potential final warning
- Severe violations: Immediate termination possible

---

## 12. Contact Information

| Role | Contact | Availability |
|------|---------|--------------|
| Security Team | security@techcorp.com | Business hours |
| Security Incidents | #security-incidents | 24/7 |
| CISO | ciso@techcorp.com | Business hours |
| Privacy | privacy@techcorp.com | Business hours |
| Compliance | compliance@techcorp.com | Business hours |

**Emergency Security Line**: +1-555-SEC-RITY (24/7)

---

## Appendix: Quick Reference

### Security Checklist for Employees

- [ ] Complete annual security training
- [ ] Enable MFA on all accounts
- [ ] Use 1Password for credentials
- [ ] Lock laptop when away from desk
- [ ] Report suspicious emails to #security-incidents
- [ ] Keep software updated
- [ ] Use VPN when working remotely
- [ ] Know how to report incidents

### Security Don'ts

❌ Share passwords  
❌ Click links in suspicious emails  
❌ Install unapproved software  
❌ Access customer data without business need  
❌ Discuss confidential info in public  
❌ Use personal devices for restricted data  
❌ Ignore security training  

---

*Policy Owner: Security Team*
*Approved By: CISO*
*Effective Date: January 2025*
*Next Review: July 2025*
