# AtomicBot Standard Specification

## Table of Contents

- [AtomicBot Standard Specification](#atomicbot-standard-specification)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Scope](#2-scope)
  - [3. Normative References](#3-normative-references)
  - [4. Definitions](#4-definitions)
  - [5. Events](#5-events)
    - [5.1 Event Format](#51-event-format)
      - [Add optional fields commonly used in events](#add-optional-fields-commonly-used-in-events)
    - [5.2 Event Example](#52-event-example)
  - [6. Actions](#6-actions)
    - [6.1 Actions Overview](#61-actions-overview)
    - [6.2 Sending a Message Example](#62-sending-a-message-example)
  - [7. HTTP Communication](#7-http-communication)
    - [7.1 Configuration](#71-configuration)
    - [7.2 Authentication](#72-authentication)
    - [7.3 Content Types](#73-content-types)
    - [7.4 Event Polling](#74-event-polling)
    - [7.5 Webhook](#75-webhook)
      - [7.5.1 Webhook Headers](#751-webhook-headers)
      - [7.5.2 Webhook Authentication](#752-webhook-authentication)
      - [7.5.3 Webhook Timeout](#753-webhook-timeout)
  - [8. WebSocket Communication](#8-websocket-communication)
    - [8.1 Authentication](#81-authentication)
    - [8.2 Events and Actions](#82-events-and-actions)
    - [8.3 WebSocket Forward](#83-websocket-forward)
    - [8.4 WebSocket Reverse](#84-websocket-reverse)
  - [9. Data Types](#9-data-types)
    - [9.1 Type Values](#91-type-values)
    - [9.2 Action Response](#92-action-response)
  - [10. Return Codes](#10-return-codes)
    - [10.1 Request Errors](#101-request-errors)
    - [10.2 Handler Errors](#102-handler-errors)
  - [11. Robot Self Identification](#11-robot-self-identification)
  - [12. Security Considerations](#12-security-considerations)
  - [13. Compliance and Conformance](#13-compliance-and-conformance)
  - [14. Examples and Use Cases](#14-examples-and-use-cases)
    - [14.1 Sending a Message Example](#141-sending-a-message-example)
    - [14.2 Receiving an Event Example](#142-receiving-an-event-example)
  - [15. Markdown Encoding and Double-Bracketed Entities](#15-markdown-encoding-and-double-bracketed-entities)

## 1. Introduction

The AtomicBot standard defines a common API for developing chatbots, standardizing communication, data formats, and interfaces. It aims to provide interoperability between different chatbot platforms and implementations.

## 2. Scope

This document specifies the communication protocols, data formats, and interfaces for implementing and using AtomicBot. It covers the structure of events, action requests, and responses, as well as supported communication methods.

## 3. Normative References

- [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt): Key words for use in RFCs to Indicate Requirement Levels
- JSON Data Interchange Format - ECMA-404

## 4. Definitions

| Term                     | Definition                                           |
| ------------------------ | ---------------------------------------------------- |
| Robot/Bot                | Chatbot                                              |
| Robot Platform           | Platforms like QQ, WeChat that provide chatbot APIs  |
| AtomicBot                | The standard or an implementation                    |
| AtomicBot Standard       | The AtomicBot API specification                      |
| AtomicBot Implementation | A program implementing the AtomicBot standard        |
| AtomicBot Application    | A program using AtomicBot to implement chatbot logic |
| AtomicBot SDK            | Helper libraries for building AtomicBot apps         |
| AtomicBot Library        | Reusable code for AtomicBot implementations          |

## 5. Events

### 5.1 Event Format

Events are objects with required fields:

- `id`: Unique ID
- `type`: Event type
- `detail_type`: Optional detail defining subtype of event (e.g., private, group, channel)
- `message`: Event message content (e.g., text, image, file)

#### Add optional fields commonly used in events

- `source`: The source/origin of the event (e.g. user, group, channel)
- `target`: The target/destination of the event
- `content`: The main content of the event (e.g. message text, image, file)
- `metadata`: Additional metadata about the event

### 5.2 Event Example

```json
{
  "id": "123",
  "type": "message",
  "detail_type": "private",
  "message": [
    {"type": "text", "data": {
      "text": "Hello world"
    }}
  ]
}
```

## 6. Actions

### 6.1 Actions Overview

Action requests are sent by the application to request services. Responses are returned by AtomicBot after processing the requests.

### 6.2 Sending a Message Example

Action Request Example:

```json
{
  "action": "send_message",
  "params": {
    "message": ["Hi there!"]
  },
  "self": {
    "platform": "telegram",
    "user_id": "123"
  }
}
```

Action Response Example:

```json
{
  "status": "ok",
  "retcode": 0,
  "data": {
    "result": "success"
  },
  "echo": "123"
}
```

## 7. HTTP Communication

### 7.1 Configuration

AtomicBot runs an HTTP server based on configuration:

- `host`: Listening IP
- `port`: Listening port
- `access_token`: Authentication token
- `event_enabled`: Enable event polling
- `event_buffer_size`: Event buffer size

AtomicBot handles requests at `/` and returns action responses.

### 7.2 Authentication

If `access_token` is set, AtomicBot authenticates via:

- `Authorization` header
- `access_token` query parameter

### 7.3 Content Types

Supported request content types:

- `application/json` (MUST be supported)
- `application/msgpack` (MAY be supported)

Response `Content-Type` mirrors request.

### 7.4 Event Polling

If `event_enabled` is true, AtomicBot supports `get_latest_events` to poll events. It provides an event buffer of configurable `event_buffer_size`.

### 7.5 Webhook

AtomicBot pushes events to a webhook URL based on configuration:

- `url`: Webhook URL
- `access_token`: Authentication
- `timeout`: Request timeout

#### 7.5.1 Webhook Headers

Required request headers:

- `Content-Type`: `application/json`
- `User-Agent`: AtomicBot version
- `X-AtomicBot-Version`: AtomicBot version
- `X-Impl`: AtomicBot implementation

Optional `Authorization` header for authentication.

#### 7.5.2 Webhook Authentication

Authenticates via:

- `Authorization` header
- `access_token` query parameter

#### 7.5.3 Webhook Timeout

Request timeout is based on the configured timeout value.

## 8. WebSocket Communication

AtomicBot supports WebSocket server and client roles. It forwards events to clients and handles action requests.

### 8.1 Authentication

If `access_token` is set, AtomicBot authenticates before handshake via:

- `Authorization` header
- `access_token` query parameter

### 8.2 Events and Actions

- Events as JSON
- Action requests as JSON or MessagePack
- Responses use the request format

### 8.3 WebSocket Forward

AtomicBot runs a WebSocket server based on configuration:

- `host`: Listening IP
- `port`: Listening port
- `access_token`: Authentication

It accepts connections at `/` and handles events and actions.

### 8.4 WebSocket Reverse

AtomicBot connects to a WebSocket endpoint based on configuration:

- `url`: WebSocket URL
- `access_token`: Authentication
- `reconnect_interval`: Reconnect interval

It handles events and actions after connecting.

## 9. Data Types

### 9.1 Type Values

- Integer: `int64`, `uint64`, `int32`, `uint32`, `int16`, `uint16`, `int8`, `uint8`
- Float: `float64`
- String: `string`
- Bytes: Base64-encoded string or byte array
- Array: `any[]`
- Map: `map[key_type]value_type`
- Object: `object (map[string]any)`

### 9.2 Action Response

Action responses are objects with required fields:

- `resp`: Action name
- `status`: Status
- `retcode`: Return code
- `data`: Response data
- `message`: Error message

## 10. Return Codes

Return codes indicate execution status:

- `0`: Success
- `1xxxx`: Request errors
- `2xxxx`: Handler errors
- `3xxxx`: Execution errors

### 10.1 Request Errors

Similar to HTTP 4xx client errors.

| Code  | Error               | Cause                    |
| ----- | ------------------- | ------------------------ |
| 10001 | Bad Request         | Malformed request        |
| 10002

 | Unsupported Action  | Unimplemented action     |
| 10003 | Bad Param           | Invalid parameter        |

### 10.2 Handler Errors

Similar to HTTP 5xx server errors.

| Code  | Error                   | Cause                  |
| ----- | ----------------------- | ---------------------- |
| 20001 | Bad Handler             | Implementation error   |
| 20002 | Internal Handler Error  | Uncaught exception     |

## 11. Robot Self Identification

TODO: Add detailed description of robot self-identification fields and format.

## 12. Security Considerations

- Ensure secure transmission (e.g., TLS/SSL) for HTTP and WebSocket communication.
- Use strong authentication mechanisms to protect against unauthorized access.
- Validate and sanitize all input data to prevent injection attacks.

## 13. Compliance and Conformance

To be compliant with the AtomicBot standard, implementations MUST adhere to the protocols and data formats specified in this document. Implementations SHOULD provide conformance tests to validate compliance.

## 14. Examples and Use Cases

### 14.1 Sending a Message Example

To send a message, the application sends an action request:

```json
{
  "action": "send_message",
  "params": {
    "message": ["Hi there!"]
  },
  "self": {
    "platform": "telegram",
    "user_id": "123"
  }
}
```

The AtomicBot responds:

```json
{
  "status": "ok",
  "retcode": 0,
  "data": {
    "result": "success"
  },
  "echo": "123"
}
```

### 14.2 Receiving an Event Example

An example event received from AtomicBot:

```json
{
  "id": "123",
  "time": 1632847927,
  "type": "message",
  "detail_type": "private",
  "sub_type": "",
  "self": {
    "platform": "telegram",
    "user_id": "123"
  },
  "message": [
    {
      "type": "text",
      "data": {
        "text": "Hello world"
      }
    }
  ]
}
```

## 15. Markdown Encoding and Double-Bracketed Entities

This specification is designed to be readable in plain text and common markdown renderers. To facilitate knowledge graphing and associative linking of concepts, significant entities are enclosed in double brackets like this: [[Entity Name]]. When rendered in an environment that supports it (like the Obsidian knowledge base), the double-bracketed terms become clickable links that can display contextual information and connections to related concepts. For example, [[API]] could link to documentation on what an API is, [[Chatbot]] may link to background on chatbots, and [[JSON Data Interchange Format]] could expand into details on the JSON specification.

This makes the document itself an interactive knowledge repository in supported environments, while still being readable as plain markdown elsewhere. The double-bracket syntax was chosen specifically for compatibility with the popular Obsidian.md format.

While not a requirement of the AtomicBot specification, using this markup style can turn documentation into a powerful conceptual knowledge base when authored with tools like Obsidian that support this notation.
