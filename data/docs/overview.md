# Quillstack Platform Overview

Quillstack is a high-throughput, cloud-native workflow automation and API event streaming engine designed for mission-critical developer infrastructure. It bridges asynchronous event brokers (such as Apache Kafka, AWS Kinesis, and RabbitMQ) with distributed microservices through low-latency execution pipelines.

## 1. Core Architecture and Concepts

The Quillstack execution layer is composed of four foundational abstractions:

### Workspaces
A Workspace is the primary tenant boundary within Quillstack. All authentication tokens, RBAC permissions, network isolation policies, and billing quotas are scoped to a workspace. Workspaces can operate in multi-tenant shared clusters or isolated single-tenant cells depending on subscription tier.

### Flows
A Flow is a directed acyclic graph (DAG) describing event transformations, conditional branching, enrichment filters, and downstream dispatch triggers. Flows are authored in declarative YAML or programmatically compiled using the Quillstack SDKs.

### Pipes
A Pipe represents an active, stateful streaming connection between an upstream producer and a downstream consumer. Pipes guarantee at-least-once delivery semantics under standard configurations and effectively-once semantics when paired with Shardlet WAL deduplication.

### Event Hubs and Shardlets
Quillstack clusters partition data across distributed processing nodes known as Shardlets. Each Shardlet manages an in-memory ring buffer, a local write-ahead log (WAL) on NVMe storage, and a consensus peer group using the Raft consensus protocol. Shardlets automatically rebalance across availability zones.

## 2. Global Cloud Regions

Quillstack services are deployed in three authoritative multi-region clusters:
- `us-east-quill`: Located in Northern Virginia (AWS us-east-1 and GCP us-east4 cross-connect).
- `eu-central-quill`: Located in Frankfurt, Germany (AWS eu-central-1 and Equinix FR2).
- `ap-south-quill`: Located in Mumbai, India (AWS ap-south-1).

Cross-region event replication is handled asynchronously by the Global Shardlet Mesh. Inter-region transit latency averages 72ms between US and EU, and 140ms between US and AP.

## 3. Supported Protocols and Connectivity

Quillstack supports diverse ingress and egress transport protocols:
1. **gRPC / Protocol Buffers**: High-performance binary transport over HTTP/2 with bi-directional streaming. Recommended for internal microservices and high-volume data pipelines.
2. **REST / HTTP/2 & HTTP/1.1**: Standard JSON-over-HTTPS endpoint interface for webhooks and third-party SaaS integrations.
3. **WebSocket**: Persistent full-duplex socket connections for real-time telemetry, live browser dashboards, and streaming notifications.
4. **Kafka Native Mirror**: Direct protocol compatibility with Kafka clients via the Quillstack Kafka Proxy layer on port 9092.

## 4. Key Terminology

- **Pulse**: The atomic metering unit of Quillstack. One pulse represents one executed flow step or one 4KB event payload processed through a pipe.
- **Shardlet**: A lightweight virtual execution core running in the Quillstack distributed runtime engine.
- **QuillLock**: A distributed consensus lease mechanism used to coordinate singleton flow executions and prevent split-brain processing across active-active pipes.
- **Tenant Lease**: A cryptographically signed token conferring execution authority for a specified workspace epoch.
