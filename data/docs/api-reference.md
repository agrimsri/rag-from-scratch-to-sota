# Quillstack Complete API Reference Specification

Welcome to the comprehensive API reference for Quillstack v3. This document provides end-to-end specifications for all REST endpoints, gRPC service methods, header protocols, payload formats, and query parameters.

All API calls must be directed to `https://api.quillstack.io/v3` or regional endpoint aliases like `https://us-east.api.quillstack.io/v3`.

## Authentication Headers
All requests must supply:
`Authorization: Bearer <API_SECRET_KEY>`
`Content-Type: application/json` (or `application/x-protobuf` for gRPC-REST bridge).

## Global Ingress Endpoints

### Endpoint `POST /v3/pipes/pipe-001/events`
- **Description**: Publishes an event or batch of events to pipe instance 1.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.1",
  "source": "sensor-gateway-1.edge",
  "data": {
    "reading_index": 1,
    "temperature_celsius": 20.5,
    "pressure_kpa": 101.39999999999999,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000001-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-001/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 1.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-001",
  "active_shards": 4,
  "in_flight_messages": 12,
  "consumer_lag_ms": 3
}
```

### Endpoint `POST /v3/pipes/pipe-002/events`
- **Description**: Publishes an event or batch of events to pipe instance 2.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.2",
  "source": "sensor-gateway-2.edge",
  "data": {
    "reading_index": 2,
    "temperature_celsius": 21.0,
    "pressure_kpa": 101.5,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000002-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-002/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 2.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-002",
  "active_shards": 4,
  "in_flight_messages": 24,
  "consumer_lag_ms": 6
}
```

### Endpoint `POST /v3/pipes/pipe-003/events`
- **Description**: Publishes an event or batch of events to pipe instance 3.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.3",
  "source": "sensor-gateway-3.edge",
  "data": {
    "reading_index": 3,
    "temperature_celsius": 21.5,
    "pressure_kpa": 101.6,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000003-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-003/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 3.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-003",
  "active_shards": 4,
  "in_flight_messages": 36,
  "consumer_lag_ms": 9
}
```

### Endpoint `POST /v3/pipes/pipe-004/events`
- **Description**: Publishes an event or batch of events to pipe instance 4.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.4",
  "source": "sensor-gateway-4.edge",
  "data": {
    "reading_index": 4,
    "temperature_celsius": 22.0,
    "pressure_kpa": 101.7,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000004-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-004/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 4.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-004",
  "active_shards": 4,
  "in_flight_messages": 48,
  "consumer_lag_ms": 12
}
```

### Endpoint `POST /v3/pipes/pipe-005/events`
- **Description**: Publishes an event or batch of events to pipe instance 5.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.5",
  "source": "sensor-gateway-5.edge",
  "data": {
    "reading_index": 5,
    "temperature_celsius": 22.5,
    "pressure_kpa": 101.8,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000005-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-005/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 5.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-005",
  "active_shards": 4,
  "in_flight_messages": 60,
  "consumer_lag_ms": 15
}
```

### Endpoint `POST /v3/pipes/pipe-006/events`
- **Description**: Publishes an event or batch of events to pipe instance 6.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.6",
  "source": "sensor-gateway-6.edge",
  "data": {
    "reading_index": 6,
    "temperature_celsius": 23.0,
    "pressure_kpa": 101.89999999999999,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000006-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-006/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 6.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-006",
  "active_shards": 4,
  "in_flight_messages": 72,
  "consumer_lag_ms": 18
}
```

### Endpoint `POST /v3/pipes/pipe-007/events`
- **Description**: Publishes an event or batch of events to pipe instance 7.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.7",
  "source": "sensor-gateway-7.edge",
  "data": {
    "reading_index": 7,
    "temperature_celsius": 23.5,
    "pressure_kpa": 102.0,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000007-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-007/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 7.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-007",
  "active_shards": 4,
  "in_flight_messages": 84,
  "consumer_lag_ms": 21
}
```

### Endpoint `POST /v3/pipes/pipe-008/events`
- **Description**: Publishes an event or batch of events to pipe instance 8.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.8",
  "source": "sensor-gateway-8.edge",
  "data": {
    "reading_index": 8,
    "temperature_celsius": 24.0,
    "pressure_kpa": 102.1,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000008-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-008/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 8.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-008",
  "active_shards": 4,
  "in_flight_messages": 96,
  "consumer_lag_ms": 24
}
```

### Endpoint `POST /v3/pipes/pipe-009/events`
- **Description**: Publishes an event or batch of events to pipe instance 9.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.9",
  "source": "sensor-gateway-9.edge",
  "data": {
    "reading_index": 9,
    "temperature_celsius": 24.5,
    "pressure_kpa": 102.2,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000009-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-009/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 9.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-009",
  "active_shards": 4,
  "in_flight_messages": 108,
  "consumer_lag_ms": 27
}
```

### Endpoint `POST /v3/pipes/pipe-010/events`
- **Description**: Publishes an event or batch of events to pipe instance 10.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.10",
  "source": "sensor-gateway-10.edge",
  "data": {
    "reading_index": 10,
    "temperature_celsius": 25.0,
    "pressure_kpa": 102.3,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000010-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-010/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 10.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-010",
  "active_shards": 4,
  "in_flight_messages": 120,
  "consumer_lag_ms": 30
}
```

### Endpoint `POST /v3/pipes/pipe-011/events`
- **Description**: Publishes an event or batch of events to pipe instance 11.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.11",
  "source": "sensor-gateway-11.edge",
  "data": {
    "reading_index": 11,
    "temperature_celsius": 25.5,
    "pressure_kpa": 102.39999999999999,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000011-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-011/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 11.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-011",
  "active_shards": 4,
  "in_flight_messages": 132,
  "consumer_lag_ms": 33
}
```

### Endpoint `POST /v3/pipes/pipe-012/events`
- **Description**: Publishes an event or batch of events to pipe instance 12.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.12",
  "source": "sensor-gateway-12.edge",
  "data": {
    "reading_index": 12,
    "temperature_celsius": 26.0,
    "pressure_kpa": 102.5,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000012-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-012/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 12.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-012",
  "active_shards": 4,
  "in_flight_messages": 144,
  "consumer_lag_ms": 36
}
```

### Endpoint `POST /v3/pipes/pipe-013/events`
- **Description**: Publishes an event or batch of events to pipe instance 13.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.13",
  "source": "sensor-gateway-13.edge",
  "data": {
    "reading_index": 13,
    "temperature_celsius": 26.5,
    "pressure_kpa": 102.6,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000013-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-013/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 13.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-013",
  "active_shards": 4,
  "in_flight_messages": 156,
  "consumer_lag_ms": 39
}
```

### Endpoint `POST /v3/pipes/pipe-014/events`
- **Description**: Publishes an event or batch of events to pipe instance 14.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.14",
  "source": "sensor-gateway-14.edge",
  "data": {
    "reading_index": 14,
    "temperature_celsius": 27.0,
    "pressure_kpa": 102.7,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000014-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-014/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 14.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-014",
  "active_shards": 4,
  "in_flight_messages": 168,
  "consumer_lag_ms": 42
}
```

### Endpoint `POST /v3/pipes/pipe-015/events`
- **Description**: Publishes an event or batch of events to pipe instance 15.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.15",
  "source": "sensor-gateway-15.edge",
  "data": {
    "reading_index": 15,
    "temperature_celsius": 27.5,
    "pressure_kpa": 102.8,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000015-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-015/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 15.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-015",
  "active_shards": 4,
  "in_flight_messages": 180,
  "consumer_lag_ms": 45
}
```

### Endpoint `POST /v3/pipes/pipe-016/events`
- **Description**: Publishes an event or batch of events to pipe instance 16.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.16",
  "source": "sensor-gateway-16.edge",
  "data": {
    "reading_index": 16,
    "temperature_celsius": 28.0,
    "pressure_kpa": 102.89999999999999,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000016-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-016/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 16.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-016",
  "active_shards": 4,
  "in_flight_messages": 192,
  "consumer_lag_ms": 48
}
```

### Endpoint `POST /v3/pipes/pipe-017/events`
- **Description**: Publishes an event or batch of events to pipe instance 17.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.17",
  "source": "sensor-gateway-17.edge",
  "data": {
    "reading_index": 17,
    "temperature_celsius": 28.5,
    "pressure_kpa": 103.0,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000017-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-017/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 17.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-017",
  "active_shards": 4,
  "in_flight_messages": 204,
  "consumer_lag_ms": 51
}
```

### Endpoint `POST /v3/pipes/pipe-018/events`
- **Description**: Publishes an event or batch of events to pipe instance 18.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.18",
  "source": "sensor-gateway-18.edge",
  "data": {
    "reading_index": 18,
    "temperature_celsius": 29.0,
    "pressure_kpa": 103.1,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000018-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-018/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 18.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-018",
  "active_shards": 4,
  "in_flight_messages": 216,
  "consumer_lag_ms": 54
}
```

### Endpoint `POST /v3/pipes/pipe-019/events`
- **Description**: Publishes an event or batch of events to pipe instance 19.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.19",
  "source": "sensor-gateway-19.edge",
  "data": {
    "reading_index": 19,
    "temperature_celsius": 29.5,
    "pressure_kpa": 103.2,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000019-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-019/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 19.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-019",
  "active_shards": 4,
  "in_flight_messages": 228,
  "consumer_lag_ms": 57
}
```

### Endpoint `POST /v3/pipes/pipe-020/events`
- **Description**: Publishes an event or batch of events to pipe instance 20.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.20",
  "source": "sensor-gateway-20.edge",
  "data": {
    "reading_index": 20,
    "temperature_celsius": 30.0,
    "pressure_kpa": 103.3,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000020-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-020/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 20.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-020",
  "active_shards": 4,
  "in_flight_messages": 240,
  "consumer_lag_ms": 60
}
```

### Endpoint `POST /v3/pipes/pipe-021/events`
- **Description**: Publishes an event or batch of events to pipe instance 21.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.21",
  "source": "sensor-gateway-21.edge",
  "data": {
    "reading_index": 21,
    "temperature_celsius": 30.5,
    "pressure_kpa": 103.39999999999999,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000021-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-021/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 21.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-021",
  "active_shards": 4,
  "in_flight_messages": 252,
  "consumer_lag_ms": 63
}
```

### Endpoint `POST /v3/pipes/pipe-022/events`
- **Description**: Publishes an event or batch of events to pipe instance 22.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.22",
  "source": "sensor-gateway-22.edge",
  "data": {
    "reading_index": 22,
    "temperature_celsius": 31.0,
    "pressure_kpa": 103.5,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000022-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-022/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 22.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-022",
  "active_shards": 4,
  "in_flight_messages": 264,
  "consumer_lag_ms": 66
}
```

### Endpoint `POST /v3/pipes/pipe-023/events`
- **Description**: Publishes an event or batch of events to pipe instance 23.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.23",
  "source": "sensor-gateway-23.edge",
  "data": {
    "reading_index": 23,
    "temperature_celsius": 31.5,
    "pressure_kpa": 103.6,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000023-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-023/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 23.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-023",
  "active_shards": 4,
  "in_flight_messages": 276,
  "consumer_lag_ms": 69
}
```

### Endpoint `POST /v3/pipes/pipe-024/events`
- **Description**: Publishes an event or batch of events to pipe instance 24.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.24",
  "source": "sensor-gateway-24.edge",
  "data": {
    "reading_index": 24,
    "temperature_celsius": 32.0,
    "pressure_kpa": 103.7,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000024-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-024/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 24.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-024",
  "active_shards": 4,
  "in_flight_messages": 288,
  "consumer_lag_ms": 72
}
```

### Endpoint `POST /v3/pipes/pipe-025/events`
- **Description**: Publishes an event or batch of events to pipe instance 25.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.25",
  "source": "sensor-gateway-25.edge",
  "data": {
    "reading_index": 25,
    "temperature_celsius": 32.5,
    "pressure_kpa": 103.8,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000025-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-025/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 25.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-025",
  "active_shards": 4,
  "in_flight_messages": 300,
  "consumer_lag_ms": 75
}
```

### Endpoint `POST /v3/pipes/pipe-026/events`
- **Description**: Publishes an event or batch of events to pipe instance 26.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.26",
  "source": "sensor-gateway-26.edge",
  "data": {
    "reading_index": 26,
    "temperature_celsius": 33.0,
    "pressure_kpa": 103.89999999999999,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000026-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-026/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 26.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-026",
  "active_shards": 4,
  "in_flight_messages": 312,
  "consumer_lag_ms": 78
}
```

### Endpoint `POST /v3/pipes/pipe-027/events`
- **Description**: Publishes an event or batch of events to pipe instance 27.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.27",
  "source": "sensor-gateway-27.edge",
  "data": {
    "reading_index": 27,
    "temperature_celsius": 33.5,
    "pressure_kpa": 104.0,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000027-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-027/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 27.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-027",
  "active_shards": 4,
  "in_flight_messages": 324,
  "consumer_lag_ms": 81
}
```

### Endpoint `POST /v3/pipes/pipe-028/events`
- **Description**: Publishes an event or batch of events to pipe instance 28.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.28",
  "source": "sensor-gateway-28.edge",
  "data": {
    "reading_index": 28,
    "temperature_celsius": 34.0,
    "pressure_kpa": 104.1,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000028-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-028/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 28.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-028",
  "active_shards": 4,
  "in_flight_messages": 336,
  "consumer_lag_ms": 84
}
```

### Endpoint `POST /v3/pipes/pipe-029/events`
- **Description**: Publishes an event or batch of events to pipe instance 29.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.29",
  "source": "sensor-gateway-29.edge",
  "data": {
    "reading_index": 29,
    "temperature_celsius": 34.5,
    "pressure_kpa": 104.2,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000029-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-029/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 29.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-029",
  "active_shards": 4,
  "in_flight_messages": 348,
  "consumer_lag_ms": 87
}
```

### Endpoint `POST /v3/pipes/pipe-030/events`
- **Description**: Publishes an event or batch of events to pipe instance 30.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.30",
  "source": "sensor-gateway-30.edge",
  "data": {
    "reading_index": 30,
    "temperature_celsius": 35.0,
    "pressure_kpa": 104.3,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000030-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-030/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 30.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-030",
  "active_shards": 4,
  "in_flight_messages": 360,
  "consumer_lag_ms": 90
}
```

### Endpoint `POST /v3/pipes/pipe-031/events`
- **Description**: Publishes an event or batch of events to pipe instance 31.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.31",
  "source": "sensor-gateway-31.edge",
  "data": {
    "reading_index": 31,
    "temperature_celsius": 35.5,
    "pressure_kpa": 104.39999999999999,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000031-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-031/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 31.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-031",
  "active_shards": 4,
  "in_flight_messages": 372,
  "consumer_lag_ms": 93
}
```

### Endpoint `POST /v3/pipes/pipe-032/events`
- **Description**: Publishes an event or batch of events to pipe instance 32.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.32",
  "source": "sensor-gateway-32.edge",
  "data": {
    "reading_index": 32,
    "temperature_celsius": 36.0,
    "pressure_kpa": 104.5,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000032-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-032/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 32.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-032",
  "active_shards": 4,
  "in_flight_messages": 384,
  "consumer_lag_ms": 96
}
```

### Endpoint `POST /v3/pipes/pipe-033/events`
- **Description**: Publishes an event or batch of events to pipe instance 33.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.33",
  "source": "sensor-gateway-33.edge",
  "data": {
    "reading_index": 33,
    "temperature_celsius": 36.5,
    "pressure_kpa": 104.6,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000033-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-033/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 33.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-033",
  "active_shards": 4,
  "in_flight_messages": 396,
  "consumer_lag_ms": 99
}
```

### Endpoint `POST /v3/pipes/pipe-034/events`
- **Description**: Publishes an event or batch of events to pipe instance 34.
- **Headers**:
  - `Authorization`: Bearer token.
  - `X-Workspace-Id`: UUID of workspace.
  - `X-Idempotency-Key`: Client-generated unique UUID.
- **Request Parameters**:
  - `stream_mode`: (string) one of `standard`, `prioritized`, `buffered`.
  - `flush_interval_ms`: (integer) maximum time in milliseconds before buffer commits (default 200).
- **Request Body Example**:
```json
{
  "event_type": "telemetry.metric.batch.34",
  "source": "sensor-gateway-34.edge",
  "data": {
    "reading_index": 34,
    "temperature_celsius": 37.0,
    "pressure_kpa": 104.7,
    "status": "OPERATIONAL"
  }
}
```
- **Response**:
  - `200 OK`: `{ "status": "QUEUED", "pulse_id": "pls-000034-abc", "ingest_timestamp": 1770000000 }`
  - `400 Bad Request`: Payload validation error.
  - `429 Too Many Requests`: Rate limit exceeded.

### Endpoint `GET /v3/pipes/pipe-034/telemetry`
- **Description**: Retrieves current Shardlet queue depth and consumer lag metrics for pipe 34.
- **Query Parameters**:
  - `window`: (string) `1m`, `5m`, `1h`. Default `5m`.
- **Response**:
```json
{
  "pipe_id": "pipe-034",
  "active_shards": 4,
  "in_flight_messages": 408,
  "consumer_lag_ms": 102
}
```


## Advanced Ephemeral Shardlet Partitioning

This section covers internal Shardlet memory allocations, ring buffers, and rebalancing thresholds configured via cluster orchestration manifests.

### Ephemeral Shard Buffer Allocation
The ephemeral shard buffer parameter `ephemeral_buffer_max_mb` has a default allocation of `64MB` and can be increased to `512MB` only via flag `--enable-l2-ephemeral-cache`.
When running high-cardinality event ingestion pipelines, exceeding 80% buffer capacity triggers speculative disk writes to local NVMe scratch storage.

### Shardlet Rebalance Drift Tolerance
Shardlet rebalance threshold `shard_drift_tolerance_pct` is set to `14.5%`. If drift exceeds this, rebalance trigger `SHARD_REBALANCE_IMMEDIATE` fires.
During immediate rebalance execution, the partition manager coordinates Raft snapshot transfers while pausing new ingress connections on the affected Shardlet for no more than 350 milliseconds.
