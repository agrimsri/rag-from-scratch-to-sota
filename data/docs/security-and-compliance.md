# Quillstack Security, Compliance, and Governance

Quillstack provides enterprise-grade data protection, strict security governance, and multi-tenant isolation architectures designed to meet global compliance standards.

## 1. Compliance Certifications and Audits

Quillstack undergoes annual third-party independent audits to certify adherence to industry security standards:
- **SOC 2 Type II**: Audited by Schellman & Company LLC across Security, Availability, and Confidentiality trust principles. Available to Business and Enterprise customers.
- **ISO/IEC 27001:2022**: Global information security management standard certification.
- **HIPAA BAA (Business Associate Agreement)**: Supported exclusively on the Enterprise plan with dedicated Shardlet clusters and encrypted audit trails.
- **PCI-DSS Level 1**: Tokenization and transmission compliance for payment webhook data.

## 2. Cryptographic Architecture

### Encryption in Transit
All network traffic entering or leaving Quillstack is encrypted using TLS 1.3 (with fallback to TLS 1.2 using secure cipher suites `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384`). Plain HTTP traffic is rejected at the edge load balancers.

### Encryption at Rest
All persistent storage volumes, Shardlet write-ahead logs, and message buffers are encrypted at rest with AES-256 bit encryption keys.

### Customer-Managed Encryption Keys (CMEK)
Business and Enterprise tier customers may provide their own master encryption keys to control decryption of event payloads:
- AWS Key Management Service (AWS KMS) integration via IAM assume-role policies.
- Google Cloud KMS integration via Workload Identity Federation.
Revoking CMEK key access immediately renders all workspace Shardlet storage pools cryptographically inaccessible within 60 seconds.

## 3. Network Isolation and Allowlisting

Workspaces can restrict administrative API access and event ingestion to designated IPv4 and IPv6 CIDR blocks.
- **Business Plan**: Supports up to 50 CIDR allowlist rules per workspace.
- **Enterprise Plan**: Supports up to 500 CIDR allowlist rules per workspace with custom regex matching for private VPN tunnels.

## 4. Audit Logging and Observability

Every API invocation, permission mutation, flow trigger, and administrative login generates a structured, cryptographically signed audit event.
- **Team**: Retains audit logs for 7 days.
- **Business**: Retains audit logs for 30 days.
- **Enterprise**: Retains audit logs for 365 days, with optional real-time streaming to Amazon S3, Google Cloud Storage, or Datadog.
