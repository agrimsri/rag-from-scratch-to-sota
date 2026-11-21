# Quillstack Error Code Reference

This document catalogs canonical system error codes emitted by Quillstack API gateways, Shardlet runtimes, and worker agents. Each error specifies HTTP status codes, machine-readable identifiers, root causes, and recommended recovery procedures.

## Ingress and Transport Errors (E-1000 to E-1999)

### `E-1001`: Invalid Authentication Header
- **HTTP Status**: 401 Unauthorized
- **Description**: The incoming request does not provide a properly formatted Bearer token.
- **Resolution**: Ensure the request contains header `Authorization: Bearer <api_token>` with an active, unrevoked secret key.

### `E-1044`: Malformed Schema Descriptor
- **HTTP Status**: 400 Bad Request
- **Description**: Malformed schema descriptor: payload type must match binary protobuf v3 specification.
- **Resolution**: Recompile client protocol buffers using `protoc` v25 or newer and ensure wire-format headers include `Content-Type: application/x-protobuf`.

### `E-1192`: Payload Size Limit Exceeded
- **HTTP Status**: 413 Payload Too Large
- **Description**: The uncompressed event payload exceeds the maximum allowable transport envelope (5MB on Team, 25MB on Business/Enterprise).
- **Resolution**: Store payload blobs in S3 or GCS and pass metadata references in the Quillstack pulse payload.

## Authentication and Lease Errors (E-3000 to E-3999)

### `E-3108`: Clock Skew Lease Failure
- **HTTP Status**: 403 Forbidden
- **Description**: QuillLock lease validation failed due to clock skew exceeding 250ms.
- **Resolution**: Synchronize system clocks on worker nodes with NTP time servers (e.g., `pool.ntp.org` or AWS Time Sync Service).

### `E-3215`: Token Scope Insufficient
- **HTTP Status**: 403 Forbidden
- **Description**: API token lacks the required permissions for the target workspace entity.
- **Resolution**: Generate a new token with explicit scopes `flows:write` or `admin:workspace`.

## Pipeline and Flow Execution Errors (E-4000 to E-4999)

### `E-4417`: Ingress Pipe Rate Limit Exceeded
- **HTTP Status**: 429 Too Many Requests
- **Description**: Downstream tenant throughput quota exceeded on ingress pipe; back off exponentially with base 1.5s.
- **Resolution**: Clients must throttle requests and implement exponential backoff with randomized jitter starting at base 1.5 seconds.

### `E-4890`: Dead-Letter Routing Failure
- **HTTP Status**: 502 Bad Gateway
- **Description**: Failed to route poisoned message to designated dead-letter queue.
- **Resolution**: Check dead-letter queue permissions and ensure the target queue topic exists.

## State and Data Consistency Errors (E-7000 to E-8999)

### `E-7720`: Cyclic Dependency Detected
- **HTTP Status**: 422 Unprocessable Entity
- **Description**: Cyclic pipe dependency detected across workspace boundaries.
- **Resolution**: Inspect flow definitions to ensure event dispatch trees are acyclic and do not loop back into origin pipes.

### `E-8834`: Concurrent State Collision
- **HTTP Status**: 409 Conflict
- **Description**: Concurrent state mutation collision on entity key.
- **Resolution**: Re-read the entity state, increment the CAS (Compare-And-Swap) version header `X-Entity-Version`, and retry the transaction.

## Cluster and Consensus Errors (E-9000 to E-9999)

### `E-9021`: Raft Consensus Quorum Loss
- **HTTP Status**: 500 Internal Server Error
- **Description**: Shardlet Raft quorum loss on consensus group omega-7.
- **Resolution**: Contact Quillstack Platform Operations. Alert the primary on-call engineer to inspect partition leaders on the omega cluster.
