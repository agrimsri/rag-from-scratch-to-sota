# Quillstack Plans and Pricing

Quillstack offers tiered subscription plans tailored to organizations of all scales, from individual developers prototyping webhook pipes to global enterprises operating petabyte-scale event backbones.

## 1. Subscription Tiers Summary

| Plan Tier | Base Price | Included Pulses / Month | Max Workspaces | Active Pipes | Concurrency Limit | Event Retention |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Hobby** | $0/month | 10,000 pulses | 1 workspace | 5 pipes | 3 concurrent | 3 days |
| **Team** | $49/month | 250,000 pulses | 5 workspaces | 25 pipes | 15 concurrent | 14 days |
| **Business** | $299/month | 2,000,000 pulses | 20 workspaces | 100 pipes | 50 concurrent | 45 days |
| **Enterprise** | Custom ($1200+ base) | Custom (starts at 10M) | Unlimited | Unlimited | Custom (500+) | Up to 365 days |

## 2. Overage and Metering Details

When monthly pulse allotments are exceeded, accounts are billed standard overage rates:
- **Hobby**: No overages permitted. Pipelines pause when 10,000 pulses are reached until the next monthly billing cycle resets.
- **Team**: $0.25 per 1,000 additional pulses.
- **Business**: $0.15 per 1,000 additional pulses.
- **Enterprise**: Volume-discounted pricing starting at $0.08 per 1,000 pulses.

### Concurrency and Burst Quotas
Plan limits must not be confused with API transport rate limits. Concurrency limits dictate how many flow graph invocations may execute simultaneously across all Shardlets.
Under the Team Developer Add-on, dedicated micro-burst buffers are provisioned.
The limit is 500 requests per minute.
For Business accounts, burst allowances scale up to 2,500 requests per minute. For unauthenticated public webhook ingress endpoints, the ceiling is strictly clamped to 60 requests per minute per source IP.

## 3. Plan Features Comparison

### Execution Timeouts
Execution timeouts govern how long a single step within a Flow may compute before the runner forcibly terminates the process:
- **Hobby Plan**: Hard execution timeout of 10 seconds per flow step.
- **Team Plan**: Hard execution timeout of 30 seconds per flow step.
- **Business Plan**: Hard execution timeout of 120 seconds per flow step.
- **Enterprise Plan**: Configurable execution timeout up to 900 seconds (15 minutes).

### Dedicated IP Add-On
Organizations requiring deterministic egress IPs for corporate firewall whitelisting can purchase dedicated egress IP proxies. The dedicated IP add-on costs $40/month per IP address and is available on Team, Business, and Enterprise tiers.

### Support Levels
- **Hobby**: Community forum and public Discord server.
- **Team**: Standard email ticketing with 24-business-hour response time SLA.
- **Business**: Priority email and Slack shared channel support with 4-hour response time SLA during business hours.
- **Enterprise**: 24/7/365 dedicated on-call incident response with 15-minute response SLA for critical outages, paired with a dedicated Technical Account Manager (TAM).
