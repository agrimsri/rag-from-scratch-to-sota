# Quillstack Service Level Agreement (SLA) and Incident Management

This agreement outlines the availability commitments, service credit schedules, and incident response procedures for Quillstack cloud services.

## 1. Monthly Uptime Service Commitments

Uptime percentages are calculated across each calendar month according to subscription tier:
- **Hobby Tier**: No availability commitment or uptime SLA.
- **Team Tier**: 99.5% uptime commitment.
- **Business Tier**: 99.9% uptime commitment.
- **Enterprise Tier**: 99.95% uptime commitment, backed by financial service credits.

## 2. Service Credit Schedule (Enterprise Customers)

If Quillstack fails to meet the 99.95% Enterprise availability commitment during any billing cycle, eligible customers are entitled to service credits applied against future invoice amounts:

| Monthly Uptime Percentage | Service Credit Percentage |
| :--- | :--- |
| **< 99.95% but ≥ 99.0%** | 10% monthly invoice credit |
| **< 99.0% but ≥ 95.0%** | 25% monthly invoice credit |
| **< 95.0%** | 50% monthly invoice credit |

Service credits must be requested by the account administrator within thirty (30) calendar days following the affected calendar month.

## 3. Incident Severity Tiers and Response SLAs

When disruptions occur, incidents are classified into four severity tiers:

### SEV-1: Critical Outage
- **Definition**: Complete service unavailability affecting multiple workspaces, inability to publish or ingest events across primary regions, or active data corruption.
- **Initial Response SLA**: 15 minutes (24/7/365 coverage for Enterprise; business-hours only for Business).
- **Update Frequency**: Every 30 minutes until resolution.

### SEV-2: Major Degradation
- **Definition**: Severe performance degradation, message processing backlog exceeding 10 minutes, or failure of non-critical subsystems (e.g., analytics dashboard).
- **Initial Response SLA**: 1 hour.
- **Update Frequency**: Every 2 hours.

### SEV-3: Minor Impairment
- **Definition**: Partial system defects that do not hinder core message transport; transient API errors with viable workarounds.
- **Initial Response SLA**: 8 business hours.

### SEV-4: General Inquiry / Guidance
- **Definition**: Configuration inquiries, documentation clarification, or feature requests.
- **Initial Response SLA**: 24 business hours.
