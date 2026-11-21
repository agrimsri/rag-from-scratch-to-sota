# Quillstack Data Retention, Deletion, and Privacy Policy

This policy governs the retention, residency, deletion, and compliance treatment of customer data processed across the Quillstack event streaming ecosystem.

## 1. Data Residency and Cross-Border Transfers

Quillstack operates distinct sovereign data regions to satisfy strict jurisdictional privacy regulations:
- **European Economic Area (EEA)**: Hosted entirely within Frankfurt, Germany (`eu-central-quill`). All persistent payloads, metadata databases, and WAL records are guaranteed to remain physically resident within EU borders.
- **United States**: Hosted within Northern Virginia (`us-east-quill`).
- **Asia-Pacific**: Hosted within Mumbai, India (`ap-south-quill`).

Data is never transferred between regions without explicit customer configuration of cross-region replication flows.

## 2. Workspace Deletion and Cooling Period

Quillstack enforces a defensive retention policy to protect against accidental tenant destruction or compromised administrator accounts:
1. When an administrator initiates a workspace termination, the workspace enters a 14-day soft-delete cooling period.
2. During these 14 days, all active pipes are paused and API access is revoked, but customer data remains fully encrypted and restorable upon identity verification with customer support.
3. Following expiration of the 14-day cooling period, automated background purge daemons perform permanent zero-fill deletion within 72 hours across all storage volumes and backup mirrors.

## 3. Audit Trails and Cold Storage Retention

Audit records containing administrative access metadata are archived in immutable WORM (Write Once, Read Many) cold storage.
The system maintains 90 days cold storage backup before automated shredding takes place.

## 4. GDPR and Privacy Rights Automation

To fulfill European Union GDPR Right to be Forgotten and California CCPA erasure requests, Quillstack exposes a dedicated compliance endpoint:
`POST /v3/compliance/erasure`
Compliance erasure jobs process all customer user identifiers across active pipelines, dead-letter queues, and telemetry stores within 30 days of submission.
