# Quillstack Migration Guide: Upgrading from v2 to v3

The transition from Quillstack v2 to v3 represents a fundamental modernization of the underlying streaming architecture, introducing Raft-replicated write-ahead logs, enhanced security headers, and strictly typed schemas.

## 1. Architectural Differences Between v2 and v3

| Subsystem / Feature | Quillstack v2 (Legacy) | Quillstack v3 (Modern) |
| :--- | :--- | :--- |
| **Message Broker Engine** | Redis-backed `QuillQueue` | Raft-replicated `QuillStream` WAL |
| **Default Network Port** | Plain HTTP port `8080` | TLS encrypted port `8443` |
| **Authentication Header** | Custom `X-Quill-Token` header | Standard `Authorization: Bearer <token>` |
| **Retention Parameter** | `event_ttl_seconds` | `retention_ttl_sec` |
| **Error Handling Behavior**| Dropped unhandled errors silently | Routes errors to `quill.dlq.v3` |

## 2. Breaking Changes and Migration Checklist

### Transport Port and TLS Requirement
In Quillstack v2, local testing and unencrypted internal traffic typically connected to port `8080`. In v3, plain HTTP port 8080 is deprecated and disabled by default. All client SDKs must connect to TLS port `8443`.

### Authentication Header Transition
Client requests in v2 used custom header `X-Quill-Token: <token>`. In v3, this header is rejected with error `E-1001`. Applications must provide standard HTTP header:
`Authorization: Bearer <token>`

### Parameter Renaming in Flow Declarations
When updating flow definitions from v2 YAML specs, note that parameter `event_ttl_seconds` has been renamed to `retention_ttl_sec`. Specifying the legacy parameter name will result in configuration parsing warning `W-204` and fallback to the default 86400-second retention.

### Poison Message and Error Handling
In v2, when a pipe encountered an unrecoverable transformation failure, unhandled pipe errors were dropped silently, often causing silent data loss. In v3, unhandled errors route to dead-letter queue `quill.dlq.v3` automatically for inspection and replay.
